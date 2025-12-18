from bs4 import BeautifulSoup
import re

def parse_bing_search(html: str) -> list:
    soup = BeautifulSoup(html, "lxml")

    entries = soup.find_all("li", class_="b_algo")
    print(f"Found {len(entries)} entries.")

    results = []

    for entry in entries:
        info = {"title": "", "url": "", "emails": [], "phones": []}

        title_tag = entry.find("h2")
        if title_tag:
            info["title"] = title_tag.get_text(strip=True)

        a_tag = entry.find("a", href=True)
        if a_tag:
            info["url"] = a_tag["href"]

        text = entry.get_text(" ", strip=True)

        emails = re.findall(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text
        )
        info["emails"] = list(set(emails))

        phones = re.findall(
            r'\+?\d[\d\s().-]{7,15}\d',
            text
        )
        info["phones"] = list(set(re.sub(r"\D", "", p) for p in phones))

        results.append(info)

    return results
