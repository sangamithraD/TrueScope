import os
import requests
import concurrent.futures

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
FACTCHECK_KEY = os.getenv("FACTCHECK_KEY")
GOOGLE_SEARCH_KEY = os.getenv("GOOGLE_SEARCH_KEY")
GOOGLE_CX = os.getenv("GOOGLE_CX")
NEWS_SEARCH_TIMEOUT = int(os.getenv("NEWS_SEARCH_TIMEOUT", 6))
NEWS_SEARCH_PAGE_SIZE = int(os.getenv("NEWS_SEARCH_PAGE_SIZE", 10))

def search_newsapi(title: str, lang="en"):
    if not NEWSAPI_KEY:
        return []
    try:
        params = {"q": title, "apiKey": NEWSAPI_KEY, "language": lang, "pageSize": NEWS_SEARCH_PAGE_SIZE}
        r = requests.get("https://newsapi.org/v2/everything", params=params, timeout=NEWS_SEARCH_TIMEOUT)
        results = []
        for art in r.json().get("articles", []):
            url = art.get("url")
            publisher = art.get("source", {}).get("name", "NewsAPI")
            if url:
                results.append({"url": url, "publisher": publisher, "snippet": art.get("description", "")})
        return results
    except:
        return []

def search_factcheck(title: str):
    if not FACTCHECK_KEY:
        return []
    try:
        url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
        params = {"query": title, "key": FACTCHECK_KEY, "pageSize": 5}
        r = requests.get(url, params=params, timeout=NEWS_SEARCH_TIMEOUT)
        results = []
        for claim in r.json().get("claims", []):
            cr = claim.get("claimReview", [{}])[0]
            url = cr.get("url")
            publisher = cr.get("publisher", {}).get("name", "FactCheck")
            if url:
                results.append({"url": url, "publisher": publisher, "snippet": cr.get("textualRating","")})
        return results
    except:
        return []

def search_google_cx(title: str):
    if not GOOGLE_SEARCH_KEY or not GOOGLE_CX:
        return []
    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {"q": title, "key": GOOGLE_SEARCH_KEY, "cx": GOOGLE_CX, "num": 5}
        r = requests.get(url, params=params, timeout=NEWS_SEARCH_TIMEOUT)
        results = []
        for item in r.json().get("items", []):
            link = item.get("link")
            publisher = item.get("displayLink", "GoogleSearch")
            if link:
                results.append({"url": link, "publisher": publisher, "snippet": item.get("snippet","")})
        return results
    except:
        return []

def search_wiki(title: str, lang="en"):
    try:
        url = f"https://{lang}.wikipedia.org/w/api.php"
        params = {"action": "opensearch", "search": title, "limit": 5, "format": "json"}
        r = requests.get(url, params=params, timeout=NEWS_SEARCH_TIMEOUT)
        links = r.json()[3] if len(r.json()) >= 4 else []
        return [{"url": l, "publisher": "Wikipedia", "snippet": ""} for l in links]
    except:
        return []

def find_sources(title: str, lang="en"):
    sources = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        futures = [
            ex.submit(search_newsapi, title, lang),
            ex.submit(search_factcheck, title),
            ex.submit(search_google_cx, title),
            ex.submit(search_wiki, title, lang),
        ]
        for f in concurrent.futures.as_completed(futures):
            try:
                sources.extend(f.result())
            except:
                continue
    seen = set()
    unique = []
    for s in sources:
        if s["url"] not in seen:
            seen.add(s["url"])
            unique.append(s)
    return unique
