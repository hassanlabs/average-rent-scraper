from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


def get_page_html_with_selenium(url):
    # Setup Selenium WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'table[class="market-trends-table"]'))
    )
    html_content = driver.page_source
    driver.quit()
    return html_content


def get_avg_rent_data(city, state):
    url = f"https://www.rentcafe.com/average-rent-market-trends/us/{state.lower()}/{city.lower().replace(' ', '-')}/"
    print(url)
    html_content = get_page_html_with_selenium(url)
    if html_content:
        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        fields = soup.find('table', {'class': 'market-trends-table'}).find_all('td')
        avg_rent = fields[0].text
        avg_size = fields[1].text

        avg_rent_per_sqft = float(re.sub("[^0-9]", "", avg_rent)) / float(re.sub("[^0-9]", "", avg_size))

        return {
            'Average Rent': avg_rent,
            'Average Apartment Size': avg_size,
            'Average Rent per Square Foot': round(avg_rent_per_sqft, 2)
        }

    else:
        print("Not a valid response.")


if __name__ == '__main__':
    print(get_avg_rent_data("Houston", "TX"))
    print(get_avg_rent_data("sacramento", "CA"))

    print(get_avg_rent_data("Houston", "TX"))
    print(get_avg_rent_data("sacramento", "CA"))

    print(get_avg_rent_data("Houston", "TX"))
    print(get_avg_rent_data("sacramento", "CA"))
