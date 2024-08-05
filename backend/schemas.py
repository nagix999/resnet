from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        protected_namespaces=()
    )

class Score(BaseSchema):
    name: str
    score: float

class Model(BaseSchema):
    model_name: str
    score: list[Score]
    last_updated: datetime

class Proba(BaseSchema):
    candidate: str
    proba: float

class ImageOut(BaseSchema):
    file_name: str
    base64: str

class ImageInference(BaseSchema):
    file_name: str
    probas: list[Proba]
