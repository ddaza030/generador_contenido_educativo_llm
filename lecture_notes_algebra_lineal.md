### Generación de una Evaluación Integral para Álgebra Lineal

1.  **Preguntas de Opción Múltiple:**

    *   **Pregunta 1:** ¿Cuál de las siguientes opciones describe mejor una combinación lineal de vectores en R<sup>n</sup>?

        a)  Una lista de vectores linealmente independientes.

        b)  La suma de vectores multiplicados por escalares.

        c)  El producto cruz de dos vectores.

        d)  Un conjunto de vectores ortogonales.

        *   **Respuesta Correcta:** b)
        *   **Explicación:** Una combinación lineal es una expresión construida a partir de un conjunto de vectores multiplicando cada vector por un escalar y sumando los resultados.

    *   **Pregunta 2:** Si una matriz A es invertible, ¿cuál de las siguientes afirmaciones es siempre verdadera?

        a)  El determinante de A es igual a 0.

        b)  A tiene una columna de ceros.

        c)  El sistema Ax = b tiene una solución única para toda b.

        d)  A es una matriz singular.

        *   **Respuesta Correcta:** c)
        *   **Explicación:** Una matriz invertible garantiza que el sistema de ecuaciones lineales asociado tiene una solución única para cualquier vector b.

    *   **Pregunta 3:** ¿Qué representa el núcleo (kernel) de una transformación lineal T: V -> W?

        a)  El conjunto de todos los vectores en V que se mapean al vector cero en W.

        b)  El conjunto de todos los vectores en W que son imágenes de algún vector en V.

        c)  La dimensión de V.

        d)  La dimensión de W.

        *   **Respuesta Correcta:** a)
        *   **Explicación:** El núcleo de una transformación lineal es el conjunto de vectores del dominio que se transforman en el vector cero del codominio.

2.  **Preguntas de Respuesta Corta:**

    *   **Pregunta 1:** Defina el concepto de independencia lineal en un espacio vectorial.

        *   **Respuesta Esperada:** Un conjunto de vectores es linealmente independiente si la única combinación lineal de ellos que da como resultado el vector cero es aquella en la que todos los escalares son cero.

    *   **Pregunta 2:** ¿Cuál es la relación entre el rango de una matriz y la dimensión de su espacio columna?

        *   **Respuesta Esperada:** El rango de una matriz es igual a la dimensión de su espacio columna.

    *   **Pregunta 3:** Explique cómo se utiliza el proceso de Gram-Schmidt.

        *   **Respuesta Esperada:** El proceso de Gram-Schmidt es un algoritmo para ortogonalizar un conjunto de vectores linealmente independientes en un espacio con producto interno.

3.  **Preguntas de Ensayo:**

    *   **Pregunta 1:** Discuta la importancia de los valores y vectores propios en el contexto de la diagonalización de matrices. Incluya ejemplos de aplicaciones.

        *   **Rúbrica:**
            *   **Excelente (10 puntos):** Explicación clara y completa de los valores y vectores propios, su relación con la diagonalización, y ejemplos de aplicaciones (e.g., análisis de estabilidad, sistemas dinámicos).
            *   **Bueno (8 puntos):** Explicación correcta de los conceptos y la relación, pero con ejemplos limitados o menos claros.
            *   **Regular (6 puntos):** Comprensión básica de los conceptos, pero con errores o falta de claridad en la explicación.
            *   **Deficiente (4 puntos):** Conceptos mal entendidos o explicación incompleta.

    *   **Pregunta 2:** Describa cómo las transformaciones lineales pueden representarse mediante matrices y cómo esta representación facilita el análisis de la composición e inversión de transformaciones.

        *   **Rúbrica:**
            *   **Excelente (10 puntos):** Descripción detallada de la representación matricial, cómo la multiplicación de matrices corresponde a la composición de transformaciones, y cómo la inversa de una matriz representa la inversa de la transformación.
            *   **Bueno (8 puntos):** Explicación correcta pero menos detallada, con ejemplos menos claros.
            *   **Regular (6 puntos):** Comprensión básica, pero con errores o falta de claridad.
            *   **Deficiente (4 puntos):** Conceptos mal entendidos o explicación incompleta.

4.  **Problemas de Resolución:**

    *   **Problema 1:** Resuelva el siguiente sistema de ecuaciones lineales utilizando eliminación Gaussiana:

        ```
        2x + y - z = 8
        -3x - y + 2z = -11
        -2x + y + 2z = -3
        ```

        *   **Solución:**
            1.  Escribir la matriz aumentada.
            2.  Aplicar operaciones elementales de fila para obtener la forma escalonada reducida.
            3.  Resolver para x, y, z.

    *   **Problema 2:** Determine si los siguientes vectores son linealmente independientes:

        ```
        v1 = [1, -2, 1]
        v2 = [2, -1, 0]
        v3 = [3, 1, -1]
        ```

        *   **Solución:**
            1.  Formar una matriz con los vectores como columnas.
            2.  Calcular el determinante de la matriz.
            3.  Si el determinante es diferente de cero, los vectores son linealmente independientes.

### Esquema de Calificación

*   Preguntas de Opción Múltiple: 3 puntos cada una (9 puntos en total)
*   Preguntas de Respuesta Corta: 5 puntos cada una (15 puntos en total)
*   Preguntas de Ensayo: 10 puntos cada una (20 puntos en total)
*   Problemas de Resolución: 13 puntos cada uno (26 puntos en total)

**Total: 70 puntos**
