# PaperGenerator

_Innovando en la creación de documentos académicos_

## Descripción

PaperGenerator es una herramienta de apoyo para la redacción de documentos académicos, como investigaciones, tesis y disertaciones, que utiliza la tecnología GPT-4 de inteligencia artificial para ayudar en el proceso de escritura. Este proyecto tiene como objetivo facilitar la creación de contenidos de alta calidad y mejorar la productividad en el ámbito académico.

## Características

- Generación de texto utilizando el modelo GPT-4 de OpenAI.
- Integración con LaTeX para la creación de documentos académicos con formato profesional.
- Ayuda en la creación de contenido original y estructurado.
- Asistencia en la generación de bibliografía y citas correctamente atribuidas.
- Soporte para la personalización del contenido según las necesidades del usuario.

## Instalación

1.  Asegúrate de tener instalado Python 3.6 o superior en tu sistema. Puedes descargarlo desde la [página oficial de Python](https://www.python.org/downloads/).
2.  Clona el repositorio de PaperGenerator en tu máquina local:
    git clone https://github.com/alejomaf/PaperGenerator.git
3.  Navega hasta la carpeta del proyecto:

        cd paper-generator

4.  Crea un entorno virtual para instalar las dependencias:

        python3 -m venv venv

5.  Activa el entorno virtual:

- En Windows:

  ```
  venv\Scripts\activate
  ```

- En macOS y Linux:

  ```
  source venv/bin/activate
  ```

6.  Instala las dependencias del proyecto:

        pip install -r requirements.txt

## Uso

1.  Asegúrate de que el entorno virtual esté activado antes de ejecutar PaperGenerator.
2.  Edita el archivo `config.py` con tus credenciales de la API de OpenAI y las preferencias para el proyecto.
3.  Ejecuta el script principal:

        python paper_generator.py

4.  Sigue las instrucciones en pantalla para proporcionar información sobre el documento que deseas generar, como el título, los capítulos y los subapartados.
5.  PaperGenerator generará los archivos LaTeX (.tex) correspondientes a cada capítulo y subapartado, así como el archivo main.tex que incluye todas las secciones.
6.  Utiliza una herramienta de compilación LaTeX, como [TeXstudio](https://www.texstudio.org/) o [Overleaf](https://www.overleaf.com/), para compilar los archivos .tex y obtener un documento PDF con el contenido generado.

## Precauciones y responsabilidad

PaperGenerator está diseñado como una herramienta de apoyo y no como una solución completa para la creación de documentos académicos. Los usuarios deben ser conscientes de que esta herramienta no debe utilizarse como sustituto de su propio trabajo y esfuerzo. El contenido generado por PaperGenerator debe ser revisado y ajustado según las necesidades de cada proyecto específico.

Por favor, utiliza PaperGenerator de manera ética y responsable, cumpliendo con las políticas de integridad académica establecidas por las instituciones educativas. Los desarrolladores de PaperGenerator no se hacen responsables del uso indebido de la herramienta o de las consecuencias derivadas de su uso inapropiado.

## Contribución

Si deseas contribuir al proyecto, por favor sigue estos pasos:

1. Haz fork del repositorio en tu cuenta de GitHub.
2. Crea una nueva rama con un nombre descriptivo relacionado con las características o mejoras que deseas implementar.
3. Realiza los cambios en tu rama y asegúrate de que el código funciona correctamente.
4. Envía una solicitud de extracción desde tu rama a la rama principal del repositorio original.
5. Espera a que los mantenedores del proyecto revisen y aprueben tu solicitud.

También puedes contribuir reportando problemas o solicitando nuevas funcionalidades a través de la sección de _Issues_ del repositorio en GitHub.

## Licencia

Este proyecto está licenciado bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para obtener más detalles.

## Contacto

Si tienes preguntas o comentarios, no dudes en ponerte en contacto conmigo:

- Alejo
- Correo electrónico: [alejomaf@outlook.com](mailto:alejomaf@outlook.com)
- Página de GitHub: [http://alejomaf.github.io/](http://alejomaf.github.io/)
