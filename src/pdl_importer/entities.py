from csv import DictReader
from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, URIRef, Literal
from pydantic import BaseModel
from pdl_importer.models import VaseData, GemData, CoinData, SculptureData
from pdl_importer.models import SiteData, BuildingData

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
image = Namespace("http://perseus.tufts.edu/ns/artifact/images/")


class AAObject:
    def __init__(self, data:BaseModel) -> None:
        self.str_id:str = data.id
        self.id = entity[self.str_id]
        self._data = data
        self.graph = Graph()
        self.graph.bind("crm", crm)
        self.graph.bind("entity", entity)
        self.graph.bind("aat", aat)
        self.graph.bind("rdf", RDF)
        self.graph.bind("rdfs", RDFS)
        self.type:[str|None] = None

        self.graph.add((self.id, RDF.type, crm['E22_Human-Made_Object']))


    @property
    def rdf(self):
        return self.graph.serialize()



class Artifact(AAObject):
    """Artifact collects all the properties common to subclasses
       of Artifact (vases, coins, gems, sculptures)
    """
    def __init__(self, data, collection_index) -> None:
        super().__init__(data)
        self.graph.add((self.id, RDFS.label, Literal(self._data.name)))
        self.graph.add((self.id, crm['P1i_is_identified_by'], Literal(self._data.name)))
        if self._data.collection:
            self.collection = collection_index.get(self._data.collection)
            if self.collection:
                self.graph.add((self.id, crm["P50_has_current_keeper"], URIRef(self.collection.id)))


    def __repr__(self) -> str:
        return f"Artifact('{self.id}')"


class Vase(Artifact):
    def __init__(self, data:VaseData, collection_index) -> None:
        super().__init__(data, collection_index)
        # self.graph.bind("vase", vase)
        self.id = entity[self.str_id]
        self.graph.add((self.id, RDF.type, aat['300132254']))
        self.graph.add((self.id, RDFS.label, Literal(self._data.name)))
        self.graph.add((self.id, crm['P1i_is_identified_by'], Literal(self._data.name)))
        self.collection = collection_index.get(self._data.collection)
        if self.collection:
            self.graph.add((self.id, crm["P50_has_current_keeper"], URIRef(self.collection.id)))
        # Make the remaining attributes notes for now
        # self.graph.add((self.id, crm['P3_has_note'], Literal(self._data.collection)))
        self.graph.add((self.id, crm['P3_has_note'], Literal(self._data.summary)))

    def __repr__(self) -> str:
        return f"Vase('{self.id}')"


class Gem(Artifact):
    def __init__(self, data:GemData, collection_index) -> None:
        super().__init__(data, collection_index)
        self.graph.add((self.id, RDF.type, aat['300011172']))


    def __repr__(self) -> str:
        return f"Gem('{self.id}')"


class Sculpture(Artifact):
    def __init__(self, data:SculptureData, collection_index) -> None:
        super().__init__(data, collection_index)
        self.graph.add((self.id, RDF.type, aat['sculpture']))


class Coin(Artifact):
    def __init__(self, data:CoinData, collection_index) -> None:
        super().__init__(data, collection_index)
        self.graph.add((self.id, RDF.type, aat['coin']))



class Building(AAObject):
    def __init__(self, data:BuildingData) -> None:
        super().__init__(data)
        self.graph.add((self.id, RDF.type, aat['building']))


class Site(AAObject):
    def __init__(self, data:SiteData) -> None:
        super().__init__(data)
        self.graph.add((self.id, RDF.type, aat['site']))




class Image:
    def __init__(self, data) -> None:
        self.graph = Graph()
        self.graph.bind("crm", crm)
        self.graph.bind("image", image)
        self.graph.bind("entity", entity)
        self.str_id = data.id
        self.id = image[self.str_id]
        self.caption = data.caption
        self.credits = data.credits
        self.represents = data.represents
        self._data = data

        self.graph.add((self.id, RDF.type, crm['E36_Visual_Item']))
        self.graph.add((self.id, crm['P138_represents'], entity[self.represents]))
        self.graph.add((entity[self.represents], crm['P138i_is_represented_by'], self.id))
        self.graph.add((self.id, crm['P3_has_note'], Literal(self.caption)))
        self.graph.add((self.id, crm['P3_has_note'], Literal(self.credits)))


    @property
    def rdf(self):
        return self.graph.serialize()



class Collection():
    def __init__(self, data) -> None:
        self.graph = Graph()
        self.graph.bind('crm', crm)
        self.index = data.index
        self.name = data.name.strip()
        self.key = hash(self.name)
        self.id = URIRef(data.uri)
        self.graph.add((self.id, RDF.type, crm['E74_Group']))
        self.graph.add((self.id, RDFS.label, Literal(self.name)))

def vasegraph(vases) -> Graph:
    g = Graph()
    g.bind("crm", crm)
    g.bind("entity", entity)
    g.bind("aat", aat)
    for v in vases:
        vase = Vase(v)
        g += vase.graph
    return g


def imagegraph(imgs) -> Graph:
    g = Graph()
    g.bind("crm", crm)
    g.bind("image", image)
    g.bind("entity", entity)
    for i in imgs:
        img = Image(i)
        g += img.graph
    return g
