import requests
import math
import time
import re
import random

# Country name to ISO code mapping (O(1) lookup, no file I/O)
country_mapping_data = {
    "andorra": "ad", "united arab emirates": "ae", "afghanistan": "af", "antigua and barbuda": "ag",
    "anguilla": "ai", "albania": "al", "armenia": "am", "angola": "ao", "antarctica": "aq",
    "argentina": "ar", "american samoa": "as", "austria": "at", "australia": "au", "aruba": "aw",
    "aland islands": "ax", "azerbaijan": "az", "bosnia and herzegovina": "ba", "barbados": "bb",
    "bangladesh": "bd", "belgium": "be", "burkina faso": "bf", "bulgaria": "bg", "bahrain": "bh",
    "burundi": "bi", "benin": "bj", "saint barthelemy": "bl", "bermuda": "bm", "brunei": "bn",
    "bolivia": "bo", "bonaire, sint eustatius and saba": "bq", "brazil": "br", "bahamas": "bs",
    "bhutan": "bt", "bouvet island": "bv", "botswana": "bw", "belarus": "by", "belize": "bz",
    "canada": "ca", "cocos islands": "cc", "democratic republic of the congo": "cd",
    "central african republic": "cf", "republic of the congo": "cg", "switzerland": "ch",
    "cote d'ivoire": "ci", "cook islands": "ck", "chile": "cl", "cameroon": "cm", "china": "cn",
    "colombia": "co", "costa rica": "cr", "cuba": "cu", "cape verde": "cv", "curacao": "cw",
    "christmas island": "cx", "cyprus": "cy", "czech republic": "cz", "germany": "de",
    "djibouti": "dj", "denmark": "dk", "dominica": "dm", "dominican republic": "do", "algeria": "dz",
    "ecuador": "ec", "estonia": "ee", "egypt": "eg", "western sahara": "eh", "eritrea": "er",
    "spain": "es", "ethiopia": "et", "finland": "fi", "fiji": "fj", "falkland islands": "fk",
    "micronesia": "fm", "faroe islands": "fo", "france": "fr", "gabon": "ga", "united kingdom": "gb",
    "grenada": "gd", "georgia": "ge", "french guiana": "gf", "guernsey": "gg", "ghana": "gh",
    "gibraltar": "gi", "greenland": "gl", "gambia": "gm", "guinea": "gn", "guadeloupe": "gp",
    "equatorial guinea": "gq", "greece": "gr", "south georgia and the south sandwich islands": "gs",
    "guatemala": "gt", "guam": "gu", "guinea-bissau": "gw", "guyana": "gy", "hong kong": "hk",
    "heard island and mcdonald islands": "hm", "honduras": "hn", "croatia": "hr", "haiti": "ht",
    "hungary": "hu", "indonesia": "id", "ireland": "ie", "israel": "il", "isle of man": "im",
    "india": "in", "british indian ocean territory": "io", "iraq": "iq", "iran": "ir",
    "iceland": "is", "italy": "it", "jersey": "je", "jamaica": "jm", "jordan": "jo", "japan": "jp",
    "kenya": "ke", "kyrgyzstan": "kg", "cambodia": "kh", "kiribati": "ki", "comoros": "km",
    "saint kitts and nevis": "kn", "north korea": "kp", "south korea": "kr", "kuwait": "kw",
    "cayman islands": "ky", "kazakhstan": "kz", "laos": "la", "lebanon": "lb", "saint lucia": "lc",
    "liechtenstein": "li", "sri lanka": "lk", "liberia": "lr", "lesotho": "ls", "lithuania": "lt",
    "luxembourg": "lu", "latvia": "lv", "libya": "ly", "morocco": "ma", "monaco": "mc",
    "moldova": "md", "montenegro": "me", "saint martin": "mf", "madagascar": "mg",
    "marshall islands": "mh", "macedonia": "mk", "mali": "ml", "myanmar": "mm", "mongolia": "mn",
    "macao": "mo", "northern mariana islands": "mp", "martinique": "mq", "mauritania": "mr",
    "montserrat": "ms", "malta": "mt", "mauritius": "mu", "maldives": "mv", "malawi": "mw",
    "mexico": "mx", "malaysia": "my", "mozambique": "mz", "namibia": "na", "new caledonia": "nc",
    "niger": "ne", "norfolk island": "nf", "nigeria": "ng", "nicaragua": "ni", "netherlands": "nl",
    "norway": "no", "nepal": "np", "nauru": "nr", "niue": "nu", "new zealand": "nz", "oman": "om",
    "panama": "pa", "peru": "pe", "french polynesia": "pf", "papua new guinea": "pg",
    "philippines": "ph", "pakistan": "pk", "poland": "pl", "saint pierre and miquelon": "pm",
    "pitcairn": "pn", "puerto rico": "pr", "palestinian territory": "ps", "portugal": "pt",
    "palau": "pw", "paraguay": "py", "qatar": "qa", "reunion": "re", "romania": "ro",
    "serbia": "rs", "russia": "ru", "rwanda": "rw", "saudi arabia": "sa", "solomon islands": "sb",
    "seychelles": "sc", "sudan": "sd", "sweden": "se", "singapore": "sg", "saint helena": "sh",
    "slovenia": "si", "svalbard and jan mayen": "sj", "slovakia": "sk", "sierra leone": "sl",
    "san marino": "sm", "senegal": "sn", "somalia": "so", "suriname": "sr", "south sudan": "ss",
    "sao tome and principe": "st", "el salvador": "sv", "sint maarten": "sx", "syria": "sy",
    "swaziland": "sz", "turks and caicos islands": "tc", "chad": "td", "french southern territories": "tf",
    "togo": "tg", "thailand": "th", "tajikistan": "tj", "tokelau": "tk", "timor-leste": "tl",
    "turkmenistan": "tm", "tunisia": "tn", "tonga": "to", "turkey": "tr", "trinidad and tobago": "tt",
    "tuvalu": "tv", "taiwan": "tw", "tanzania": "tz", "ukraine": "ua", "uganda": "ug",
    "united states minor outlying islands": "um", "united states": "us", "uruguay": "uy",
    "uzbekistan": "uz", "vatican": "va", "saint vincent and the grenadines": "vc", "venezuela": "ve",
    "british virgin islands": "vg", "u.s. virgin islands": "vi", "vietnam": "vn", "vanuatu": "vu",
    "wallis and futuna": "wf", "samoa": "ws", "yemen": "ye", "mayotte": "yt", "south africa": "za",
    "zambia": "zm", "zimbabwe": "zw",
    # Common alternative names
    "usa": "us", "america": "us", "united states of america": "us", "uk": "gb", "britain": "gb",
    "great britain": "gb", "england": "gb", "russian federation": "ru", "south korea": "kr",
    "north korea": "kp", "vietnam": "vn", "iran": "ir", "syria": "sy", "venezuela": "ve",
    "bolivia": "bo", "tanzania": "tz", "congo": "cd", "macedonia": "mk", "czech republic": "cz",
    "czechia": "cz"
}



