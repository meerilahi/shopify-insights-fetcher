from typing import List, Optional
from pydantic import BaseModel, HttpUrl, EmailStr


class Product(BaseModel):
    name: str
    description: Optional[str] = None
    price: Optional[float] = None
    url: Optional[str] = None
    image_url: Optional[HttpUrl] = None


class FAQ(BaseModel):
    question: str
    answer: str


class SocialHandles(BaseModel):
    instagram: Optional[HttpUrl] = None
    facebook: Optional[HttpUrl] = None
    tiktok: Optional[HttpUrl] = None
    twitter: Optional[HttpUrl] = None
    youtube: Optional[HttpUrl] = None
    linkedin: Optional[HttpUrl] = None


class ContactDetails(BaseModel):
    emails: List[EmailStr] = []
    phone_numbers: List[str] = []


class ImportantLinks(BaseModel):
    order_tracking: Optional[HttpUrl] = None
    contact_us: Optional[HttpUrl] = None
    blogs: Optional[HttpUrl] = None
    others: List[HttpUrl] = []


class BrandData(BaseModel):
    whole_product_catalog: List[Product]
    hero_products: List[Product]
    privacy_policy: Optional[str] = None
    return_refund_policy: Optional[str] = None
    faqs: List[FAQ]
    social_handles: Optional[SocialHandles] = None
    contact_details: Optional[ContactDetails] = None
    brand_description: Optional[str] = None
    important_links: Optional[ImportantLinks] = None
