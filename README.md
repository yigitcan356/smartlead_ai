# SmartLead AI

Yapay zekâ destekli lead toplama ve yönetim sistemi.

SmartLead AI; web ziyaretçileriyle yapay zekâ üzerinden sohbet edilmesini, potansiyel müşterilerin iletişim bilgilerinin (lead) güvenli biçimde kaydedilmesini ve bu kayıtların işletme sahibi tarafından yönetim paneli üzerinden görüntülenmesini sağlayan bir MVP'dir.

## Proje Amacı

Proje, yönergede belirtilen **Separation of Concerns (SoC)** yaklaşımına uygun, sorumlulukları ayrılmış ve canlı ortamda çalışabilen bir web uygulaması geliştirmek amacıyla hazırlanmıştır.

Sistem iki temel kullanıcı yüzünden oluşur:

- **Karşılama / sohbet arayüzü:** Ziyaretçi yapay zekâ ile konuşabilir ve iletişim bilgilerini bırakabilir.
- **Yönetim paneli:** İşletme sahibi oluşturulan lead kayıtlarını görüntüleyebilir.

## Temel Özellikler

- Yapay zekâ destekli sohbet
- Konuşma geçmişinin AI servisine aktarılması
- İsim ve telefon bilgileriyle lead oluşturma
- Lead kayıtlarının SQLite veritabanında saklanması
- Lead kayıtlarını listeleyen REST API
- Yönetim paneli
- Güvenli hata yönetimi
- Environment variable tabanlı gizli anahtar yönetimi
- GitHub + Render üzerinde canlı backend
- Wix / Wix Velo frontend entegrasyonu

## Teknolojiler

- Python 3.9+
- Flask
- SQLite
- Groq API
- HTML / CSS / JavaScript
- Wix / Wix Velo
- Render
- GitHub
- Gunicorn

## Sistem Mimarisi

```text
Wix / Frontend
      │
      │ REST API
      ▼
   Flask Backend
      │
      ├──────────────► AI Service ─────► Groq API
      │
      └──────────────► Database Layer ──► SQLite
```

Backend içerisinde sorumluluklar katmanlara ayrılmıştır:

```text
smartlead_ai/
├── run.py
├── config.py
├── requirements.txt
├── .gitignore
└── app/
    ├── __init__.py
    ├── database.py
    ├── routes.py
    ├── services/
    │   ├── __init__.py
    │   └── ai_service.py
    └── templates/
        ├── index.html
        └── dashboard.html
```

### Katmanların Sorumlulukları

| Dosya | Sorumluluk |
|---|---|
| `config.py` | Uygulama yapılandırması ve environment variable yönetimi |
| `database.py` | SQLite bağlantısı, tablo oluşturma, lead ekleme ve listeleme |
| `ai_service.py` | Groq API ile yapay zekâ iletişimi |
| `routes.py` | HTTP sayfa ve API rotaları |
| `app/__init__.py` | Flask application factory |
| `run.py` | Uygulamanın giriş noktası |

Bu yapı sayesinde HTTP rotaları doğrudan SQL işlemleri veya doğrudan AI API çağrıları gerçekleştirmez.

## Backend API

| Method | Endpoint | Açıklama |
|---|---|---|
| `GET` | `/` | Karşılama sayfası |
| `GET` | `/dashboard` | Yönetim paneli |
| `GET` | `/health` | Backend sağlık kontrolü |
| `POST` | `/api/sohbet` | AI sohbet isteği |
| `POST` | `/api/leads` | Yeni lead oluşturma |
| `GET` | `/api/leads` | Lead kayıtlarını listeleme |

API katmanında eksik veriler ve dış servis hataları güvenli JSON yanıtlarıyla ele alınır.

## Veritabanı

SQLite üzerinde `leads` tablosu kullanılmaktadır.

Alanlar:

- `id`
- `isim`
- `telefon`
- `mesaj`
- `tarih`

Lead ekleme işlemlerinde parametreli SQL sorguları kullanılır.

## Yapay Zekâ Katmanı

AI entegrasyonu `app/services/ai_service.py` içerisinde izole edilmiştir.

Routes katmanı AI sağlayıcısına doğrudan bağlanmaz. Bu sayede AI servisinin değiştirilmesi veya geliştirilmesi diğer uygulama katmanlarından bağımsız yapılabilir.

## Güvenlik

- API anahtarları kaynak kodunda tutulmaz.
- Gizli değerler environment variable üzerinden okunur.
- `.env` dosyası GitHub'a yüklenmez.
- SQL işlemlerinde parametreli sorgular kullanılır.
- Dış servis ve uygulama hataları `try/except` ile güvenli yanıtlarla ele alınır.

> **Not:** Gerçek API anahtarları bu repository'ye veya README dosyasına eklenmemelidir.

## Yerel Kurulum

### 1. Repository'yi klonlayın

```bash
git clone https://github.com/yigitcan356/smartlead_ai.git
cd smartlead_ai
```

### 2. Sanal ortam oluşturun

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Bağımlılıkları yükleyin

```bash
pip install -r requirements.txt
```

### 4. Environment variable'ları tanımlayın

Örnek:

```env
AI_PROVIDER=groq
GROQ_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
```

Gerçek anahtarları paylaşmayın veya GitHub'a yüklemeyin.

### 5. Uygulamayı çalıştırın

```bash
python run.py
```

Ardından uygulamayı:

```text
http://127.0.0.1:5000
```

adresinden açabilirsiniz.

## Canlı Sistem

**GitHub Repository**  
https://github.com/yigitcan356/smartlead_ai

**Render Backend**  
https://smartlead-ai-1k1q.onrender.com

**Wix Web Sitesi**  
https://rilvontech.wixstudio.com/elektronik-ve-haber

## Yayınlama

Backend Render üzerinde Gunicorn kullanılarak production ortamında çalıştırılmaktadır.

Wix tarafındaki frontend, Render üzerinde çalışan REST API ile haberleşecek şekilde yapılandırılmıştır.

## Demo Akışı

1. Wix karşılama sayfası açılır.
2. Ziyaretçi AI ile sohbet eder.
3. Ziyaretçi isim ve telefon bilgilerini bırakır.
4. Lead bilgileri backend API üzerinden kaydedilir.
5. Kayıtlar SQLite veritabanında tutulur.
6. Yönetim paneli lead kayıtlarını backend üzerinden görüntülemek üzere kullanılır.

## Proje Durumu

SmartLead AI; backend, AI servis katmanı, SQLite lead yönetimi, REST API, Wix frontend entegrasyonu ve Render deployment bileşenlerini içeren çalışan bir MVP olarak hazırlanmıştır.

Teslim kapsamında:

- GitHub repository
- Canlı Render backend
- Yayınlanmış Wix sitesi
- README
- Proje sunumu / demo

birlikte değerlendirilmek üzere hazırlanmıştır.

## Lisans

Bu proje eğitim ve proje teslim amacıyla geliştirilmiştir.
