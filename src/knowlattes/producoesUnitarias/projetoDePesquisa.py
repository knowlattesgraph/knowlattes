#!/usr/bin/python
# encoding: utf-8
# filename: projetoDePesquisa.py
#
#  scriptLattes V8
#  Copyright 2005-2013: Jesús P. Mena-Chalco e Roberto M. Cesar-Jr.
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


import re
import datetime
import unicodedata

from knowlattes.util import similaridade_entre_cadeias


class ProjetoDePesquisa:
    """ Missing

    Attributes
    ----------
    id_membro = None
    anoInicio = None
    anoConclusao = None
    nome = ""
    descricao = ""
    chave = None
    ano = None
    """

    def __init__(self, id_membro, partesDoItem):
        # partesDoItem[0]: Periodo do projeto de pesquisa
        # partesDoItem[1]: cargo e titulo do projeto
        # partesDoItem[2]: Descricao (resto)

        self.id_membro = list([])
        self.id_membro.append(id_membro)

        anos = partesDoItem[0].partition("-")
        self.anoInicio = anos[0].strip()
        self.anoConclusao = anos[2].strip()

        # detalhe = partesDoItem[1].rpartition(":")
        # self.cargo = detalhe[0].strip()
        # self.nome = detalhe[2].strip()
        self.nome = partesDoItem[1]

        self.descricao = list([])
        self.descricao.append(partesDoItem[2])

        self.chave = self.nome  # chave de comparação entre os objetos

        self.ano = self.anoInicio  # para comparação entre objetos

    def html(self, listaDeMembros):
        if self.anoConclusao == datetime.datetime.now().year:
            self.anoConclusao = "Atual"

        if self.anoInicio == 0 and self.anoConclusao == 0:
            s = '<span class="projects"> (*) </span> '
        else:
            s = '<span class="projects">' + str(self.anoInicio) + "-" + str(self.anoConclusao) + "</span>. "
        s += "<b>" + unicodedata.normalize("NFKD", self.nome).encode("ASCII", "ignore") + "</b>"

        for i in range(0, len(self.id_membro)):
            s += "<br><i><font size=-1>" + self.descricao[i] + "</font></i>"
            m = listaDeMembros[self.id_membro[i]]

            nome_membro = unicodedata.normalize("NFKD", m.nome_completo).encode("ASCII", "ignore")
            s += '<br><i><font size=-1>Membro: <a href="' + m.url + '">' + nome_membro + "</a>.</font>"

        return s

    def compararCom(self, objeto):
        if set(self.id_membro).isdisjoint(set(objeto.id_membro)) and similaridade_entre_cadeias(self.nome, objeto.nome):
            # Os IDs dos membros são agrupados.
            # Essa parte é importante para a geracao do relorio de projetos
            self.id_membro.extend(objeto.id_membro)

            self.descricao.extend(objeto.descricao)  # Apenas juntamos as descrições

            return self
        else:  # nao similares
            return None

    # ------------------------------------------------------------------------ #
    def __str__(self):
        s = "\n[PROJETO DE PESQUISA] \n"
        s += "+ID-MEMBRO   : " + str(self.id_membro) + "\n"
        s += "+ANO INICIO  : " + str(self.anoInicio) + "\n"
        s += "+ANO CONCLUS.: " + str(self.anoConclusao) + "\n"
        s += "+NOME        : " + self.nome.encode("utf8", "replace") + "\n"
        s += "+DESCRICAO   : " + str(self.descricao).encode("utf8", "replace") + "\n"
        return s
