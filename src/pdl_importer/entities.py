from csv import DictReader
from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, URIRef, Literal
from pydantic import BaseModel
from pdl_importer.models import VaseData

crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
aat = Namespace("http://vocab.getty.edu/aat/")
entity = Namespace("http://perseus.tufts.edu/ns/entities/")
artifact = Namespace("http://perseus.tufts.edu/ns/artifact/")
vase = Namespace("http://perseus.tufts.edu/ns/artifact/vase/")
gem = Namespace("http://perseus.tufts.edu/ns/artifact/gem/")
sculpture = Namespace("http://perseus.tufts.edu/ns/artifact/sculpture/")
coin = Namespace("http://perseus.tufts.edu/ns/artifact/coin/")
building = Namespace("http://perseus.tufts.edu/ns/building/")
site = Namespace("http://perseus.tufts.edu/ns/artifact/site/")
image = Namespace("http://perseus.tufts.edu/ns/artifact/image/")


class AAObject:
    def __init__(self, data:BaseModel) -> None:
        self.str_id:str = data.id
        self._data = data
        self._graph = Graph()
        self._graph.bind("crm", crm)
        self._graph.bind("entity", entity)
        self._graph.bind("aat", aat)
        self._graph.bind("rdf", RDF)
        self._graph.bind("rdfs", RDFS)
        self.type:[str|None] = None


    @property
    def rdf(self):
        return self._graph.serialize()



class Artifact(AAObject):
    def __init__(self, data) -> None:
        super().__init__(data)


    def __repr__(self) -> str:
        return f"Artifact('{self.id}')"


class Vase(Artifact):
    def __init__(self, data:VaseData, collection_index) -> None:
        super().__init__(data)
        self._graph.bind("vase", vase)
        self.id = entity[self.str_id]
        self._graph.add((self.id, RDF.type, aat['300132254']))
        self._graph.add((self.id, RDFS.label, Literal(self._data.name)))
        self._graph.add((self.id, crm['P1i_is_identified_by'], Literal(self._data.name)))
        self.collection = collection_index.get(self._data.collection)
        if self.collection:
            self._graph.add((self.id, crm["P50_has_current_keeper"], URIRef(self.collection.uri)))
        # Make the remaining attributes notes for now
        # self._graph.add((self.id, crm['P3_has_note'], Literal(self._data.collection)))
        self._graph.add((self.id, crm['P3_has_note'], Literal(self._data.summary)))

    def __repr__(self) -> str:
        return f"Vase('{self.id}')"


class Gem(Artifact):
    pass

class Sculpture(Artifact):
    pass

class Coin(Artifact):
    pass

class Building(AAObject):
    pass


class Site(AAObject):
    pass


class Image:
    def __init__(self, data) -> None:
        self._graph = Graph()
        self._graph.bind("crm", crm)
        self._graph.bind("image", image)
        self._graph.bind("entity", entity)
        self.str_id = data.id
        self.id = image[self.str_id]
        self.caption = data.caption
        self.credits = data.credits
        self.represents = data.represents
        self._data = data

        self._graph.add((self.id, RDF.type, crm['E36_Visual_Item']))
        self._graph.add((self.id, crm['P138_represents'], entity[self.represents]))
        self._graph.add((entity[self.represents], crm['P138i_is_represented_by'], self.id))
        self._graph.add((self.id, crm['P3_has_note'], Literal(self.caption)))
        self._graph.add((self.id, crm['P3_has_note'], Literal(self.credits)))


    @property
    def rdf(self):
        return self._graph.serialize()



class Collection():
    def __init__(self, data) -> None:
        self._graph = Graph()
        self.graph.bind('crm', crm)
        self.name = data.name.strip()
        self.key = hash(self.name)
        self.id = URIRef(self.url)

        self._graph.add()


def vase_graph(vases) -> Graph:
    g = Graph()
    g.bind("crm", crm)
    g.bind("entity", entity)
    g.bind("aat", aat)
    for v in vases:
        vase = Vase(v)
        g += vase._graph
    return g


def image_graph(imgs) -> Graph:
    g = Graph()
    g.bind("crm", crm)
    g.bind("image", image)
    g.bind("entity", entity)
    for i in imgs:
        img = Image(i)
        g += img._graph
    return g
