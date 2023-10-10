import os
import openai
import json
from unidecode import unidecode
from dotenv import load_dotenv
from docx import Document
from docx.shared import Inches
from PyPDF2 import PdfReader

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
    "El modelo debe ser capaz de generar contenido basado en situaciones comunes en trabajos académicos, incluso si "
    "no se han proporcionado detalles específicos."
    "Puede inventar información basada en situaciones que no han pasado pero que es normal que ocurran en este tipo "
    "de trabajos."
    "Todas las respuestas deben estar enfocadas en la redacción del documento y estar escritas en lenguaje de "
    "programación LaTeX."
    "Centrate en elaborar el contenido de forma extensa, ahondando en la temática y desarrollando y explicando los "
    "conceptos."
    "Solo aborda el capítulo que se te pide y los sub apartados que tiene, redactalos de forma larga y extensa, "
    "redactalo en formato latex"
    "No concluyas cada texto que generes, no digas lo de 'En resumen...'"
)

text_analysis_prompt = (
    "Necesito que elabores del siguiente texto un análisis de la escritura de menos de 200 palabras que trate de:"
    "La definición del estilo de escritura del texto, no de qué trata el texto, sino del estilo de escritura de la persona que lo ha escrito"
    "Si ves que hay ciertas palabras que se repiten indícalo en el análisis, palabras que son características de la persona que ha escrito el texto"
    "Valora del 0 al 10, siendo 10 el nivel más alto, el nivel de complejidad de las oraciones del texto"
    "En el caso de que haya errores ortográficos, indícalo en el análisis"
    "En el caso de que haya errores gramaticales, indícalo en el análisis"
    "En el caso de que haya errores de puntuación, indícalo en el análisis"
)

project_guideline_analysis_prompt = (
    "Necesito que de este texto donde se pide la realización de un proyecto se devuelvas un objeto json con el siguiente formato: "
    "{ resumen : 'resumen del texto del proyecto que se desea realizar', indice_propuesto : [{nombre_del_capitulo_1: [subapartado_1, subapartado2...]},{nombre_del_capitulo_2: [subapartado_1, subapartado2...]}...] }"
)

indice = {}
project_summary = ""

type_of_project = -1
style_of_writing = ""
project_guideline_summary = ""


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

    return "Resumen de " + chapter + " " + response.choices[0].message["content"]


def gpt_text_analysis(text, model="gpt-4", max_tokens=700):
    messages = [
        {"role": "system", "content": text_analysis_prompt},
        {"role": "user", "content": text}]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.4,
    )
    print(response.choices[0].message["content"])
    return response.choices[0].message["content"]


def gpt_project_guideline_analysis(text, model="gpt-4", max_tokens=4000):
    messages = [
        {"role": "system", "content": project_guideline_analysis_prompt},
        {"role": "user", "content": text}]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=0.45,
    )
    print(response.choices[0].message["content"])
    return response.choices[0].message["content"]


def initialize_gpt_context(title, model="gpt-4", max_tokens=700):
    global project_context
    global indice
    messages = [
        {"role": "user",
         "content": "Elabora un guión y un resumen de 100 palabras para desarrollar un proyecto que trate de: " + title}]
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
        {"role": "user",
         "content": "Elabora un índice para desarrollar un un proyecto que trate de: '" + title + "' proyecta ese índice en formato json de la siguiente forma [\{nombre_del_capitulo_1: [subapartado_1, subapartado2...]\},\{nombre_del_capitulo_2: [subapartado_1, subapartado2...]\}...]"}]
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


def get_general_info_for_thesis():
    title = input("Introduce el título del trabajo: ")
    author = input("Introduce tu nombre: ")
    supervisor = input("Introduce el nombre de tu supervisor/tutor: ")
    department = input("Introduce el nombre del departamento: ")
    institution = input("Introduce el nombre de la institución: ")
    # initialize_gpt_context(title)
    # generate_main_file(title, author, supervisor, department, institution)
    return title, author, supervisor, department, institution


def get_general_info_for_projects():
    title = input("Introduce el título del proyecto: ")
    author = input("Introduce tu nombre: ")
    # initialize_gpt_context(title)
    # generate_main_file(title, author, "", "", "")
    return title, author, "", "", ""


def generate_latex_files(chapters):
    os.makedirs("generated", exist_ok=True)

    # Archivo .bib para la bibliografía
    bib_file = "generated/references.bib"
    write_latex_file(bib_file, "")

    # Archivos .tex individuales para cada capítulo
    for chapter_name, content in chapters.items():
        filename = f"generated/{chapter_name}.tex"
        write_latex_file(filename, content)


def write_new_file(filename, content):
    if_file_exists_delete(filename)
    with open(filename, "w") as file:
        file.write(content)


def if_file_exists_delete(filename):
    if os.path.exists(filename):
        os.remove(filename)


def select_project_type():
    global type_of_project
    type_of_project = input("¿Qué tipo de proyecto quieres generar? (1) Trabajo fin de grado, (2) Trabajo fin de "
                            "máster,(3) Trabajo estándar: ")
    while type_of_project not in ["1", "2", "3"]:
        type_of_project = input("Por favor, introduce un número válido: ")


