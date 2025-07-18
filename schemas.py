from typing import List, Optional
from pydantic import BaseModel, EmailStr


class Product(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None


class FAQ(BaseModel):
    question: str
    answer: str


class BrandData(BaseModel):
    whole_product_catalog: List[Product]
    hero_products: List[Product]
    privacy_policy: Optional[str] = None
    return_refund_policy: Optional[str] = None
    faqs: List[FAQ]
    social_handles: Optional[List[str]] = None
    emails: List[EmailStr] = []
    phone_numbers: List[str] = []
    brand_description: Optional[str] = None
    important_links: Optional[List[str]] = None
