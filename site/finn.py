import httpx
import asyncio
from bs4 import BeautifulSoup
import re

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

async def fetch_page(client, base_url, query, location_params, page):
    params = location_params + [("q", query), ("page", str(page))]
    try:
        resp = await client.get(base_url, params=params, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        articles = soup.find_all("article", class_="sf-search-ad")
        jobs = []
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
                })
        return jobs
    except Exception as e:
        print(f"Failed to fetch page {page}: {e}")
        return []

async def fetch_finn_jobs_async(query, locations, max_pages=50):
    base_url = "https://www.finn.no/job/fulltime/search.html"
    locations = [loc.strip().lower() for loc in locations]
    location_params = []

    for loc in locations:
        code = location_codes.get(loc)
        if code:
            location_params.append(("location", code))

    if not location_params:
        return {"error": "No valid locations provided."}

    jobs = []

    async with httpx.AsyncClient() as client:
        tasks = [fetch_page(client, base_url, query, location_params, page) for page in range(1, max_pages + 1)]
        results = await asyncio.gather(*tasks)
        for result in results:
            jobs.extend(result)

    return {"jobs": jobs}
