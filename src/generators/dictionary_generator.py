# src/generators/dictionary_generator.py

import sys
import os

# Add the project root directory to the Python path to import 'config'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from config import DEFAULT_TLDS, DICTIONARY_FILE

def generate_dictionary_domains():
    """
    Generates domain names by taking words from a dictionary file.
    """
    try:
        with open(DICTIONARY_FILE, 'r') as f:
            words = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print(f"Error: Dictionary file not found at {DICTIONARY_FILE}")
        return []

    generated_domains = []
    for word in words:
        for tld in DEFAULT_TLDS:
            generated_domains.append(f"{word}{tld}")
    
    return generated_domains

if __name__ == '__main__':
    print("Generating domains from dictionary file...")
    domains = generate_dictionary_domains()
    if domains:
        print(f"Generated {len(domains)} domains.")
        # Print the first 10 for a sample
        for domain in domains[:10]:
            print(domain)
    else:
        print("No domains generated or an error occurred.") 