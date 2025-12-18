from bs4 import BeautifulSoup
import json
import re

def parse_instagram(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")

    info = {
        "title": "","sub_title": "","about":"","posts": "","followers": "","following": "","address": "","category": "","phones": "","emails": "","website": ""
    }

    title_tag= soup.find("h2", dir="auto")
    if title_tag:
        info["title"] = title_tag.get_text(strip=True)

    sub_title_tag = soup.find("span",dir="auto",string=re.compile(""))
    if sub_title_tag:
        info["sub_title"] = sub_title_tag.get_text(strip=True)

    about_tag = soup.find("span", class_=re.compile("_ap3a"))
    if about_tag:
        info["about"] = about_tag.get_text(" ", strip=True)

    category_tag = soup.find("div",dir="auto")
    if category_tag:
        info["category"] = category_tag.get_text(strip=True)

    address_tag = soup.find("h1", dir="auto", string=re.compile(""))
    if address_tag:
        info["address"] = address_tag.get_text(strip=True)

    full_text = soup.get_text(" ", strip=True)

    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", full_text)
    if email_match:
        info["emails"] = email_match.group()

    website_match = re.search(r"(https?://[^\s]+|www\.[^\s]+)", full_text)
    if website_match:
        info["website"] = website_match.group()

    text = soup.get_text(" ", strip=True)
    phone_match = re.search(r"\b\d{10,15}\b", text)

    if phone_match:
        info["phones"] = phone_match.group()

    for a in soup.find_all("a"):
        txt = a.get_text(" ", strip=True)

        posts_match = re.search(r"(\d[\d,]*\s*[kKmM]?)\s*posts", txt, re.IGNORECASE)
        if posts_match:
            info["posts"] = posts_match.group(1).strip()

        fol_match = re.search(r"(\d[\d,\.]*\s*[kKmM]?)\s*followers", txt, re.IGNORECASE)
        if fol_match:
            info["followers"] = fol_match.group(1).strip()

        following_match = re.search(r"(\d[\d,\.]*\s*[kKmM]?)\s*following", txt, re.IGNORECASE)
        if following_match:
            info["following"] = following_match.group(1).strip()

    return info