from bs4 import BeautifulSoup
import re

def parse_twitter(html: str) -> list:
    soup = BeautifulSoup(html, "lxml")
    entries = soup.find_all("div", class_="MjjYud")
    print(f"Found {len(entries)} entries.")

    results = []

    for entry in entries:
        info = {"title": "","url": "","emails": [],"phones": [],"followers": ""}

        title_tag = entry.find("h3")
        if title_tag:
            info["title"] = title_tag.get_text(strip=True)

        a_tag = entry.find("a", class_="zReHs", href=True)
        if a_tag:
            info["url"] = a_tag["href"]

        text = entry.get_text(" ", strip=True)
       
        info["emails"] = list(set(re.findall(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",text
        )))

        phones = re.findall(r'\+?\d[\d\s().-]{7,15}\d', text)
        info["phones"] = list(set(re.sub(r"\D", "", p) for p in phones))

        cite_tag = entry.find("cite", string=re.compile("followers", re.I))
        if cite_tag:
            match = re.search(r"(\d[\d,\.]*\s*[kKmM]?)\s*", cite_tag.get_text())
            if match:
                info["followers"] = match.group(1)

        results.append(info)

    return results