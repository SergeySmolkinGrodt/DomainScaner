# domainscanner/generators/news_generator.py
import requests
import re
from typing import List
import nltk
from bs4 import BeautifulSoup

from .. import config

# Download necessary NLTK data (only if not already present)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    print("Downloading NLTK stopwords...")
    nltk.download('stopwords')

from nltk.corpus import stopwords

def _get_news_headlines(rss_url: str) -> List[str]:
    """Fetches headlines from an RSS feed."""
    headlines = []
    try:
        response = requests.get(rss_url, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'xml')
        # RSS <item> tags contain news articles, <title> has the headline
        items = soup.find_all('item')
        for item in items:
            title = item.find('title')
            if title:
                headlines.append(title.text)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news from {rss_url}: {e}")
    return headlines

def _extract_keywords(headlines: List[str]) -> List[str]:
    """Extracts meaningful keywords from a list of headlines."""
    stop_words = set(stopwords.words('english'))
    keywords = set()
    
    for title in headlines:
        # Remove non-alphanumeric characters and split into words
        words = re.findall(r'\b\w+\b', title.lower())
        # Filter out short words, numbers, and stopwords
        for word in words:
            if word not in stop_words and len(word) > 3 and not word.isdigit():
                keywords.add(word)
                
    return list(keywords)

def generate_news_based_domains() -> List[str]:
    """
    Generates domain names from keywords found in recent news headlines.
    """
    all_keywords = []
    for source_url in config.NEWS_SOURCES:
        headlines = _get_news_headlines(source_url)
        keywords = _extract_keywords(headlines)
        all_keywords.extend(keywords)

    if not all_keywords:
        return []

    # Use the same suffixes as the trend generator for consistency
    suffixes = ['solutions', 'labs', 'future', 'systems', 'tech', 'works', 'group', 'ventures']
    
    generated_domains = []
    for keyword in set(all_keywords): # Use set to avoid duplicate keywords
        for suffix in suffixes:
            base_name = f"{keyword}{suffix}"
            for tld in config.DEFAULT_TLDS:
                generated_domains.append(f"{base_name}{tld}")
    
    return generated_domains

if __name__ == '__main__':
    print("Generating domains from news headlines...")
    domains = generate_news_based_domains()
    if domains:
        print(f"Generated {len(domains)} domains.")
        # Print a sample
        for domain in domains[:20]:
            print(domain)
    else:
        print("No domains generated or an error occurred.") 