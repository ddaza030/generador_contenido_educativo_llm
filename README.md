# Realizado para Tarea 4: Generador de contenido educativo

**Redes Neuronales y Algoritmos Bio-inspirados**
**Universidad Nacional de Colombia sede Medellín**
---

### Autores
**Juan Manuel Vera Echeverri jverae@unal.edu.co**
**Daniel Daza Macías dadazam@unal.edu.co**
**Carlos Sebastián Zamora Rosero cazamorar@unal.edu.co**
**Alejandra Uribe Sierra aluribes@unal.edu.co**
**Julián Orrego Martínez jorrego@unal.edu.co**  
  

# Generador de Contenido Educativo con LLM

Este proyecto permite generar automáticamente diferentes tipos de contenido educativo a partir de un syllabus, utilizando modelos de lenguaje de Google (Gemini).

## Instalación

### Requisitos previos
- Python 3.7 o superior
- Pip (gestor de paquetes de Python)

### Pasos de instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/ddaza030/generador_contenido_educativo_llm.git
   cd generador_contenido_educativo_llm
   ```

2. Instala el paquete:
   ```bash
   pip install .
   ```

   O instálalo directamente desde GitHub:
   ```bash
   pip install git+https://github.com/ddaza030/generador_contenido_educativo_llm.git
   ```

### Configuración de la API Key

Para utilizar este generador, necesitas configurar una API Key de Google Gemini:

#### En Windows:

**Temporalmente (para la sesión actual):**
```bash
# En CMD
set API_KEY=tu_api_key_aquí

# En PowerShell
$env:API_KEY = "tu_api_key_aquí"
```

**Permanentemente:**
```bash
# En CMD (como administrador)
setx API_KEY "tu_api_key_aquí"

# En PowerShell (como administrador)
[Environment]::SetEnvironmentVariable("API_KEY", "tu_api_key_aquí", "User")
```

#### En Linux/macOS:
```bash
export API_KEY=tu_api_key_aquí
```

Para que sea permanente, añade esta línea a tu archivo `~/.bashrc` o `~/.zshrc`.

## Uso

### Desde la línea de comandos

Estructura básica del comando:
```bash
edu-generator --syllabus RUTA_SYLLABUS --type TIPO_CONTENIDO [opciones adicionales]
```

#### Opciones disponibles:

| Opción | Descripción | Valores posibles | Requerido |
|--------|-------------|-----------------|-----------|
| `--syllabus` | Ruta al archivo del syllabus | Ruta de archivo (.txt, .md) | Sí |
| `--type` | Tipo de contenido a generar | `lecture_notes`, `slides`, `practice_problems`, `discussion_questions`, `assessment` | Sí |
| `--topic` | Tema específico del syllabus | Texto (ej: "matrices", "derivadas") | No |
| `--output` | Archivo de salida | Ruta de archivo | No |
| `--evaluate` | Evaluar la calidad del contenido | Flag (sin valor) | No |

#### Ejemplos:

Generar notas de clase sobre álgebra lineal:
```bash
edu-generator --syllabus syllabus/algebra_lineal.txt --type lecture_notes --output notas_clase.md
```

Generar problemas prácticos sobre un tema específico:
```bash
edu-generator --syllabus syllabus/calculo.txt --type practice_problems --topic "Integrales definidas" --output problemas.md
```

Generar y evaluar preguntas de discusión:
```bash
edu-generator --syllabus syllabus/fisica.txt --type discussion_questions --evaluate
```

### Desde Python

También puedes usar el generador como módulo dentro de tus scripts Python:

```python
from edu_content_generator import main

# Generar contenido
main(
    syllabus="ruta/al/syllabus.txt",
    content_type="lecture_notes",
    topic="tema específico",  # opcional
    output="resultado.md",    # opcional
    evaluate=True             # opcional
)
```

## Tipos de contenido disponibles

- **lecture_notes**: Notas detalladas para clases
- **slides**: Diapositivas para presentaciones
- **practice_problems**: Problemas prácticos con soluciones
- **discussion_questions**: Preguntas para fomentar la discusión
- **assessment**: Evaluaciones y exámenes

## Ejemplos de syllabus

El formato recomendado para el syllabus es texto plano estructurado con secciones claramente definidas:

```
TÍTULO DEL CURSO: Álgebra Lineal

DESCRIPCIÓN:
Este curso introduce los conceptos fundamentales del álgebra lineal...

OBJETIVOS DE APRENDIZAJE:
- Comprender los conceptos de espacios vectoriales
- Resolver sistemas de ecuaciones lineales
- ...

TEMARIO:
1. Sistemas de ecuaciones lineales
2. Matrices y operaciones matriciales
   2.1. Suma y resta de matrices
   2.2. Multiplicación de matrices
3. Determinantes
...
```

## Solución de problemas

Si encuentras problemas al instalar o ejecutar el generador:

1. Verifica que la API KEY esté correctamente configurada
2. Asegúrate de tener las dependencias instaladas
3. Revisa que el formato del syllabus sea correcto

