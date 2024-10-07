import random
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from faker import Faker

# Initialize Faker to generate random user data
fake = Faker()

# Your smartlink (or landing page that redirects to the smartlink)
smartlink_url = 'https://tinyurl.com/se-smartlink'

# Set up the browser (use headless to keep it stealth, but visible if needed for debugging)
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1200x600')

# Random User-Agents to rotate through (simulate different browsers/devices)
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
]

# Paid rotating proxies (replace with your real proxies later if needed)
paid_proxies = [
    'http://user:password@proxy1.example.com:8080',
    'http://user:password@proxy2.example.com:8080',
    'http://user:password@proxy3.example.com:8080',
]

# API URL for free proxies (you can use ProxyScrape)
free_proxy_api_url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=1000&country=all"

# Fetch fresh free proxies from the API
def fetch_free_proxies():
    try:
        response = requests.get(free_proxy_api_url)
        if response.status_code == 200:
            proxy_list = response.text.strip().split("\n")
            return [f"http://{proxy}" for proxy in proxy_list if proxy]
        else:
            print(f"Failed to fetch free proxies. Status code: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching proxies: {e}")
        return []

# Combine paid and free proxies (free proxies are fetched dynamically)
def get_proxy_pool():
    free_proxies = fetch_free_proxies()  # Fetch free proxies dynamically
    return paid_proxies + free_proxies  # Combine paid and free proxies

# Initialize browser with proxy
def init_browser():
    user_agent = random.choice(user_agents)
    proxy = random.choice(get_proxy_pool())

    options.add_argument(f'user-agent={user_agent}')
    options.add_argument(f'--proxy-server={proxy}')

    return webdriver.Chrome(options=options)

# Simulate filling out forms and completing actions
def complete_cpa_action(browser):
    # Simulate common form fields
    try:
        # Fill out an email field
        email_field = browser.find_element("xpath", '//input[@type="email"]')
        if email_field:
            fake_email = fake.email()
            email_field.send_keys(fake_email)
            print(f"Filled email: {fake_email}")
            human_delay(1, 3)

        # Fill out a name field if available
        name_field = browser.find_element("xpath", '//input[@type="text"]')
        if name_field:
            fake_name = fake.first_name()
            name_field.send_keys(fake_name)
            print(f"Filled name: {fake_name}")
            human_delay(1, 3)

        # Fill out a phone field if available
        phone_field = browser.find_element("xpath", '//input[@type="tel"]')
        if phone_field:
            fake_phone = fake.phone_number()
            phone_field.send_keys(fake_phone)
            print(f"Filled phone: {fake_phone}")
            human_delay(1, 3)

        # Find and click the submit button
        submit_button = browser.find_element("xpath", '//button[@type="submit"]')
        if submit_button:
            submit_button.click()
            print("Clicked the submit button")
            human_delay(5, 7)  # Wait for the action to process

    except Exception as e:
        print(f"Error completing CPA action: {e}")

# Function to simulate human-like delays
def human_delay(min_sec, max_sec):
    time.sleep(random.uniform(min_sec, max_sec))

# List of search engines to exploit
search_engines = ['https://duckduckgo.com/', 'https://www.ecosia.org/']

# List of low-competition, high-intent search queries
search_queries = [
    "best deals on latest gadgets",
    "cheapest insurance rates",
    "how to make money quickly online",
    "best credit card deals",
]

# Function to search on each engine and redirect to your smartlink
def perform_search_and_redirect(engine, query):
    browser = init_browser()  # Create a new instance of browser with new proxy for each search
    browser.get(engine)
    
    # Find search box by inspecting page (different search engines use different attributes)
    if 'duckduckgo' in engine:
        search_box = browser.find_element("name", "q")  # DuckDuckGo
    elif 'ecosia' in engine:
        search_box = browser.find_element("name", "q")  # Ecosia

    # Simulate typing the query into the search box
    search_box.clear()
    search_box.send_keys(query)
    human_delay(2, 5)  # Simulate human typing time
    search_box.send_keys(Keys.RETURN)
    
    # Wait for the results page to load
    human_delay(3, 7)

    # Select a random result to click (not always the first one)
    try:
        result_links = browser.find_elements("xpath", '//a[@href]')  # Finds clickable results
        if result_links:
            result_to_click = random.choice(result_links[:5])  # Click one of the top 5 results randomly
            result_to_click.click()
            print(f"Clicked result for '{query}' on {engine}")

            # After clicking, redirect to your smartlink after a delay
            human_delay(5, 10)
            browser.get(smartlink_url)
            print(f"Redirected to Smartlink for '{query}'")

            # Once on the landing page, complete the action
            complete_cpa_action(browser)

        else:
            print(f"No results found for '{query}' on {engine}")
    
    except Exception as e:
        print(f"Error during search and redirect for '{query}' on {engine}: {e}")

    finally:
        browser.quit()

# Main execution loop with randomized delays and search order
def run_script():
    # Shuffle search engines and queries to make each iteration unpredictable
    random.shuffle(search_engines)
    random.shuffle(search_queries)

    for engine in search_engines:
        for query in search_queries:
            perform_search_and_redirect(engine, query)
            
            # Randomized delay between searches to prevent bot detection
            human_delay(60, 300)  # Wait 1 to 5 minutes before the next search

            # Occasionally simulate a backtracking action by searching again without clicking
            if random.random() > 0.8:
                print(f"Simulating backtracking for '{query}' on {engine}")
                human_delay(5, 10)
                perform_search_and_redirect(engine, query)

if __name__ == "__main__":
    run_script()
