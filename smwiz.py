import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Initialize browser with proper ChromeDriver path and options
def init_browser():
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--remote-debugging-port=9222")  # Enable remote debugging
    options.add_argument("--window-size=1920x1080")  # Set window size
    options.add_argument("--user-data-dir=/tmp/user_data")  # Avoid session issues
    options.add_argument("--disable-infobars")  # Disable info bar
    options.add_argument("--disable-extensions")  # Disable extensions

    driver_path = r"C:\Users\kevin\OneDrive\Documents\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    browser = webdriver.Chrome(executable_path=driver_path, options=options)
    
    return browser

# Fetch free proxy list from a source
def fetch_free_proxies():
    url = 'https://www.sslproxies.org/'
    response = requests.get(url)
    proxies = []
    
    # Parse proxies (This is a simplified example; you can use BeautifulSoup for a better solution)
    for line in response.text.splitlines():
        if 'data-proxy-port' in line:
            ip = line.split('data-proxy-ip="')[1].split('"')[0]
            port = line.split('data-proxy-port="')[1].split('"')[0]
            proxies.append(f'{ip}:{port}')
    
    return proxies

# Rotate proxies and restart browser with new proxy
def init_browser_with_proxy(proxy):
    options = Options()
    options.add_argument(f'--proxy-server={proxy}')
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--user-data-dir=/tmp/user_data")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    
    driver_path = r"C:\Users\kevin\OneDrive\Documents\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    browser = webdriver.Chrome(executable_path=driver_path, options=options)
    
    return browser

# Handle captcha using a service like 2Captcha (replace with your API key)
def solve_captcha(image_element):
    captcha_image_url = image_element.get_attribute('src')
    # Send image URL to captcha solving service
    api_key = "YOUR_2CAPTCHA_API_KEY"
    url = f"http://2captcha.com/in.php?key={api_key}&method=userrecaptcha&googlekey={captcha_image_url}&pageurl=YOUR_PAGE_URL"
    captcha_id = requests.get(url).text.split('|')[1]
    time.sleep(10)  # Wait for captcha to be solved
    url = f"http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}"
    captcha_solution = requests.get(url).text.split('|')[1]
    
    return captcha_solution

# Perform form interaction, JavaScript handling, and Ajax calls
def interact_with_landing_page(browser):
    try:
        wait = WebDriverWait(browser, 10)
        
        # Wait and fill in form fields
        form_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='email']")))
        form_field.send_keys('test@example.com')

        # Handle submit action
        submit_button = browser.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()
        
        # Handle any AJAX requests or additional form steps
        time.sleep(5)  # Adjust sleep for any JS/AJAX delays

    except Exception as e:
        print(f"Error interacting with page: {e}")

# Perform search and redirect on a random search engine
def perform_search_and_redirect(engine, query, smartlink_url):
    try:
        browser = init_browser()  # Create a new instance of browser with new proxy for each search
        browser.get(engine)
        
        # Search for query
        search_field = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.NAME, "q")))
        search_field.send_keys(query)
        search_field.send_keys(Keys.RETURN)
        
        # Wait for results to load and click on the desired result (simulate a user)
        first_result = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a")))
        first_result.click()
        
        # Redirect to the smartlink
        browser.get(smartlink_url)

        # Interact with landing page (AJAX, JS forms, etc.)
        interact_with_landing_page(browser)

    except Exception as e:
        print(f"Error during search and redirect for '{query}' on {engine}: {e}")
    finally:
        browser.quit()

# Main function to run the process
def run_script():
    smartlink_url = "https://tinyurl.com/se-smartlink"
    proxies = fetch_free_proxies()

    search_engines = ['https://www.google.com/', 'https://www.bing.com/', 'https://www.ecosia.org/']
    search_queries = ['best insurance rates', 'cheapest insurance rates', 'affordable health plans']

    for query in search_queries:
        for engine in search_engines:
            proxy = random.choice(proxies)  # Select a random proxy
            browser = init_browser_with_proxy(proxy)  # Start browser with proxy
            perform_search_and_redirect(engine, query, smartlink_url)
            time.sleep(random.uniform(5, 15))  # Random delay between actions

# Execute the script
if __name__ == "__main__":
    run_script()
