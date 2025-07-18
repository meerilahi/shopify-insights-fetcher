from fastapi import FastAPI, Query, HTTPException
from pydantic import HttpUrl
from schemas import BrandData
from service import get_brand_data_service 

app = FastAPI()


@app.get("/extract-brand-data", response_model=BrandData)
def extract_brand_data(url: HttpUrl = Query(..., description="Brand website URL")):
    try:
        brand_data = get_brand_data_service(url)
        return brand_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
