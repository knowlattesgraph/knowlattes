
Welcome to knowlattes documentation!
====================================
This library provides the code to parse a lattes web page and, using the type extracted, create knowledge graph with RDFLib containing the triples from the lattes using the schema.org ontology

Installation
============

You can install knowlattes package with pip, by cloning the repository and then:

.. code-block:: console
    
    $ pip install -e .

to build the documentation you can, then, in the docs path, build it with

.. code-block:: console
    
    $ make apidocs

Compatibility
=============

knowlattes was tested on Python 3.6 and 3.7.


Contributing
============

https://github.com/knowlattes_graph/knowlattes


Documentation
=============
.. toctree::
    :maxdepth: 2
    :caption: Contents:

    modules
    knowlattes.eventos
    knowlattes.orientacoes
    knowlattes.producoesArtisticas
    knowlattes.producoesBibliograficas
    knowlattes.producoesTecnicas
    knowlattes.producoesUnitarias
    knowlattes
    knowlattes.server
    example

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
