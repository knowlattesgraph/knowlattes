from rdflib import Graph, plugin
from rdflib.store import Store
from rdflib_sqlalchemy import registerplugins

import os
import sys
import re
from tqdm import tqdm

from knowlattes.util import find_non_lattes_pages, all_the_files_in_directory
from knowlattes.parser_lattes import ParserLattes
from knowlattes.crawler import exception_handler

from rdflib import Graph, Namespace, plugin, Literal, URIRef
from rdflib.store import Store
from rdflib_sqlalchemy import registerplugins

import re
import hashlib
from toolz import curry


def add_lattes_reasercher_to_graph(lattes_page, graph, schema):
    """Given a lattes page object, adds all the possible triples on graph

    It adds a lattes page to RDFLib graph given a schema

    Parameters
    ----------
    lattes_page : lattes_object
        Lattes page object
    graph : rdflib_graph
        RDFLib graph
    schema: rdflib_schema
        RDFLib schema

    Returns
    -------
    None


    """

    @curry
    def add_non_duplicated(triple_or_quad, graph):
        """
            As RDFLib may fail when adding a triple that already exists, this function
            checks before adding the triple if it is already on the graph
        """
        if triple_or_quad not in graph:
            graph.add(triple_or_quad)

    add_triple = add_non_duplicated(graph=graph)

    uri = lattes_page.id_membro
    name = lattes_page.nome_completo
    first_name = name.split(" ")[0]
    family_name = " ".join(name.split(" ")[1:])
    gender = lattes_page.sexo

    researcher = URIRef(uri)

    add_triple((researcher, schema.type, schema.Person))
    add_triple((researcher, schema.name, Literal(name)))
    add_triple((researcher, schema.familyName, Literal(family_name)))
    add_triple((researcher, schema.givenName, Literal(first_name)))
    add_triple((researcher, schema.gender, Literal(gender)))

    # Check if the ID in lista_id_lattes_colaboradores is the same as uri (as in uri = lattes_page.id_membro)
    for colaborador in sorted(lattes_page.lista_id_lattes_colaboradores):
        # I assume the colaborator will be added to type Person in a different iteration.
        add_triple((researcher, schema.knows, URIRef(colaborador)))

    for idioma in lattes_page.lista_idioma:
        nome_idioma = idioma.nome
        add_triple((URIRef(nome_idioma), schema.type, schema.Language))
        add_triple((researcher, schema.knowsLanguage, Literal(nome_idioma)))

    for formacao_academica in lattes_page.lista_formacao_academica:
        tipo_formacao = formacao_academica.tipo
        instituicao = formacao_academica.nomeInstituicao
        instituicao_md5 = hashlib.md5(instituicao.encode("utf-8")).hexdigest()

        add_triple((URIRef(instituicao_md5), schema.type, schema.EducationalOrganization))
        add_triple((URIRef(instituicao_md5), schema.name, Literal(instituicao)))
        add_triple((researcher, schema.hasCredential, Literal(tipo_formacao)))
        add_triple((researcher, schema.alumniOf, Literal(instituicao)))

    for artigo_periodico in lattes_page.lista_artigo_em_periodico:
        doi_url = artigo_periodico.doi
        # Added springer nature format (we can remove later if needed)
        doi = re.sub("http://dx.doi.org/", "", doi_url)
        sameAsSpriger = "http://scigraph.springernature.com/" + "pub." + re.sub("http://dx.doi.org/", "", doi_url)
        # We are not using 'autores' for now.
        autores = artigo_periodico.autores
        ano = artigo_periodico.ano
        titulo = artigo_periodico.titulo
        genre = "artigo em periodico"

        if doi != "":
            add_triple((URIRef(doi), schema.name, Literal(titulo)))
            add_triple((URIRef(doi), schema.type, schema.ScholarlyArticle))
            add_triple((URIRef(doi), schema.author, researcher))
            add_triple((URIRef(doi), schema.datePublished, Literal(ano)))
            add_triple((URIRef(doi), schema.genre, Literal(genre)))
            add_triple((URIRef(doi), schema.sameAs, URIRef(sameAsSpriger)))

    for artigo_aceito in lattes_page.listaArtigoAceito:
        doi_url = artigo_periodico.doi
        doi = re.sub("http://dx.doi.org/", "", doi_url)
        # Added springer nature format (we can remove later if needed)
        sameAsSpriger = "http://scigraph.springernature.com/" + "pub." + re.sub("http://dx.doi.org/", "", doi_url)
        autores = artigo_aceito.autores
        ano = artigo_aceito.ano
        titulo = artigo_aceito.titulo
        genre = "artigo aceito para publicacao"

        if doi != "":
            add_triple((URIRef(doi), schema.type, schema.ScholarlyArticle))
            add_triple((URIRef(doi), schema.author, researcher))
            add_triple((URIRef(doi), schema.datePublished, Literal(ano)))
            add_triple((URIRef(doi), schema.name, Literal(titulo)))
            add_triple((URIRef(doi), schema.genre, Literal(genre)))
            add_triple((URIRef(doi), schema.sameAs, URIRef(sameAsSpriger)))

    for projeto_de_pesquisa in lattes_page.lista_projeto_de_pesquisa:
        ano = projeto_de_pesquisa.ano
        descricao = projeto_de_pesquisa.descricao
        nome = projeto_de_pesquisa.nome
        nome_md5 = hashlib.md5(nome.encode("utf-8")).hexdigest()

        add_triple((URIRef(nome_md5), schema.name, Literal(nome)))
        add_triple((URIRef(nome_md5), schema.type, schema.ResearchProject))
        # Maybe this property does not exist
        add_triple((URIRef(nome_md5), schema.year, Literal(ano)))
        add_triple((URIRef(nome_md5), schema.description, Literal(descricao)))
        add_triple((URIRef(nome_md5), schema.author, researcher))

    for trabalho_tecnico in lattes_page.listaTrabalhoTecnico:
        # We are not using 'autores' for now.
        autores = trabalho_tecnico.autores
        ano = trabalho_tecnico.ano
        titulo = trabalho_tecnico.titulo
        genre = "trabalho tecnico"
        nome_md5 = hashlib.md5(titulo.encode("utf-8")).hexdigest()

        add_triple((URIRef(nome_md5), schema.name, Literal(titulo)))
        add_triple((URIRef(nome_md5), schema.type, schema.TechArticle))
        add_triple((URIRef(nome_md5), schema.datePublished, Literal(ano)))
        add_triple((URIRef(nome_md5), schema.author, researcher))
        add_triple((URIRef(nome_md5), schema.genre, Literal(genre)))

    for livro in lattes_page.lista_livro_publicado:
        ano = livro.ano
        titulo = livro.titulo
        # We are not using 'autores' for now.
        autores = livro.autores
        edicao = livro.edicao
        editora = livro.editora
        paginas = livro.paginas
        nome_md5 = hashlib.md5(titulo.encode("utf-8")).hexdigest()

        add_triple((URIRef(nome_md5), schema.name, Literal(titulo)))
        add_triple((URIRef(nome_md5), schema.type, schema.Book))
        add_triple((URIRef(nome_md5), schema.datePublished, Literal(ano)))
        # Use researcher or 'autores'?
        add_triple((URIRef(nome_md5), schema.author, researcher))
        add_triple((URIRef(nome_md5), schema.bookEdition, Literal(edicao)))
        add_triple((URIRef(nome_md5), schema.editor, Literal(editora)))
        add_triple((URIRef(nome_md5), schema.numberOfPages, Literal(paginas)))

    for capitulo_livro in lattes_page.listaCapituloDeLivroPublicado:
        ano = capitulo_livro.ano
        titulo = capitulo_livro.titulo
        # We are not using 'autores' for now.
        autores = capitulo_livro.autores
        editora = capitulo_livro.editora
        paginas = capitulo_livro.paginas
        livro = capitulo_livro.livro
        nome_md5 = hashlib.md5(titulo.encode("utf-8")).hexdigest()

        add_triple((URIRef(nome_md5), schema.name, Literal(titulo)))
        add_triple((URIRef(nome_md5), schema.type, schema.Book))
        add_triple((URIRef(nome_md5), schema.datePublished, Literal(ano)))
        # Use researcher or 'autores'?
        add_triple((URIRef(nome_md5), schema.author, researcher))
        add_triple((URIRef(nome_md5), schema.isPartOf, Literal(livro)))
        add_triple((URIRef(nome_md5), schema.editor, Literal(editora)))
        add_triple((URIRef(nome_md5), schema.pagination, Literal(paginas)))


