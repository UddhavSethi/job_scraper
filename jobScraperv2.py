import time
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
from fallback_scraper import fallback_scrape_jobs


def scrape_linkedin_jobs(keyword="Python Developer", experience="1,2", max_jobs=30):
    # Configure Chrome options for Render deployment
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = None
    try:
        driver = uc.Chrome(options=chrome_options)
    except Exception as e:
        print(f"Failed to initialize Chrome driver: {e}")
        # Fallback to basic selenium if undetected_chromedriver fails
        try:
            from selenium import webdriver
            driver = webdriver.Chrome(options=chrome_options)
        except Exception as e2:
            print(f"Basic Selenium also failed: {e2}")
            print("Using fallback scraper...")
            return fallback_scrape_jobs(keyword, experience, max_jobs)

    if not driver:
        print("No driver available, using fallback scraper...")
        return fallback_scrape_jobs(keyword, experience, max_jobs)

    try:
        # Format experience levels (LinkedIn codes)
        # 1 = Internship, 2 = Entry level, 3 = Associate, 4 = Mid-Senior, 5 = Director, 6 = Executive
        search_url = (
            f"https://www.linkedin.com/jobs/search/?keywords={keyword.replace(' ', '%20')}"
            f"&location=India&f_E={experience}"
        )
        driver.get(search_url)
        time.sleep(5)

        job_links = set()
        last_height = driver.execute_script("return document.body.scrollHeight")

        while len(job_links) < max_jobs:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            jobs = driver.find_elements(By.CLASS_NAME, "base-card")
            for job in jobs:
                try:
                    link = job.find_element(By.TAG_NAME, "a").get_attribute("href")
                    if link and link not in job_links:
                        job_links.add(link)
                        if len(job_links) >= max_jobs:
                            break
                except:
                    continue

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        print(f"🔗 Collected {len(job_links)} job links. Now extracting company names...")

        final_data = []

        for idx, link in enumerate(job_links):
            try:
                driver.get(link)
                time.sleep(3)

                try:
                    company_elem = driver.find_element(By.CLASS_NAME, "topcard__org-name-link")
                except:
                    try:
                        company_elem = driver.find_element(By.CLASS_NAME, "topcard__flavor")
                    except:
                        # If we can't find company name, use a placeholder
                        company_name = "Company"
                        final_data.append({"Company": company_name, "Link": link})
                        print(f"[{idx+1}] ✅ {company_name}")
                        continue

                company_name = company_elem.text.strip()
                final_data.append({"Company": company_name, "Link": link})
                print(f"[{idx+1}] ✅ {company_name}")
            except Exception as e:
                print(f"[{idx+1}] ⚠ Error at {link} — {e}")
                # Add the job with a placeholder company name
                final_data.append({"Company": "Company", "Link": link})
                continue

        print(f"\n✅ Successfully scraped {len(final_data)} job links")
        driver.quit()
        return final_data

    except Exception as e:
        print(f"Error during scraping: {e}")
        if driver:
            driver.quit()
        # Use fallback scraper if everything fails
        print("Using fallback scraper due to errors...")
        return fallback_scrape_jobs(keyword, experience, max_jobs)


# MAIN
if __name__ == "__main__":
    field = input("Enter the job field (e.g. Cyber Security, Data Analyst): ").strip()
    print("\nExperience Levels:\n1 = Internship\n2 = Entry level\n3 = Associate\n4 = Mid-Senior\n5 = Director\n6 = Executive")
    experience = input("Enter experience level(s) separated by commas (e.g. 1,2): ").strip()

    max_jobs = int(input("Enter max number of jobs to scrape: ").strip())

    scrape_linkedin_jobs(field, experience, max_jobs)
