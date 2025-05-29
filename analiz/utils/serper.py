import requests
from django.conf import settings  # settings içinden çekmek için

def serper_google_search(query, num=10):
    """
    Serper API kullanarak Google araması yapar.
    Dönüş: [(link, snippet), ...]
    """
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": settings.SERPER_API_KEY,  # ← .env içinden geldi artık
        "Content-Type": "application/json"
    }
    payload = {
        "q": query,
        "num": num
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return [
                (result.get("link", ""), result.get("snippet", ""))
                for result in data.get("organic", [])
            ]
        else:
            return []
    except Exception as e:
        return []
