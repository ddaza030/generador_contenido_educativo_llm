import argparse
import logging

from edu_content_generator.syllabus import SyllabusParser
from edu_content_generator.content import ContentGenerator
from edu_content_generator.evaluator import QualityEvaluator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("edu_content_generator")


def main(syllabus=None, content_type=None, topic=None, output=None, evaluate=False):
    """Main entry point for the CLI application, allowing both CLI and function arguments."""

    if syllabus is None or content_type is None:
        # Si los argumentos no se pasan como parámetros, tomarlos desde la línea de comandos
        parser = argparse.ArgumentParser(description="Educational Content Generator")
        parser.add_argument("--syllabus", required=True, 
                            help="Path to syllabus file (PDF, DOCX, or TXT)")
        parser.add_argument("--type",
                            choices=["lecture_notes", "slides", "practice_problems",
                                     "discussion_questions", "assessment", "suggested_readings"],
                            required=True, help="Type of content to generate")
        parser.add_argument("--topic", help="Specific topic to focus on (optional)")
        parser.add_argument("--output", help="Output file path (optional)")
        parser.add_argument("--evaluate", action="store_true",
                            help="Evaluate generated content")

        args = parser.parse_args()

        # Asignar valores de argparse a variables locales
        syllabus = args.syllabus
        content_type = args.type
        topic = args.topic
        output = args.output
        evaluate = args.evaluate

    # Crear instancia de SyllabusParser
    parser = SyllabusParser()

    # Usar el nuevo método parse_file para manejar diferentes tipos de archivos
    syllabus_data = parser.parse_file(syllabus)

    if "error" in syllabus_data:
        logger.error(f"Error parsing syllabus: {syllabus_data['error']}")
        return 1

    # Generar contenido
    generator = ContentGenerator()
    content = generator.generate_content(syllabus_data, content_type, topic)

    # Evaluar si se solicita
    if evaluate:
        evaluator = QualityEvaluator()
        evaluation = evaluator.evaluate_content(content, syllabus_data, content_type)
        logger.info(
            f"Content evaluation: Overall score: {evaluation.get('overall_score', 'N/A')}")
        for criterion, details in evaluation.items():
            if isinstance(details, dict) and 'score' in details:
                logger.info(f"- {criterion}: {details['score']}/5")

    # Guardar o mostrar resultado
    if output:
        try:
            with open(output, 'w', encoding='utf-8') as file:
                file.write(content)
            logger.info(f"Content saved to {output}")
        except IOError as e:
            logger.error(f"Failed to write output file: {str(e)}")
    else:
        print("\n" + "=" * 80 + "\n")
        print(content)
        print("\n" + "=" * 80 + "\n")

    return 0

if __name__ == "__main__":
    main(syllabus="algebra.pdf", content_type="slides", output="lecture_notes_algebra_lineal.md", evaluate=True)