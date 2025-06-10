# src/analyzers/availability.py

import whois
from typing import List, Tuple
import time

def check_single_domain(domain: str) -> Tuple[str, bool]:
    """
    Checks if a single domain is available.
    Returns the domain and a boolean indicating availability.
    Includes retry logic for network errors.
    """
    retries = 3
    for i in range(retries):
        try:
            w = whois.whois(domain)
            if not w.status or not w.expiration_date:
                return domain, True # Available
            return domain, False # Taken
        except whois.parser.PywhoisError:
            # No WHOIS record often means available for gTLDs
            return domain, True # Available
        except Exception:
            # Catch other exceptions, likely network-related
            if i < retries - 1:
                wait = 2**i # Exponential backoff: 1, 2 seconds
                time.sleep(wait)
                continue
            else:
                # All retries failed, assume taken or problematic
                return domain, False
    return domain, False # Fallback

def check_domain_availability(domains: List[str]) -> List[str]:
    """
    DEPRECATED: This function is kept for compatibility but the main logic
    should use check_single_domain with a ThreadPoolExecutor.
    """
    available_domains = []
    for domain in domains:
        domain_name, is_available = check_single_domain(domain)
        if is_available:
            print(f"[AVAILABLE] {domain_name}")
            available_domains.append(domain_name)
        else:
            print(f"[TAKEN] {domain_name}")
            
    return available_domains

if __name__ == '__main__':
    # A list of example domains to check
    test_domains = [
        'google.com', 
        'thisisdefinitelyanavailabledomain12345.com',
        'another-random-available-domain-xyz.io',
        'facebook.ai'
    ]
    print(f"Checking availability for {len(test_domains)} domains...")
    
    available = check_domain_availability(test_domains)
    
    print("\n--- Results ---")
    if available:
        print("Available domains found:")
        for domain in available:
            print(f"- {domain}")
    else:
        print("No available domains found in the test list.") 