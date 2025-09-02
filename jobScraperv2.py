import time
import pandas as pd
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By


def scrape_linkedin_jobs(keyword="Python Developer", experience="1,2", max_jobs=30):
    driver = uc.Chrome(headless=True)

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
                company_elem = driver.find_element(By.CLASS_NAME, "topcard__flavor")

            company_name = company_elem.text.strip()
            final_data.append({"Company": company_name, "Link": link})
            print(f"[{idx+1}] ✅ {company_name}")
        except Exception as e:
            print(f"[{idx+1}] ⚠ Error at {link} — {e}")
            continue

    # Save with pandas
    df = pd.DataFrame(final_data)
    csv_path = "C:/Users/uddha/Desktop/job_links_pandas.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8")

    print(f"\n✅ Saved {len(final_data)} job links with company names to: {csv_path}")
    driver.quit()
    return final_data


# MAIN
if __name__ == "__main__":
    field = input("Enter the job field (e.g. Cyber Security, Data Analyst): ").strip()
    print("\nExperience Levels:\n1 = Internship\n2 = Entry level\n3 = Associate\n4 = Mid-Senior\n5 = Director\n6 = Executive")
    experience = input("Enter experience level(s) separated by commas (e.g. 1,2): ").strip()

    max_jobs = int(input("Enter max number of jobs to scrape: ").strip())

    scrape_linkedin_jobs(field, experience, max_jobs)
