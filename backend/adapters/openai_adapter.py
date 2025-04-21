import httpx
import time

def test_openai_key(key_value: str):
    """
    Test an OpenAI API key by listing models. Returns status, response_time_ms, error_message.
    """
    headers = {"Authorization": f"Bearer {key_value}"}
    start = time.time()
    try:
        response = httpx.get("https://api.openai.com/v1/models", headers=headers, timeout=10.0)
        elapsed_ms = (time.time() - start) * 1000
        if response.status_code == 200:
            return "OK", elapsed_ms, None
        elif response.status_code == 401:
            return "EXPIRED", elapsed_ms, response.text
        elif response.status_code == 429:
            return "RATE_LIMITED", elapsed_ms, response.text
        else:
            return "ERROR", elapsed_ms, response.text
    except Exception as e:
        elapsed_ms = (time.time() - start) * 1000
        return "ERROR", elapsed_ms, str(e)
