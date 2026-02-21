from parsers.facebook import parse_facebook
from parsers.youtube import parse_youtube
from parsers.linkedin import parse_linkedin
from parsers.instagram import parse_instagram
from parsers.website import parse_website
from parsers.google_search import parse_google_search
from parsers.bing_search import parse_bing_search
from parsers.duck_go_search import parse_duck_go_search
from parsers.google_map import parse_google_map
from parsers.gst_google import parse_gst_google
from parsers.gst_bing import parse_gst_bing
from parsers.gst_duckgo import parse_gst_duckgo
from parsers.metaad import parse_metaad
from parsers.twitter import parse_twitter
from parsers.pinterest import parse_pinterest
from parsers.nextdoor import parse_nextdoor

PARSER_REGISTRY = {
    "facebook": parse_facebook,
    "youtube": parse_youtube,
    "linkedin": parse_linkedin,
    "instagram": parse_instagram,
    "website": parse_website,
    "google_search": parse_google_search,
    "bing_search": parse_bing_search,
    "duck_go_search": parse_duck_go_search,
    "google_map": parse_google_map,
    "gst_google": parse_gst_google,
    "gst_bing": parse_gst_bing,
    "gst_duckgo": parse_gst_duckgo,
    "metaad": parse_metaad,
    "twitter": parse_twitter,
    "pinterest": parse_pinterest,
    "nextdoor": parse_nextdoor,        
}

def get_parser(platform: str):
    platform = platform.lower()
    if platform not in PARSER_REGISTRY:
        raise ValueError(f"Parser not found for platform: {platform}")
    return PARSER_REGISTRY[platform]