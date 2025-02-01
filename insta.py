# insta_growth_panel.py
import time
import random
import logging
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv

load_dotenv()

class InstaGrowthMaster:
    def __init__(self):
        self.driver = None
        self.actions = None
        self.session_start = datetime.now()
        self.config = {
            "daily_limits": {
                "follows": random.randint(35, 50),
                "likes": random.randint(70, 100),
                "comments": random.randint(5, 10)
            },
            "behavior": {
                "scroll_variants": [300, 500, 700, -200],
                "work_hours": (10, 21),  # 10 AM - 9 PM
                "human_delay": (1.8, 4.2)
            },
            "selectors": {
                "username": '//input[@name="username"]',
                "password": '//input[@name="password"]',
                "login_btn": '//button[@type="submit"]',
                "followers_link": '//a[contains(@href, "/followers")]',
                "follow_btn": '//div[@role="button"]//div[text()="Follow"]',
                "like_btn": '//*[@aria-label="Like"]',
                "comment_box": '//textarea[@aria-label="Add a comment"]',
                "post_xpath": '//article//div[@role="button"]'
            }
        }
        self.init_driver()
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            filename='growth_panel.log',
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            filemode='a'
        )

    def init_driver(self):
        chrome_options = webdriver.ChromeOptions()
        
        # Windows 11 Optimization
        chrome_options.add_argument("--disable-features=RendererCodeIntegrity")
        chrome_options.add_argument("--disable-gpu-sandbox")
        chrome_options.add_argument("--no-default-browser-check")
        
        # Anti-Detection Config
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_argument(f"user-agent={self.random_user_agent()}")
        
        # Path to your ChromeDriver (update this path)
        self.driver = webdriver.Chrome(
            executable_path=r'C:\path\to\chromedriver.exe',
            options=chrome_options
        )
        self.actions = ActionChains(self.driver)

    def random_user_agent(self):
        agents = [
            # Updated 2025 user agents
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        return random.choice(agents)

    def human_delay(self):
        min_t, max_t = self.config["behavior"]["human_delay"]
        time.sleep(random.uniform(min_t, max_t) + random.random())

    def human_click(self, element):
        try:
            self.actions.move_to_element_with_offset(
                element, 
                random.uniform(3,7), 
                random.uniform(3,7)
            ).pause(random.uniform(0.2, 0.8)).click().perform()
            self.human_delay()
        except Exception:
            element.click()

    def login(self):
        try:
            self.driver.get("https://www.instagram.com/accounts/login/")
            
            # Fill credentials
            username = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, self.config["selectors"]["username"]))
            )
            self.smart_type(username, os.getenv("INSTA_USER"))
            
            password = self.driver.find_element(By.XPATH, self.config["selectors"]["password"])
            self.smart_type(password, os.getenv("INSTA_PASS"))
            
            # Login
            login_btn = self.driver.find_element(By.XPATH, self.config["selectors"]["login_btn"])
            self.human_click(login_btn)
            
            # Handle post-login
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '//nav[@role="navigation"]'))
            )
            self.dismiss_popups()

        except Exception as e:
            logging.error(f"Login failed: {str(e)}")
            self.driver.save_screenshot("login_error.png")
            self.restart_session()

    def smart_type(self, element, text):
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.08, 0.15))
            if random.random() < 0.05:
                element.send_keys(Keys.BACKSPACE)
                time.sleep(0.1)
                element.send_keys(char)

    def dismiss_popups(self):
        popups = [
            '//button[text()="Not Now"]',
            '//div[text()="Cancel"]',
            '//button[text()="Close"]'
        ]
        for popup in popups:
            try:
                btn = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, popup))
                )
                self.human_click(btn)
            except:
                continue

    def organic_growth_sequence(self, target_account):
        try:
            self.driver.get(f"https://www.instagram.com/{target_account}/")
            self.human_delay()
            
            # Engage with followers
            self.human_click(self.driver.find_element(
                By.XPATH, self.config["selectors"]["followers_link"]
            ))
            self.human_delay()
            
            # Growth algorithm
            container = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '//div[@role="dialog"]'))
            )
            
            for _ in range(3):  # 3 scroll passes
                self.driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollHeight",
                    container
                )
                self.human_delay()
                
                # Follow users
                follow_buttons = container.find_elements(
                    By.XPATH, self.config["selectors"]["follow_btn"]
                )[:5]  # Only first 5 to be safe
                
                for btn in follow_buttons:
                    if random.random() < 0.7:  # 70% follow rate
                        self.human_click(btn)
                        self.human_delay()
                        logging.info("Followed user")

            # Close followers dialog
            self.driver.find_element(
                By.XPATH, '//*[@aria-label="Close"]'
            ).click()
            
            # Engage with posts
            posts = self.driver.find_elements(
                By.XPATH, self.config["selectors"]["post_xpath"]
            )[:3]
            
            for post in posts:
                self.human_click(post)
                self.human_delay()
                
                # Like post
                self.human_click(self.driver.find_element(
                    By.XPATH, self.config["selectors"]["like_btn"]
                ))
                self.human_delay()
                
                # Comment (occasionally)
                if random.random() < 0.3:
                    comment_box = self.driver.find_element(
                        By.XPATH, self.config["selectors"]["comment_box"]
                    )
                    self.smart_type(comment_box, random.choice([
                        "Great content! 👏",
                        "Amazing! 😍",
                        "Love this! ❤️"
                    ]))
                    comment_box.send_keys(Keys.ENTER)
                    self.human_delay()
                
                self.driver.back()
                self.human_delay()

        except Exception as e:
            logging.error(f"Growth sequence error: {str(e)}")
            self.driver.save_screenshot("growth_error.png")

    def session_management(self):
        elapsed = datetime.now() - self.session_start
        if elapsed.seconds > 3600:  # 1 hour session limit
            self.restart_session()
        if not self.within_work_hours():
            logging.info("Outside working hours - pausing")
            time.sleep(3600)  # Sleep 1 hour

    def within_work_hours(self):
        now = datetime.now().hour
        return self.config["behavior"]["work_hours"][0] <= now < self.config["behavior"]["work_hours"][1]

    def restart_session(self):
        logging.info("Restarting session...")
        self.driver.quit()
        time.sleep(300)  # 5 minute cooldown
        self.__init__()
        self.login()

if __name__ == "__main__":
    panel = InstaGrowthMaster()
    panel.login()
    
    try:
        while True:
            target = os.getenv("TARGET_ACCOUNT")
            panel.organic_growth_sequence(target)
            panel.session_management()
            time.sleep(random.randint(300, 600))  # 5-10 minute breaks
            
    except KeyboardInterrupt:
        logging.info("Session stopped by user")
    finally:
        panel.driver.quit()