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

# Load environment variables

class QualityEvaluator:
    """Evaluates the quality of generated educational content."""

    def __init__(self):
        self.evaluation_criteria = {
            "accuracy": "Content is factually correct and up-to-date",
            "alignment": "Content aligns with learning objectives",
            "completeness": "Content covers all necessary topics comprehensively",
            "clarity": "Content is clearly presented and understandable",
            "engagement": "Content is engaging and promotes active learning",
            "level_appropriateness": "Content is appropriate for the intended audience"
        }

    def evaluate_content(self, content: str, syllabus_data: Dict,
                         content_type: str) -> Dict:
        """
        Evaluate generated content against quality criteria.

        Args:
            content: Generated content to evaluate
            syllabus_data: Original syllabus information
            content_type: Type of content being evaluated

        Returns:
            Dictionary with evaluation scores and feedback
        """
        logger.info("Evaluating generated content...")

        # Build evaluation prompt
        evaluation_prompt = self._build_evaluation_prompt(content, syllabus_data,
                                                          content_type)

        # Get evaluation from LLM
        evaluation_response = self._call_llm(evaluation_prompt, max_tokens=1500)

        try:
            # Convert the LLM response to a structured dictionary
            evaluation_data = json.loads(evaluation_response)
            logger.info("Successfully evaluated content")
            return evaluation_data
        except json.JSONDecodeError:
            logger.error("Failed to parse evaluation response as JSON")
            return {"error": "Failed to generate structured evaluation"}

    def _build_evaluation_prompt(self, content: str, syllabus_data: Dict,
                                 content_type: str) -> str:
        """Build prompt for evaluating content."""
        criteria_list = "\n".join(
            [f"- {k}: {v}" for k, v in self.evaluation_criteria.items()])

        prompt = f"""
        You are an expert in educational content evaluation with extensive experience in quality assessment.

        Evaluate the following {content_type} content against these criteria:
        {criteria_list}

        The content was generated for this course:
        - Title: {syllabus_data.get('course_title', 'N/A')}
        - Code: {syllabus_data.get('course_code', 'N/A')}
        - Learning Objectives: {syllabus_data.get('learning_objectives', 'Not specified')}

        Content to evaluate:
        {content}

        Provide your evaluation as a JSON object with:
        1. A score for each criterion (1-5 where 5 is excellent)
        2. Specific feedback for each criterion
        3. Overall score
        4. Improvement suggestions

        Output only valid JSON without additional text:
        """
        return prompt

    def _call_llm(self, prompt: str, max_tokens: int = 1500) -> str:
        """Make API call to the Gemini LLM service for evaluation."""
        import google.generativeai as genai
        import json
        from google.api_core.exceptions import GoogleAPIError

        logger.info(
            f"Calling Gemini API for evaluation with prompt length: {len(prompt)}")

        if not API_KEY:
            logger.warning("Gemini API key not configured. Returning placeholder.")
            return json.dumps({
                "accuracy": {"score": 4, "feedback": "Placeholder evaluation feedback"},
                "alignment": {"score": 3, "feedback": "Placeholder evaluation feedback"},
                "completeness": {"score": 4,
                                 "feedback": "Placeholder evaluation feedback"},
                "clarity": {"score": 3, "feedback": "Placeholder evaluation feedback"},
                "engagement": {"score": 3, "feedback": "Placeholder evaluation feedback"},
                "level_appropriateness": {"score": 4,
                                          "feedback": "Placeholder evaluation feedback"},
                "overall_score": 3.5,
                "improvement_suggestions": [
                    "This is a placeholder for evaluation suggestions"]
            })

        try:
            # Configure the API key
            genai.configure(api_key=API_KEY)

            # Select the Gemini model (default to gemini-pro if not specified)
            model_name = "gemini-2.0-flash-001"
            model = genai.GenerativeModel(model_name)

            # Set generation parameters
            generation_config = {
                "max_output_tokens": max_tokens,
                "temperature": 0.3
            }

            # Generate a response
            response = model.generate_content(
                prompt,
                generation_config=generation_config
            )

            # Extract and return the text, expecting it to be JSON
            if hasattr(response, 'text'):
                # Validate that the response is valid JSON
                try:
                    json_response = json.loads(response.text)
                    return response.text
                except json.JSONDecodeError:
                    # If response is not valid JSON, wrap it in a JSON structure
                    logger.warning(
                        "Response is not valid JSON. Wrapping in error structure.")
                    return json.dumps({"error": "Invalid JSON response from model",
                                       "raw_response": response.text})
            else:
                return json.dumps({"error": "No text in response"})

        except GoogleAPIError as e:
            logger.error(f"Gemini API call failed: {str(e)}")
            return json.dumps({"error": f"Error calling Gemini API: {str(e)}"})
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return json.dumps({"error": f"Unexpected error: {str(e)}"})