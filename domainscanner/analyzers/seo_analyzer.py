# src/analyzers/seo_analyzer.py
import sys
import os
from typing import List, Tuple
import random

from .. import config

def get_single_domain_seo(domain: str) -> Tuple[str, int]:
    """
    Simulates fetching SEO metrics for a single domain.
    Returns the domain and its score.
    """
    if not config.MOZ_ACCESS_ID or not config.MOZ_SECRET_KEY:
        # Simulate a score for demonstration purposes
        score = random.randint(5, 40) 
    else:
        # TODO: Implement actual API call to Mozscape API
        score = random.randint(5, 40) # Still using random for now
    
    return domain, score

def get_seo_metrics(domains: List[str]) -> dict:
    """
    DEPRECATED: This function is kept for compatibility but the main logic
    should use get_single_domain_seo with a ThreadPoolExecutor.
    """
    print("\n--- Checking SEO Metrics (Simulation) ---")
    if not config.MOZ_ACCESS_ID or not config.MOZ_SECRET_KEY:
        print("WARNING: Moz API keys are not set in config.py. Using simulated data.")
        print("To get real data, sign up for a free Moz API key and add it to the config.")
    
    seo_scores = {}
    for domain in domains:
        domain_name, score = get_single_domain_seo(domain)
        print(f"[SEO SCORE] {domain_name}: DA = {score}")
        seo_scores[domain_name] = score
        
    return seo_scores

if __name__ == '__main__':
    test_domains = [
        'expired-domain-with-history.com',
        'another-good-one.net',
        'formerly-a-blog.org'
    ]
    
    get_seo_metrics(test_domains) 