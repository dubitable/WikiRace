import requests, time

BASE_URL = "https://en.wikipedia.org/w/api.php"
USER_AGENT =  "WikiGraph/1.0 (pierrequereuil@gmail.com)"
TIME_DELAY = 1

def get_params(title, continue_token):
    return {
        "action": "query",
        "prop": "links",
        "format": "json",
        "origin": "*",
        "pllimit": "max",
        "titles": title,
        "plcontinue": continue_token
    }

def get_headers():
    return {
        "User-Agent": USER_AGENT
    }

def send_request(title, continue_token = None):
    params = get_params(title, continue_token)
    headers = get_headers()

    response = requests.get(BASE_URL, params=params, headers=headers)
    data = response.json()

    links = []

    if "query" in data and "pages" in data["query"]:
        pages = data["query"]["pages"]
        keys = list(pages.keys())

        if len(keys) >= 0:
            page_id = keys[0]
            if "links" in pages[page_id]:
                links = [link["title"] for link in pages[page_id]["links"]]

    token = None

    if "continue" in data and "plcontinue" in data["continue"]:
        token = data["continue"]["plcontinue"]

    time.sleep(TIME_DELAY)

    return {
        "links": links,
        "continue_token": token
    }

def get_all_links(title):
    result = send_request(title, continue_token = None)

    links = result["links"]
    token = result["continue_token"]

    while token != None:
        result = send_request(title, token)
        links = links + result["links"]
        token = result["continue_token"]

    return links
