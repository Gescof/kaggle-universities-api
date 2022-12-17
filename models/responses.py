from pydantic import BaseModel


class CountriesOutput(BaseModel):
    country_code: str


class WorldUniversitiesOutput(BaseModel):
    country_code: str
    name: str
    url: str
