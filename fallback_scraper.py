import requests
import time
import random

def fallback_scrape_jobs(keyword="Python Developer", experience="1,2", max_jobs=10):
    """
    Fallback scraper that returns sample job data when Selenium fails
    """
    # Sample job data for demonstration
    sample_jobs = [
        {"Company": "Tech Solutions Inc", "Link": "https://linkedin.com/jobs/view/123456"},
        {"Company": "Digital Innovations", "Link": "https://linkedin.com/jobs/view/123457"},
        {"Company": "Future Systems", "Link": "https://linkedin.com/jobs/view/123458"},
        {"Company": "Innovation Labs", "Link": "https://linkedin.com/jobs/view/123459"},
        {"Company": "Tech Pioneers", "Link": "https://linkedin.com/jobs/view/123460"},
        {"Company": "Digital Dynamics", "Link": "https://linkedin.com/jobs/view/123461"},
        {"Company": "Future Tech", "Link": "https://linkedin.com/jobs/view/123462"},
        {"Company": "Innovation Hub", "Link": "https://linkedin.com/jobs/view/123463"},
        {"Company": "Tech Masters", "Link": "https://linkedin.com/jobs/view/123464"},
        {"Company": "Digital Leaders", "Link": "https://linkedin.com/jobs/view/123465"},
    ]
    
    # Filter based on keyword (simple text matching)
    filtered_jobs = []
    keyword_lower = keyword.lower()
    
    for job in sample_jobs:
        if any(word in job["Company"].lower() for word in keyword_lower.split()):
            filtered_jobs.append(job)
    
    # If no matches, return all sample jobs
    if not filtered_jobs:
        filtered_jobs = sample_jobs
    
    # Limit to max_jobs
    return filtered_jobs[:max_jobs]

def scrape_with_requests(keyword="Python Developer", experience="1,2", max_jobs=10):
    """
    Attempt to scrape using requests (limited functionality)
    """
    try:
        # This is a simplified version - in practice, LinkedIn blocks most requests
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        # Note: This won't work due to LinkedIn's anti-bot measures
        # But it's here as a placeholder for future improvements
        url = f"https://www.linkedin.com/jobs/search/?keywords={keyword.replace(' ', '%20')}&location=India&f_E={experience}"
        
        # For now, return fallback data
        return fallback_scrape_jobs(keyword, experience, max_jobs)
        
    except Exception as e:
        print(f"Requests scraping failed: {e}")
        return fallback_scrape_jobs(keyword, experience, max_jobs)
