# domainscanner/generators/dictionary_generator.py

from .. import config

def generate_dictionary_domains():
    """
    Generates domain names by taking words from a dictionary file.
    """
    try:
        with open(config.DICTIONARY_FILE, 'r') as f:
            words = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print(f"Error: Dictionary file not found at {config.DICTIONARY_FILE}")
        return []

    generated_domains = []
    for word in words:
        for tld in config.DEFAULT_TLDS:
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