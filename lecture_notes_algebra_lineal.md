### Evaluación Integral de Álgebra Lineal (Código: 1000003)

**I. Preguntas de Selección Múltiple (2 puntos cada una, total 20 puntos)**

1.  ¿Cuál de las siguientes opciones es una combinación lineal de los vectores  `v1 = [1, 2]` y `v2 = [3, 4]`?
    a) `[4, 6]`
    b) `[2, 3]`
    c) `[5, 8]`
    d) `[0, 0]`

    *Respuesta Correcta: c) `[5, 8]`*

    *Explicación: Una combinación lineal es de la forma `a*v1 + b*v2`. En este caso, `1*v1 + (4/3)*v2 = [5, 8]`.*

2.  ¿Cuál de las siguientes afirmaciones es verdadera sobre el producto punto de dos vectores ortogonales?
    a) Siempre es positivo.
    b) Siempre es negativo.
    c) Siempre es cero.
    d) Depende de la longitud de los vectores.

    *Respuesta Correcta: c) Siempre es cero.*

    *Explicación: Dos vectores son ortogonales si su producto punto es cero.*

3.  Si A y B son matrices de nxn, ¿cuál de las siguientes es generalmente verdadera?
    a)  AB = BA
    b)  (A + B)^2 = A^2 + 2AB + B^2
    c)  (A + B)C = AC + BC
    d)  A^-1 siempre existe

    *Respuesta Correcta: c) (A + B)C = AC + BC*

    *Explicación: La multiplicación de matrices no es conmutativa, por lo que AB no siempre es igual a BA. La distributividad sí se cumple.*

4.  ¿Cuál de las siguientes afirmaciones define correctamente un subespacio de Rn?
    a) Debe contener el vector cero.
    b) Debe ser cerrado bajo la suma de vectores.
    c) Debe ser cerrado bajo la multiplicación escalar.
    d) Todas las anteriores.

    *Respuesta Correcta: d) Todas las anteriores.*

    *Explicación: Un subespacio debe cumplir las tres condiciones.*

5.  ¿Cuál de las siguientes NO es una operación elemental de fila?
    a) Intercambiar dos filas.
    b) Multiplicar una fila por un escalar no cero.
    c) Sumar un múltiplo de una fila a otra fila.
    d) Multiplicar una columna por un escalar no cero.

    *Respuesta Correcta: d) Multiplicar una columna por un escalar no cero.*

    *Explicación: Las operaciones elementales se definen sobre las filas.*

6.  ¿Qué representa el núcleo (kernel) de una transformación lineal?
    a) El conjunto de vectores que se transforman en el vector cero.
    b) El conjunto de todos los vectores resultantes de la transformación.
    c) El determinante de la matriz asociada.
    d) El rango de la matriz asociada.

    *Respuesta Correcta: a) El conjunto de vectores que se transforman en el vector cero.*

    *Explicación: El núcleo es el conjunto de vectores que mapean al vector cero bajo la transformación.*

7.  ¿Cuál es el proceso de Gram-Schmidt utilizado para?
    a) Resolver sistemas de ecuaciones lineales.
    b) Encontrar los valores propios de una matriz.
    c) Ortogonalizar un conjunto de vectores.
    d) Calcular la inversa de una matriz.

    *Respuesta Correcta: c) Ortogonalizar un conjunto de vectores.*

    *Explicación: El proceso de Gram-Schmidt transforma un conjunto de vectores linealmente independientes en un conjunto ortogonal.*

8.  ¿Qué significa que una matriz sea diagonalizable?
    a) Que su determinante es diferente de cero.
    b) Que es invertible.
    c) Que puede ser transformada en una matriz diagonal mediante una matriz de cambio de base.
    d) Que tiene todos sus valores propios iguales a cero.

    *Respuesta Correcta: c) Que puede ser transformada en una matriz diagonal mediante una matriz de cambio de base.*

    *Explicación: Una matriz es diagonalizable si existe una matriz invertible P tal que P^-1AP es una matriz diagonal.*

9.  ¿Qué caracteriza a una matriz ortogonal?
    a) Su inversa es igual a su transpuesta.
    b) Su determinante es igual a cero.
    c) Todos sus elementos son iguales a uno.
    d) Es simétrica.

    *Respuesta Correcta: a) Su inversa es igual a su transpuesta.*

    *Explicación: Una matriz ortogonal cumple que A^-1 = A^T.*

