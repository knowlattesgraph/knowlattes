#!/usr/bin/python
# encoding: utf-8
# filename: parserLattes.py
#
# scriptLattes V8
# Copyright 2005-2013: Jesús P. Mena-Chalco e Roberto M. Cesar-Jr.
#  http://scriptlattes.sourceforge.net/
#
#
#  Este programa é um software livre; você pode redistribui-lo e/ou
#  modifica-lo dentro dos termos da Licença Pública Geral GNU como
#  publicada pela Fundação do Software Livre (FSF); na versão 2 da
#  Licença, ou (na sua opinião) qualquer versão.
#
#  Este programa é distribuído na esperança que possa ser util,
#  mas SEM NENHUMA GARANTIA; sem uma garantia implicita de ADEQUAÇÂO a qualquer
#  MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a
#  Licença Pública Geral GNU para maiores detalhes.
#
#  Você deve ter recebido uma cópia da Licença Pública Geral GNU
#  junto com este programa, se não, escreva para a Fundação do Software
#  Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#

import sys, re
from html.entities import name2codepoint
from tidylib import tidy_document

# ---------------------------------------------------------------------------- #
from html.parser import HTMLParser
from knowlattes.producoesUnitarias.formacaoAcademica import *
from knowlattes.producoesUnitarias.areaDeAtuacao import *
from knowlattes.producoesUnitarias.idioma import *
from knowlattes.producoesUnitarias.premioOuTitulo import *
from knowlattes.producoesUnitarias.projetoDePesquisa import *

from knowlattes.producoesBibliograficas.artigoEmPeriodico import *
from knowlattes.producoesBibliograficas.livroPublicado import *
from knowlattes.producoesBibliograficas.capituloDeLivroPublicado import *
from knowlattes.producoesBibliograficas.textoEmJornalDeNoticia import *
from knowlattes.producoesBibliograficas.trabalhoCompletoEmCongresso import *
from knowlattes.producoesBibliograficas.resumoExpandidoEmCongresso import *
from knowlattes.producoesBibliograficas.resumoEmCongresso import *
from knowlattes.producoesBibliograficas.artigoAceito import *
from knowlattes.producoesBibliograficas.apresentacaoDeTrabalho import *
from knowlattes.producoesBibliograficas.outroTipoDeProducaoBibliografica import *

from knowlattes.producoesTecnicas.softwareComPatente import *
from knowlattes.producoesTecnicas.softwareSemPatente import *
from knowlattes.producoesTecnicas.produtoTecnologico import *
from knowlattes.producoesTecnicas.processoOuTecnica import *
from knowlattes.producoesTecnicas.trabalhoTecnico import *
from knowlattes.producoesTecnicas.outroTipoDeProducaoTecnica import *

from knowlattes.producoesArtisticas.producaoArtistica import *

from knowlattes.orientacoes.orientacaoEmAndamento import *
from knowlattes.orientacoes.orientacaoConcluida import *

from knowlattes.eventos.organizacaoDeEvento import *
from knowlattes.eventos.participacaoEmEvento import *

sys.tracebacklimit = 0


