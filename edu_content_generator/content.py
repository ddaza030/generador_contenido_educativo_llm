from typing import Dict
import logging
import os
import time

import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError
from edu_content_generator.limiter import RateLimiter


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("edu_content_generator")

# Load environment variables
class ContentGenerator:
    """Generates educational content based on syllabus information."""

    def __init__(self):
        self.content_types = {
            "lecture_notes": self._generate_lecture_notes,
            "slides": self._generate_slides,
            "practice_problems": self._generate_practice_problems,
            "discussion_questions": self._generate_discussion_questions,
            "assessment": self._generate_assessment,
            "suggested_readings": self.generate_suggested_readings
        }

        # Initialize rate limiter
        self.rate_limiter = RateLimiter()

        # Load the main prompt template
        self.base_prompt = """
        # Initial Prompt Template for LLM Educational Content Generator

        You are an expert educational content developer with extensive experience in creating university-level course materials. You have deep knowledge of pedagogical principles, curriculum design, and academic writing. You will help me develop an LLM-based agent for generating teaching materials from course syllabi.

        ## Context Setting
        I am developing an intelligent agent that takes a course syllabus as input and generates comprehensive teaching materials. The agent needs to:
        1. Parse and understand course syllabi
        2. Generate appropriate teaching materials
        3. Maintain academic rigor and consistency
        4. Follow best practices in educational content development

        ## Request Structure
        For each interaction, I will need your help with one or more of the following aspects:

        ### System Design
        - Analyzing syllabus structure and components
        - Identifying key information extraction points
        - Developing prompt engineering strategies
        - Planning content generation workflows
        - Designing evaluation metrics

        ### Content Generation
        - Creating templates for different types of teaching materials
        - Developing quality control mechanisms
        - Maintaining consistency across materials
        - Handling domain-specific terminology
        - Ensuring academic standards

        ### Evaluation and Improvement
        - Reviewing generated content
        - Suggesting improvements
        - Identifying potential issues
        - Recommending refinements to prompts or workflows

        ## Required Output Format
        Please structure your responses with:
        - Clear section headings
        - Numbered lists for sequential steps
        - Examples in code blocks where appropriate
        - Clear distinctions between different components
        - Explicit reasoning for recommendations

        ## Constraints and Considerations
        Please consider:
        - Academic integrity requirements
        - Educational best practices
        - Technical limitations of LLMs
        - Scalability needs
        - Quality assurance requirements

        When responding, please:
        1. Think step by step
        2. Provide concrete examples
        3. Highlight key decision points
        4. Suggest alternatives where relevant
        5. Identify potential challenges
        6. answer in SPANISH
        7. It should not include additional explanations, greetings or farewells.
        8. The output should contain only the requested content.
        9. NOT include explanations of the generation process.
        """

    def generate_content(self, syllabus_data: Dict, content_type: str,
                         topic = None) -> str:
        """
        Generate educational content based on syllabus data.

        Args:
            syllabus_data: Parsed syllabus information
            content_type: Type of content to generate (lecture_notes, slides, etc.)
            topic: Specific topic to focus on (optional)

        Returns:
            Generated content as string
        """
        if content_type not in self.content_types:
            logger.error(f"Unknown content type: {content_type}")
            return f"Error: Unknown content type '{content_type}'"

        logger.info(f"Generating {content_type} content...")
        return self.content_types[content_type](syllabus_data, topic)

    def _generate_lecture_notes(self, syllabus_data: Dict,
                                topic = None) -> str:
        """Generate comprehensive lecture notes."""
        topics_to_cover = [topic] if topic else syllabus_data.get("topics", [])
        if not topics_to_cover:
            return "Error: No topics available to generate lecture notes"

        prompt = f"""
        {self.base_prompt}

        ## Content Generation Task
        Generate detailed lecture notes for the following course and topic(s).

        ### Course Information
        - Title: {syllabus_data.get('course_title', 'N/A')}
        - Code: {syllabus_data.get('course_code', 'N/A')}
        - Description: {syllabus_data.get('course_description', 'N/A')}

        ### Learning Objectives
        {syllabus_data.get('learning_objectives', 'Not specified')}

        ### Topics to Cover
        {', '.join(topics_to_cover)}

        ### Required Format
        Structure your lecture notes with:
        1. Introduction and key concepts
        2. Main content with clear headings and subheadings
        3. Examples and applications
        4. Summary and key takeaways
        5. References and additional resources

        Ensure academic rigor and accuracy while maintaining clarity and comprehensiveness.
        """

        return self._call_llm(prompt, max_tokens=4000)

    def _generate_slides(self, syllabus_data: Dict, topic = None) -> str:
        """Generate presentation slides content."""
        topics_to_cover = [topic] if topic else syllabus_data.get("topics", [])
        if not topics_to_cover:
            return "Error: No topics available to generate slides"

        prompt = f"""
        {self.base_prompt}

        ## Content Generation Task
        Generate presentation slides content for the following course and topic(s).

        ### Course Information
        - Title: {syllabus_data.get('course_title', 'N/A')}
        - Code: {syllabus_data.get('course_code', 'N/A')}

        ### Topics to Cover
        {', '.join(topics_to_cover)}

        ### Required Format
        Present the content as slide-by-slide markdown with:
        - Clear slide titles (## Slide Title)
        - Bullet points for key information
        - Notes for the presenter in blockquotes (> Note: explanation)
        - Include approximately 10-15 slides
        - Include an introductory slide and a summary slide

        Focus on visual presentation and concise key points rather than comprehensive text.
        """

        return self._call_llm(prompt, max_tokens=3000)

    def _generate_practice_problems(self, syllabus_data: Dict,
                                    topic = None) -> str:
        """Generate practice problems with solutions."""
        topics_to_cover = [topic] if topic else syllabus_data.get("topics", [])
        if not topics_to_cover:
            return "Error: No topics available to generate practice problems"

        prompt = f"""
        {self.base_prompt}

        ## Content Generation Task
        Generate a set of practice problems with detailed solutions for the following course and topic(s).

        ### Course Information
        - Title: {syllabus_data.get('course_title', 'N/A')}
        - Code: {syllabus_data.get('course_code', 'N/A')}

        ### Learning Objectives
        {syllabus_data.get('learning_objectives', 'Not specified')}

        ### Topics to Cover
        {', '.join(topics_to_cover)}

        ### Required Format
        For each problem:
        1. State the problem clearly
        2. Indicate difficulty level (Basic, Intermediate, Advanced)
        3. Provide a detailed step-by-step solution
        4. Include explanations of key concepts used in the solution

        Create 5-7 practice problems that test different aspects of the topic(s) and promote critical thinking.
        """

        return self._call_llm(prompt, max_tokens=4000)

    def _generate_discussion_questions(self, syllabus_data: Dict,
                                       topic = None) -> str:
        """Generate discussion questions and prompts."""
        topics_to_cover = [topic] if topic else syllabus_data.get("topics", [])
        if not topics_to_cover:
            return "Error: No topics available to generate discussion questions"

        prompt = f"""
        {self.base_prompt}

        ## Content Generation Task
        Generate thought-provoking discussion questions related to the following course and topic(s).

        ### Course Information
        - Title: {syllabus_data.get('course_title', 'N/A')}
        - Code: {syllabus_data.get('course_code', 'N/A')}
        - Description: {syllabus_data.get('course_description', 'N/A')}

        ### Topics to Cover
        {', '.join(topics_to_cover)}

        ### Required Format
        For each discussion question:
        1. Provide the main question
        2. Include 2-3 follow-up questions to deepen the discussion
        3. Offer brief notes on potential directions the discussion might take
        4. Connect the question to course learning objectives where possible

        Create 8-10 discussion questions that encourage critical thinking, application of concepts, and diverse perspectives.
        """

        return self._call_llm(prompt, max_tokens=3000)

    def _generate_assessment(self, syllabus_data: Dict,
                             topic = None) -> str:
        """Generate assessment items such as quizzes or exam questions."""
        topics_to_cover = [topic] if topic else syllabus_data.get("topics", [])
        if not topics_to_cover:
            return "Error: No topics available to generate assessment items"

        prompt = f"""
        {self.base_prompt}

        ## Content Generation Task
        Generate a comprehensive assessment covering the following course and topic(s).

        ### Course Information
        - Title: {syllabus_data.get('course_title', 'N/A')}
        - Code: {syllabus_data.get('course_code', 'N/A')}

        ### Learning Objectives
        {syllabus_data.get('learning_objectives', 'Not specified')}

        ### Topics to Cover
        {', '.join(topics_to_cover)}

        ### Required Format
        Include a mix of question types:
        1. Multiple choice questions with 4 options and explanations
        2. Short answer questions with expected responses
        3. Essay questions with grading rubrics
        4. Problem-solving items with step-by-step solutions

        Create a balanced assessment that evaluates different levels of Bloom's taxonomy.
        Provide a marking scheme with point allocations for each question.
        """

        return self._call_llm(prompt, max_tokens=4000)
    def generate_suggested_readings(self, syllabus_data, topic=None):
        """
        Generate suggested readings and resources
        
        Args:
            syllabus_data: Parsed syllabus information
            topic: Optional specific topic
        
        Returns:
            List of suggested readings
        """
        # Implement reading suggestion generation
        suggested_readings_prompt = f"""
        Generate an academically rigorous list of suggested readings for:
        Course: {syllabus_data.get('course_title', 'N/A')}
        Topic: {topic or 'General Course Content'}
        
        Include:
        - Academic journal articles
        - Textbook chapters
        - Online resources
        - Supplementary materials
        """
        
        return self._call_llm(suggested_readings_prompt, max_tokens=1000)

    def _call_llm(self, prompt: str, max_tokens: int = 2000) -> str:
        """Make API call to the Gemini LLM service."""
        logger.info(f"Calling Gemini API with prompt length: {len(prompt)}")

        if not os.getenv('API_KEY'):
            logger.warning("Gemini API key not configured. Returning placeholder.")
            return "This is a placeholder for generated content. Configure Gemini API key to enable real generation."
        # Estimate token count (rough approximation)
        estimated_tokens = len(prompt.split()) * 1.3  # Approximate conversion from words to tokens
        
        # Apply rate limiting
        if not self.rate_limiter.consume_tokens(int(estimated_tokens) + max_tokens):
            wait_time = 60  # seconds to wait for rate limit reset
            logger.warning(f"Rate limit exceeded. Waiting {wait_time} seconds before proceeding...")
            time.sleep(wait_time)
            
            # Check again after waiting
            if not self.rate_limiter.consume_tokens(int(estimated_tokens) + max_tokens):
                logger.error("Rate limit still exceeded after waiting. Consider reducing request frequency.")
                return "Error: API rate limit exceeded. Please try again later."
        try:
            # Configure the API key
            genai.configure(api_key=os.getenv('API_KEY'))

            # Select the Gemini model (default to gemini-pro if not specified)
            model_name = "gemini-2.0-flash-001"
            model = genai.GenerativeModel(model_name)

            # Set generation parameters
            generation_config = {
                "max_output_tokens": max_tokens,
                "temperature": 0.7
            }

            # Generate a response
            response = model.generate_content(
                prompt,
                generation_config=generation_config
            )

            # Extract and return the text
            if hasattr(response, 'text'):
                return response.text
            else:
                return "Error: No text in response"

        except GoogleAPIError as e:
            logger.error(f"Gemini API call failed: {str(e)}")
            return f"Error calling Gemini API: {str(e)}"
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return f"Unexpected error: {str(e)}"

