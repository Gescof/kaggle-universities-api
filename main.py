import json
import pandas as pd
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi
from fastapi import FastAPI
from fastapi_pagination import Page, add_pagination, paginate
from models.responses import CountriesOutput, WorldUniversitiesOutput

kaggle_api = KaggleApi()
kaggle_api.authenticate()
app = FastAPI()
add_pagination(app)

# downloading from kaggle.com/thedevastator/all-universities-in-the-world
# we write to the current directory path with './'
kaggle_api.dataset_download_files('thedevastator/all-universities-in-the-world', path='./')
with zipfile.ZipFile('all-universities-in-the-world.zip', 'r') as zipref:
    zipref.extractall('data')


@app.get("/countries", response_model=Page[CountriesOutput])
async def get_countries():
    # Reading Dataset of world universities
    path_csv = 'data/world-universities.csv'
    df_countries = pd.read_csv(path_csv)
    df_countries.columns = ['country_code', 'name', 'url']
    df_countries.drop(['name', 'url'], axis=1, inplace=True)
    df_output = df_countries.drop_duplicates().to_json(orient='records')
    return paginate(json.loads(df_output))


@app.get("/universities", response_model=Page[WorldUniversitiesOutput])
async def get_universities(country_code: str | None = None):
    # Reading Dataset of world universities
    path_csv = 'data/world-universities.csv'
    df_universities = pd.read_csv(path_csv)
    df_universities.columns = ['country_code', 'name', 'url']
    df_output = df_universities.to_json(orient='records')
    if country_code:
        df_output = df_universities.query(f'country_code == \"{country_code}\"').to_json(orient='records')
    return paginate(json.loads(df_output))
