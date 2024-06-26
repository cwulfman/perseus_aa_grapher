"""
importer.py

This module provides a class that imports data from CSV files containing
data about collections, artifacts, and images and converts that data into
graphs.  It can serialize the graphs to files.

In order to create links between artifacts and the collections that own them,
the Importer must first import collections data.
"""

import json
from csv import DictReader
from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, URIRef, Literal
from pdl_importer.models import VaseData, ImageData, CollectionData, GemData
from pdl_importer.models import ArtifactData, SculptureData, CoinData, BuildingData, SiteData
from pdl_importer.entities import Artifact, Vase, Image, Collection, Gem, Sculpture, Building, Site, Coin

from pdl_importer.entities import crm, entity, aat, image


class Importer:
    def __init__(self) -> None:
        self.data_graph = Graph()
        self.data_graph.bind("crm", crm)
        self.data_graph.bind("entity", entity)
        self.data_graph.bind("aat", aat)
        self.data_graph.bind("rdf", RDF)
        self.data_graph.bind("rdfs", RDFS)
        self.data_graph.bind("image", image)
        self.collections = {}
        self.images = []
        self.artifacts = []

    def import_collections(self, fpath) -> None:
        with open(fpath, 'r') as f:
            reader: DictReader = DictReader(f)
            for row in reader:
                c = CollectionData(**row)
                self.collections[c.index] = Collection(c)


    def import_data(self, fpath) -> None:
        with open(fpath, 'r') as f:
            data = json.load(f)
        for o in data['object']:
            otype = o['type']
            obj = None
            if otype == 'Vase':
                obj_data = VaseData(**o)
                obj = Vase(obj_data, self.collections)
            elif otype == 'Gem':
                obj = Gem(GemData(**o), self.collections)
            elif otype == 'Sculpture':
                obj = Sculpture(SculptureData(**o), self.collections)
            elif otype == 'Coin':
                obj = Coin(CoinData(**o), self.collections)
            elif otype == 'Building':
                obj = Building(BuildingData(**o))
            elif otype == 'Site':
                obj = Site(SiteData(**o))
            if obj:
                self.data_graph += obj.graph
                self.artifacts.append(obj)


    def import_images(self, fpath) -> None:
        with open(fpath, 'r') as f:
            data = json.load(f)
        for img in data['image']:
            self.images.append(Image(ImageData(**img)))

    @property
    def vases(self):
        return filter(lambda x: x.__class__ == 'Vase', self.artifacts)


    def collection(self, index):
        return self.collections.get(index)


    def image(self, index):
        return next(filter(lambda x: x.str_id == index, self.images))


    def export_images(self, fpath):
        g = Graph()
        g.bind('crm', crm)
        g.bind('entity', entity)
        g.bind('image', image)
        for v in self.images:
            g += v.graph
        g.serialize(destination=fpath)


    def export_collections(self, fpath):
        g = Graph()
        g.bind('crm', crm)
        g.bind('entity', entity)
        for v in self.collections.values():
            g += v.graph
        g.serialize(destination=fpath)


    def export_artifacts(self, fpath):
        g = Graph()
        g.bind('crm', crm)
        g.bind('entity', entity)
        for a in self.artifacts:
            g += a.graph
        g.serialize(destination=fpath)
