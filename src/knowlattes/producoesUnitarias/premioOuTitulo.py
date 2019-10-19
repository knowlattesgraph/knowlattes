#!/usr/bin/python
# encoding: utf-8
# filename: premioOuTitulo.py
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


class PremioOuTitulo:
    """ Missing
    
    Attributes
    ----------
    id_membro = None
    ano = ""
    descricao = ""
    chave = None

    """

    def __init__(self, id_membro, partesDoItem):
        # partesDoItem[0]: Ano
        # partesDoItem[1]: Descricao do titulo ou premio
        self.id_membro = set([])
        self.id_membro.add(id_membro)

        self.ano = partesDoItem[0].strip()
        self.descricao = partesDoItem[1].strip()
        self.chave = self.descricao  # chave de comparação entre os objetos

    def compararCom(self, objeto):
        return None

    def __repr__(self):
        return '"' + self.ano + " " + self.descricao + " " + self.chave + '"\n'

    # Prêmios considerados de forma individual
    # if self.id_membro.isdisjoint(objeto.id_membro) and similaridade_entre_cadeias(self.descricao, objeto.descricao):
    # 	# Os IDs dos membros são agrupados.
    # 	# Essa parte é importante para a criação do GRAFO de colaborações
    # 	self.id_membro.update(objeto.id_membro)
    #
    # 	if len(self.descricao)<len(objeto.descricao):
    # 		self.descricao = objeto.descricao
    #
    # 	return self
    # else: # nao similares
    # 	return None

    def html(self, listaDeMembros):
        s = self.descricao + ". "
        s += str(self.ano) + "." if str(self.ano).isdigit() else "."

        m = listaDeMembros[list(self.id_membro)[0]]
        s += '<br><i><font size=-1>Membro: <a href="' + m.url + '">' + m.nome_completo + "</a>.</font>"

        return s

    # ------------------------------------------------------------------------ #
    def __str__(self):
        s = "\n[PREMIO OU TITULO] \n"
        s += "+ID-MEMBROL  : " + str(self.id_membro) + "\n"
        s += "+ANO         : " + str(self.ano) + "\n"
        s += "+DESCRICAO   : " + self.descricao.encode("utf8", "replace") + "\n"
        return s
