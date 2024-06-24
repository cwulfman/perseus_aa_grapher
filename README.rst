.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/pdl_importer.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/pdl_importer
    .. image:: https://readthedocs.org/projects/pdl_importer/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://pdl_importer.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/pdl_importer/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/pdl_importer
    .. image:: https://img.shields.io/pypi/v/pdl_importer.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/pdl_importer/
    .. image:: https://img.shields.io/conda/vn/conda-forge/pdl_importer.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/pdl_importer
    .. image:: https://pepy.tech/badge/pdl_importer/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/pdl_importer
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/pdl_importer

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

=====================================
Perseus Art and Archaeology Grapher
=====================================

This repository contains classes and scripts that may be used to
convert data harvested from the original Perseus Art and Archaeology
database into RDF graphs in the CIDOC CRM ontology.

Installation
------------

These instructions assume you have Python 3.8 or greater installed

Begin by downloading or cloning this repository to your computer::
  * git clone git@github.com:cwulfman/perseus_aa_grapher.git
  * cd perseus_aa_grapher
  * [ do some things ]

Usage
-----

There are three scripts that may be run from the command line:

  * gen_collections `sourcedir` `targetdir`
  * gen_images `sourcedir` `targetdir`
  * gen_artifacts `sourcedir` `collectionsfile` `targetdir`

This installation includes a version of the source data in the
top-level `data/` directory, so in general you simply need to run
these commands:

  * gen_collections data/collections.csv data/rdf/collections.ttl
  * gen_images data/images.json data/rdf/images.ttl
  * gen_artifacts `data/artifacts.json data/collections.csv/ data/rdf/artifacts.ttl


.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.5. For details and usage
information on PyScaffold see https://pyscaffold.org/.
