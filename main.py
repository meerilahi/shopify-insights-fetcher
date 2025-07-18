from fastapi import FastAPI, Query, HTTPException
from pydantic import HttpUrl
from schemas import BrandData
from service import get_brand_data_service 

app = FastAPI()


import traceback

@app.get("/extract-brand-data", response_model=BrandData)
def extract_brand_data(url:str):
    try:
        brand_data = get_brand_data_service(url)
        return brand_data
    except Exception as e:
        traceback.print_exc()  # Logs the full traceback
        raise HTTPException(status_code=500, detail=str(e))

