# src/main.py

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import datetime

from domainscanner.generators.trend_generator import generate_trend_domains
from domainscanner.generators.dictionary_generator import generate_dictionary_domains
from domainscanner.generators.news_generator import generate_news_based_domains
from domainscanner.parsers.expired_domains_parser import get_expired_domains
from domainscanner.analyzers.availability import check_single_domain
from domainscanner.analyzers.metrics import filter_by_length, check_single_domain_history
from domainscanner.analyzers.seo_analyzer import get_single_domain_seo
from domainscanner.publishers.marketplace_lister import list_domain_on_marketplaces

# Constants
MAX_WORKERS = 5 # Reduced from 10 to be even less aggressive

def run_parallel(func, items, description=""):
    """Helper function to run a function in parallel on a list of items."""
    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Create a future for each item
        futures = [executor.submit(func, item) for item in items]
        # Process as they complete, with a progress bar
        for future in tqdm(as_completed(futures), total=len(items), desc=description):
            results.append(future.result())
    return results

def save_results(filename, domains):
    """Saves a list of domains to a file in the data directory."""
    filepath = os.path.join('data', filename)
    with open(filepath, 'w') as f:
        # Add a timestamp to the file
        f.write(f"# Results from {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        for domain in domains:
            f.write(f"{domain}\n")
    print(f"\n[SUCCESS] Results saved to {filepath}")

def process_new_domains():
    """Pipeline for finding valuable new domains."""
    print("\n\n=========================================")
    print("🚀 Starting Pipeline for NEW Domains 🚀")
    print("=========================================")
    
    # 1. Generate domain names
    print("\n--- Generating Domains ---")
    trend_domains = generate_trend_domains()
    print(f"Generated {len(trend_domains)} domain candidates from trends.")
    dictionary_domains = generate_dictionary_domains()
    print(f"Generated {len(dictionary_domains)} domain candidates from the dictionary.")
    news_domains = generate_news_based_domains()
    print(f"Generated {len(news_domains)} domain candidates from news headlines.")
    generated_domains = list(set(trend_domains + dictionary_domains + news_domains))
    
    # 2. Analyze for availability (in parallel)
    availability_results = run_parallel(check_single_domain, generated_domains, "Checking Availability")
    available_domains = [domain for domain, is_available in availability_results if is_available]
    
    # 3. Filter by length
    short_domains = filter_by_length(available_domains)
    print(f"\nFiltered down to {len(short_domains)} domains based on length.")
    
    # 4. Filter for clean history (in parallel)
    history_results = run_parallel(check_single_domain_history, short_domains, "Checking History")
    clean_domains = [domain for domain, has_history in history_results if not has_history]
    
    # 5. Print and save results
    print("\n--- ✅ Final Results for NEW Domains ---")
    sorted_domains = sorted(clean_domains)
    if sorted_domains:
        print(f"Found {len(sorted_domains)} domains that meet all criteria (available, short, clean history):")
        for domain in sorted_domains:
            print(f"  -> {domain}")
            list_domain_on_marketplaces(domain)
        save_results('new_domains_found.txt', sorted_domains)
    else:
        print("No new domains found that meet all criteria.")

def process_expired_domains():
    """Pipeline for finding valuable expired domains."""
    print("\n\n===========================================")
    print("💎 Starting Pipeline for EXPIRED Domains 💎")
    print("===========================================")
    
    # 1. Parse domains
    print("\n--- Parsing Expired Domains ---")
    expired_domains = get_expired_domains()
    if not expired_domains:
        print("No expired domains found or parser failed.")
        return

    # 2. Check availability (in parallel)
    availability_results = run_parallel(check_single_domain, expired_domains, "Checking Availability")
    available_expired = [domain for domain, is_available in availability_results if is_available]
    
    # 3. Check SEO metrics for the available ones (in parallel)
    if not available_expired:
        print("\nNo available domains found from the parsed list.")
        return
        
    seo_results = run_parallel(get_single_domain_seo, available_expired, "Checking SEO (Simulated)")
    
    # 4. Filter or sort by score (e.g., show domains with DA > 20)
    print("\n--- ✅ Final Results for EXPIRED Domains (DA > 20) ---")
    high_value_domains = {domain: score for domain, score in seo_results if score > 20}
    
    if high_value_domains:
        # Sort by score, descending
        sorted_domains = sorted(high_value_domains.items(), key=lambda item: item[1], reverse=True)
        print(f"Found {len(sorted_domains)} high-value expired domains:")
        # Prepare list for saving
        domains_to_save = []
        for domain, score in sorted_domains:
            line = f"{domain} (DA: {score})"
            print(f"  -> {line}")
            domains_to_save.append(line)
            list_domain_on_marketplaces(domain)
        save_results('expired_domains_found.txt', domains_to_save)
    else:
        print("No high-value expired domains found that meet the criteria.")

def main():
    """Main function to run the domain scanner bot."""
    print("Initializing Domain Scanner Bot...")
    
    process_new_domains()
    process_expired_domains()
    
    print("\n\nDomain Scanner Bot finished.")

if __name__ == "__main__":
    main() 