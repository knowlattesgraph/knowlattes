#!/bin/python3
####################################
# Heavily inspired on ScriptLattes #
####################################

import sys, os
import codecs

from knowlattes.baixa_lattes import baixaCVLattes
from knowlattes.parser_lattes import ParserLattes

DIRETORIO_CACHE = "./cache"
ID_FILE_TYPE = ".html"
NUMBER_OF_FILES_TO_CRAWL = 50000
MEM_CACHE_SIZE = 50000


def criarDiretorio(dir):
    """Creates a directory if it doesnt' exists

    Extended description of function.

    Parameters
    ----------
    arg1 : dir
        path to create the directory

    Returns
    -------
    int
        0 if error or 1 if correct

    """
    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
        except:
            print("\n[ERRO] Não foi possível criar ou atualizar o diretório: " + dir.encode("utf8"))
            print("[ERRO] Você conta com as permissões de escrita? \n")
            return 0
    return 1


def baixa_lattes(id_membro, debug=False):
    """Download a CV file of a give id_membro

    It checks if th lattes page already have been doewloaded, if not, it downloads it calling
    baixaCVLattes.

    Parameters
    ----------
    id_membro : str
        String of lattes id
    debug : bool
        if should print debug

    Returns
    -------
    lattes_page
        return the object of lattes

    """
    cvPath = DIRETORIO_CACHE + "/" + idMembro + ID_FILE_TYPE

    # Checking if already cached
    if not os.path.exists(cvPath):
        print(" (*) O CV Nao esta em cache")
        try:
            cvLattesHTML = baixaCVLattes(id_membro, debug=debug)
            cvLattesHTML = cvLattesHTML.decode("ISO-8859-1", "replace")

            file = open(cvPath, "w", encoding="ISO-8859-1")
            file.write(cvLattesHTML)
            file.close()
            print("\t(*) O CV está sendo armazenado no Cache")
        except Exception as e:
            print(e)
    else:
        print("\t(*) O CV ja esta no cache")
        file = open(cvPath, "r", encoding="ISO-8859-1")
        cvLattesHTML = file.read()

    lattes_page = ParserLattes(idMembro, cvLattesHTML)

    return lattes_page


def exception_handler(exception_type, exception, traceback):
    """ Error handler

    This function is a handler for log output.
    As lattes pages are in iso8859, using this function will hide all the warning outputs generated
    by the parser

    Parameters
    ----------
    exception_type : any
        ---
    exception : any
        ---
    traceback: any
        ---

    Returns
    -------
    str
        Error message to be displayed

    """
    return ""  # "%s: %s" % (exception_type.__name__, exception)


def crawler_main():
    """ Crawlers

    Crawler a lattes_id, getting all the sub ids and crawling them.
    This will download all the linked pages

    Parameters
    ----------

    Returns
    -------
    None

    """
    sys.excepthook = exception_handler

    idMembro = sys.argv[1]
    criarDiretorio(DIRETORIO_CACHE)

    paginas_visitadas = []

    paginas_a_visitar = [idMembro]

    while len(paginas_visitadas) < NUMBER_OF_FILES_TO_CRAWL:
        print("Paginas visitadas " + str(len(paginas_visitadas)))
        print("Paginas a visitar " + str(len(paginas_a_visitar)))

        lattes_page = paginas_a_visitar.pop()
        url = "http://lattes.cnpq.br/" + lattes_page
        print("visitando: " + url)

        if not (lattes_page in paginas_visitadas):
            paginas_visitadas.append(lattes_page)
            try:
                new_lattes = baixa_lattes(str(lattes_page))
                if len(paginas_a_visitar) < MEM_CACHE_SIZE:
                    paginas_a_visitar = new_lattes.listaIDLattesColaboradores + paginas_a_visitar
            except Exception as e:
                print(e)
        else:
            print("\tPagina ja visitada")


if __name__ == "__main__":
    crawler_main()
