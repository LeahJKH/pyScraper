import requests
from bs4 import BeautifulSoup
import re
import os

location_codes = {
 "agder": "1.20001.22042",
    "akershus": "1.20001.20003",
    "buskerud": "1.20001.20007",
    "finnmark": "1.20001.20020",
    "innlandet": "1.20001.22034",
    "møre og romsdal": "1.20001.20015",
    "nordland": "1.20001.20018",
    "oslo": "1.20001.20061",
    "rogaland": "1.20001.20012",
    "svalbard": "1.20001.20506",
    "telemark": "1.20001.20009",
    "troms": "1.20001.20019",
    "trøndelag": "1.20001.20016",
    "vestfold": "1.20001.20008",
    "vestland": "1.20001.22046",
    "bergen": "2.20001.22046.20220",
    "østfold": "1.20001.20002",
    "norge": "0.20001",
    "utlandet": "0.20534",
    "porsgrunn": "2.20001.20009.20146",
    "ålesund": "2.20001.20015.20282"
    }

def make_safe_filename(text):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', text.strip().lower())

def fetch_finn_jobs(query, locations):
    locations = [loc.strip().lower() for loc in locations]
    location_params = []
    valid_location_names = []

    for loc in locations:
        code = location_codes.get(loc)
        if code:
            location_params.append(("location", code))
            valid_location_names.append(loc)

    if not location_params:
        return {"error": "No valid locations provided."}

    base_url = "https://www.finn.no/job/fulltime/search.html"
    jobs = []

    # this finds the object on finn
    for page in range(1, 51):  
        params = location_params + [("q", query), ("page", str(page))]
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            articles = soup.find_all("article", class_="sf-search-ad") # this is the main article around the ad
            for article in articles:
                title_tag = article.find("a", class_="sf-search-ad-link")
                company_tag = article.find("div", class_="flex flex-col text-xs")
                if title_tag:
                    title = title_tag.text.strip()
                    link = title_tag['href']
                    company_info = []
                    if company_tag:
                        company_info = [span.text for span in company_tag.find_all("span")]
                    jobs.append({
                        "title": title,
                        "link": link,
                        "company_info": company_info
                    }) # creates the object
        else:
            return {"error": f"Failed to fetch page {page}. Status code: {response.status_code}"}

    return {"jobs": jobs}
