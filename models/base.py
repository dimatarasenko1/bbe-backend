from pydantic import BaseModel


# in api all fields returned in camelCase by default
def to_camel(string: str) -> str:
    parts = string.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


class CamelCaseModel(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True