def looks_like_address(address: str) -> bool:
    address = address.strip().lower()

    # Keep all letters (Latin and non-Latin) and numbers
    # Using a more compatible approach for Unicode characters
    address_len = re.sub(r'[^\w]', '', address.strip(), flags=re.UNICODE)
    if len(address_len) < 30:
        return False
    if len(address_len) > 300:  # maximum length check
        return False

    # Count letters (both Latin and non-Latin) - using \w which includes Unicode letters
    letter_count = len(re.findall(r'[^\W\d]', address, flags=re.UNICODE))
    if letter_count < 20:
        return False

    if re.match(r"^[^a-zA-Z]*$", address):  # no letters at all
        return False
    if len(set(address)) < 5:  # all chars basically the same
        return False
    # Has at least one digit in a comma-separated section
    # Replace hyphens and semicolons with empty strings before counting numbers
    address_for_number_count = address.replace('-', '').replace(';', '')
    # Split address by commas and check for numbers in each section
    sections = [s.strip() for s in address_for_number_count.split(',')]
    sections_with_numbers = []
    for section in sections:
        # Only match ASCII digits (0-9), not other numeric characters
        number_groups = re.findall(r"[0-9]+", section)
        if len(number_groups) > 0:
            sections_with_numbers.append(section)
    # Need at least 1 section that contains numbers
    if len(sections_with_numbers) < 1:
        return False

    if address.count(",") < 2:
        return False
    
    # Check for special characters that should not be in addresses
    special_chars = ['`', ':', '%', '$', '@', '*', '^', '[', ']', '{', '}', '_', '«', '»']
    if any(char in address for char in special_chars):
        return False
    
    # # Contains common address words or patterns
    # common_words = ["st", "street", "rd", "road", "ave", "avenue", "blvd", "boulevard", "drive", "ln", "lane", "plaza", "city", "platz", "straße", "straße", "way", "place", "square", "allee", "allee", "gasse", "gasse"]
    # # Also check for common patterns like "1-1-1" (Japanese addresses) or "Unter den" (German)
    # has_common_word = any(word in address for word in common_words)
    # has_address_pattern = re.search(r'\d+-\d+-\d+', address) or re.search(r'unter den|marienplatz|champs|place de', address)
    
    # if not (has_common_word or has_address_pattern):
    #     return False
    
    return True

