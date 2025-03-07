import os
import json
from typing import Dict
import logging
import time

from edu_content_generator.limiter import RateLimiter
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError

import PyPDF2
import docx

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("edu_content_generator")

class SyllabusParser:
    """Extracts structured information from course syllabi in various formats."""

    def __init__(self):
        self.components = [
            "course_title",
            "course_code",
            "instructor_info",
            "course_description",
            "learning_objectives",
            "prerequisites",
            "required_materials",
            "grading_policy",
            "schedule",
            "topics"
        ]
        self.rate_limiter = RateLimiter()

    def parse_file(self, file_path: str) -> Dict:
        """
        Parse syllabus from different file types.

        Args:
            file_path: Path to the syllabus file

        Returns:
            Dictionary containing extracted components
        """
        # Validate file exists
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return {"error": "File not found"}

        # Determine file type and extract text
        file_extension = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_extension == '.pdf':
                syllabus_text = self._extract_text_from_pdf(file_path)
            elif file_extension in ['.docx', '.doc']:
                syllabus_text = self._extract_text_from_docx(file_path)
            elif file_extension in ['.txt', '.text']:
                with open(file_path, 'r', encoding='utf-8') as file:
                    syllabus_text = file.read()
            else:
                logger.error(f"Unsupported file type: {file_extension}")
                return {"error": f"Unsupported file type: {file_extension}"}

            # Parse the extracted text
            return self.parse(syllabus_text)

        except Exception as e:
            logger.error(f"Error parsing file {file_path}: {str(e)}")
            return {"error": f"Error parsing file: {str(e)}"}

    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from a PDF file.

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Extracted text from the PDF
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            raise

    def _extract_text_from_docx(self, docx_path: str) -> str:
        """
        Extract text from a DOCX file.

        Args:
            docx_path: Path to the DOCX file

        Returns:
            Extracted text from the DOCX
        """
        try:
            doc = docx.Document(docx_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            logger.error(f"Error extracting text from DOCX: {str(e)}")
            raise

    def parse(self, syllabus_text: str) -> Dict:
        """
        Parse syllabus text and extract structured information.

        Args:
            syllabus_text: Raw text from the syllabus document

        Returns:
            Dictionary containing extracted components
        """
        logger.info("Parsing syllabus...")

        extraction_prompt = self._build_extraction_prompt(syllabus_text)
        
        # Estimated token count (rough approximation)
        estimated_tokens = len(extraction_prompt.split()) * 1.3
        
        # Check rate limit before making API call
        if not self.rate_limiter.consume_tokens(int(estimated_tokens)):
            logger.warning("Rate limit exceeded. Waiting before making API call...")
            time.sleep(60)  # Wait for rate limit to reset
        
        extracted_data = self._call_llm(extraction_prompt, max_tokens=2000)

        try:
            # Convert the LLM response to a structured dictionary
            parsed_data = json.loads(extracted_data)
            logger.info(
                f"Successfully extracted {len(parsed_data)} components from syllabus")
            return parsed_data
        except json.JSONDecodeError:
            logger.error("Failed to parse LLM response as JSON")
            return {"error": "Failed to extract structured data from syllabus"}

    def _build_extraction_prompt(self, syllabus_text: str) -> str:
        """Build prompt for extracting information from syllabus."""
        prompt = f"""
        Usted es un experto analista educativo especializado en analizar programas de cursos.
        Extraiga los siguientes componentes del texto del plan de estudios que se proporciona a continuación:
        {', '.join(self.components)}

        Formatee su respuesta como un objeto JSON con estos componentes como claves.
        Si no se encuentra un componente, establezca su valor en null.
        
        Texto del programa:
        {syllabus_text}

        Emita sólo JSON válido sin explicaciones adicionales, además asegurese de no incluir los saltos de line en el JSON.
        """
        return prompt

    def _call_llm(self, prompt: str, max_tokens: int = 10000) -> str:
        """Make API call to the Gemini LLM service."""

        logger.info(f"Calling Gemini API with prompt length: {len(prompt)}")

        if not os.getenv('API_KEY'):
            logger.warning("Gemini API key not configured. Returning placeholder.")
            return "This is a placeholder for generated content. Configure Gemini API key to enable real generation."

        try:
            genai.configure(api_key=os.getenv('API_KEY'))

            model_name = "gemini-2.0-flash-001"
            model = genai.GenerativeModel(model_name)

            generation_config = {
                "max_output_tokens": max_tokens,
                "temperature": 0.7
            }

            response = model.generate_content(
                prompt,
                generation_config=generation_config
            )

            if hasattr(response, 'text'):
                texto = response.text[8:-4]
                return texto
            else:
                return "Error: No text in response"

        except GoogleAPIError as e:
            logger.error(f"Gemini API call failed: {str(e)}")
            return f"Error calling Gemini API: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return f"Unexpected error: {str(e)}"
        