from bs4 import BeautifulSoup
import json
import re

def parse_youtube(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")

    info = {
    "title": "","sub_title": "","about":"","subscribers": "","views": "","videos": "","country": "","phones": "","emails": "","website": "","joined":"","social_media":[]
    }

    title_tag= soup.find("h1",class_="dynamicTextViewModelH1")
    if title_tag:
        info["title"] = title_tag.get_text(strip=True)

    sub_title_tag = None
    for span in soup.find_all("span", class_="yt-core-attributed-string--link-inherit-color"):
        if span.text.strip().startswith("@"):
            sub_title_tag = span.text.strip()
            break

    if sub_title_tag:
        info["sub_title"] = sub_title_tag

    about_tag = soup.find(id="description-container") or soup.find(id="message")
    if about_tag:
        info["about"] = about_tag.get_text(" ", strip=True)

    country_tag = soup.find("td", string=re.compile(r"United States|USA|India|UK|Canada|Australia|Philippines|UAE", re.I))
    if country_tag:
        info["country"] = country_tag.get_text(strip=True)

    joined_text = soup.find(string=re.compile(r"Joined", re.I))
    if joined_text:
        info["joined"] = joined_text.strip()

    social_section = soup.find("div",id="link-list-container")

    if social_section:
        for a in social_section.find_all("a"):
            link = a.get_text(strip=True) 
            if not link:
                continue

            if link.startswith("instagram.com") or "instagram.com" in link.lower():
                info["social_media"].append({"name": "instagram", "link": "https://" + link})
            elif link.startswith("facebook.com") or "facebook.com" in link.lower():
                info["social_media"].append({"name": "facebook", "link": "https://" + link})
            elif "whatsapp" in link.lower():
                info["social_media"].append({"name": "whatsapp", "link": link})

    full_text = soup.get_text(" ", strip=True)

    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", full_text)
    if email_match:
        info["emails"] = email_match.group()

    for a in soup.find_all("a"):
        website_match = a.get_text(" ",strip=True)

        website_match = re.search(r"(https?://[^\s]+|www\.[^\s]+)", full_text)
        if website_match:
            info["website"] = website_match.group()

    text = soup.get_text(" ", strip=True)
    phone_match = re.search(r"\b\d{10,15}\b", text)

    if phone_match:
        info["phones"] = phone_match.group()

    for a in soup.find_all("div"):
        txt = a.get_text(" ", strip=True)

        subscribers_match = re.search(r"(\d[\d,\.]*\s*[kKmM]?)\s*subscribers", txt, re.IGNORECASE)
        if subscribers_match:
            info["subscribers"] = subscribers_match.group(1).strip()

        views_match = re.search(r"(\d[\d,\.]*\s*[kKmM]?)\s*views", txt, re.IGNORECASE)
        if views_match:
            info["views"] = views_match.group(1).strip()

        video_match = re.search(r"(\d[\d,\.]*\s*[kKmM]?)\s*videos", txt, re.IGNORECASE)
        if video_match:
            info["videos"] = video_match.group(1).strip()

    return info