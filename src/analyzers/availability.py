# src/analyzers/availability.py

import whois
from typing import List

def check_domain_availability(domains: List[str]):
    """
    Checks the availability of a list of domains.
    
    Args:
        domains: A list of domain names to check.
        
    Returns:
        A list of available domain names.
    """
    available_domains = []
    for domain in domains:
        try:
            w = whois.whois(domain)
            # If the domain has no expiration date or status, it's likely available.
            # The logic might need to be adjusted based on the python-whois library's output for different TLDs.
            if not w.status or not w.expiration_date:
                print(f"[AVAILABLE] {domain}")
                available_domains.append(domain)
            else:
                print(f"[TAKEN] {domain}")

        except whois.parser.PywhoisError as e:
            # This error often means the TLD is not supported or the domain does not exist.
            # We can often assume it's available, but it's safer to log it.
            print(f"[AVAILABLE/UNKNOWN] {domain} (might be available, TLD not recognized by whois or other error: {e})")
            available_domains.append(domain)
        except Exception as e:
            print(f"Could not check domain {domain}. Error: {e}")
            
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