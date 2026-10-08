import requests

API_URL = "http://127.0.0.1:8000"


def request(method, path, token=None, **kwargs):
    headers = kwargs.pop("headers", {})
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.request(
        method,
        f"{API_URL}{path}",
        headers=headers,
        timeout=15,
        **kwargs,
    )

    if not response.ok:
        try:
            detail = response.json().get("detail", response.text)
        except Exception:
            detail = response.text
        raise Exception(str(detail))

    if response.status_code == 204:
        return None

    return response.json()
