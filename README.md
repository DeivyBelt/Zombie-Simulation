# Zombie-Simulation
Simulación computacional basada en la interacción entre agentes discretos que representan humanos, zombies y muertos dentro de un entorno bidimensional.

# Análisis cibernético

# Introducción

El presente análisis aborda una simulación computacional basada en la interacción entre agentes discretos que representan humanos, zombies y muertos dentro de un entorno bidimensional. El sistema evoluciona a partir de condiciones iniciales definidas y reglas locales de interacción, lo que permite estudiar su comportamiento desde la perspectiva de la cibernética y la teoría de sistemas. Se examinan aspectos fundamentales como la naturaleza del sistema, los mecanismos de retroalimentación, el lenguaje interno, las reglas de funcionamiento, la autorregulación, las posibles oscilaciones, así como las propiedades de caos y complejidad.

# Naturaleza del sistema: abierto, cerrado o aislado

El sistema analizado se clasifica principalmente como un sistema cerrado. Durante su ejecución, no existe intercambio de materia, energía ni información con el entorno externo. Su evolución depende exclusivamente de las condiciones iniciales y de los parámetros internos definidos antes del inicio de la simulación, tales como la probabilidad de infección y el tiempo de muerte de los zombies.

No obstante, puede considerarse una aproximación a un sistema aislado en términos teóricos, ya que, una vez iniciado, no recibe perturbaciones externas ni intervenciones del usuario. Sin embargo, esta clasificación no es estricta, dado que las condiciones iniciales son introducidas externamente y, en algunos casos, los parámetros pueden modificarse durante la simulación.

Por lo tanto, bajo condiciones de ejecución sin intervención, el sistema opera como un sistema cerrado con características cercanas a un sistema aislado.

# Mecanismos de retroalimentación

El sistema presenta una combinación de retroalimentación positiva y negativa, lo cual es característico de sistemas dinámicos complejos.

En primer lugar, se identifica un mecanismo de retroalimentación positiva en el proceso de infección. A medida que aumenta la cantidad de zombies, incrementa la probabilidad de que los humanos cercanos sean infectados, lo que a su vez genera más zombies. Este proceso puede conducir a un crecimiento acelerado de la población infectada, especialmente en etapas iniciales.

En segundo lugar, existe un mecanismo de retroalimentación negativa asociado a la muerte de los zombies. Cada zombie tiene un tiempo de vida limitado, tras el cual pasa al estado de muerto. Este proceso reduce la cantidad de agentes activos capaces de propagar la infección, actuando como un factor de control interno del sistema.

La interacción entre ambos mecanismos determina la dinámica global, pudiendo generar tanto expansión rápida como estabilización o colapso.

# Lenguaje del sistema

El lenguaje del sistema se basa en una representación discreta de estados y espacio. Cada celda del entorno se modela como una unidad que puede adoptar uno de tres estados posibles:

Humano
Zombie
Muerto

Estos estados se codifican numéricamente, lo que permite su manipulación computacional eficiente. El espacio está estructurado como una matriz bidimensional, donde cada celda interactúa únicamente con sus vecinas inmediatas. El tiempo, por su parte, es discreto y avanza en iteraciones sucesivas.

Esta estructura corresponde a un autómata celular estocástico, en el cual las transiciones de estado dependen tanto de reglas determinísticas como de componentes probabilísticos.

# Reglas de funcionamiento

Las reglas que gobiernan el sistema son locales y relativamente simples, pero generan comportamientos globales complejos. Estas reglas pueden resumirse de la siguiente manera:

Un humano puede convertirse en zombie si existe al menos un zombie en su vecindad inmediata y si se cumple una condición probabilística determinada por la probabilidad de infección.
Un zombie incrementa su contador interno de tiempo en cada iteración.
Cuando el tiempo acumulado de un zombie supera un umbral definido, este pasa al estado de muerto.

Estas reglas operan de manera simultánea sobre todas las celdas del sistema en cada iteración, lo que produce una evolución global emergente a partir de interacciones locales.

# Autorregulación

El sistema presenta un nivel de autorregulación, ya que su evolución no requiere intervención externa una vez iniciada la simulación. Los procesos internos, como la propagación de la infección y la muerte de los zombies, generan dinámicas que tienden a limitar el crecimiento indefinido de la población infectada.

La autorregulación se manifiesta principalmente en el equilibrio entre la generación de nuevos zombies y la desaparición de estos debido a su tiempo de vida limitado. Además, la disminución de la población humana disponible actúa como un factor adicional que restringe la propagación.

Sin embargo, el sistema no es adaptativo, ya que no modifica sus parámetros en respuesta a cambios internos ni aprende de su evolución. Por tanto, se trata de un sistema autorregulado pero no adaptativo.

# Oscilaciones

El comportamiento oscilatorio del sistema no es una característica dominante, pero puede presentarse bajo ciertas condiciones iniciales. En escenarios donde la probabilidad de infección es moderada y la población inicial de zombies es limitada, pueden observarse fluctuaciones en las cantidades de humanos y zombies a lo largo del tiempo.

Estas oscilaciones no son periódicas ni estables en sentido estricto, sino que corresponden a transiciones dinámicas entre fases de crecimiento y decrecimiento. En otros casos, el sistema puede converger rápidamente hacia estados finales, como la extinción de los humanos o la desaparición de los zombies, sin presentar oscilaciones significativas.

# Caos

El sistema exhibe propiedades asociadas al comportamiento caótico en un sentido práctico. Aunque no se trata de caos determinista formalmente definido, sí presenta características como:

Alta sensibilidad a las condiciones iniciales.
Evolución no lineal.
Dificultad para predecir el estado del sistema a largo plazo.

Pequeñas variaciones en la distribución inicial de humanos y zombies o en los parámetros del sistema pueden generar resultados significativamente diferentes. Esto implica que, aunque las reglas sean simples, la dinámica global es altamente impredecible en horizontes temporales extendidos.

# Complejidad

El sistema puede clasificarse como un sistema complejo emergente. A pesar de que sus reglas de funcionamiento son simples y locales, la interacción simultánea de múltiples agentes produce patrones globales no triviales.

La complejidad del sistema se manifiesta en:

La emergencia de comportamientos colectivos a partir de interacciones individuales.
La distribución espacial de estados que evoluciona de manera no uniforme.
La imposibilidad de inferir el comportamiento global únicamente a partir de las reglas locales.

Se trata de una complejidad distribuida y no lineal, característica de sistemas basados en autómatas celulares y modelos de propagación.
