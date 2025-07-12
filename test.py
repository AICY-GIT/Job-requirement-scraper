import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
url = "https://www.topcv.vn/viec-lam-it?sort=&skill_id=&skill_id_other=&keyword=&company_field=&position=50&salary="
driver.get(url)

def take_job_requirements(job_elements):
    for job_element in job_elements:
        job_title = job_element.text.strip()
        job_link = job_element.get_attribute("href")

        # Open a new Chrome window for each job link
        driverTemp = webdriver.Chrome()
        driverTemp.get(job_link)

        try:
            WebDriverWait(driverTemp, 20).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="box-job-information-detail"]/div[2]/div/div[1]/div/ul'))
            )
            # Extract job requirements
            requirements_elements = driverTemp.find_elements(
                By.XPATH, '//*[@id="box-job-information-detail"]/div[2]/div/div[1]/div/ul/li'
            )
            requirements = "\n".join([req.text.strip() for req in requirements_elements])

            # Write job details to the CSV file
            with open("job_data.csv", "a", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([job_title, job_link, requirements])

            print(f"Saved job: {job_title}")

        except Exception as e:
            print(f"Failed to extract data for {job_title}: {e}")

        finally:
            driverTemp.quit()  # Close the new window regardless of success or failure

        # Pause to avoid overwhelming the server
        time.sleep(2)

# Wait for the first page to load
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div[1]/div[3]/div[4]/div[1]/div[1]'))
    )
    print("Page loaded successfully.")
except Exception as e:
    print(f"Page load timeout: {e}")
    driver.quit()

# Create CSV file with headers
with open("job_data.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Job Title", "Job Link", "Requirements"])

# Extract job elements from the first page
job_elements = driver.find_elements(
    By.XPATH, '//*[@id="main"]/div[1]/div[3]/div[4]/div[1]/div[1]/div/div/div[2]/div[2]/h3/a'
)
take_job_requirements(job_elements)

# Find the last page number
try:
    last_page_element = driver.find_element(By.XPATH, "//ul[@class='pagination']/li[last()-1]/a")
    last_page_number = int(last_page_element.text)
    print(f"Found last page: {last_page_number}")
except Exception as e:
    print(f"Failed to find the last page: {e}")
    last_page_number = 1

# Loop through pages 2 to last page
for pageNum in range(2, last_page_number + 1):
    driverJoblist = webdriver.Chrome()
    driverJoblist.get(f'https://www.topcv.vn/viec-lam-it?sort=&skill_id=&skill_id_other=&keyword=&company_field=&position=50&salary=&page={pageNum}')
    
    try:
        WebDriverWait(driverJoblist, 10).until(  
            EC.presence_of_element_located((By.CLASS_NAME, 'job-list-2'))
        )
        print(f"Loaded page {pageNum} successfully.")

        job_elements = driverJoblist.find_elements(  
            By.XPATH, '//*[@id="main"]/div[1]/div[3]/div[4]/div[1]/div[1]/div/div/div[2]/div[2]/h3/a'
        )               

        take_job_requirements(job_elements)

    except Exception as e:
        print(f"Failed to load page {pageNum}: {e}")
    finally:
        driverJoblist.quit()  # Close the new window regardless of success or failure

    time.sleep(2)

# Close the main driver
driver.quit()
