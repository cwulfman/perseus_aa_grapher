import json
from csv import DictReader
from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, URIRef, Literal
from pdl_importer.models import VaseData, ImageData, CollectionData
from pdl_importer.entities import Vase, Image, Collection



class Importer:
    def __init__(self) -> None:
        self.collections = {}
        self.vases = {}
        self.gems = {}
        self.coins = {}
        self.sculptures = {}
        self.buildings = {}
        self.sites = {}
        self.images = {}

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

            if otype == 'Vase':
                vase_data = VaseData(**o)
                vase = Vase(vase_data, self.collections)
                self.vases[vase.str_id] = vase
                print(f"object type invalid: {otype}")


    def import_images(self, fpath) -> None:
        with open(fpath, 'r') as f:
            data = json.load(f)
        for img in data['image']:
            image_data = ImageData(**img)
            image = Image(image_data)
            self.images[image.str_id] = image


    def collection(self, index):
        return self.collections.get(index)


    def image(self, index):
        return self.images.get(index)


    def export_vases(self, fpath):
        g = Graph()
        for v in self.vases.values():
            g += v.graph
        g.serialize(destination=fpath)


    def export_collections(self, fpath):
        g = Graph()
        breakpoint()
        for v in self.collections.values():
            g += v.graph
        g.serialize(destination=fpath)


    def export_images(self, fpath):
        pass
