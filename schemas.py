"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Add your own schemas here:
# --------------------------------------------------

class Application(BaseModel):
    """Visitor training program application
    Collection name: "application"
    """
    ad_soyad: str = Field(..., description="Başvuru sahibinin adı soyadı")
    email: EmailStr = Field(..., description="E-posta")
    telefon: str = Field(..., description="Telefon numarası")
    kopek_adi: Optional[str] = Field(None, description="Köpeğin adı")
    kopek_yasi: Optional[int] = Field(None, ge=0, le=25, description="Köpeğin yaşı")
    kopek_cinsi: Optional[str] = Field(None, description="Köpeğin ırkı/cinsi")
    egitim_gecmisi: Optional[str] = Field(None, description="Önceki eğitim geçmişi")
    program: str = Field(..., description="Seçilen eğitim programı: temel, ileri, vip")
    mesaj: Optional[str] = Field(None, description="Ek not/mesaj")

class Message(BaseModel):
    """Ziyaretçiden eğitmenlere soru veya iletişim mesajı
    Collection name: "message"
    """
    ad_soyad: str = Field(..., description="Gönderenin adı soyadı")
    email: EmailStr = Field(..., description="E-posta")
    telefon: Optional[str] = Field(None, description="Telefon")
    egitmen_id: Optional[str] = Field(None, description="Hedef eğitmen ID")
    konu: str = Field(..., description="Konu")
    mesaj: str = Field(..., description="Mesaj içeriği")

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