10. ¿Qué representa un valor propio de una matriz?
    a) Un vector que no cambia de dirección cuando se aplica la transformación lineal representada por la matriz.
    b) Un escalar que, al ser multiplicado por un vector propio, resulta en el mismo vector transformado por la matriz.
    c) El determinante de la matriz.
    d) La traza de la matriz.

    *Respuesta Correcta: b) Un escalar que, al ser multiplicado por un vector propio, resulta en el mismo vector transformado por la matriz.*

    *Explicación: Un valor propio λ satisface la ecuación A*v = λ*v, donde v es el vector propio.*

**II. Preguntas de Respuesta Corta (5 puntos cada una, total 20 puntos)**

1.  Defina brevemente qué es la independencia lineal.

    *Respuesta Esperada: Un conjunto de vectores es linealmente independiente si ninguno de ellos puede ser escrito como una combinación lineal de los otros.*

2.  Explique en qué consiste la eliminación Gaussiana.

    *Respuesta Esperada: Es un método para resolver sistemas de ecuaciones lineales transformando la matriz aumentada en una forma escalonada reducida mediante operaciones elementales de fila.*

3.  ¿Cuál es la relación entre el rango de una matriz y la dimensión de su espacio columna?

    *Respuesta Esperada: El rango de una matriz es igual a la dimensión de su espacio columna.*

4.  Describa brevemente el concepto de transformación lineal.

    *Respuesta Esperada: Una transformación lineal es una función entre dos espacios vectoriales que preserva las operaciones de suma de vectores y multiplicación por un escalar.*

**III. Preguntas de Ensayo (10 puntos cada una, total 30 puntos)**

1.  Discuta cómo el concepto de base y dimensión de un espacio vectorial es fundamental en álgebra lineal. Incluya ejemplos.

    *Rúbrica:
        *   Definición clara de base y dimensión (3 puntos)
        *   Explicación de la importancia (4 puntos)
        *   Ejemplos concretos (3 puntos)*

2.  Explique la importancia de los valores y vectores propios en el análisis de sistemas lineales.

    *Rúbrica:
        *   Definición clara de valores y vectores propios (3 puntos)
        *   Explicación de su uso en sistemas lineales (4 puntos)
        *   Ejemplos de aplicaciones (3 puntos)*

3.  Describa el proceso de diagonalización ortogonal de matrices simétricas y su aplicación en formas cuadráticas.

    *Rúbrica:
        *   Descripción del proceso de diagonalización ortogonal (4 puntos)
        *   Explicación de su relación con formas cuadráticas (3 puntos)
        *   Ejemplo de aplicación (3 puntos)*

**IV. Problemas (10 puntos cada uno, total 30 puntos)**

1.  Resuelva el siguiente sistema de ecuaciones lineales utilizando eliminación Gaussiana:
    ```
    2x + y - z = 8
    -3x - y + 2z = -11
    -2x + y + 2z = -3
    ```

    *Solución Esperada:
        *   Matriz aumentada correcta (2 puntos)
        *   Operaciones elementales correctas (5 puntos)
        *   Solución correcta: x=2, y=3, z=-1 (3 puntos)*

2.  Encuentre los valores propios y vectores propios de la matriz:
    ```
    A = [[5, -2], [1, 2]]
    ```

    *Solución Esperada:
        *   Cálculo correcto del polinomio característico (3 puntos)
        *   Valores propios correctos: λ1=4, λ2=3 (3 puntos)
        *   Vectores propios correctos para cada valor propio (4 puntos)*

3.  Determine si los vectores `v1 = [1, 2, 1]`, `v2 = [2, 1, 0]` y `v3 = [1, 0, 0]` son linealmente independientes.

    *Solución Esperada:
        *   Planteamiento correcto de la ecuación (3 puntos)
        *   Resolución correcta del sistema (4 puntos)
        *   Conclusión correcta sobre la independencia lineal (3 puntos)*

**Esquema de Puntuación:**

*   Sección I: 20 puntos
*   Sección II: 20 puntos
*   Sección III: 30 puntos
*   Sección IV: 30 puntos

**Total: 100 puntos**
