import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

try:
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(options=options)
    print("Browser opened")
    
    driver.get("https://www.pro-football-reference.com/years/2024/draft.htm")
    print("Page loading...")
    
    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "title"))
    )
    
    time.sleep(15)  # Extra delay for content
    
    print(f"Page title: {driver.title}")
    
    # Try to get some page content
    soup = BeautifulSoup(driver.page_source, "html.parser")
    print(f"Page loaded successfully")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()