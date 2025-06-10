# src/parsers/expired_domains_parser.py

import requests
from bs4 import BeautifulSoup

def get_expired_domains():
    """
    Parses ExpiredDomains.net to get a list of recently expired or deleted domains.
    
    NOTE: This is a basic implementation for demonstration.
    Scraping websites can be against their terms of service.
    A more robust solution would use an official API if available.
    """
    
    # This URL is for .com domains deleted and available for registration
    url = "https://www.expireddomains.net/deleted-com-domains/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Raise an exception for bad status codes
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the table containing the domains
        # The exact selectors might change if the website layout changes
        domain_table = soup.find('table', {'class': 'base1'})
        
        if not domain_table:
            print("Could not find the domain table on the page.")
            return []
            
        domains = []
        # Find all 'a' tags that are links to domain details
        for link in domain_table.find_all('a', title=True):
            domain_name = link.text
            if '.' in domain_name: # Basic check to see if it's a domain
                domains.append(domain_name)
                
        return domains
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return []

if __name__ == '__main__':
    print("Fetching expired .com domains...")
    expired_domains = get_expired_domains()
    if expired_domains:
        print(f"Found {len(expired_domains)} domains.")
        # Print the first 10 for a sample
        for domain in expired_domains[:10]:
            print(domain)
    else:
        print("No domains found or an error occurred.") 