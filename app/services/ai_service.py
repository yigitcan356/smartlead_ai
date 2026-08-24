import requests

from config import Config


class AIServiceError(Exception):
    """AI servisinde oluşan hatalar için özel hata sınıfı."""
    pass


class AIService:
    """RILVON yapay zeka servis katmanı."""

    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.provider = Config.AI_PROVIDER

    def _sistem_talimati(self):
        """RILVON'un sistem talimatını döndürür."""
        return Config.BUSINESS_CONTEXT

    def yanit_uret(self, mesaj, gecmis=None):
        """Kullanıcı mesajını Groq API'ye gönderir ve AI cevabını döndürür."""

        if not self.api_key:
            return (
                "Demo modundayız. Şu anda yapay zekâ servisi "
                "yapılandırılmamış durumda."
            )

        messages = [
            {
                "role": "system",
                "content": self._sistem_talimati(),
            }
        ]

        if gecmis:
            messages.extend(gecmis)

        messages.append(
            {
                "role": "user",
                "content": mesaj,
            }
        )

        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "openai/gpt-oss-20b",
            "messages": messages,
            "temperature": 0.4,
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=30,
            )

            response.raise_for_status()

            data = response.json()

            return data["choices"][0]["message"]["content"]

        except requests.HTTPError as exc:
            raise AIServiceError(
                f"Groq HTTP hatası ({response.status_code}): "
                f"{response.text}"
            ) from exc

        except requests.RequestException as exc:
            raise AIServiceError(
                f"Groq API bağlantı hatası: {exc}"
            ) from exc

        except (KeyError, IndexError, TypeError) as exc:
            raise AIServiceError(
                "Groq API yanıtı beklenen formatta değil."
            ) from exc


ai_service = AIService()