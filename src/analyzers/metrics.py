# src/analyzers/metrics.py
import sys
import os
from typing import List

# Add the project root directory to the Python path to import 'config'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from config import MAX_DOMAIN_LENGTH

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
        if len(name_part) <= MAX_DOMAIN_LENGTH:
            short_domains.append(domain)
        else:
            print(f"[REJECTED - TOO LONG] {domain}")
            
    return short_domains

if __name__ == '__main__':
    test_domains = [
        'short.com',
        'averylongdomainnamethatistoolong.com',
        'mediumlength.io',
        'perfect.ai',
        'thisoneisjustontheedge.com' # 15 chars
    ]
    print(f"Filtering {len(test_domains)} domains by max length ({MAX_DOMAIN_LENGTH})...")
    
    filtered = filter_by_length(test_domains)
    
    print("\n--- Results ---")
    if filtered:
        print("Domains that passed the length check:")
        for domain in filtered:
            print(f"- {domain}")
    else:
        print("No domains passed the check.") 