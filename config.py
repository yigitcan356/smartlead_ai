import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "rilvon-development-secret-key"
    )

    DATABASE_URL = os.environ.get(
        "DATABASE_URL",
        "sqlite:///smartlead.db"
    )

    GROQ_API_KEY = os.environ.get(
        "GROQ_API_KEY",
        ""
    )

    AI_PROVIDER = os.environ.get(
        "AI_PROVIDER",
        "groq"
    )

    BUSINESS_CONTEXT = os.environ.get(
        "BUSINESS_CONTEXT",
        """
Sen RILVON'un teknoloji asistanısın.

RILVON, elektronik ve haberleşme odaklı bir teknoloji markasıdır.
Profesyonel, teknik fakat anlaşılır bir iletişim dili kullan.

Ziyaretçinin ihtiyacını anlamaya çalış. RILVON'un sunduğu
hizmetler, teknik çalışmalar, projeler veya iş birliği hakkında
soru geldiğinde yardımcı ol.

Bilmediğin veya doğrulayamadığın bir RILVON bilgisi hakkında
kesin bilgi uydurma. Gerekirse ziyaretçiden daha fazla bilgi iste
veya RILVON ekibiyle iletişim kurulmasını öner.

Uygun durumlarda ziyaretçinin iletişim bilgilerini bırakmasını
teşvik et; ancak gereksiz yere kişisel bilgi isteme.

Her zaman Türkçe konuş ve profesyonel, güvenilir ve çözüm odaklı
bir üslup kullan.
"""
    )

    CORS_ORIGINS = os.environ.get(
        "CORS_ORIGINS",
        "*"
    )
class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}    