def set_style_of_writing():
    global style_of_writing
    style_of_writing = input(
        "¿Qué tipo de estilo de escritura quieres generar? (1) Formal, (2) Personalizado (debes cargar un PDF), (3) Carga un estilo anterior: ")
    while style_of_writing not in ["1", "2", "3"]:
        style_of_writing = input("Por favor, introduce un número válido: ")
    if style_of_writing == "2":
        style_of_writing = input("Introduce la ruta del PDF: ")
        while not os.path.exists(style_of_writing):
            style_of_writing = input("Por favor, introduce una ruta válida: ")
        document_text = PdfReader(style_of_writing).pages[
            int(len(PdfReader(style_of_writing).pages) / 2)].extract_text()
        style_of_writing = gpt_text_analysis(document_text)
        save_style = input("¿Quieres guardar el estilo de escritura? (s/n): ")
        while save_style not in ["s", "n"]:
            save_style = input("Por favor, introduce una opción válida: ")
        if save_style == "s":
            save_style_of_writing()
    elif style_of_writing == "3":
        load_style_of_writing()


def save_style_of_writing():
    global style_of_writing
    style_of_writing = input("Introduce el nombre del estilo: ")
    while style_of_writing == "":
        style_of_writing = input("Por favor, introduce un nombre válido: ")
    write_latex_file(f"relevant_data/styles_of_writing/{style_of_writing}.txt", project_context)


def load_style_of_writing():
    global style_of_writing
    print("Estilos de escritura disponibles: ")
    list_of_writing_styles = os.listdir("data/styles_of_writing")
    for file_name in list_of_writing_styles:
        print(file_name)
    style_of_writing_name = input("Introduce el nombre del estilo: ")
    while style_of_writing_name not in list_of_writing_styles:
        style_of_writing_name = input("Por favor, introduce un nombre válido: ")
    style_of_writing = open(f"data/styles_of_writing/{style_of_writing}", "r").read()


def load_project_guidelines():
    get_project_guidelines = input("¿Quieres generar un proyecto para realizar? (s/n): ")
    while get_project_guidelines not in ["s", "n"]:
        get_project_guidelines = input("Por favor, introduce una opción válida: ")
    if get_project_guidelines == "s":
        generate_new_project_guideline_summary()
    else:
        print("Proyectos disponibles: ")
        list_of_project_guidelines = os.listdir("data/generated_guidelines/works")
        for file_name in list_of_project_guidelines:
            print(file_name)
        project_guideline = input("Introduce el nombre de la guía del proyecto: ")
        while project_guideline not in list_of_project_guidelines:
            style_of_writing_name = input("Por favor, introduce un nombre válido: ")
        load_project_guidelines_summary_from_json(project_guideline)


def generate_new_project_guideline_summary():
    print("Proyectos para realizar disponibles: ")
    list_of_project_guidelines = os.listdir("data/generated_guidelines")
    for file_name in list_of_project_guidelines:
        print(file_name)
    project_guideline = input("Introduce el nombre de la guía del proyecto: ")
    while project_guideline not in list_of_project_guidelines:
        style_of_writing_name = input("Por favor, introduce un nombre válido: ")
    # Read all the pages of the pdf
    document_text = ""
    for page in PdfReader(f"data/generated_guidelines/{project_guideline}").pages:
        document_text += page.extractText()
    project_guideline_json = gpt_project_guideline_analysis(document_text, project_guideline)
    save_project_guidelines_summary_in_json(project_guideline_json, project_guideline)


def save_project_guidelines_summary_in_json(project_guideline_json, filename):
    global project_guideline_summary
    global indice
    project_guideline_summary = project_guideline_json["resumen"]
    indice = project_guideline_json["indice_propuesto"]
    if os.path.exists(f"data/generated_guidelines/works/{filename}.json"):
        os.remove(f"data/generated_guidelines/works/{filename}.json")
    with open(f"data/generated_guidelines/works/{filename}.json", "w") as outfile:
        json.dump(project_guideline_json, outfile)


def load_project_guidelines_summary_from_json(filename):
    global project_guideline_summary
    global indice
    with open(f"data/generated_guidelines/works/{filename}", "r") as outfile:
        project_guideline_json = json.load(outfile)
    project_guideline_summary = project_guideline_json["resumen"]
    indice = project_guideline_json["indice_propuesto"]


def main():
    global project_context
    global type_of_project
    global indice

    select_project_type()

    set_style_of_writing()

    # clear_project_folder()

    if type_of_project == "1":
        title, author, supervisor, department, institution = get_general_info_for_thesis()
    elif type_of_project == "2":
        title, author, supervisor, department, institution = get_general_info_for_thesis()
    else:
        title, author, supervisor, department, institution = get_general_info_for_projects()

    load_project_guidelines()

    # for chapter in indice:
    #     for chapter_name, subchapters in chapter.items():
    #         # Genera el texto para el capítulo
    #         chapter_text = generate_text(
    #             chapter_name, f"Escribe la introducción a un capítulo sobre {chapter_name}. Recuerda hacerlo en latex",
    #             add_context=False)
    #         print(f"Capítulo: {chapter_name}\n{chapter_text}\n\n")
    #
    #         # Itera a través de los subapartados y genera el texto
    #         for subchapter in subchapters:
    #             subchapter_text = generate_text(
    #                 subchapter,
    #                 f"Escribe un subapartado para el capitulo de '{chapter_name}' que trate de '{subchapter}', recuerda hacerlo en latex",
    #                 add_context=False)
    #             print(f"Subapartado: {subchapter}\n{subchapter_text}\n\n")
    #             chapter_text += "\n" + subchapter_text
    #
    #     project_context = summarize_chapter(chapter_name, chapter_text)
    #     file_name = unidecode(chapter_name).lower().replace(" ", "_")
    #     generate_latex_files({file_name: chapter_text})


if __name__ == "__main__":
    main()
