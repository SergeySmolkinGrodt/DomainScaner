# src/main.py

import sys
import os

# Add the project root directory to the Python path
# This allows us to import modules from the root, like `config.py`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from generators.trend_generator import generate_trend_domains
from generators.dictionary_generator import generate_dictionary_domains
from analyzers.availability import check_domain_availability
from analyzers.metrics import filter_by_length
# from parsers.expired_domains_parser import get_expired_domains # Will be used later

def main():
    """
    Main function to run the domain scanner bot.
    """
    print("Initializing Domain Scanner Bot...")
    
    # 1. Generate domain names
    print("\n--- Generating Domains ---")
    
    trend_domains = generate_trend_domains()
    print(f"Generated {len(trend_domains)} domain candidates from trends.")
    
    dictionary_domains = generate_dictionary_domains()
    print(f"Generated {len(dictionary_domains)} domain candidates from the dictionary.")

    candidate_domains = list(set(trend_domains + dictionary_domains)) # Combine and remove duplicates
    
    if candidate_domains:
        print(f"Total unique domains to check: {len(candidate_domains)}.")
        # Print a small sample
        print("Sample:", candidate_domains[:5])
    else:
        print("Could not generate any domains.")
        return # Exit if no domains to check

    # 2. Analyze domains for availability
    print("\n--- Analyzing Availability ---")
    available_domains = check_domain_availability(candidate_domains)
    
    # 3. Filter available domains by length
    print("\n--- Filtering by Length ---")
    short_and_available_domains = filter_by_length(available_domains)

    # 4. Print results
    print("\n--- Final Results ---")
    if short_and_available_domains:
        print(f"Found {len(short_and_available_domains)} short and available domains:")
        for domain in short_and_available_domains:
            print(f"  -> {domain}")
    else:
        print("No available domains found that meet all criteria.")

    print("\nDomain Scanner Bot finished.")

if __name__ == "__main__":
    main() 