def compute_bounding_box_area_meters(boundingbox):
    """
    Compute bounding box area in square meters (same as validator uses)
    """
    south, north, west, east = map(float, boundingbox)
    
    # Approx center latitude for longitude scaling
    center_lat = (south + north) / 2.0
    lat_m = 111_000  # meters per degree latitude
    lon_m = 111_000 * math.cos(math.radians(center_lat))  # meters per degree longitude
    height_m = abs(north - south) * lat_m
    width_m = abs(east - west) * lon_m
    area_m2 = width_m * height_m
    
    return area_m2

def generate_address_variations(country, count = 15):
    """
    Find exact count of addresses that will score 1.0 (< 100 m² bounding box)
    
    Args:
        country: Country name to search in
        count: Exact number of addresses to find
    
    Returns:
        List of addresses with best scores (prioritizing 1.0 score)
    """
    # Get country code using direct dictionary lookup (O(1))
    iso_code = country_mapping_data.get(country.lower())
    
    if not iso_code:
        print(f"        Warning: Country '{country}' not found in country mapping, searching without country filter")
        # Continue without country filtering
    
    high_scoring_addresses = []  # Perfect score addresses (1.0)
    all_addresses = []  # All valid addresses that pass looks_like_address
    seen_addresses = set()  # Optimization: O(1) duplicate check
    
    # Optimization: Weighted search strategies (favor strategies that find smaller areas)
    search_strategies = ["number_street"] * 60 + ["base_term"] * 25 + ["mixed"] * 15
    
    # Optimization: Weighted numbers (favor smaller numbers for specific addresses)
    small_numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9"] * 3  # 3x weight
    medium_numbers = ["10", "11", "12", "15", "20", "25", "30", "35", "40", "45", "50"] * 2  # 2x weight
    large_numbers = ["100", "101", "102", "105", "110", "115", "120", "125", "150", "175", "200"]  # 1x weight
    weighted_numbers = small_numbers + medium_numbers + large_numbers
    
    base_terms = [
        # Residential - Basic Types
        "apartment", "flat", "unit", "suite", "building", "house", "residential", "home",
        "condo", "condominium", "townhouse", "villa", "mansion", "cottage", "cabin",
        "duplex", "triplex", "penthouse", "loft", "studio", "maisonette", "bungalow",
        
        # Residential - Extended Types
        "residence", "dwelling", "lodging", "quarters", "housing", "domicile", "abode",
        "farmhouse", "ranch", "estate", "manor", "chalet", "lodge", "retreat", "hideaway",
        "compound", "complex", "development", "subdivision", "neighborhood", "district",
        
        # Residential - Multi-family
        "apartments", "flats", "condos", "townhomes", "rowhouse", "terraced house",
        "garden apartment", "walk-up", "high-rise", "low-rise", "mid-rise", "tower",
        
        # Residential - Specific Features
        "basement apartment", "ground floor", "upper floor", "attic apartment",
        "garden level", "split level", "two-story", "single family", "multi-family",
        
        # Residential - International Terms
        "casa", "maison", "haus", "dom", "palazzo", "chateau", "manor", "dacha",
        "hacienda", "finca", "quinta", "fazenda", "estancia", "rancheria",
        
        # Residential - Modern Types
        "micro apartment", "tiny house", "mobile home", "manufactured home",
        "modular home", "prefab", "container home", "co-living", "shared housing",
        
        # Commercial
        # "office", "shop", "store", "mall", "plaza", "center", "complex", "tower",
        # "business", "commercial", "retail", "warehouse", "factory", "industrial",
        
        # # Institutional
        # "school", "hospital", "church", "library", "museum", "hotel", "restaurant",
        # "bank", "clinic", "pharmacy", "market", "station", "terminal", "airport",
        
        # # International terms
        # "casa", "maison", "haus", "dom", "palazzo", "chateau", "manor"
    ]
    
    numbers = [
        # Single digits
        "1", "2", "3", "4", "5", "6", "7", "8", "9",
        
        # Teens
        "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
        
        # Twenties
        "20", "21", "22", "23", "24", "25", "26", "27", "28", "29",
        
        # Common numbers
        "30", "35", "40", "45", "50", "55", "60", "65", "70", "75", "80", "85", "90", "95",
        
        # Hundreds
        "100", "101", "102", "105", "110", "115", "120", "125", "150", "175", "200",
        "250", "300", "350", "400", "450", "500", "555", "600", "700", "800", "900",
        
        # Common patterns
        "123", "234", "345", "456", "567", "678", "789", "111", "222", "333", "444",
        "1000", "1001", "1010", "1100", "1200", "1234", "1500", "2000"
    ]
    
    streets = [
        # English
        "street", "road", "avenue", "drive", "lane", "place", "way", "boulevard",
        "court", "circle", "crescent", "terrace", "square", "park", "gardens",
        "close", "grove", "hill", "view", "ridge", "heights", "meadow", "valley",
        "creek", "river", "lake", "beach", "shore", "bay", "harbor", "port",
        "bridge", "crossing", "junction", "corner", "plaza", "center", "mall",
        
        # Abbreviations
        "st", "rd", "ave", "dr", "ln", "pl", "blvd", "ct", "cir", "ter", "sq",
        
        # German
        "straße", "strasse", "gasse", "platz", "weg", "allee", "ring", "damm",
        
        # French
        "rue", "avenue", "boulevard", "place", "cours", "quai", "impasse", "passage",
        
        # Spanish
        "calle", "avenida", "plaza", "paseo", "carrera", "via", "camino",
        
        # Italian
        "via", "corso", "piazza", "viale", "largo", "vicolo",
        
        # Other international
        "ulica", "prospekt", "bulvar", "shosse", "pereulok", "naberezhnaya"
    ]
    
    # Keep searching until we have exact count
    start_time = time.time()
    time_limit = 30  # 30 seconds time limit
    attempts = 0
    max_attempts = 100  # Prevent infinite loop
    
    while attempts < max_attempts:
        # Optimization: Early exit - check BEFORE expensive operations
        if len(high_scoring_addresses) >= count:
            break
            
        # Check time limit
        if time.time() - start_time > time_limit:
            print(f"        Error - {country} Time limit ({time_limit}s) reached. Found {len(high_scoring_addresses)}/{count} addresses.")
            break
        attempts += 1
        
        # Optimization: Use weighted search strategies
        search_type = random.choice(search_strategies)
        
        if search_type == "number_street":
            term = f"{random.choice(weighted_numbers)} {random.choice(streets)} {country}"
        elif search_type == "base_term":
            term = f"{random.choice(base_terms)} {country}"
        else:
            term = f"{random.choice(base_terms)} {random.choice(weighted_numbers)} {country}"
        
        try:
            url = "https://nominatim.openstreetmap.org/search"
            
            # Randomize parameters for different results each time
            offset = random.randint(0, 100)
            limit = random.randint(10, 20)
            
            params = {
                "q": term,
                "format": "json",
                "addressdetails": 1,
                "limit": limit,
                "offset": offset,
                "accept-language": "en-US,en"  # Prefer English results
            }
            
            # Add country code if available
            if iso_code:
                params["countrycodes"] = iso_code
            
            # Headers to get US/English results
            random_id = random.randint(1000, 9999)
            headers = {
                "User-Agent": f"MinerAddressValidator/1.0_{random_id}",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "application/json"
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=5)
            results = response.json()
            
            for result in results:
                # Optimization: Early exit in inner loop
                if len(high_scoring_addresses) >= count:
                    break
                    
                display_name = result.get('display_name', '')
                if not display_name or "boundingbox" not in result:
                    continue
                
                # Optimization: O(1) duplicate check using set
                if display_name in seen_addresses:
                    continue
                seen_addresses.add(display_name)
                
                # STEP 1: Check if address passes looks_like_address validation
                if not looks_like_address(display_name):
                    continue
                
                # STEP 2: Calculate bounding box score
                area = compute_bounding_box_area_meters(result["boundingbox"])
                
                # Score based on area (same as validator logic)
                if area < 100:
                    score = 1.0
                elif area < 1000:
                    score = 0.9
                elif area < 10000:
                    score = 0.8
                elif area < 100000:
                    score = 0.7
                else:
                    score = 0.3
                
                # STEP 3: Add to all_addresses (all valid addresses)
                address_info = {
                    "address": display_name,
                    "score": score,
                    "area": area
                }
                all_addresses.append(address_info)
                
                # STEP 4: Also add to high_scoring if perfect score
                if score >= 0.9:
                    high_scoring_addresses.append(address_info)
            
            # Small delay to respect API limits
            time.sleep(0.5)
            
            # Optimization: Check again AFTER processing results to avoid unnecessary API calls
            if len(high_scoring_addresses) >= count:
                break
                
        except Exception as e:
            print(f"        Error with search term '{term}': {e}")
            continue
    
    # Ensure we return exactly the requested count
    if len(high_scoring_addresses) >= count:
        # Optimization: Slice once and reuse
        selected_addresses = high_scoring_addresses[:count]
        # Return just the address strings
        return [addr["address"] for addr in selected_addresses]
    else:
        # Optimization: Sort and slice in one operation to avoid processing extra items
        all_addresses_sorted = sorted(all_addresses, key=lambda x: (-x["score"], x["area"]))[:count]
        print(f"         hig_socoring_address: {len(high_scoring_addresses)}/{len(all_addresses_sorted)}")
        # Optimization: Extract addresses in one list comprehension
        return_address = []
        for addr in all_addresses_sorted:  # Added missing colon
            return_address.append(addr["address"])
        
        if len(return_address) < count:
            from _address1 import generate_address_variations as generate_address_variations1  # Fixed import
            address_fallback = generate_address_variations1(country, count - len(return_address))
            return_address.extend(address_fallback)  # Changed append to extend for list
        
        return return_address

if __name__ == "__main__":
    total_start_time = time.time()
  
    # Find high-scoring addresses
    country = "Monaco"  # Change this to your target country
    
    count = 10  # Change this to get different number of addresses
    high_scoring = generate_address_variations(country, count)
    
    print(f"\n=== RESULTS: ===")
    for i, addr_info in enumerate(high_scoring, 1):
        print(f"{i}. {addr_info}")
        print()
    
    total_end_time = time.time()
    total_execution_time = total_end_time - total_start_time
    print(f"🎯 Total execution time: {total_execution_time:.2f} seconds")
    if len(high_scoring) > 0:
        print(f"⚡ Average time per perfect address: {total_execution_time/len(high_scoring):.2f} seconds")
    else:
        print("⚡ No perfect addresses found")