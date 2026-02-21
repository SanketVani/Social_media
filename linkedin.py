from bs4 import BeautifulSoup
import re

def parse_linkedin(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")

    info = {
        "title": "","sub-title": "","about us": "","address": "","website": "","followers": "","company-size": "","industry": "",
        "headqurter": "","type": "","founded": "","speciality": "","phones": [],"emails": []
    }

    name_tag = soup.find("h1", class_="top-card-layout__title")
    if name_tag:
        info["title"] = name_tag.get_text(strip=True)

    addresses = soup.find_all("div",id=lambda x: x in ["address-0", "address-1", "address-2", "address-3"])
    if addresses:
        info["address"] = " | ".join(addr.get_text(strip=True) for addr in addresses)

    followers_tag = soup.find("h3", class_="top-card-layout__first-subline")
    if followers_tag:
        text = followers_tag.get_text(" ", strip=True)
        match = re.search(r"([\d,]+)\s*followers", text)
        if match:
            info["followers"] = match.group(1)

    sub_title_tag = soup.find("h4", class_="top-card-layout__second-subline")
    if sub_title_tag:
        info["sub-title"] = sub_title_tag.get_text(strip=True)

    about_us_tag = soup.find("p", {"data-test-id": "about-us__description"})
    if about_us_tag:
        info["about us"] = about_us_tag.get_text(strip=True)

    website_tag = soup.find("a", {"data-tracking-control-name": "about_website"})
    if website_tag:
        info["website"] = website_tag.get("href")

    full_text = soup.get_text(" ", strip=True)

    phone_pattern =  r'\+?\d[\d\s().-]{7,}\d'
    phone_matches = re.findall(phone_pattern, full_text)

    phones = set()
    for phone in phone_matches:
        cleaned = re.sub(r"[^\d+]", "", phone)
        phones.add(cleaned)

    info["phones"] = list(phones)

    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    info["emails"] = list(set(re.findall(email_pattern, full_text)))

    def get_about_dd(test_id):
        container = soup.find("div", {"data-test-id": test_id})
        if container:
            dd = container.find("dd")
            if dd:
                return dd.get_text(strip=True)
        return ""

    info["industry"]     = get_about_dd("about-us__industry")
    info["company-size"] = get_about_dd("about-us__size")
    info["headqurter"]   = get_about_dd("about-us__headquarters")
    info["type"]         = get_about_dd("about-us__organizationType")
    info["founded"]      = get_about_dd("about-us__foundedOn")
    info["speciality"]   = get_about_dd("about-us__specialties")

    return info