import json
import re
from typing import Dict
import logging
import os

import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError

# Configuración del sistema de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("edu_content_generator")

class QualityEvaluator:
    """
    Clase para evaluar la calidad del contenido educativo generado.
    """
    def __init__(self):
        self.evaluation_criteria = {
            "accuracy": "El contenido es correcto y actualizado.",
            "alignment": "El contenido está alineado con los objetivos de aprendizaje.",
            "completeness": "El contenido cubre todos los temas necesarios de manera completa.",
            "clarity": "El contenido está presentado de manera clara y comprensible.",
            "engagement": "El contenido fomenta el aprendizaje activo y es atractivo.",
            "level_appropriateness": "El contenido es adecuado para la audiencia objetivo.",
            "relevance": "El contenido es relevante para el curso y el tema específico.",
            "consistency": "El contenido es consistente y no presenta contradicciones.",
            "readability": "El contenido es legible y tiene una complejidad adecuada.",
            "domain_terminology": "El contenido utiliza correctamente la terminología específica del dominio."
        }

    def evaluate_content(self, content: str, syllabus_data: Dict, content_type: str) -> Dict:
        """
        Evalúa el contenido generado en base a criterios de calidad.

        Args:
            content: Contenido generado a evaluar.
            syllabus_data: Información del sílabo del curso.
            content_type: Tipo de contenido evaluado (ej. notas, diapositivas, ejercicios, etc.).

        Returns:
            Diccionario con puntuaciones y retroalimentación sobre cada criterio de evaluación.
        """
        logger.info("Evaluando contenido generado...")

        # Construcción del prompt de evaluación
        evaluation_prompt = self._build_evaluation_prompt(content, syllabus_data, content_type)

        # Llamada al LLM para obtener la evaluación
        evaluation_response = self._call_llm(evaluation_prompt, max_tokens=2000)

        # Intentar extraer el bloque JSON de la respuesta usando una expresión regular
        evaluation_response_clean = self._extract_json(evaluation_response)

        try:
            # Convertir la respuesta limpia del LLM a un diccionario estructurado
            evaluation_data = json.loads(evaluation_response_clean)
            logger.info("Evaluación completada con éxito.")
            return evaluation_data
        except json.JSONDecodeError:
            logger.error("Error al analizar la respuesta de la evaluación como JSON.")
            return {"error": "No se pudo generar una evaluación estructurada."}

    def _extract_json(self, text: str) -> str:
        """
        Extrae el primer bloque JSON encontrado en un texto.
        """
        # Buscar la primera ocurrencia de un bloque JSON
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return match.group(0)
        return text

    def _build_evaluation_prompt(self, content: str, syllabus_data: Dict, content_type: str) -> str:
        """
        Construye el prompt para la evaluación del contenido.
        """
        criteria_list = "\n".join([f"- {k}: {v}" for k, v in self.evaluation_criteria.items()])

        prompt = f"""
        Eres un experto en evaluación de contenido educativo con experiencia en calidad académica.
        
        Evalúa el siguiente contenido de {content_type} basándote en los siguientes criterios:
        {criteria_list}
        
        Información del curso:
        - Título: {syllabus_data.get('course_title', 'N/A')}
        - Código: {syllabus_data.get('course_code', 'N/A')}
        - Objetivos de Aprendizaje: {syllabus_data.get('learning_objectives', 'No especificado')}
        
        Contenido a evaluar:
        {content}
        
        Devuelve la evaluación en un JSON con la siguiente estructura:
        {{
            \"accuracy\": {{ \"score\": (1-5), \"feedback\": \"Retroalimentación específica\" }},
            \"alignment\": {{ \"score\": (1-5), \"feedback\": \"Retroalimentación específica\" }},
            \"completeness\": {{ \"score\": (1-5), \"feedback\": \"Retroalimentación específica\" }},
            \"clarity\": {{ \"score\": (1-5), \"feedback\": \"Retroalimentación específica\" }},
            \"engagement\": {{ \"score\": (1-5), \"feedback\": \"Retroalimentación específica\" }},
            \"level_appropriateness\": {{ \"score\": (1-5), \"feedback\": \"Retroalimentación específica\" }},
            \"relevance\": {{ \"score\": (1-5), \"feedback\": \"Retroalimentación específica\" }},
            \"consistency\": {{ \"score\": (1-5), \"feedback\": \"Retroalimentación específica\" }},
            \"readability\": {{ \"score\": (1-5), \"feedback\": \"Retroalimentación específica\" }},
            \"domain_terminology\": {{ \"score\": (1-5), \"feedback\": \"Retroalimentación específica\" }},
            \"overall_score\": \"(Promedio de las puntuaciones)\",\n            \"improvement_suggestions\": [\"Sugerencia 1\", \"Sugerencia 2\"]\n        }}
        """
        return prompt

    def _call_llm(self, prompt: str, max_tokens: int = 2000) -> str:
        """
        Realiza una llamada al modelo de lenguaje para evaluar el contenido.
        """
        logger.info(f"Llamando a la API de Gemini para evaluación. Longitud del prompt: {len(prompt)}")

        if not os.getenv('API_KEY'):
            logger.warning("Clave de API no configurada. Devolviendo evaluación simulada.")
            return json.dumps({
                "accuracy": {"score": 4, "feedback": "Buena precisión, pero se pueden mejorar ejemplos."},
                "alignment": {"score": 5, "feedback": "Bien alineado con los objetivos de aprendizaje."},
                "completeness": {"score": 4, "feedback": "Cubre la mayoría de los temas, pero falta profundidad en algunos."},
                "clarity": {"score": 3, "feedback": "Algunas partes pueden ser más claras."},
                "engagement": {"score": 4, "feedback": "Usa ejemplos interesantes, pero puede mejorar en interactividad."},
                "level_appropriateness": {"score": 5, "feedback": "Adecuado para el nivel del curso."},
                "relevance": {"score": 4, "feedback": "Relevante, pero se pueden agregar más conexiones prácticas."},
                "consistency": {"score": 5, "feedback": "No se detectan contradicciones."},
                "readability": {"score": 3, "feedback": "El lenguaje puede simplificarse en algunas secciones."},
                "domain_terminology": {"score": 5, "feedback": "Uso correcto de términos técnicos."},
                "overall_score": 4.3,
                "improvement_suggestions": [
                    "Agregar más ejemplos en profundidad.",
                    "Reformular algunas explicaciones para mayor claridad.",
                    "Mejorar la interactividad del contenido."
                ]
            })

        try:
            # Configurar la API de Gemini con la clave
            genai.configure(api_key=os.getenv('API_KEY'))
            model = genai.GenerativeModel("gemini-2.0-flash-001")
            response = model.generate_content(prompt, generation_config={"max_output_tokens": max_tokens, "temperature": 0.3})
            # Retornar el texto de la respuesta si existe, de lo contrario, un mensaje de error en formato JSON
            return response.text if hasattr(response, 'text') else json.dumps({"error": "Respuesta vacía"})
        except GoogleAPIError as e:
            logger.error(f"Error en la API de Gemini: {str(e)}")
            return json.dumps({"error": f"Error en la API: {str(e)}"})
        except Exception as e:
            logger.error(f"Error inesperado: {str(e)}")
            return json.dumps({"error": f"Error inesperado: {str(e)}"})
