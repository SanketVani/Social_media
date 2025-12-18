from bs4 import BeautifulSoup
import re

def parse_duck_go_search(html: str) -> list:
    soup = BeautifulSoup(html, "lxml")

    entries = soup.find_all("article", {"data-testid": "result"})
    print(f"Found {len(entries)} entries.")

    results = []

    for entry in entries:
        info = {
            "title": "","url": "","emails": [],"phones": []
        }

        h2 = entry.find("h2")
        if h2:
            a_tag = h2.find("a", href=True)
            if a_tag:
                info["title"] = a_tag.get_text(strip=True)
                info["url"] = a_tag["href"]

        text = " ".join(
            elem.get_text(" ", strip=True)
            for elem in entry.find_all(["span", "p"])
        )

        emails = re.findall(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text
        )
        info["emails"] = list(set(emails))

        phones = re.findall(
        r"(?<!\d)(?:\+?\d{1,3}[\s.-])(?:\d{2,4}[\s.-]){2,3}\d{2,4}(?!\d)|(?<!\d)(?:\+?91[\s.-])(?:\d{2}[\s.-])\d{8}(?!\d)",
        text
        )
        info["phones"] = list(set(re.sub(r"\D", "", p) for p in phones))

        results.append(info)

    return results