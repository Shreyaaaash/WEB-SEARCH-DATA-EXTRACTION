import requests
def search_entities(entity, query, api_key):
    search_query = query.replace("PLACEHOLDER", entity)
    params = {
        "q": search_query,
        "api_key": api_key
    }
    response = requests.get("https://serpapi.com/search", params=params)
    if response.status_code == 200:
        return response.json().get("organic_results", [])
    else:
        return []
