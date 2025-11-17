import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId

from database import db, create_document, get_documents

app = FastAPI(title="Protection Dog Training API", description="Koruma köpeği eğitimi web sitesi için backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ApplicationIn(BaseModel):
    ad_soyad: str
    email: EmailStr
    telefon: str
    kopek_adi: Optional[str] = None
    kopek_yasi: Optional[int] = Field(None, ge=0, le=25)
    kopek_cinsi: Optional[str] = None
    egitim_gecmisi: Optional[str] = None
    program: str = Field(..., description="temel|ileri|vip")
    mesaj: Optional[str] = None

class MessageIn(BaseModel):
    ad_soyad: str
    email: EmailStr
    telefon: Optional[str] = None
    egitmen_id: Optional[str] = None
    konu: str
    mesaj: str

@app.get("/")
def read_root():
    return {"message": "Protection Dog Training API"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"

            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    return response

@app.post("/api/apply")
def submit_application(payload: ApplicationIn):
    try:
        inserted_id = create_document("application", payload)
        return {"ok": True, "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/message")
def send_message(payload: MessageIn):
    try:
        inserted_id = create_document("message", payload)
        return {"ok": True, "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/blogs")
def list_blogs(limit: int = 6):
    # Demo static list; replace with DB later if needed
    posts = [
        {
            "id": i,
            "title": title,
            "excerpt": excerpt,
            "slug": slug,
            "cover": cover
        }
        for i, (title, excerpt, slug, cover) in enumerate([
            ("Koruma Köpeği Seçerken Dikkat Edilmesi Gerekenler", "Doğru ırk, mizaç ve eğitim geçmişi nasıl değerlendirilir?", "koruma-kopegini-secerken", "https://images.unsplash.com/photo-1543466835-00a7907e9de1?q=80&w=1600&auto=format&fit=crop"),
            ("Koruma Köpeği Eğitiminin Faydaları", "Aile ve iş güvenliği için eğitimli bir köpeğin sağladığı avantajlar", "egitimin-faydalari", "https://images.unsplash.com/photo-1507149833265-60c372daea22?q=80&w=1600&auto=format&fit=crop"),
            ("Eğitimde Kullanılan Ekipmanlar", "Isırma manşonu, tasma, ödül oyuncakları ve daha fazlası", "ekipmanlar", "https://images.unsplash.com/photo-1542060748-10c28b62716a?q=80&w=1600&auto=format&fit=crop"),
            ("Sağlıklı Gelişim İçin İpuçları", "Beslenme, egzersiz ve zihinsel uyarımın önemi", "saglikli-gelisim", "https://images.unsplash.com/photo-1558944351-c6a8f6f9cb6a?q=80&w=1600&auto=format&fit=crop"),
            ("İleri Düzey Tehdit Algılama", "Gerçek senaryolarla yapılan eğitim aşamaları", "tehdit-algilama", "https://images.unsplash.com/photo-1525253086316-d0c936c814f8?q=80&w=1600&auto=format&fit=crop"),
            ("Sık Sorulan Sorular", "Programlar, süreç ve fiyatlandırma hakkında yanıtlar", "sss", "https://images.unsplash.com/photo-1534361960057-19889db9621e?q=80&w=1600&auto=format&fit=crop"),
        ])
    ]
    return {"ok": True, "posts": posts[:limit]}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
