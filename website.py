from bs4 import BeautifulSoup
import json
import re

def parse_website(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")

    info = {
        "title": "","sub_title": "","description": "","keyword": "","phones": [],"emails": [],"whatsapp_num":[],"social_media":[]
        }

    title_tag = soup.find("title")
    if title_tag:
        info["title"] = title_tag.get_text(strip=True)

    h1_tag = soup.find("h1")
    if h1_tag:
        info["sub_title"] = h1_tag.get_text(strip=True)

    meta_desc = soup.find("meta", attrs={"name": "description"})
    og_desc = soup.find("meta", property="og:description")

    if og_desc and og_desc.get("content"):
        info["description"] = og_desc["content"].strip()
    elif meta_desc and meta_desc.get("content"):
        info["description"] = meta_desc["content"].strip()

    keyword_tag = soup.find("meta", attrs={"name":"keywords"})
    if keyword_tag and keyword_tag.get("content"):
        info["keyword"] = keyword_tag["content"].strip()

    full_text = soup.get_text(" ", strip=True)

    email_set = set()

    mailto_tags = soup.find_all("a", href=re.compile(r"mailto:", re.I))
    for tag in mailto_tags:
        href = tag.get("href", "")
        match = re.search(r"mailto:([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", href)
        if match:
            email_set.add(match.group(1).strip())

    email_matches = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", full_text)
    for email in email_matches:
        email_set.add(email.strip())

    info["emails"] = list(email_set) 

    phone_set = set()

    for a in soup.find_all("a"):
        text = a.get_text(" ", strip=True)
        phones = re.findall(r"(?:\+?\d[\d ]{6,}\d)|(?:0\d[\d ]{5,}\d)", text)
        for p in phones:
            phone_set.add(p.strip())

    phone_matches = re.findall(r"\+?\d[\d ]{6,}\d(?!\s*0\d{5,})", full_text)
    for number in phone_matches:
        phone_set.add(number.strip())

    info["phones"] = list(phone_set) 
                  
    whatsapp_set = set()
    whatsapp_tags = soup.find_all("a", href=re.compile(r"whatsapp.com/send|wa\.me"))

    for tag in whatsapp_tags:
        href = tag.get("href", "")

        wa_direct = re.search(r"wa\.me/(\d+)", href)
        if wa_direct:
            whatsapp_set.add(wa_direct.group(1))
            continue

        match = re.search(r"phone=([^&]+)", href)
        if match:
            number = match.group(1).replace("%2B", "+").strip()
            whatsapp_set.add(number)

        info["whatsapp_num"] = list(whatsapp_set) 

    social_section = soup.find_all("a")

    for a in social_section:
        href = a.get("href", "").lower()
    
        if not href:
            continue

        if "instagram.com" in href:
            info["social_media"].append({"name": "instagram", "link": href})
        elif "facebook.com" in href:
            info["social_media"].append({"name": "facebook", "link": href})
        elif "twitter.com" in href or "x.com" in href:
            info["social_media"].append({"name": "twitter", "link": href})
        elif "linkedin.com" in href:
            info["social_media"].append({"name": "linkedin", "link": href})
        elif "youtube.com" in href:
            info["social_media"].append({"name": "youtube", "link": href})

    return info