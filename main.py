import os
import openai
import json
from unidecode import unidecode
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Importar la clave de la API de OpenAI desde el archivo .env
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

project_context = (
    "Estoy asistiendo en la elaboración de trabajos fin de grado y fin de máster en español de España. "
    "Los documentos serán escritos en tercera persona y en formato LaTeX. "
    "El usuario me proporcionará capítulo por capítulo para que vaya elaborando cada uno de los apartados. "
    "Debo elaborar el contenido de forma extensa, ahondando en la temática y desarrollando y explicando los conceptos. "
    "El modelo debe ser capaz de generar contenido basado en situaciones comunes en trabajos académicos, incluso si no se han proporcionado detalles específicos. "
    "Puede inventar información basada en situaciones que no han pasado pero que es normal que ocurran en este tipo de trabajos. "
    "Todas las respuestas deben estar enfocadas en la redacción del documento y estar escritas en lenguaje de programación LaTeX."
    "Centrate en elaborar el contenido de forma extensa, ahondando en la temática y desarrollando y explicando los conceptos."
    "Solo aborda el capítulo que se te pide y los subapartados que tiene, redactalos de forma larga y extensa, redactalo en formato latex"
    "No concluyas cada texto que generes, no digas lo de 'En resumen...'"
)

indice = {}


def generate_text(chapter, prompt, add_context=True, model="gpt-3.5-turbo", max_tokens=1000):
    global project_context
    messages = [{"role": "system", "content": project_context},
                {"role": "user", "content": prompt}]

    content_generated = False

    while not content_generated:
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                n=1,
                stop=None,
                temperature=0.4,  # this is the degree of randomness of the model's output
            )
            content_generated = True
        except:
            print("Error en la generación del capítulo, volviendo a intentar...")

    chapter_generated = response.choices[0].message["content"]
    if add_context:
        project_context += "\n" + summarize_chapter(chapter, prompt)
    # project_context += "\n" + chapter_generated
    print(project_context)
    return chapter_generated


def summarize_chapter(chapter, prompt, model="gpt-3.5-turbo", max_tokens=700):
    global project_context
    messages = [
        {"role": "system", "content": project_context},
        {"role": "user", "content": "Haz un resumen de este capítulo de menos de 60 palabras: " + prompt}]

    content_generated = False

    while not content_generated:
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                n=1,
                stop=None,
                temperature=0,  # this is the degree of randomness of the model's output
            )
            content_generated = True
        except:
            print("Error en la generación del resumen, volviendo a intentar...")

    return "Resumen de "+chapter+" "+response.choices[0].message["content"]


def initialize_gpt_context(title, model="gpt-3.5-turbo", max_tokens=700):
    global project_context
    global indice
    messages = [
        {"role": "user", "content": "Elabora un guión y un resumen de 100 palabras para desarrollar un proyecto que trate de: " + title}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.2,  # this is the degree of randomness of the model's output
    )
    project_context += "\n El proyecto trata de " + \
        response.choices[0].message["content"]

    messages = [
        {"role": "user", "content": "Elabora un índice para desarrollar un un proyecto que trate de: '" + title + "' proyecta ese índice en formato json de la siguiente forma [\{nombre_del_capitulo_1: [subapartado_1, subapartado2...]\},\{nombre_del_capitulo_2: [subapartado_1, subapartado2...]\}...]"}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    indice = json.loads(response.choices[0].message["content"])

    print(project_context)
    print(indice)


def get_general_info():
    title = input("Introduce el título del trabajo: ")
    author = input("Introduce tu nombre: ")
    supervisor = input("Introduce el nombre de tu supervisor/tutor: ")
    department = input("Introduce el nombre del departamento: ")
    institution = input("Introduce el nombre de la institución: ")
    initialize_gpt_context(title)
    generate_main_file(title, author, supervisor, department, institution)
    return title, author, supervisor, department, institution


def generate_latex_files(chapters):
    os.makedirs("proyecto", exist_ok=True)

    # Archivo .bib para la bibliografía
    bib_file = "proyecto/references.bib"
    write_latex_file(bib_file, "")

    # Archivos .tex individuales para cada capítulo
    for chapter_name, content in chapters.items():
        filename = f"proyecto/{chapter_name}.tex"
        write_latex_file(filename, content)


def write_latex_file(filename, content):
    # Eliminar el archivo si ya existe
    if os.path.exists(filename):
        os.remove(filename)

    # Crear un nuevo archivo con el nuevo contenido
    with open(filename, "w") as file:
        file.write(content)


def generate_main_file(title, author, supervisor, department, institution):
    global indice
    chapter_names = [list(d.keys())[0] for d in indice]

    # Crear una lista de las rutas de los archivos de capítulo
    chapter_filepaths = [
        f"{unidecode(chapter_name).lower().replace(' ', '_')}.tex" for chapter_name in chapter_names]

    # Archivo main.tex que incluye los archivos .tex de las secciones
    main_tex = f"""\\documentclass[12pt,a4paper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{lmodern}}
\\usepackage{{graphicx}}
\\usepackage{{hyperref}}
\\usepackage[backend=bibtex,style=numeric]{{biblatex}}


\\title{{{title}}}
\\author{{{author}}}
\\date{{}}

\\begin{{document}}

\\maketitle
"""

    # Agregar las rutas de los archivos de capítulo al main.tex
    for chapter_filepath in chapter_filepaths:
        main_tex += f"\\input{{{chapter_filepath}}}\n"

    main_tex += """
\\printbibliography

\\end{{document}}
"""

    write_latex_file("proyecto/main.tex", main_tex)


def clear_project_folder():
    folder = "proyecto"
    for file_name in os.listdir(folder):
        file_path = os.path.join(folder, file_name)
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            os.rmdir(file_path)


def main():
    global project_context
    global indice
    clear_project_folder()
    title, author, supervisor, department, institution = get_general_info()

    for chapter in indice:
        for chapter_name, subchapters in chapter.items():
            # Genera el texto para el capítulo
            chapter_text = generate_text(
                chapter_name, f"Escribe la introducción a un capítulo sobre {chapter_name}. Recuerda hacerlo en latex", add_context=False)
            print(f"Capítulo: {chapter_name}\n{chapter_text}\n\n")

            # Itera a través de los subapartados y genera el texto
            for subchapter in subchapters:
                subchapter_text = generate_text(
                    subchapter, f"Escribe un subapartado para el capitulo de '{chapter_name}' que trate de '{subchapter}', recuerda hacerlo en latex", add_context=False)
                print(f"Subapartado: {subchapter}\n{subchapter_text}\n\n")
                chapter_text += "\n"+subchapter_text

        project_context = summarize_chapter(chapter_name, chapter_text)
        file_name = unidecode(chapter_name).lower().replace(" ", "_")
        generate_latex_files({file_name: chapter_text})


if __name__ == "__main__":
    main()