class ParserLattes(HTMLParser):
    """This is the class that starts the HTML page parser.
    
    It will go though each one of the html tags, searching for known patterns and filling the object lattes page
    with its info

    Parameters
    ----------
    
    Returns
    -------
    
    """

    identificador16 = ""
    item = None
    nome_completo = ""
    bolsa_produtividade = ""
    endereco_profissional = ""
    sexo = ""
    nome_em_citacoes_bibliograficas = ""
    atualizacao_cv = ""
    foto = ""
    textoResumo = ""

    salvarIdentificador16 = None
    salvar_nome = None
    salvar_bolsa_produtividade = None
    salvar_endereco_profissional = None
    salvarSexo = None
    salvar_nomeEmCitacoes = None
    salvaratualizacao_cv = None
    salvarTextoResumo = None
    salvarFormacaoAcademica = None
    salvarProjetoDePesquisa = None
    salvarAreaDeAtuacao = None
    salvarIdioma = None
    salvarPremioOuTitulo = None
    salvarItem = None
    salvarParticipacaoEmEvento = None
    salvarOrganizacaoDeEvento = None

    # novos atributos
    achouIdentificacao = None
    achouEndereco = None
    salvarParte1 = None
    salvarParte2 = None
    salvarParte3 = None
    achouProducoes = None
    achouProducaoEmCTA = None
    achouProducaoTecnica = None
    achouProducaoArtisticaCultural = None
    achouOutraProducaoArtisticaCultural = None
    achouBancas = None
    achouEventos = None
    achouOrientacoes = None
    achouOutrasInformacoesRelevantes = None
    spanInformacaoArtigo = None

    recuperarIdentificador16 = None

    achouGrupo = None
    achouendereco_profissional = None
    achouSexo = None
    achouNomeEmCitacoes = None
    achouFormacaoAcademica = None
    achouProjetoDePesquisa = None
    achouAreaDeAtuacao = None
    achouIdioma = None
    achouPremioOuTitulo = None

    achouArtigoEmPeriodico = None
    achouLivroPublicado = None
    achouCapituloDeLivroPublicado = None
    achouTextoEmJornalDeNoticia = None
    achouTrabalhoCompletoEmCongresso = None
    achouResumoExpandidoEmCongresso = None
    achouResumoEmCongresso = None
    achouArtigoAceito = None
    achouApresentacaoDeTrabalho = None
    achouOutroTipoDeProducaoBibliografica = None

    achouSoftwareComPatente = None
    achouSoftwareSemPatente = None
    achouProdutoTecnologico = None
    achouProcessoOuTecnica = None
    achouTrabalhoTecnico = None
    achouOutroTipoDeProducaoTecnica = None

    achouPatente = None
    achouProgramaComputador = None
    achouDesenhoIndustrial = None
    achouPatenteRegistro = None

    achouProducaoArtistica = None

    achouOrientacoesEmAndamento = None
    achouOrientacoesConcluidas = None
    achouSupervisaoDePosDoutorado = None
    achouTeseDeDoutorado = None
    achouDissertacaoDeMestrado = None
    achouMonografiaDeEspecializacao = None
    achouTCC = None
    achouIniciacaoCientifica = None
    achouOutroTipoDeOrientacao = None

    achouParticipacaoEmEvento = None
    achouOrganizacaoDeEvento = None

    procurarCabecalho = None
    partesDoItem = []

    lista_id_lattes_colaboradores = []
    lista_formacao_academica = []
    lista_projeto_de_pesquisa = []
    lista_area_de_atuacao = []
    lista_idioma = []
    lista_premio_ou_titulo = []

    lista_artigo_em_periodico = []
    lista_livro_publicado = []
    listaCapituloDeLivroPublicado = []
    listaTextoEmJornalDeNoticia = []
    listaTrabalhoCompletoEmCongresso = []
    listaResumoExpandidoEmCongresso = []
    listaResumoEmCongresso = []
    listaArtigoAceito = []
    listaApresentacaoDeTrabalho = []
    listaOutroTipoDeProducaoBibliografica = []

    listaSoftwareComPatente = []
    listaSoftwareSemPatente = []
    listaProdutoTecnologico = []
    listaProcessoOuTecnica = []
    listaTrabalhoTecnico = []
    listaOutroTipoDeProducaoTecnica = []

    listaPatente = []
    listaProgramaComputador = []
    listaDesenhoIndustrial = []

    listaProducaoArtistica = []

    # Orientaççoes em andamento (OA)
    listaOASupervisaoDePosDoutorado = []
    listaOATeseDeDoutorado = []
    listaOADissertacaoDeMestrado = []
    listaOAMonografiaDeEspecializacao = []
    listaOATCC = []
    listaOAIniciacaoCientifica = []
    listaOAOutroTipoDeOrientacao = []

    # Orientações concluídas (OC)
    listaOCSupervisaoDePosDoutorado = []
    listaOCTeseDeDoutorado = []
    listaOCDissertacaoDeMestrado = []
    listaOCMonografiaDeEspecializacao = []
    listaOCTCC = []
    listaOCIniciacaoCientifica = []
    listaOCOutroTipoDeOrientacao = []

    # Eventos
    listaParticipacaoEmEvento = []
    listaOrganizacaoDeEvento = []

    # auxiliares
    doi = ""
    relevante = 0
    umaUnidade = 0
    id_orientando = None
    citado = 0
    complemento = ""

    # ------------------------------------------------------------------------ #
    def __init__(self, id_membro, cv_lattes_html):
        """Parse the page, receiving the id_membro and the cv_lattes_html page

        Parameters
        ----------
        id_membro : str
            membro_id of lattes
        cv_lattes_html : str
            html page of id_membro

        Returns
        -------
        lattes_page: Object
            Lattes page object

        """
        HTMLParser.__init__(self)

        # inicializacao obrigatoria
        self.id_membro = id_membro
        self.sexo = "Masculino"
        self.nome_completo = u"[Nome-nao-identificado]"

        self.item = ""
        self.issn = ""
        self.lista_id_lattes_colaboradores = []
        self.lista_formacao_academica = []
        self.lista_projeto_de_pesquisa = []
        self.lista_area_de_atuacao = []
        self.lista_idioma = []
        self.lista_premio_ou_titulo = []

        self.lista_artigo_em_periodico = []
        self.lista_livro_publicado = []
        self.listaCapituloDeLivroPublicado = []
        self.listaTextoEmJornalDeNoticia = []
        self.listaTrabalhoCompletoEmCongresso = []
        self.listaResumoExpandidoEmCongresso = []
        self.listaResumoEmCongresso = []
        self.listaArtigoAceito = []
        self.listaApresentacaoDeTrabalho = []
        self.listaOutroTipoDeProducaoBibliografica = []

        self.listaSoftwareComPatente = []
        self.listaSoftwareSemPatente = []
        self.listaProdutoTecnologico = []
        self.listaProcessoOuTecnica = []
        self.listaTrabalhoTecnico = []
        self.listaOutroTipoDeProducaoTecnica = []

        self.listaPatente = []
        self.listaProgramaComputador = []
        self.listaDesenhoIndustrial = []

        self.listaProducaoArtistica = []

        self.listaOASupervisaoDePosDoutorado = []
        self.listaOATeseDeDoutorado = []
        self.listaOADissertacaoDeMestrado = []
        self.listaOAMonografiaDeEspecializacao = []
        self.listaOATCC = []
        self.listaOAIniciacaoCientifica = []
        self.listaOAOutroTipoDeOrientacao = []

        self.listaOCSupervisaoDePosDoutorado = []
        self.listaOCTeseDeDoutorado = []
        self.listaOCDissertacaoDeMestrado = []
        self.listaOCMonografiaDeEspecializacao = []
        self.listaOCTCC = []
        self.listaOCIniciacaoCientifica = []
        self.listaOCOutroTipoDeOrientacao = []

        self.listaParticipacaoEmEvento = []
        self.listaOrganizacaoDeEvento = []

        # inicializacao para evitar a busca exaustiva de algumas palavras-chave
        self.salvaratualizacao_cv = 1
        self.salvarFoto = 1
        self.procurarCabecalho = 0
        self.achouGrupo = 0
        self.doi = ""
        self.relevante = 0
        self.id_orientando = ""
        self.complemento = ""

        # contornamos alguns erros do HTML da Plataforma Lattes
        cv_lattes_html = cv_lattes_html.replace("<![CDATA[", "")
        cv_lattes_html = cv_lattes_html.replace("]]>", "")
        cv_lattes_html = cv_lattes_html.replace("<x<", "&lt;x&lt;")

        # pdb.set_trace()

        # feed it!
        tidy_options = {
            # 'output-xhtml': 0,
            # 'force-output': 1,
            "numeric-entities": 1,
            # "char-encoding": "iso8859-1",
            "input-encoding": "iso8859-1",
        }

        try:
            cv_lattes_html, errors = tidy_document(cv_lattes_html, options=tidy_options)
        except UnicodeDecodeError:
            # In case something happens in pytidylib we'll try again with
            # a proper encoding
            cv_lattes_html = tidy_document(cv_lattes_html.encode("utf-8"), options=tidy_options)
            tidied, errors = cv_lattes_html
            cv_lattes_html = tidied.decode("utf-8"), errors

        # tentativa errada (não previsível)
        # options = dict(output_xhtml=1, add_xml_decl=1, indent=1, tidy_mark=0)
        # cv_lattes_html = str(tidy.parseString(cv_lattes_html, **options)).decode("utf8")

        self.feed(cv_lattes_html)

    # ------------------------------------------------------------------------ #

    def parse_issn(self, url):
        """

        """
        s = url.find("issn=")
        if s == -1:
            return None
        e = url.find("&", s)
        if e == -1:
            return None

        issnvalue = url[s:e].split("=")
        issn = issnvalue[1]
        if len(issn) < 8:
            return
        issn = issn[:8]
        self.issn = issn[0:4] + "-" + issn[4:8]

    def handle_starttag(self, tag, attributes):
        """
            
        """
        if tag == "h2":
            for name, value in attributes:
                if name == "class" and value == "nome":
                    self.salvar_nome = 1
                    self.item = ""
                    break

        if tag == "li":
            self.recuperarIdentificador16 = 1

        if tag == "p":
            for name, value in attributes:
                if name == "class" and value == "resumo":
                    self.salvarTextoResumo = 1
                    self.item = ""
                    break

        if tag == "span" and self.salvar_nome:
            self.item = ""
            self.salvar_bolsa_produtividade = 1
            self.salvar_nome = 0

        if tag == "div":
            self.citado = 0

            for name, value in attributes:
                if name == "cvuri":
                    self.parse_issn(value)

            for name, value in attributes:
                if name == "class" and value == "title-wrapper":
                    self.umaUnidade = 1
                    break

            for name, value in attributes:
                if name == "class" and value == "layout-cell-pad-5":
                    if self.achouNomeEmCitacoes:
                        self.salvar_nomeEmCitacoes = 1
                        self.item = ""

                    if self.achouSexo:
                        self.salvarSexo = 1
                        self.item = ""

                    if self.achouendereco_profissional:
                        self.salvar_endereco_profissional = 1
                        self.item = ""

                    if self.salvarParte1:
                        self.salvarParte1 = 0
                        self.salvarParte2 = 1

                if name == "class" and value == "layout-cell-pad-5 text-align-right":
                    self.item = ""
                    if (
                        self.achouFormacaoAcademica
                        or self.achouAtuacaoProfissional
                        or self.achouProjetoDePesquisa
                        or self.achouMembroDeCorpoEditorial
                        or self.achouRevisorDePeriodico
                        or self.achouAreaDeAtuacao
                        or self.achouIdioma
                        or self.achouPremioOuTitulo
                        or self.salvarItem
                    ):
                        self.salvarParte1 = 1
                        self.salvarParte2 = 0
                        if not self.salvarParte3:
                            self.partesDoItem = []

                if name == "class" and (value == "citacoes" or value == "citado"):
                    self.citado = 1

                if name == "cvuri" and self.citado:
                    self.citado = 0
                    self.complemento = value.replace("/buscatextual/servletcitacoes?", "")

        if tag == "h1" and self.umaUnidade:
            self.procurarCabecalho = 1

            self.achouIdentificacao = 0
            self.achouEndereco = 0
            self.achouFormacaoAcademica = 0
            self.achouAtuacaoProfissional = 0
            self.achouProjetoDePesquisa = 0
            self.achouMembroDeCorpoEditorial = 0
            self.achouRevisorDePeriodico = 0
            self.achouAreaDeAtuacao = 0
            self.achouIdioma = 0
            self.achouPremioOuTitulo = 0
            self.achouProducoes = 0
            # self.achouProducaoEmCTA = 0
            # self.achouProducaoTecnica = 0
            # self.achouProducaoArtisticaCultural = 0
            self.achouBancas = 0
            self.achouEventos = 0
            self.achouOrientacoes = 0
            self.achouOutrasInformacoesRelevantes = 0
            self.salvarItem = 0
            self.achouPatenteRegistro = 0

        if tag == "img":
            if self.salvarFoto:
                for name, value in attributes:
                    if name == "src" and u"servletrecuperafoto" in value:
                        self.foto = value
                        self.salvarFoto = 0
                        break

            if self.salvarItem:
                for name, value in attributes:
                    if name == "src" and u"ico_relevante" in value:
                        self.relevante = 1
                        break

                """for name,value in attributes:
                    if name=='data-issn':
                        if len(value) == 8:
                            self.issn = value[0:4]+'-'+value[4:8]
                        break
                """

        if tag == "br":
            self.item = self.item + " "

        if tag == "span":
            if self.achouProducaoEmCTA:
                for name, value in attributes:
                    if name == "class" and value == u"informacao-artigo":
                        self.spanInformacaoArtigo = 1

        if tag == "a":
            if self.salvarItem:  # and self.achouArtigoEmPeriodico:
                for name, value in attributes:
                    if name == "href" and u"doi" in value:
                        self.doi = value
                        break

                    id = re.findall(u"http://lattes.cnpq.br/(\d{16})", value)
                    if name == "href" and len(id) > 0:
                        self.lista_id_lattes_colaboradores.append(id[0])
                        if self.achouOrientacoesEmAndamento or self.achouOrientacoesConcluidas:
                            self.id_orientando = id[0]
                        break

    # ------------------------------------------------------------------------ #
    def handle_endtag(self, tag):
        """
            
        """
        # pdb.set_trace()
        # Informações do pesquisador (pre-cabecalho)
        if tag == "h2" and self.salvar_nome:
            self.nome_completo = stripBlanks(self.item)
            self.salvar_nome = 0
            self.item = ""

        if tag == "p":
            if self.salvarTextoResumo:
                self.textoResumo = stripBlanks(self.item)
                self.salvarTextoResumo = 0

        if tag == "span" and self.salvar_bolsa_produtividade:
            self.bolsa_produtividade = stripBlanks(self.item)
            self.bolsa_produtividade = re.sub(
                "Bolsista de Produtividade em Pesquisa do CNPq - ", "", self.bolsa_produtividade
            )
            self.bolsa_produtividade = self.bolsa_produtividade.strip("()")
            self.salvar_bolsa_produtividade = 0
            self.item = ""

        if tag == "span" and self.salvarIdentificador16 == 1:
            self.identificador16 = re.findall(u"http://lattes.cnpq.br/(\d{16})", value)
            self.salvarIdentificador16 = 0

        # Cabeçalhos
        if tag == "h1" and self.procurarCabecalho:
            self.procurarCabecalho = 0

        if tag == "div":
            if self.salvar_nomeEmCitacoes:
                self.nome_em_citacoes_bibliograficas = stripBlanks(self.item)
                self.salvar_nomeEmCitacoes = 0
                self.achouNomeEmCitacoes = 0
            if self.salvarSexo:
                self.sexo = stripBlanks(self.item)
                self.salvarSexo = 0
                self.achouSexo = 0
            if self.salvar_endereco_profissional:
                self.endereco_profissional = stripBlanks(self.item)
                self.endereco_profissional = re.sub("'", "", self.endereco_profissional)
                self.endereco_profissional = re.sub('"', "", self.endereco_profissional)
                self.salvar_endereco_profissional = 0
                self.achouendereco_profissional = 0

            if (self.salvarParte1 and not self.salvarParte2) or (self.salvarParte2 and not self.salvarParte1):
                if len(stripBlanks(self.item)) > 0:
                    self.partesDoItem.append(stripBlanks(self.item))  # acrescentamos cada celula da linha em uma lista!
                    self.item = ""

                if self.salvarParte2:
                    self.salvarParte1 = 0
                    self.salvarParte2 = 0

                    if self.achouFormacaoAcademica and len(self.partesDoItem) >= 2:
                        iessimaFormacaoAcademica = FormacaoAcademica(
                            self.partesDoItem
                        )  # criamos um objeto com a lista correspondentes às celulas da linha
                        self.lista_formacao_academica.append(
                            iessimaFormacaoAcademica
                        )  # acrescentamos o objeto de FormacaoAcademica

                    # if self.achouAtuacaoProfissional:
                    # 	print self.partesDoItem

                    if self.achouProjetoDePesquisa:
                        if not self.salvarParte3:
                            self.salvarParte3 = 1
                        else:
                            self.salvarParte3 = 0
                            if len(self.partesDoItem) >= 3:
                                iessimoProjetoDePesquisa = ProjetoDePesquisa(
                                    self.id_membro, self.partesDoItem
                                )  # criamos um objeto com a lista correspondentes às celulas da linha
                                self.lista_projeto_de_pesquisa.append(
                                    iessimoProjetoDePesquisa
                                )  # acrescentamos o objeto de ProjetoDePesquisa

                    # if self.achouMembroDeCorpoEditorial:
                    # 	print self.partesDoItem

                    # if self.achouRevisorDePeriodico:
                    # 	print self.partesDoItem

                    if self.achouAreaDeAtuacao and len(self.partesDoItem) >= 2:
                        iessimaAreaDeAtucao = AreaDeAtuacao(
                            self.partesDoItem
                        )  # criamos um objeto com a lista correspondentes às celulas da linha
                        self.lista_area_de_atuacao.append(
                            iessimaAreaDeAtucao
                        )  # acrescentamos o objeto de AreaDeAtuacao

                    if self.achouIdioma and len(self.partesDoItem) >= 2:
                        iessimoIdioma = Idioma(
                            self.partesDoItem
                        )  # criamos um objeto com a lista correspondentes às celulas da linha
                        self.lista_idioma.append(iessimoIdioma)  # acrescentamos o objeto de Idioma

                    if self.achouPremioOuTitulo and len(self.partesDoItem) >= 2:
                        iessimoPremio = PremioOuTitulo(
                            self.id_membro, self.partesDoItem
                        )  # criamos um objeto com a lista correspondentes às celulas da linha
                        self.lista_premio_ou_titulo.append(iessimoPremio)  # acrescentamos o objeto de PremioOuTitulo

                        # if self.achouPatenteRegistro:
                    # 	#print "===>>>> PROCESSANDO PATENTE e REGISTRO"
                    # 	if self.achouPatente:
                    # 		iessimoItem = Patente(self.id_membro, self.partesDoItem, self.relevante)
                    # 		self.listaPatente.append(iessimoItem)
                    # 	if self.achouProgramaComputador:
                    # 		iessimoItem = ProgramaComputador(self.id_membro, self.partesDoItem, self.relevante)
                    # 		self.listaProgramaComputador.append(iessimoItem)
                    # 	if self.achouDesenhoIndustrial:
                    # 		iessimoItem = DesenhoIndustrial(self.id_membro, self.partesDoItem, self.relevante)
                    # 		self.listaDesenhoIndustrial.append(iessimoItem)

                    if self.achouProducoes:
                        if self.achouProducaoEmCTA:
                            if self.achouArtigoEmPeriodico:
                                iessimoItem = ArtigoEmPeriodico(
                                    self.id_membro, self.partesDoItem, self.doi, self.relevante, self.complemento
                                )
                                self.lista_artigo_em_periodico.append(iessimoItem)
                                self.doi = ""
                                self.issn = ""
                                self.relevante = 0
                                self.complemento = ""

                            if self.achouLivroPublicado:
                                iessimoItem = LivroPublicado(self.id_membro, self.partesDoItem, self.relevante)
                                self.lista_livro_publicado.append(iessimoItem)
                                self.relevante = 0

                            if self.achouCapituloDeLivroPublicado:
                                iessimoItem = CapituloDeLivroPublicado(
                                    self.id_membro, self.partesDoItem, self.relevante
                                )
                                self.listaCapituloDeLivroPublicado.append(iessimoItem)
                                self.relevante = 0

                            if self.achouTextoEmJornalDeNoticia:
                                iessimoItem = TextoEmJornalDeNoticia(self.id_membro, self.partesDoItem, self.relevante)
                                self.listaTextoEmJornalDeNoticia.append(iessimoItem)
                                self.relevante = 0

                            if self.achouTrabalhoCompletoEmCongresso:
                                iessimoItem = TrabalhoCompletoEmCongresso(
                                    self.id_membro, self.partesDoItem, self.doi, self.relevante
                                )
                                self.listaTrabalhoCompletoEmCongresso.append(iessimoItem)
                                self.doi = ""
                                self.relevante = 0

                            if self.achouResumoExpandidoEmCongresso:
                                iessimoItem = ResumoExpandidoEmCongresso(
                                    self.id_membro, self.partesDoItem, self.doi, self.relevante
                                )
                                self.listaResumoExpandidoEmCongresso.append(iessimoItem)
                                self.doi = ""
                                self.relevante = 0

                            if self.achouResumoEmCongresso:
                                iessimoItem = ResumoEmCongresso(
                                    self.id_membro, self.partesDoItem, self.doi, self.relevante
                                )
                                self.listaResumoEmCongresso.append(iessimoItem)
                                self.doi = ""
                                self.relevante = 0

                            if self.achouArtigoAceito:
                                iessimoItem = ArtigoAceito(self.id_membro, self.partesDoItem, self.doi, self.relevante)
                                self.listaArtigoAceito.append(iessimoItem)
                                self.doi = ""
                                self.relevante = 0

                            if self.achouApresentacaoDeTrabalho:
                                iessimoItem = ApresentacaoDeTrabalho(self.id_membro, self.partesDoItem, self.relevante)
                                self.listaApresentacaoDeTrabalho.append(iessimoItem)

                            if self.achouOutroTipoDeProducaoBibliografica:
                                iessimoItem = OutroTipoDeProducaoBibliografica(
                                    self.id_membro, self.partesDoItem, self.relevante
                                )
                                self.listaOutroTipoDeProducaoBibliografica.append(iessimoItem)

                        if self.achouProducaoTecnica:
                            if self.achouSoftwareComPatente:
                                iessimoItem = SoftwareComPatente(self.id_membro, self.partesDoItem, self.relevante)
                                self.listaSoftwareComPatente.append(iessimoItem)

                            if self.achouSoftwareSemPatente:
                                iessimoItem = SoftwareSemPatente(self.id_membro, self.partesDoItem, self.relevante)
                                self.listaSoftwareSemPatente.append(iessimoItem)

                            if self.achouProdutoTecnologico:
                                iessimoItem = ProdutoTecnologico(self.id_membro, self.partesDoItem, self.relevante)
                                self.listaProdutoTecnologico.append(iessimoItem)

                            if self.achouProcessoOuTecnica:
                                iessimoItem = ProcessoOuTecnica(self.id_membro, self.partesDoItem, self.relevante)
                                self.listaProcessoOuTecnica.append(iessimoItem)

                            if self.achouTrabalhoTecnico:
                                iessimoItem = TrabalhoTecnico(self.id_membro, self.partesDoItem, self.relevante)
                                self.listaTrabalhoTecnico.append(iessimoItem)

                            if self.achouOutroTipoDeProducaoTecnica:
                                iessimoItem = OutroTipoDeProducaoTecnica(
                                    self.id_membro, self.partesDoItem, self.relevante
                                )
                                self.listaOutroTipoDeProducaoTecnica.append(iessimoItem)

                        if self.achouProducaoArtisticaCultural:
                            if self.achouOutraProducaoArtisticaCultural:
                                iessimoItem = ProducaoArtistica(self.id_membro, self.partesDoItem, self.relevante)
                                self.listaProducaoArtistica.append(iessimoItem)

                    # if self.achouBancas:

                    if self.achouEventos:
                        if self.achouParticipacaoEmEvento:
                            self.listaParticipacaoEmEvento.append(
                                ParticipacaoEmEvento(self.id_membro, self.partesDoItem)
                            )

                        if self.achouOrganizacaoDeEvento:
                            self.listaOrganizacaoDeEvento.append(OrganizacaoDeEvento(self.id_membro, self.partesDoItem))

                    if self.achouOrientacoes:
                        if self.achouOrientacoesEmAndamento:
                            if self.achouSupervisaoDePosDoutorado:
                                self.listaOASupervisaoDePosDoutorado.append(
                                    OrientacaoEmAndamento(self.id_membro, self.partesDoItem, self.id_orientando)
                                )
                                self.id_orientando = ""
                            if self.achouTeseDeDoutorado:
                                self.listaOATeseDeDoutorado.append(
                                    OrientacaoEmAndamento(self.id_membro, self.partesDoItem, self.id_orientando)
                                )
                                self.id_orientando = ""
                            if self.achouDissertacaoDeMestrado:
                                self.listaOADissertacaoDeMestrado.append(
                                    OrientacaoEmAndamento(self.id_membro, self.partesDoItem, self.id_orientando)
                                )
                                self.id_orientando = ""
                            if self.achouMonografiaDeEspecializacao:
                                self.listaOAMonografiaDeEspecializacao.append(
                                    OrientacaoEmAndamento(self.id_membro, self.partesDoItem, self.id_orientando)
                                )
                                self.id_orientando = ""
                            if self.achouTCC:
                                self.listaOATCC.append(
                                    OrientacaoEmAndamento(self.id_membro, self.partesDoItem, self.id_orientando)
                                )
                                self.id_orientando = ""
                            if self.achouIniciacaoCientifica:
                                self.listaOAIniciacaoCientifica.append(
                                    OrientacaoEmAndamento(self.id_membro, self.partesDoItem, self.id_orientando)
                                )
                                self.id_orientando = ""
                            if self.achouOutroTipoDeOrientacao:
                                self.listaOAOutroTipoDeOrientacao.append(
                                    OrientacaoEmAndamento(self.id_membro, self.partesDoItem, self.id_orientando)
                                )
                                self.id_orientando = ""

                        if self.achouOrientacoesConcluidas:
                            if self.achouSupervisaoDePosDoutorado:
                                self.listaOCSupervisaoDePosDoutorado.append(
                                    OrientacaoConcluida(self.id_membro, self.partesDoItem, self.id_orientando)
                                )
                                self.id_orientando = ""
                            if self.achouTeseDeDoutorado:
                                self.listaOCTeseDeDoutorado.append(
                                    OrientacaoConcluida(self.id_membro, self.partesDoItem, self.id_orientando)
                                )
                                self.id_orientando = ""
                            if self.achouDissertacaoDeMestrado:
                                self.listaOCDissertacaoDeMestrado.append(
                                    OrientacaoConcluida(self.id_membro, self.partesDoItem, self.id_orientando)
                                )
                                self.id_orientando = ""
                            if self.achouMonografiaDeEspecializacao:
                                self.listaOCMonografiaDeEspecializacao.append(
                                    OrientacaoConcluida(self.id_membro, self.partesDoItem, self.id_orientando)
                                )
                                self.id_orientando = ""
                            if self.achouTCC:
                                self.listaOCTCC.append(
                                    OrientacaoConcluida(self.id_membro, self.partesDoItem, self.id_orientando)
                                )
                                self.id_orientando = ""
                            if self.achouIniciacaoCientifica:
                                self.listaOCIniciacaoCientifica.append(
                                    OrientacaoConcluida(self.id_membro, self.partesDoItem, self.id_orientando)
                                )
                                self.id_orientando = ""
                            if self.achouOutroTipoDeOrientacao:
                                self.listaOCOutroTipoDeOrientacao.append(
                                    OrientacaoConcluida(self.id_membro, self.partesDoItem, self.id_orientando)
                                )
                                self.id_orientando = ""

        if tag == "span":
            if self.spanInformacaoArtigo:
                self.spanInformacaoArtigo = 0

    # ------------------------------------------------------------------------ #
    def handle_data(self, dado):
        """
            
        """
        if not self.spanInformacaoArtigo:
            self.item = self.item + htmlentitydecode(dado)

        dado = stripBlanks(dado)

        if self.salvaratualizacao_cv:
            data = re.findall(u"Última atualização do currículo em (\d{2}/\d{2}/\d{4})", dado)
            if len(data) > 0:  # se a data de atualizacao do CV for identificada
                self.atualizacao_cv = stripBlanks(data[0])
                self.salvaratualizacao_cv = 0

        if self.procurarCabecalho:
            if u"Identificação" == dado:
                self.achouIdentificacao = 1
            if u"Endereço" == dado:
                self.achouEndereco = 1
            if u"Formação acadêmica/titulação" == dado:
                self.achouFormacaoAcademica = 1
            if u"Atuação Profissional" == dado:
                self.achouAtuacaoProfissional = 1
            if u"Projetos de pesquisa" == dado:
                self.achouProjetoDePesquisa = 1
            if u"Membro de corpo editorial" == dado:
                self.achouMembroDeCorpoEditorial = 1
            if u"Revisor de periódico" == dado:
                self.achouRevisorDePeriodico = 1
            if u"Áreas de atuação" == dado:
                self.achouAreaDeAtuacao = 1
            if u"Idiomas" == dado:
                self.achouIdioma = 1
            if u"Prêmios e títulos" == dado:
                self.achouPremioOuTitulo = 1
            if u"Produções" == dado:  # !---
                self.achouProducoes = 1
                # self.achouProducaoEmCTA = 1
            # if u'Produção técnica'==dado:
            # 	self.achouProducaoTecnica = 1
            # if u'Produção artística/cultural'==dado:
            # 	self.achouProducaoArtisticaCultural = 1
            if u"Bancas" == dado:
                self.achouBancas = 1
            if u"Eventos" == dado:
                self.achouEventos = 1
            if u"Orientações" == dado:
                self.achouOrientacoes = 1
            if u"Patentes e registros" == dado:
                self.achouPatenteRegistro = 1
                # print "0==>>>>ACHOU PATENTE e REGISTRO"
            if u"Outras informações relevantes" == dado:
                self.achouOutrasInformacoesRelevantes = 1
            self.umaUnidade = 0
        if self.achouIdentificacao:
            if u"Nome em citações bibliográficas" == dado:
                self.achouNomeEmCitacoes = 1
            if u"Sexo" == dado:
                self.achouSexo = 1

        if self.achouEndereco:
            if u"Endereço Profissional" == dado:
                self.achouendereco_profissional = 1

        if self.achouPatenteRegistro:
            if u"Patente" == dado:
                self.salvarItem = 1
                self.achouPatente = 1
                self.achouProgramaComputador = 0
                self.achouDesenhoIndustrial = 0
                # print "1==>>>>ACHOU PATENTE e REGISTRO"
            if u"Programa de computador" == dado:
                self.salvarItem = 1
                self.achouPatente = 0
                self.achouProgramaComputador = 1
                self.achouDesenhoIndustrial = 0
                # print "2==>>>>ACHOU PATENTE e REGISTRO"
            if u"Desenho industrial" == dado:
                self.salvarItem = 1
                self.achouPatente = 0
                self.achouProgramaComputador = 0
                self.achouDesenhoIndustrial = 1

        if self.achouProducoes:
            if u"Produção bibliográfica" == dado:
                self.achouProducaoEmCTA = 1
                self.achouProducaoTecnica = 0
                self.achouProducaoArtisticaCultural = 0
            if u"Produção técnica" == dado:
                self.achouProducaoEmCTA = 0
                self.achouProducaoTecnica = 1
                self.achouProducaoArtisticaCultural = 0
            if u"Produção artística/cultural" == dado:
                self.achouProducaoEmCTA = 0
                self.achouProducaoTecnica = 0
                self.achouProducaoArtisticaCultural = 1

            if u"Demais trabalhos" == dado:
                self.salvarItem = 0
                self.achouProducaoEmCTA = 0
                self.achouProducaoTecnica = 0
                self.achouProducaoArtisticaCultural = 0

            if self.achouProducaoEmCTA:
                if u"Artigos completos publicados em periódicos" == dado:
                    self.salvarItem = 1
                    self.achouArtigoEmPeriodico = 1
                    self.achouLivroPublicado = 0
                    self.achouCapituloDeLivroPublicado = 0
                    self.achouTextoEmJornalDeNoticia = 0
                    self.achouTrabalhoCompletoEmCongresso = 0
                    self.achouResumoExpandidoEmCongresso = 0
                    self.achouResumoEmCongresso = 0
                    self.achouArtigoAceito = 0
                    self.achouApresentacaoDeTrabalho = 0
                    self.achouOutroTipoDeProducaoBibliografica = 0
                if u"Livros publicados/organizados ou edições" == dado:
                    self.salvarItem = 1
                    self.achouArtigoEmPeriodico = 0
                    self.achouLivroPublicado = 1
                    self.achouCapituloDeLivroPublicado = 0
                    self.achouTextoEmJornalDeNoticia = 0
                    self.achouTrabalhoCompletoEmCongresso = 0
                    self.achouResumoExpandidoEmCongresso = 0
                    self.achouResumoEmCongresso = 0
                    self.achouArtigoAceito = 0
                    self.achouApresentacaoDeTrabalho = 0
                    self.achouOutroTipoDeProducaoBibliografica = 0
                if u"Capítulos de livros publicados" == dado:
                    self.salvarItem = 1
                    self.achouArtigoEmPeriodico = 0
                    self.achouLivroPublicado = 0
                    self.achouCapituloDeLivroPublicado = 1
                    self.achouTextoEmJornalDeNoticia = 0
                    self.achouTrabalhoCompletoEmCongresso = 0
                    self.achouResumoExpandidoEmCongresso = 0
                    self.achouResumoEmCongresso = 0
                    self.achouArtigoAceito = 0
                    self.achouApresentacaoDeTrabalho = 0
                    self.achouOutroTipoDeProducaoBibliografica = 0
                if u"Textos em jornais de notícias/revistas" == dado:
                    self.salvarItem = 1
                    self.achouArtigoEmPeriodico = 0
                    self.achouLivroPublicado = 0
                    self.achouCapituloDeLivroPublicado = 0
                    self.achouTextoEmJornalDeNoticia = 1
                    self.achouTrabalhoCompletoEmCongresso = 0
                    self.achouResumoExpandidoEmCongresso = 0
                    self.achouResumoEmCongresso = 0
                    self.achouArtigoAceito = 0
                    self.achouApresentacaoDeTrabalho = 0
                    self.achouOutroTipoDeProducaoBibliografica = 0
                if u"Trabalhos completos publicados em anais de congressos" == dado:
                    self.salvarItem = 1
                    self.achouArtigoEmPeriodico = 0
                    self.achouLivroPublicado = 0
                    self.achouCapituloDeLivroPublicado = 0
                    self.achouTextoEmJornalDeNoticia = 0
                    self.achouTrabalhoCompletoEmCongresso = 1
                    self.achouResumoExpandidoEmCongresso = 0
                    self.achouResumoEmCongresso = 0
                    self.achouArtigoAceito = 0
                    self.achouApresentacaoDeTrabalho = 0
                    self.achouOutroTipoDeProducaoBibliografica = 0
                if u"Resumos expandidos publicados em anais de congressos" == dado:
                    self.salvarItem = 1
                    self.achouArtigoEmPeriodico = 0
                    self.achouLivroPublicado = 0
                    self.achouCapituloDeLivroPublicado = 0
                    self.achouTextoEmJornalDeNoticia = 0
                    self.achouTrabalhoCompletoEmCongresso = 0
                    self.achouResumoExpandidoEmCongresso = 1
                    self.achouResumoEmCongresso = 0
                    self.achouArtigoAceito = 0
                    self.achouApresentacaoDeTrabalho = 0
                    self.achouOutroTipoDeProducaoBibliografica = 0
                if u"Resumos publicados em anais de congressos" in dado:
                    self.salvarItem = 1
                    self.achouArtigoEmPeriodico = 0
                    self.achouLivroPublicado = 0
                    self.achouCapituloDeLivroPublicado = 0
                    self.achouTextoEmJornalDeNoticia = 0
                    self.achouTrabalhoCompletoEmCongresso = 0
                    self.achouResumoExpandidoEmCongresso = 0
                    self.achouResumoEmCongresso = 1
                    self.achouArtigoAceito = 0
                    self.achouApresentacaoDeTrabalho = 0
                    self.achouOutroTipoDeProducaoBibliografica = 0
                if u"Artigos aceitos para publicação" == dado:
                    self.salvarItem = 1
                    self.achouArtigoEmPeriodico = 0
                    self.achouLivroPublicado = 0
                    self.achouCapituloDeLivroPublicado = 0
                    self.achouTextoEmJornalDeNoticia = 0
                    self.achouTrabalhoCompletoEmCongresso = 0
                    self.achouResumoExpandidoEmCongresso = 0
                    self.achouResumoEmCongresso = 0
                    self.achouArtigoAceito = 1
                    self.achouApresentacaoDeTrabalho = 0
                    self.achouOutroTipoDeProducaoBibliografica = 0
                if u"Apresentações de Trabalho" == dado:
                    self.salvarItem = 1
                    self.achouArtigoEmPeriodico = 0
                    self.achouLivroPublicado = 0
                    self.achouCapituloDeLivroPublicado = 0
                    self.achouTextoEmJornalDeNoticia = 0
                    self.achouTrabalhoCompletoEmCongresso = 0
                    self.achouResumoExpandidoEmCongresso = 0
                    self.achouResumoEmCongresso = 0
                    self.achouArtigoAceito = 0
                    self.achouApresentacaoDeTrabalho = 1
                    self.achouOutroTipoDeProducaoBibliografica = 0
                if u"Outras produções bibliográficas" == dado:
                    # if u'Demais tipos de produção bibliográfica'==dado:
                    self.salvarItem = 1
                    self.achouArtigoEmPeriodico = 0
                    self.achouLivroPublicado = 0
                    self.achouCapituloDeLivroPublicado = 0
                    self.achouTextoEmJornalDeNoticia = 0
                    self.achouTrabalhoCompletoEmCongresso = 0
                    self.achouResumoExpandidoEmCongresso = 0
                    self.achouResumoEmCongresso = 0
                    self.achouArtigoAceito = 0
                    self.achouApresentacaoDeTrabalho = 0
                    self.achouOutroTipoDeProducaoBibliografica = 1

            if self.achouProducaoTecnica:
                # if u'Softwares com registro de patente'==dado:
                if u"Programas de computador com registro de patente" == dado:
                    self.salvarItem = 1
                    self.achouSoftwareComPatente = 1
                    self.achouSoftwareSemPatente = 0
                    self.achouProdutoTecnologico = 0
                    self.achouProcessoOuTecnica = 0
                    self.achouTrabalhoTecnico = 0
                    self.achouOutroTipoDeProducaoTecnica = 0
                if u"Programas de computador sem registro de patente" == dado:
                    self.salvarItem = 1
                    self.achouSoftwareComPatente = 0
                    self.achouSoftwareSemPatente = 1
                    self.achouProdutoTecnologico = 0
                    self.achouProcessoOuTecnica = 0
                    self.achouTrabalhoTecnico = 0
                    self.achouOutroTipoDeProducaoTecnica = 0
                if u"Produtos tecnológicos" == dado:
                    self.salvarItem = 1
                    self.achouSoftwareComPatente = 0
                    self.achouSoftwareSemPatente = 0
                    self.achouProdutoTecnologico = 1
                    self.achouProcessoOuTecnica = 0
                    self.achouTrabalhoTecnico = 0
                    self.achouOutroTipoDeProducaoTecnica = 0
                if u"Processos ou técnicas" == dado:
                    self.salvarItem = 1
                    self.achouSoftwareComPatente = 0
                    self.achouSoftwareSemPatente = 0
                    self.achouProdutoTecnologico = 0
                    self.achouProcessoOuTecnica = 1
                    self.achouTrabalhoTecnico = 0
                    self.achouOutroTipoDeProducaoTecnica = 0
                if u"Trabalhos técnicos" == dado:
                    self.salvarItem = 1
                    self.achouSoftwareComPatente = 0
                    self.achouSoftwareSemPatente = 0
                    self.achouProdutoTecnologico = 0
                    self.achouProcessoOuTecnica = 0
                    self.achouTrabalhoTecnico = 1
                    self.achouOutroTipoDeProducaoTecnica = 0
                if u"Demais tipos de produção técnica" == dado:
                    self.salvarItem = 1
                    self.achouSoftwareComPatente = 0
                    self.achouSoftwareSemPatente = 0
                    self.achouProdutoTecnologico = 0
                    self.achouProcessoOuTecnica = 0
                    self.achouTrabalhoTecnico = 0
                    self.achouOutroTipoDeProducaoTecnica = 1
                # if u'Demais trabalhos'==dado:
                # 	self.salvarItem = 0
                # 	self.achouSoftwareComPatente = 0
                # 	self.achouSoftwareSemPatente = 0
                # 	self.achouProdutoTecnologico = 0
                # 	self.achouProcessoOuTecnica = 0
                # 	self.achouTrabalhoTecnico = 0
                # 	self.achouOutroTipoDeProducaoTecnica = 0

            if self.achouProducaoArtisticaCultural:
                # if u'Produção artística/cultural'==dado:
                if u"Outras produções artísticas/culturais" == dado or u"Artes Cênicas" == dado or u"Música" == dado:
                    # separar as listas de producoes artisticas por tipos
                    self.salvarItem = 1
                    self.achouOutraProducaoArtisticaCultural = 1

        if self.achouBancas:
            if u"Participação em bancas de trabalhos de conclusão" == dado:
                self.salvarItem = 0

        if self.achouEventos:
            if u"Participação em eventos, congressos, exposições e feiras" == dado:
                self.salvarItem = 1
                self.achouParticipacaoEmEvento = 1
                self.achouOrganizacaoDeEvento = 0
            if u"Organização de eventos, congressos, exposições e feiras" == dado:
                self.salvarItem = 1
                self.achouParticipacaoEmEvento = 0
                self.achouOrganizacaoDeEvento = 1

        if self.achouOrientacoes:
            if u"Orientações e supervisões em andamento" == dado:
                self.achouOrientacoesEmAndamento = 1
                self.achouOrientacoesConcluidas = 0
            if u"Orientações e supervisões concluídas" == dado:
                self.achouOrientacoesEmAndamento = 0
                self.achouOrientacoesConcluidas = 1

            # Tipos de orientações (em andamento ou concluídas)
            if u"Supervisão de pós-doutorado" == dado:
                self.salvarItem = 1
                self.achouSupervisaoDePosDoutorado = 1
                self.achouTeseDeDoutorado = 0
                self.achouDissertacaoDeMestrado = 0
                self.achouMonografiaDeEspecializacao = 0
                self.achouTCC = 0
                self.achouIniciacaoCientifica = 0
                self.achouOutroTipoDeOrientacao = 0
            if u"Tese de doutorado" == dado:
                self.salvarItem = 1
                self.achouSupervisaoDePosDoutorado = 0
                self.achouTeseDeDoutorado = 1
                self.achouDissertacaoDeMestrado = 0
                self.achouMonografiaDeEspecializacao = 0
                self.achouTCC = 0
                self.achouIniciacaoCientifica = 0
                self.achouOutroTipoDeOrientacao = 0
            if u"Dissertação de mestrado" == dado:
                self.salvarItem = 1
                self.achouSupervisaoDePosDoutorado = 0
                self.achouTeseDeDoutorado = 0
                self.achouDissertacaoDeMestrado = 1
                self.achouMonografiaDeEspecializacao = 0
                self.achouTCC = 0
                self.achouIniciacaoCientifica = 0
                self.achouOutroTipoDeOrientacao = 0
            if u"Monografia de conclusão de curso de aperfeiçoamento/especialização" == dado:
                self.salvarItem = 1
                self.achouSupervisaoDePosDoutorado = 0
                self.achouTeseDeDoutorado = 0
                self.achouDissertacaoDeMestrado = 0
                self.achouMonografiaDeEspecializacao = 1
                self.achouTCC = 0
                self.achouIniciacaoCientifica = 0
                self.achouOutroTipoDeOrientacao = 0
            if u"Trabalho de conclusão de curso de graduação" == dado:
                self.salvarItem = 1
                self.achouSupervisaoDePosDoutorado = 0
                self.achouTeseDeDoutorado = 0
                self.achouDissertacaoDeMestrado = 0
                self.achouMonografiaDeEspecializacao = 0
                self.achouTCC = 1
                self.achouIniciacaoCientifica = 0
                self.achouOutroTipoDeOrientacao = 0
            if u"Iniciação científica" in dado or u"Iniciação Científica" == dado:
                self.salvarItem = 1
                self.achouSupervisaoDePosDoutorado = 0
                self.achouTeseDeDoutorado = 0
                self.achouDissertacaoDeMestrado = 0
                self.achouMonografiaDeEspecializacao = 0
                self.achouTCC = 0
                self.achouIniciacaoCientifica = 1
                self.achouOutroTipoDeOrientacao = 0
            if u"Orientações de outra natureza" == dado:
                self.salvarItem = 1
                self.achouSupervisaoDePosDoutorado = 0
                self.achouTeseDeDoutorado = 0
                self.achouDissertacaoDeMestrado = 0
                self.achouMonografiaDeEspecializacao = 0
                self.achouTCC = 0
                self.achouIniciacaoCientifica = 0
                self.achouOutroTipoDeOrientacao = 1

        if self.achouOutrasInformacoesRelevantes:
            self.salvarItem = 0

        if self.recuperarIdentificador16 and self.identificador16 == "":
            id = re.findall(u"http://lattes.cnpq.br/(\d{16})", dado)
            if len(id) > 0:
                self.identificador16 = id[0]

        if self.achouProjetoDePesquisa:
            if dado.startswith(u"Projeto certificado pelo(a) coordenador(a)") or dado.startswith(
                u"Projeto certificado pela empresa"
            ):
                # if u'Projeto certificado pelo(a) coordenador(a)' in dado or u'Projeto certificado pela empresa' in dado:
                self.item = ""
                self.salvarParte3 = 0

    def __str__(self):
        return (
            str(self.nome_completo)
            + "\n\t"
            + "Contribuicoes: "
            + str(set(self.lista_id_lattes_colaboradores))
            + "\n\t"
            + str(self.lista_premio_ou_titulo)
        )


# ---------------------------------------------------------------------------- #
def stripBlanks(s):
    """ 
    """
    return re.sub("\s+", " ", s).strip()


def htmlentitydecode(s):
    """       
    """
    return re.sub("&(%s);" % "|".join(name2codepoint), lambda m: chr(name2codepoint[m.group(1)]), s)
