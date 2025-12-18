from parsers.facebook import parse_facebook
from parsers.youtube import parse_youtube
from parsers.linkedin import parse_linkedin
from parsers.instagram import parse_instagram
from parsers.website import parse_website
from parsers.google_search import parse_google_search
from parsers.bing_search import parse_bing_search
from parsers.duck_go_search import parse_duck_go_search

PARSER_REGISTRY = {
    "facebook": parse_facebook,
    "youtube": parse_youtube,
    "linkedin": parse_linkedin,
    "instagram": parse_instagram,
    "website": parse_website,
    "google_search": parse_google_search,
    "bing_search": parse_bing_search,
    "duck_go_search": parse_duck_go_search,
    
}

def get_parser(platform: str):
    platform = platform.lower()
    if platform not in PARSER_REGISTRY:
        raise ValueError(f"Parser not found for platform: {platform}")
    return PARSER_REGISTRY[platform]