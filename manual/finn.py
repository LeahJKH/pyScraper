import requests
from bs4 import BeautifulSoup
import re
import os

# here u can add more locations if u want remember too use finn codes if u want more implimented send me a msg on disc
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

query = input("What are you looking for? ").strip()
location_input = input("Which regions (comma-separated, e.g. Oslo, Agder)? ").strip().lower()

locations = [loc.strip() for loc in location_input.split(',')]
location_params = []
valid_location_names = []

for loc in locations:
    code = location_codes.get(loc)
    if code:
        location_params.append(("location", code))
        valid_location_names.append(loc)
    else:
        print(f"Warning: '{loc}' not recognized.")

if not location_params:
    print("No valid locations provided.")
    exit()

def make_safe_filename(text):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', text.strip().lower())

safe_query = make_safe_filename(query)
safe_locations = "_".join(make_safe_filename(loc) for loc in valid_location_names)
filename = f"finn_jobs_{safe_query}_{safe_locations}.txt" #gives unique file names too overwrite later

output_dir = "finn_jobs"
os.makedirs(output_dir, exist_ok=True)

filepath = os.path.join(output_dir, filename)

def fetch_finn_jobs():
    base_url = "https://www.finn.no/job/fulltime/search.html" #url it builds off
    output_lines = []

    for page in range(1, 51):
        params = location_params + [("q", query), ("page", str(page))]
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            articles = soup.find_all("article", class_="sf-search-ad") #main ad article
            for article in articles:
                title_tag = article.find("a", class_="sf-search-ad-link")
                company_tag = article.find("div", class_="flex flex-col text-xs")
                if title_tag:
                    title = title_tag.text.strip()
                    link = title_tag['href']
                    output_lines.append(f"Title: {title}")
                    output_lines.append(f"Link: {link}")
                    if company_tag:
                        company_info = [span.text for span in company_tag.find_all("span")]
                        output_lines.append("Company Info: " + ", ".join(company_info))
                    output_lines.append("-" * 60)
        else:
            output_lines.append(f"Failed to fetch page {page}. Status code: {response.status_code}")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines)) #makes a file if you are using manual

    print(f"Job data saved to {filepath}")

fetch_finn_jobs()