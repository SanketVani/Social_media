from bs4 import BeautifulSoup
import json
import re

def parse_facebook(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")

    info = {
    "title": "","intro": "","likes": "","followers": "","address": "","website": "","instagram": "","category": "","phones": "","emails":""
    }

    name_tag = soup.find("h1", class_="html-h1")
    if name_tag:
        info["title"] = name_tag.get_text(strip=True)

    intro_tag = soup.find(
        ["span", "p", "div"],
        text=re.compile(r"(business|company|service|store|organisation|community|students)", re.I)
    )
    if intro_tag:
        info["intro"] = intro_tag.get_text(strip=True)

    page_tag = soup.find(
        lambda tag:
            tag.name in [ "span", "a"] and
            tag.get_text(strip=True).lower().startswith("page")
    )
    if page_tag:
        info["category"] = page_tag.get_text(strip=True)

    address_tag = soup.find("div", role="button", string=re.compile(""))
    if address_tag:
        info["address"] = address_tag.get_text(strip=True)

    text = soup.get_text(" ", strip=True)

    phone_match = re.search(r"(\+?\d[\d\s\-\(\)]{7,}\d)", text)
    if phone_match:
        phone = phone_match.group()
        phone = re.sub(r"[^\d+]", "", phone) 
        info["phones"] = phone

    email_tag = soup.find("span", dir="auto", string=re.compile("@"))
    if email_tag:
        info["emails"] = email_tag.get_text(strip=True)

    ig_tag = soup.find("a", href=re.compile("instagram"))
    if ig_tag:
        info["instagram"] = ig_tag.get("href")

    web_tag = soup.find("a",href=re.compile(""))
    if web_tag: 
        info["website"] = web_tag.get("href")

    for a in soup.find_all("a"):
        txt = a.get_text(" ", strip=True)

        like_match = re.search(r"(\d[\d,]*)\s*likes", txt, re.IGNORECASE)
        if like_match:
            info["likes"] = like_match.group(1).strip()

        fol_match = re.search(r"(\d[\d,\.]*\s*[kKmM]?)\s*followers", txt, re.IGNORECASE)
        if fol_match:
            info["followers"] = fol_match.group(1).strip()

    return info