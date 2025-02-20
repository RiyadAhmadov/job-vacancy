from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait  # Import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # Import expected_conditions
import time
import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')
import re

chrome_driver_path = r"C:\Users\HP\OneDrive\İş masası\chromedriver-win64\chromedriver.exe"
chrome_options = Options()
# chrome_options.add_argument("--headless") 
chrome_options.add_argument("--start-maximized")

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://www.jobsearch.az/vacancies"
driver.get(url)
time.sleep(3)

# Wait for the scroller element to be present
try:
    scroller = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="scroller_desctop"]'))
    )
    print("Scroller element found.")
except Exception as e:
    print(f"Scroller element not found. Error: {e}")
    driver.quit()
    exit()

min_vacancies = 50
scroll_pause_time = 20  # Pause time between scrolls
job_elements = []

while len(job_elements) < min_vacancies:
    driver.execute_script("arguments[0].scrollTop += arguments[0].scrollHeight;", scroller)
    time.sleep(scroll_pause_time)

    job_elements += driver.find_elements(By.XPATH, "//*[contains(@class, 'list__item--vip')]")

    current_count = len(list(set(job_elements)))

    if current_count >= min_vacancies:
        print(f"Vacancies loaded so far: {current_count}")
        break

    print(f"Scrolling... Vacancies loaded so far: {current_count}")

# job_elements = driver.find_elements(By.CLASS_NAME, "list__item--vip")

job_data = []

for job in job_elements:
    link_tag = job.find_element(By.TAG_NAME, "a")
    vacancy_link = link_tag.get_attribute("href") if link_tag else "No link"

    try:
        company_name = job.find_element(By.TAG_NAME, "h3").find_element(By.XPATH, "..").text.strip().split("\n")[-1]
    except:
        company_name = "No company name"

    try:
        vacancy_name = job.find_element(By.CLASS_NAME, "list__item__title").text.strip()
    except:
        vacancy_name = "No vacancy name"

    html_content = job.get_attribute("outerHTML")
    
    date_pattern = r'class="text-transform-none">\s*(.*?)\s*</span>'
    date_match = re.search(date_pattern, html_content)
    sharing_date = date_match.group(1).strip() if date_match else "No sharing date"

    viewer_pattern = r'<svg[^>]*>.*?</svg>\s*([\d.]+[KM]?)\s*</span>'
    viewer_match = re.search(viewer_pattern, html_content)
    viewer_count = viewer_match.group(1).strip() if viewer_match else "No viewer count"

    driver.execute_script(f"window.open('{vacancy_link}', '_blank');")
    driver.switch_to.window(driver.window_handles[1])  # Switch to the new tab
    time.sleep(2)  

    try:
        deadline_element = driver.find_element(By.CSS_SELECTOR, "span.vacancy__deadline")
        job_deadline = deadline_element.text.strip()
    except:
        job_deadline = "No deadline"

    try:
        description_element = driver.find_element(By.CSS_SELECTOR, "div.content-text")
        job_description = description_element.text.strip()
    except:
        job_description = "No description"

    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    job_data.append([
        vacancy_link, vacancy_name, company_name, sharing_date,
        viewer_count, job_deadline, job_description
    ])

df = pd.DataFrame(job_data, columns=[
    "Vacancy Link", "Vacancy Name", "Company Name", "Sharing Date",
    "Viewer Count", "Job Deadline", "Job Description"
])

excel_file_path = "vacancy_data.xlsx"
df.to_excel(excel_file_path, index=False)

driver.quit()
