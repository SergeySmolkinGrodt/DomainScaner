# src/generators/trend_generator.py

from .. import config

def generate_trend_domains():
    """
    Generates domain names by combining trending keywords with common suffixes.
    """
    try:
        with open(config.TREND_KEYWORDS_FILE, 'r') as f:
            trends = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print(f"Error: Trend keywords file not found at {config.TREND_KEYWORDS_FILE}")
        return []

    suffixes = ['solutions', 'labs', 'future', 'systems', 'tech', 'works', 'group', 'ventures']
    
    generated_domains = []
    for trend in trends:
        for suffix in suffixes:
            base_name = f"{trend}{suffix}"
            for tld in config.DEFAULT_TLDS:
                generated_domains.append(f"{base_name}{tld}")
    
    return generated_domains

if __name__ == '__main__':
    print("Generating domains from trend words...")
    domains = generate_trend_domains()
    if domains:
        print(f"Generated {len(domains)} domains.")
        # Print the first 10 for a sample
        for domain in domains[:10]:
            print(domain)
    else:
        print("No domains generated or an error occurred.") 