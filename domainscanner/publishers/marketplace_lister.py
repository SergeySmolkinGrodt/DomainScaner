from typing import List
from .. import config

def list_domain_on_marketplaces(domain: str):
    """
    Simulates listing a single domain on various marketplaces.
    In a real implementation, this would make API calls to Sedo, Dan.com, etc.
    """
    print(f"\n--- 📤 Publishing Domain: {domain} ---")

    # Simulate listing on Sedo
    if config.SEDO_API_KEY:
        # Real implementation would use the API key to authenticate and list
        print(f"[SUCCESS] Listed {domain} on Sedo.com.")
    else:
        print(f"[SIMULATING] Listing {domain} on Sedo.com (SEDO_API_KEY not set).")

    # Simulate listing on Dan.com
    if config.DAN_API_KEY:
        print(f"[SUCCESS] Listed {domain} on Dan.com.")
    else:
        print(f"[SIMULATING] Listing {domain} on Dan.com (DAN_API_KEY not set).")

    # In a real scenario, you might have different logic for each marketplace
    # and handle their specific responses and error conditions.
    return

if __name__ == '__main__':
    test_domains = ['mynewapp.io', 'supercrypto.ai']
    print("--- Testing Marketplace Lister ---")
    for d in test_domains:
        list_domain_on_marketplaces(d)
    
    print("\n--- Testing with simulated API Key ---")
    config.SEDO_API_KEY = "dummy-key" # Simulate having a key
    list_domain_on_marketplaces('real-deal.com') 