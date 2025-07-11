# da-cloner

## Paso 2: Descargar el audio del listado de vídeos
* Instalar dependencia: pip install yt-dlp
* Da un error, necesitamos configurar ffmpeg.
    - Lo descargamos en .zip desde: https://www.gyan.dev/ffmpeg/builds/
    - Lo descomprimimos pegamos el diretorio bin en el proyecto /downloader/ffmpg/bin

## Paso 1: Recopilar información de Youtube

* Instalación de dependencias:
    - pip install python-dotenv google-api-python-client
* En youtube/youtube_search.py tenemos el script que rastrea los vídeos
* pytube falla. Intentamos arreglarlo con:
    - C:\Users\Alday Lab\AppData\Local\Programs\Python\Python313\Lib\site-packages\pytube\cipher.py

* Debemos filtrar la búsqueda para evitar videos que no sean del propio personaje hablando. Podemos filtrar con terminos tipo "entrevista" o "conferencia"
* Sería lo ideal poder acceder a las "tags" o "etiquetas" asociadas a ese vídeo para luego categorizar el pensamiento en diversos temas de esa persona

PASOS CONCEPTUALES:

- Recibir el nombre del personaje público
- Filtrar para obtener conferencias, entrevistas, ponencias
- Obtener, además de los vídeos, descripciones y etiquetas


-----------------------------


## Entendiendo el reto:

* ¿Qué es fine-tuning?

* ¿Qué es Supervised Fine Tuning (formato chat completions de OpenAI)?

* ¿Cómo se dispone un dataset para entrenar un modelo?

* ¿Qué particularidades tiene JSONL?



## Enunciado del reto:

Construye el software definitivo para clonar personalidades a través de IA

CONTEXTO
La revolución de los Large Language Models ha abierto una frontera fascinante: la posibilidad de capturar y replicar el conocimiento, estilo y metodologías de pensadores únicos. Pero existe un cuello de botella crítico en este proceso.

Hoy, para crear un asistente de IA que piense como una personalidad específica, necesitas ser un experto en ML, dominar técnicas de scraping, transcripción, procesamiento de lenguaje natural y fine-tuning. Es un proceso artesanal que puede tomar semanas o meses.

¿Y si pudiéramos automatizarlo completamente?

Por eso nace esta misión: crear Da Cloner, un software que tome como input el nombre de cualquier persona relevante con suficiente contenido público, y genere automáticamente un dataset de calidad profesional listo para Supervised Fine Tuning (formato chat completions de OpenAI).

EL CASO DE PRUEBA: JAVIER GONZÁLEZ RECUENCO
Para demostrar tu sistema, lo probaremos con Javier González Recuenco, una elección estratégica por múltiples razones:

Personalidad única: CEO de Singular Solving y Presidente de Mensa España, Recuenco es un especialista singular en Complex Problem Solving (CPS). Ha desarrollado metodologías propias para abordar problemas "complejos" (sin precedentes válidos) versus problemas "complicados" (con métodos conocidos de resolución).

Contenido rico y disperso: Ha aparecido en más de 50 podcasts y entrevistas, es co-presentador del podcast semanal "Heavy Mental", y tiene aproximadamente 100-150 horas de contenido audiovisual donde explica frameworks únicos de pensamiento, personotecnia aplicada, transformación de incertidumbre en valor, y orquestación de equipos multidisciplinarios.

Reto técnico interesante: Su contenido está disperso en múltiples canales de YouTube (no tiene canal propio), requiere distinguir entre preguntas de entrevistadores y sus respuestas, y presenta vocabulario técnico específico del ámbito de resolución de problemas complejos.

TU MISIÓN
Desarrollar Da Cloner: un sistema generalizable que, dado el nombre de una persona relevante, produzca automáticamente un dataset de alta calidad para Supervised Fine Tuning.

ENTRADA DEL SISTEMA:

Nombre de la personalidad objetivo
(Opcional) URLs o fuentes específicas adicionales
SALIDA DEL SISTEMA:

Dataset estructurado en formato JSONL listo para fine-tuning (formato chatgpt completions).
System prompt optimizado para replicar el estilo de pensamiento
(Opcional) Modelo fine-tuneado como prueba de concepto
¿QUÉ DEBE CONSEGUIR PERSONALITY CLONER?
1. DESCUBRIMIENTO INTELIGENTE Tu sistema debe encontrar automáticamente todo el contenido relevante de la persona objetivo. YouTube será la fuente principal, pero puedes explorar otras plataformas (podcasts, entrevistas, charlas, el turrero post...) si consideras que añaden valor significativo.

El reto aquí es que la mayoría de personalidades aparecen como invitados en contenido de otros, no en sus propios canales.

2. EXTRACCIÓN Y VERIFICACIÓN Debe descargar el contenido encontrado y verificar que efectivamente corresponde a la persona objetivo. No queremos contaminar el dataset con contenido de otras personas.

3. TRANSCRIPCIÓN Y SEGMENTACIÓN Convertir el audio a texto con alta precisión y segmentar inteligentemente entre preguntas de entrevistadores y respuestas del objetivo. Este es crítico para generar pares Q&A de calidad.

4. GENERACIÓN DE DATASET Estructurar la información extraída en un dataset optimizado para Supervised Fine Tuning, incluyendo:

Pares pregunta-respuesta coherentes
Ejemplos de razonamiento característicos
Variaciones de contexto y situaciones
System prompt que capture el estilo único de pensamiento
5. AUTOMATIZACIÓN COMPLETA El sistema debe requerir mínima intervención manual. Idealmente, introduces "Javier González Recuenco" y en unas horas tienes un dataset listo para entrenar un modelo que piense como él.

CRITERIOS DE EVALUACIÓN
Automatización: ¿Puede una persona sin conocimientos técnicos usar tu sistema?

Calidad del output: ¿El dataset generado realmente captura el conocimiento y estilo único de Javier G. Recuenco?

Escalabilidad: ¿Tu sistema funcionaría igual de bien con otras personalidades?

Diseño del sistema

Capacidad de abordar el reto sin conocimientos previos del tema - Lo importante aquí no es si consigues crear el sistema, es ver cómo has pensado, y cómo te has acercado al objetivo. Eso nos dice mucho de ti.

(No tiene porque haber front-end, puedes hacer todo en consola. ¡Sin florituras!)

PLAZO
Tienes 7 días desde la recepción del reto.

LO QUE BUSCAMOS
No estamos construyendo un clon de Javier G. Recuenco. Estamos construyendo la infraestructura para democratizar la creación de asistentes de IA personalizados.

Tu sistema podría permitir que cualquier empresa clone el conocimiento de su CEO, que investigadores preserven el pensamiento de expertos, o que educadores creen tutores personalizados basados en los mejores profesores.

Demuéstranos que tienes la visión para ver el futuro de la personalización de IA y las habilidades para construirlo.

La personalización masiva de la inteligencia artificial empieza aquí.