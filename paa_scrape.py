import requests
import csv
from bs4 import BeautifulSoup
import time


# ============================
# 1. SEED KEYWORDS (ENGLISH)
# ============================
seed_keywords = [
    "presentation problems",
    "presentation issues",
    "presentation anxiety",
    "boring presentations",
    "poor slide design",
    "ineffective presentation",
    "confusing presentation",
    "public speaking fear",
    "how to improve presentations",
    "why my presentation fails"
]


# ============================
# 2. GOOGLE AUTOCOMPLETE
# ============================
def get_autocomplete(keyword):
    url = f"http://suggestqueries.google.com/complete/search?client=firefox&hl=en&q={keyword}"
    r = requests.get(url)
    try:
        return r.json()[1]
    except:
        return []


# ============================
# 3. PEOPLE ALSO ASK SCRAPER
# ============================
def get_paa(keyword):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://www.google.com/search?q={keyword}"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    paa_items = []
    for div in soup.find_all("div"):
        if div.get("jsname") == "Cpkphb":   # PAA question selector
            paa_items.append(div.get_text(strip=True))

    return paa_items


# ============================
# 4. RELATED SEARCHES
# ============================
def get_related_searches(keyword):
    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://www.google.com/search?q={keyword}"
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    related = []
    for a in soup.find_all("a"):
        if "/search?q=" in a.get("href", "") and "related" in a.text.lower():
            related.append(a.text)

    return related


# ============================
# 5. AUTO-CLUSTERING FUNCTION
# ============================
def auto_cluster(sentence):
    sentence = sentence.lower()

    if any(x in sentence for x in ["anxiety", "fear", "nervous", "stage fright"]):
        return "Psychological / Anxiety"
    if any(x in sentence for x in ["design", "slides", "visual", "graphics"]):
        return "Slide Design Problems"
    if any(x in sentence for x in ["engage", "boring", "attention"]):
        return "Audience Engagement"
    if any(x in sentence for x in ["structure", "flow", "confusing"]):
        return "Content Structure"
    if any(x in sentence for x in ["presenter", "delivery", "voice"]):
        return "Delivery Technique"
    if any(x in sentence for x in ["tool", "software", "technical", "export", "ppt"]):
        return "Technical Problems"

    return "Other"


# ============================
# 6. MAIN SCRIPT
# ============================
results = []

print("🚀 Starting super keyword scraper...\n")

for keyword in seed_keywords:

    print(f"🔎 Processing: {keyword}")

    # Autocomplete
    ac = get_autocomplete(keyword)

    # People Also Ask
    paa = get_paa(keyword)

    # Related Searches
    related = get_related_searches(keyword)

    # Combine all
    for item in ac:
        results.append([keyword, item, "autocomplete", auto_cluster(item)])
    for item in paa:
        results.append([keyword, item, "people_also_ask", auto_cluster(item)])
    for item in related:
        results.append([keyword, item, "related_search", auto_cluster(item)])

    time.sleep(1)  # avoid Google blocking


# ============================
# 7. SAVE TO CSV
# ============================
with open("presentation_keyword_research.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["seed_keyword", "query", "source", "cluster"])
    writer.writerows(results)

print("\n✅ DONE! File saved as: presentation_keyword_research.csv")





