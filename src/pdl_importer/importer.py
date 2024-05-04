import json
from csv import DictReader
from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, URIRef, Literal
from pdl_importer.models import VaseData, ImageData, CollectionData, GemData
from pdl_importer.models import ArtifactData, SculptureData, CoinData, BuildingData, SiteData
from pdl_importer.entities import Artifact, Vase, Image, Collection, Gem, Sculpture, Building, Site, Coin

from pdl_importer.entities import crm, entity, aat


class Importer:
    def __init__(self) -> None:
        self.data_graph = Graph()
        self.data_graph.bind("crm", crm)
        self.data_graph.bind("entity", entity)
        self.data_graph.bind("aat", aat)
        self.data_graph.bind("rdf", RDF)
        self.data_graph.bind("rdfs", RDFS)
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

            # else:
                # obj = Artifact(ArtifactData(**o), self.collection)
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
        for v in self.images:
            g += v.graph
        g.serialize(destination=fpath)


    def export_collections(self, fpath):
        g = Graph()
        for v in self.collections.values():
            g += v.graph
        g.serialize(destination=fpath)


    def export_artifacts(self, fpath):
        g = Graph()
        for a in self.artifacts:
            g += a.graph
        g.serialize(destination=fpath)

class ImporterOld:
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
            else:
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
        for v in self.collections.values():
            g += v.graph
        g.serialize(destination=fpath)


    def export_images(self, fpath):
        g = Graph()
        for v in self.images.values():
            g += v.graph
        g.serialize(destination=fpath)
