import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import re

# List of web and app development related technologies
technologies = [
    "react", "electron"
]

# Initialize Selenium WebDriver
driver = webdriver.Chrome()  # You can replace 'Chrome' with the browser of your choice

# Open the webpage
driver.get("https://summerofcode.withgoogle.com/programs/2024/organizations")

# Open file for writing
with open("gsoc_technologies.txt", "w") as file:
    # Find anchor tags with class "content"
    time.sleep(10)
    content_links = driver.find_elements(By.CSS_SELECTOR, "a.content")
    for content_link in content_links:
        # Get the href attribute of the anchor tag
        href = content_link.get_attribute("href")
        # Extract the name from the content link
        name = content_link.find_element(By.CSS_SELECTOR, "div.name").text
        
        # Open link in a new tab
        ActionChains(driver).key_down(Keys.CONTROL).click(content_link).key_up(Keys.CONTROL).perform()
        
        # Switch to newly opened tab
        driver.switch_to.window(driver.window_handles[-1])

        try:

            # Get the href attribute of the "View ideas list" link
            time.sleep(3)
            view_ideas_list_link_href = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[text()=' View ideas list ']/ancestor::a"))).get_attribute("href")
            
            # Open "View ideas list" link in a new tab
            driver.execute_script("window.open(arguments[0]);", view_ideas_list_link_href)

            
            # Switch to the newly opened tab
            driver.switch_to.window(driver.window_handles[-1])

            # Check all technologies mentioned on the page
            time.sleep(2)
            page_source = driver.page_source.lower()  # Convert page source to lowercase for case-insensitive matching
            
            # Extract text inside tags
            text_inside_tags = re.sub(r'<[^>]+>', '', page_source)

            for tech in technologies:
                if tech.lower() in text_inside_tags:
                    print(f"{name} - {tech}")
                    file.write(f"{name} - {tech}\n")

        except TimeoutException:
            print(f"Timeout: 'View ideas list' link not found for organization: {name}")


        # Close the tab
        driver.close()

        # Switch back to the main tab
        driver.switch_to.window(driver.window_handles[-1])

        # Close the original tab
        driver.close()

        driver.switch_to.window(driver.window_handles[0])

        # Delay for a short while to ensure the page has loaded properly
        time.sleep(1)

# Close the browser
driver.quit()
