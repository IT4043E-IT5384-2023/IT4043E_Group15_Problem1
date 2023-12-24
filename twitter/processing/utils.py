import pycountry_convert as pc
from ..config import MISSING_CN_TO_CNT

def country_to_continent(country_name: str) -> str:
    try:
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
        return country_continent_name
    except:
        if country_name in ["Europe", "Africa", "Antarctica"]:
            return country_name
        elif country_name in MISSING_CN_TO_CNT:
            return MISSING_CN_TO_CNT[country_name]