import os
import openai
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
    "Solo aborda el capítulo que se te pide, redactalo en formato latex"
)


def generate_text(chapter, prompt, model="gpt-3.5-turbo", max_tokens=1000):
    global project_context
    messages = [{"role": "system", "content": project_context},
                {"role": "user", "content": "Redacta el capítulo "+chapter+" en latex que trata de '''"+prompt+"'''"}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    chapter_generated = response.choices[0].message["content"]
    project_context += "\n" + summarize_chapter(chapter, prompt)
    print(project_context)
    return chapter_generated


def summarize_chapter(chapter, prompt, model="gpt-3.5-turbo", max_tokens=700):
    global project_context
    messages = [
        {"role": "system", "content": project_context},
        {"role": "user", "content": "Haz un resumen de este capítulo de menos de 100 palabras: " + prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return "Resumen de "+chapter+" "+response.choices[0].message["content"]


def initialize_gpt_context(title, model="gpt-3.5-turbo", max_tokens=700):
    global project_context
    messages = [
        {"role": "user", "content": "Elabora un guión y un resumen de 200 palabras para desarrollar un proyecto que trate de: " + title}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    project_context += "\n El proyecto trata de " + \
        response.choices[0].message["content"]
    print(project_context)


def get_general_info():
    title = input("Introduce el título del trabajo: ")
    author = input("Introduce tu nombre: ")
    supervisor = input("Introduce el nombre de tu supervisor/tutor: ")
    department = input("Introduce el nombre del departamento: ")
    institution = input("Introduce el nombre de la institución: ")
    initialize_gpt_context(title)
    generate_main_file(title, author, supervisor, department, institution)
    return title, author, supervisor, department, institution


def generate_abstract():
    abstract_prompt = input(
        "Describe brevemente el propósito y enfoque de tu investigación: ")
    abstract = generate_text(
        "Propósito y enfoque de la investigación", abstract_prompt)
    generate_latex_files({"abstract": abstract})
    return abstract


def generate_introduction():
    introduction_prompt = input(
        "Proporciona información básica sobre el tema de investigación y el problema que abordarás: ")
    introduction = generate_text(
        "Investigación y problema que se abordará", introduction_prompt)
    generate_latex_files({"introduction": introduction})
    return introduction


def generate_literature_review():
    literature_review_prompt = input(
        "Menciona algunas investigaciones o teorías relevantes relacionadas con tu tema: ")
    literature_review = generate_text(
        "Investigaciones previas", literature_review_prompt)
    generate_latex_files({"literature_review": literature_review})
    return literature_review


def generate_methodology():
    methodology_prompt = input(
        "Describe brevemente los métodos y técnicas que utilizarás en tu investigación: ")
    methodology = generate_text("Metodología y técnicas", methodology_prompt)
    generate_latex_files({"methodology": methodology})
    return methodology


def generate_results():
    results_prompt = input(
        "Describe los resultados esperados de tu investigación: ")
    results = generate_text(
        "Resultados esperados de la investigación", results_prompt)
    generate_latex_files({"results": results})
    return results


def generate_conclusion():
    conclusion_prompt = input(
        "Resume brevemente los hallazgos de tu investigación y su relevancia: ")
    conclusion = generate_text(
        "Resultados de la investigación", conclusion_prompt)
    generate_latex_files({"conclusion": conclusion})
    return conclusion


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

\\input{{abstract}}
\\input{{introduction}}
\\input{{literature_review}}
\\input{{methodology}}
\\input{{results}}
\\input{{conclusion}}

\\printbibliography

\\end{{document}}
"""
    write_latex_file("proyecto/main.tex", main_tex)
# \\addbibresource{{{bib_file}}}


def main():
    title, author, supervisor, department, institution = get_general_info()
    abstract = generate_abstract()
    introduction = generate_introduction()
    literature_review = generate_literature_review()
    methodology = generate_methodology()
    results = generate_results()
    conclusion = generate_conclusion()

    # Aquí puedes agregar código para generar el archivo LaTeX a partir de las secciones generadas
    # Agrega esta línea al final de la función 'main()' para generar los archivos LaTeX
    generate_latex_files(title, author, supervisor, department, institution,
                         abstract, introduction, literature_review, methodology, results, conclusion)


if __name__ == "__main__":
    main()
