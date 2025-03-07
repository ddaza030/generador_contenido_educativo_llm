import os
import json
from typing import Dict
import logging

import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("edu_content_generator")

class SyllabusParser:
    """Extracts structured information from course syllabi."""

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

        Emite sólo JSON válido sin explicaciones adicionales:
        """
        return prompt


    def _call_llm(self, prompt: str, max_tokens: int = 2000) -> str:
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
