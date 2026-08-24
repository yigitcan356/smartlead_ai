from flask import Blueprint, jsonify, request, render_template

from app.services.ai_service import ai_service, AIServiceError
from app.database import lead_ekle, tum_leadler


page_bp = Blueprint("pages", __name__)

api_bp = Blueprint("api", __name__, url_prefix="/api")
@page_bp.get("/")
def ana_sayfa():
    return render_template("index.html")


@page_bp.get("/dashboard")
def dashboard():
    return render_template("dashboard.html")
@api_bp.post("/sohbet")
def sohbet():
    data = request.get_json(silent=True) or {}

    mesaj = data.get("mesaj", "").strip()
    gecmis = data.get("gecmis", [])

    if not mesaj:
        return jsonify({
            "basari": False,
            "hata": "Mesaj alanı boş bırakılamaz."
        }), 400

    try:
        cevap = ai_service.yanit_uret(
            mesaj=mesaj,
            gecmis=gecmis
        )

        return jsonify({
            "basari": True,
            "cevap": cevap
        }), 200

    except AIServiceError:
        return jsonify({
            "basari": False,
            "hata": "Yapay zekâ servisine şu anda ulaşılamıyor."
        }), 503

@api_bp.post("/leads")
def lead_olustur():
    data = request.get_json(silent=True) or {}

    isim = data.get("isim", "").strip()
    telefon = data.get("telefon", "").strip()
    mesaj = data.get("mesaj", "").strip()

    if not isim or not telefon:
        return jsonify({
            "basari": False,
            "hata": "İsim ve telefon alanları zorunludur."
        }), 400

    try:
        lead_id = lead_ekle(
            isim,
            telefon,
            mesaj
        )

        return jsonify({
            "basari": True,
            "lead_id": lead_id,
            "mesaj": "İletişim bilgileriniz başarıyla kaydedildi."
        }), 201

    except Exception:
        return jsonify({
            "basari": False,
            "hata": "Lead kaydedilirken bir hata oluştu."
        }), 500
@api_bp.get("/leads")
def leadleri_getir():
    try:
        leadler = tum_leadler()

        return jsonify({
            "basari": True,
            "leadler": leadler
        }), 200

    except Exception:
        return jsonify({
            "basari": False,
            "hata": "Lead kayıtları alınırken bir hata oluştu."
        }), 500