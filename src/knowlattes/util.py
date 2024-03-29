#!/usr/bin/env python
# encoding: utf-8
#
#
#  scriptLattes
#  Copyright http://scriptlattes.sourceforge.net/
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
#
import logging
import os
import shutil
import sys
import Levenshtein

SEP = os.path.sep
BASE = "scriptLattes" + SEP
ABSBASE = os.path.abspath(".") + SEP


class OutputStream:
    """
    Pylattes utils class for parsing and reading html pages

    Parameters
    ----------
    
    Returns
    -------
    
    """

    def __init__(self, output, encoding):
        """This is the class that starts the HTML page parser.
        
        It will go though each one of the html tags, searching for known patterns and filling the object lattes page
        with its info

        Parameters
        ----------
        output: Any
            A variable to be overrided with the output from iso8859 to utf
        enconding: String
            Which enconding to use. eg: utf, iso-8859-1, etc
        
        Returns
        -------
        None
        """
        self.encoding = encoding
        self.output = output

    def write(self, text):
        """Try enconding the text in iso 8859 (lattes default) instead of utf8
    
        It will go though each one of the html tags, searching for known patterns and filling the object lattes page
        with its info

        Parameters
        ----------
        text: String

        Returns
        -------
        None
            It overrides class output 
        """

        try:
            text = text.decode(self.encoding)
        except:
            try:
                text = text.decode("utf8").encode("iso-8859-1")
            except:
                try:
                    text = text.encode("iso-8859-1")
                except:
                    pass
        try:
            self.output.write(text)
        except:
            try:
                self.output.write(unicode(text))
            except:
                self.output.write("ERRO na impressao")


def buscarArquivo(filepath, arquivoConfiguracao=None):
    """
        Search for a configuration file for pylattes
    """
    if not arquivoConfiguracao:
        arquivoConfiguracao = sys.argv[1]
    curdir = os.path.abspath(os.path.curdir)
    if not os.path.isfile(filepath) and arquivoConfiguracao:
        # vamos tentar mudar o diretorio para o atual do arquivo
        os.chdir(os.path.abspath(os.path.join(arquivoConfiguracao, os.pardir)))
    if not os.path.isfile(filepath):
        # se ainda nao existe, tentemos ver se o arquivo não está junto com o config
        filepath = os.path.abspath(os.path.basename(filepath))
    else:
        # se encontramos, definimos então caminho absoluto
        filepath = os.path.abspath(filepath)
    os.chdir(curdir)
    return filepath


def copiarArquivos(dir):
    base = ABSBASE
    try:
        dst = os.path.join(dir, "css")
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(base, "css"), dst)
    except e:
        pass  # provavelmente diretório já existe
        logging.warning(e)

    # shutil.copy2(os.path.join(base, 'css', 'scriptLattes.css'), dir)
    # shutil.copy2(os.path.join(base, 'css', 'jquery.dataTables.css'), dir)

    shutil.copy2(os.path.join(base, "imagens", "lattesPoint0.png"), dir)
    shutil.copy2(os.path.join(base, "imagens", "lattesPoint1.png"), dir)
    shutil.copy2(os.path.join(base, "imagens", "lattesPoint2.png"), dir)
    shutil.copy2(os.path.join(base, "imagens", "lattesPoint3.png"), dir)
    shutil.copy2(os.path.join(base, "imagens", "lattesPoint_shadow.png"), dir)
    shutil.copy2(os.path.join(base, "imagens", "doi.png"), dir)

    try:
        dst = os.path.join(dir, "images")
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(base, "images"), dst)
    except e:
        pass  # provavelmente diretório já existe
        logging.warning(e)

    try:
        dst = os.path.join(dir, "js")
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(os.path.join(base, "js"), dst)
    except e:
        pass  # provavelmente diretório já existe
        logging.warning(e)

    # shutil.copy2(os.path.join(base, 'js', 'jquery.min.js'), dir)
    # shutil.copy2(os.path.join(base, 'js', 'highcharts.js'), dir)
    # shutil.copy2(os.path.join(base, 'js', 'exporting.js'), dir)
    # shutil.copy2(os.path.join(base, 'js', 'drilldown.js'), dir)
    # shutil.copy2(os.path.join(base, 'js', 'jquery.dataTables.min.js'), dir)
    # shutil.copy2(os.path.join(base, 'js', 'jquery.dataTables.rowGrouping.js'), dir)

    print("\nArquivos salvos em: >>{}<<".format(os.path.abspath(dir)))


# ---------------------------------------------------------------------------- #
def similaridade_entre_cadeias(str1, str2, qualis=False):
    """Compara duas cadeias de caracteres e retorna a medida de similaridade entre elas, entre 0 e 1, onde 1 significa que as cadeias são idênticas ou uma é contida na outra.

    Parameters
    ----------
    str1: String
        First string to be compared
    str2: String
        Second string to be compared
    qualis: Bool

    Returns
    -------
        A medida de similaridade entre as cadeias, de 0 a 1.
    """
    str1 = str1.strip().lower()
    str2 = str2.strip().lower()

    # caso especial
    if u"apresentação" == str1 or u"apresentação" == str2 or u"apresentacao" == str1 or u"apresentacao" == str2:
        return 0

    if len(str1) == 0 or len(str2) == 0:
        return 0

    if len(str1) >= 20 and len(str2) >= 20 and (str1 in str2 or str2 in str1):
        return 1

    if qualis:
        dist = Levenshtein.ratio(str1, str2)
        if len(str1) >= 10 and len(str2) >= 10 and dist >= 0.90:
            # return 1
            return dist

    else:
        if len(str1) >= 10 and len(str2) >= 10 and Levenshtein.distance(str1, str2) <= 5:
            return 1
    return 0


def criarDiretorio(dir):
    """Create a directory if it doesn't exist

    Parameters
    ----------
    dir:
        Path to the directory to be created
    Returns
    -------
    
    """
    if not os.path.exists(dir):
        try:
            os.makedirs(dir)
        ### except OSError as exc:
        except:
            print("\n[ERRO] Não foi possível criar ou atualizar o diretório: " + dir.encode("utf8"))
            print("[ERRO] Você conta com as permissões de escrita? \n")
            return 0
    return 1


def merge_dols(dol1, dol2):
    """Combining Dictionaries Of Lists

    Parameters
    ----------
    dol1:
        dic of list1
    dol2:
        dic of list2
    Returns
    -------
        Combined dict of both dict1 and dict2
    """
    result = dict(dol1, **dol2)
    result.update((k, dol1[k] + dol2[k]) for k in set(dol1).intersection(dol2))
    return result


def all_the_files_in_directory(dir_path):
    """Returns a list of all the files on a given directory

    Parameters
    ----------
    dir_path:
        directory to list all the files

    Returns
    -------
        List of files inside the directory
    """
    from os import listdir
    from os.path import isfile, join

    files_names = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
    return files_names


def find_non_lattes_pages(dir_path, list_of_files):
    """Returns a list of all the files on a given directory that are note lattes page

    Parameters
    ----------
    dir_path:
        directory to list all the files

    list_of_files
        list of all files to check whether is a lattes cv

    Returns
    -------
        List of files inside the directory that are not lattes
    """
    not_lattes_pages = []
    for lattes_page in list_of_files:
        with open(dir_path + "/" + lattes_page, encoding="iso-8859-1") as f:
            if "possivel baixar" in f.read():
                not_lattes_pages.append(lattes_page)

    return not_lattes_pages