def generate_graph():
    """Main function that, will parse all the cache folder and will generate a graph with all its content
        
        Run this using python graph.py <path_to_dir_with_lattes_pages>

    Parameters
    ----------

    Returns
    -------

    """
    sys.excepthook = exception_handler
    registerplugins()

    # This is our ontology
    schema = Namespace("http://schema.org/version/latest/schema.nt#")
    identifier = URIRef("knowlattes_uriref")

    # Create the Graph ###
    SQLALCHEMY_URL = "sqlite:///%(here)s/database.sqlite" % {"here": os.getcwd()}
    print(f"Creating the file to output: {SQLALCHEMY_URL}")
    store = plugin.get("SQLAlchemy", Store)(identifier=identifier)
    graph = Graph(store, identifier=identifier)
    graph.open(SQLALCHEMY_URL, create=True)

    # Get the lattes list
    base_path = sys.argv[1]
    lattes_profile_list = all_the_files_in_directory(base_path)
    non_lattes_page = find_non_lattes_pages(base_path, lattes_profile_list)

    lattes_pages = [i for i in lattes_profile_list if i not in non_lattes_page]

    for lattes_page in tqdm(lattes_pages):
        lattes_id = re.sub(".html", "", lattes_page)

        file = open(base_path + "/" + lattes_page, "r", encoding="ISO-8859-1")
        lattes_file = file.read()
        file.close()

        lattes_page = ParserLattes(lattes_id, lattes_file)

        add_lattes_reasercher_to_graph(lattes_page, graph, schema)

    graph.close()


def load_grah(path=None):
    registerplugins()
    identifier = URIRef("rdflib_test")

    # Create the Graph
    SQLALCHEMY_URL = "sqlite:///%(here)s/database.sqlite" % {"here": os.getcwd() if path is None else path}
    print(f"Reading the file to output: {SQLALCHEMY_URL}")
    store = plugin.get("SQLAlchemy", Store)(identifier=identifier)

    graph = Graph(store, identifier=identifier)
    graph.open(SQLALCHEMY_URL, create=False)

    return graph


if __name__ == "__main__":
    generate_graph()
