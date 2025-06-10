# src/analyzers/metrics.py
import sys
import os
from typing import List, Tuple
import requests
import time

from .. import config

def filter_by_length(domains: List[str]) -> List[str]:
    """
    Filters a list of domains, keeping only those with a name length
    less than or equal to MAX_DOMAIN_LENGTH.
    
    Args:
        domains: A list of domain names.
        
    Returns:
        A list of domains that pass the length check.
    """
    short_domains = []
    for domain in domains:
        # Get the name part of the domain, e.g., 'google' from 'google.com'
        name_part = domain.split('.')[0]
        if len(name_part) <= config.MAX_DOMAIN_LENGTH:
            short_domains.append(domain)
        else:
            print(f"[REJECTED - TOO LONG] {domain}")
            
    return short_domains

def check_single_domain_history(domain: str) -> Tuple[str, bool]:
    """
    Checks a single domain against the Wayback Machine API.
    Returns the domain and a boolean indicating if it has history.
    """
    retries = 3
    for i in range(retries):
        try:
            api_url = f"http://archive.org/wayback/available?url={domain}"
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            # Use .get() to avoid error if key is missing
            if not data.get('archived_snapshots'):
                return domain, False # No history
            return domain, True # Has history
                
        except (requests.exceptions.RequestException, KeyError, ValueError):
            if i < retries - 1:
                wait = (i + 1) * 2 # Exponential backoff: 2, 4 seconds
                time.sleep(wait)
                continue
            else:
                # If all retries fail, assume it has history to be safe
                return domain, True
    return domain, True # Fallback

def filter_clean_history_domains(domains: List[str]) -> List[str]:
    """
    DEPRECATED: This function is kept for compatibility but the main logic
    should use check_single_domain_history with a ThreadPoolExecutor.
    """
    clean_domains = []
    print("Checking domain history (this may take a while)...")
    for domain in domains:
        domain_name, has_history = check_single_domain_history(domain)
        if not has_history:
            print(f"[CLEAN HISTORY] {domain_name}")
            clean_domains.append(domain_name)
        else:
            print(f"[HISTORY FOUND] {domain_name}")
        time.sleep(1) # Be respectful to the API
            
    return clean_domains

if __name__ == '__main__':
    # --- Length Check Test ---
    test_domains_length = [
        'short.com',
        'averylongdomainnamethatistoolong.com',
        'mediumlength.io',
        'perfect.ai',
        'thisoneisjustontheedge.com' # 15 chars
    ]
    print(f"Filtering {len(test_domains_length)} domains by max length ({config.MAX_DOMAIN_LENGTH})...")
    
    filtered_length = filter_by_length(test_domains_length)
    
    print("\n--- Length Results ---")
    if filtered_length:
        print("Domains that passed the length check:")
        for domain in filtered_length:
            print(f"- {domain}")
    else:
        print("No domains passed the length check.")

    # --- History Check Test ---
    test_domains_history = [
        'google.com', # Has history
        'this-domain-surely-has-no-history-12345.com', # No history
        'github.com' # Has history
    ]
    print(f"\nFiltering {len(test_domains_history)} domains by history...")
    filtered_history = filter_clean_history_domains(test_domains_history)

    print("\n--- History Results ---")
    if filtered_history:
        print("Domains with a clean history:")
        for domain in filtered_history:
            print(f"- {domain}")
    else:
        print("No domains with a clean history were found.") 