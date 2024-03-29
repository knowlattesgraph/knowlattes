#!/usr/bin/python
# encoding: utf-8
# filename: participacaoEmEvento.py
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

from knowlattes.util import similaridade_entre_cadeias


class ParticipacaoEmEvento:
    """Class of events participation
    
    Attributes
    ----------
        item = None  # dado bruto
        id_membro = []
        ano = None
        chave = None
    """

    item = None  # dado bruto
    id_membro = []

    ano = None
    chave = None

    def __init__(self, id_membro, partesDoItem=""):
        self.id_membro = set([])
        self.id_membro.add(id_membro)

        if not partesDoItem == "":
            # partesDoItem[0]: Numero (NAO USADO)
            # partesDoItem[1]: Descricao
            self.item = partesDoItem[1]

            partes = self.item
            aux = re.findall(u"\. ((?:19|20)\d\d)\\b", partes)
            if len(aux) > 0:
                self.ano = aux[0]
            else:
                self.ano = ""

            self.chave = self.item  # chave de comparação entre os objetos

        else:
            self.ano = ""

    def compararCom(self, objeto):
        """ Missing
        
        Parameters
        ----------

        Returns
        -------
            THe object if equal, otherwise, None
        """
        if self.id_membro.isdisjoint(objeto.id_membro) and similaridade_entre_cadeias(self.item, objeto.item):
            # Os IDs dos membros são agrupados.
            # Essa parte é importante para a criação do GRAFO de colaborações
            self.id_membro.update(objeto.id_membro)

            if len(self.item) < len(objeto.item):
                self.item = objeto.item

            return self
        else:  # nao similares
            return None

    def html(self, listaDeMembros):
        s = self.item

        return s

    # ------------------------------------------------------------------------ #
    def __str__(self):
        s = "\n[PARTICIPACAO EM EVENTO] \n"
        s += "+ID-MEMBRO   : " + str(self.id_membro) + "\n"
        s += "+item         : @@" + self.item.encode("utf8", "replace") + "@@\n"

        return s
