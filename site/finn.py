import httpx
import asyncio
from bs4 import BeautifulSoup
import re

location_codes = {
    "oslo": "1.20001.20061", "agder": "1.20001.22042", "akershus": "1.20001.20003",
    "buskerud": "1.20001.20007", "finnmark": "1.20001.20020", "innlandet": "1.20001.22034",
    "møre og romsdal": "1.20001.20015", "nordland": "1.20001.20018", "rogaland": "1.20001.20012",
    "svalbard": "1.20001.20506", "telemark": "1.20001.20009", "troms": "1.20001.20019",
    "trøndelag": "1.20001.20016", "vestfold": "1.20001.20008", "vestland": "1.20001.22046",
    "bergen": "2.20001.22046.20220", "østfold": "1.20001.20002", "norge": "0.20001",
    "utlandet": "0.20534", "porsgrunn": "2.20001.20009.20146", "ålesund": "2.20001.20015.20282"
}

async def fetch_page(client, query, regions, page):
    params = [("q", query), ("page", str(page))]
    params += [("location", location_codes[r]) for r in regions]

    try:
        resp = await client.get("https://www.finn.no/job/fulltime/search.html", params=params, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        jobs = []

        for ad in soup.select("article.sf-search-ad"):
            if ad.find("span", string=re.compile(r"Hentet fra NAV", re.IGNORECASE)):
                continue

            link = ad.select_one("a.sf-search-ad-link")
            if not link:
                continue

            jobs.append({
                "title": link.text.strip(),
                "link": link["href"],
                "company_info": [span.text.strip() for span in ad.select("div.flex.flex-col.text-xs span")],
                "image": ad.select_one("img")["src"] if ad.select_one("img") else ""
            })

        return jobs

    except Exception as e:
        print(f"Error fetching page {page}: {e}")
        return []

async def get_jobs(query, regions, max_pages=5):
    regions = [r.strip().lower() for r in regions if r.strip().lower() in location_codes]
    if not regions:
        return {"error": "No valid regions selected"}

    async with httpx.AsyncClient() as client:
        tasks = [fetch_page(client, query, regions, page) for page in range(1, max_pages + 1)]
        results = await asyncio.gather(*tasks)

    return {"jobs": [job for page in results for job in page]}
