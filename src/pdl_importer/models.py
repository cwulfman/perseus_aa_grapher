from pydantic import BaseModel


class ImageData(BaseModel):
    id: str
    represents: str | None
    caption: str | None
    credits: str | None


class CollectionData(BaseModel):
    index: str
    name: str
    entityid: str
    uri: str


class VaseData(BaseModel):
    id: str | None
    name: str | None
    type: str | None
    location: str | None
    summary: str | None
    perseus_version: str | None
    entered_by: str | None
    sources_used: str | None
    other_bibliography: str | None
    documentary_references: str | None
    accession_number: str | None
    dimensions: str | None
    region: str | None
    start_date: str | None
    start_mod: str | None
    end_date: str | None
    end_mod: str | None
    unitary_date: str | None
    unitary_mod: str | None
    date_for_sort: str | None
    period: str | None
    period_for_sort: str | None
    culture: str | None
    context: str | None
    context_mod: str | None
    findspot: str | None
    findspot_mod: str | None
    collection: str | None
    date_description: str | None
    collection_history: str | None
    donor: str | None
    condit: str | None
    condition_description: str | None
    comparanda: str | None
    material: str | None
    material_description: str | None
    other_notes: str | None
    graffiti: str | None
    primary_citation: str | None
    ceramic_phase: str | None
    decoration_description: str | None
    essay_number: str | None
    essay_text: str | None
    inscriptions: str | None
    painter: str | None
    painter_mod: str | None
    attributed_by: str | None
    potter: str | None
    potter_mod: str | None
    beazley_number: str | None
    relief: str | None
    shape: str | None
    shape_description: str | None
    ware: str | None
