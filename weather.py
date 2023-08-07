from requests_html import HTMLSession

def get_weather(date: str = "today", location: str = "here", unit: str = "c"):
    session = HTMLSession()

    query = ""
    url = f"https://www.google.com/search?q={location}+weather"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Accept-Langauge": "en-US,en;q=0.9",
    }
    language = "en"
    
    params = {
        "hl": language,
        "gl": "" if unit == "c" else "us"
    }

    results = session.get(
        url,
        headers=headers,
        params=params,
    )
    
    temperature = results.html.find("span#wob_tm", first=True).text
    unit = results.html.find("div.vk_bk.wob-unit span.wob_t", first=True).text
    
    return temperature + unit