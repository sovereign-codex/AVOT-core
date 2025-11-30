import json
import os

try:
    import requests
except ImportError:  # pragma: no cover - optional dependency
    requests = None


class LocalOpenAIClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI")

    @property
    def is_configured(self):
        return bool(self.api_key)

    def chat(self, model="gpt-4o-mini", messages=None, temperature=0.2, max_tokens=None):
        if not self.is_configured:
            return {
                "error": True,
                "status": "missing_api_key",
                "content": "OPENAI_API_KEY environment variable is not set.",
            }

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        payload = {
            "model": model,
            "messages": messages or [{"role": "user", "content": "Hello"}],
            "temperature": temperature,
        }
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        response_status = None
        response_text = None

        if requests:
            resp = requests.post(url, headers=headers, data=json.dumps(payload))
            response_status = resp.status_code
            response_text = resp.text
        else:  # Fallback to urllib to avoid external dependency issues
            import urllib.error
            import urllib.request

            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST",
            )
            try:
                with urllib.request.urlopen(req) as resp:  # noqa: S310 - trusted endpoint
                    response_status = resp.getcode()
                    response_text = resp.read().decode("utf-8")
            except urllib.error.HTTPError as exc:  # pragma: no cover - network dependent
                response_status = exc.code
                response_text = exc.read().decode("utf-8")
            except urllib.error.URLError as exc:  # pragma: no cover - network dependent
                response_status = "network_error"
                response_text = str(exc.reason)

        if response_status != 200:
            return {
                "error": True,
                "status": response_status,
                "content": response_text,
            }

        try:
            return json.loads(response_text)
        except Exception:
            return {
                "error": True,
                "status": response_status,
                "content": response_text,
            }


# convenience wrapper

def get_client():
    return LocalOpenAIClient()
