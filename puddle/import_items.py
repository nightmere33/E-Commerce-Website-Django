import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# CONFIG
USERNAME = "massil"
PASSWORD = "939062002"
ADMIN_URL = "http://127.0.0.1:8000/admin"
CSV_PATH = r"C:\Users\Massil\OneDrive\Bureau\PROJET FIN D'ETUDE\E-Commerce-Website-Django\puddle\items.csv"

CHROMEDRIVER_PATH = "puddle/chromedriver/chromedriver.exe"

# Lance Chrome
service = Service(CHROMEDRIVER_PATH)
options = Options()
options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"  # adapte si besoin
driver = webdriver.Chrome(service=service, options=options)

driver.get(ADMIN_URL)

# Connexion
driver.find_element(By.NAME, "username").send_keys(USERNAME)
driver.find_element(By.NAME, "password").send_keys(PASSWORD)
driver.find_element(By.XPATH, "//input[@type='submit']").click()
time.sleep(2)

# Clique sur "Item" puis "Items"
driver.find_element(By.LINK_TEXT, "ITEM").click()
time.sleep(1)
driver.find_element(By.LINK_TEXT, "Items").click()
time.sleep(1)

# Lecture du CSV
with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Clique sur "Add item"
        driver.find_element(By.LINK_TEXT, "ADD ITEM").click()
        time.sleep(1)

        # Sélection de la catégorie
        Select(driver.find_element(By.NAME, "Category")).select_by_visible_text(row['category'])

        # Nom
        driver.find_element(By.NAME, "name").send_keys(row['name'])

        # Description avec CKEditor (⚠️ ATTENTION : on passe dans l'iframe)
        time.sleep(2)  # Laisse le temps à CKEditor de charger
        iframe = driver.find_element(By.CSS_SELECTOR, "iframe.cke_wysiwyg_frame")
        driver.switch_to.frame(iframe)
        editor_body = driver.find_element(By.TAG_NAME, "body")
        editor_body.clear()
        editor_body.send_keys(row['description'])
        driver.switch_to.default_content()

        # Autres champs
        driver.find_element(By.NAME, "price").send_keys(str(row['price']))
        driver.find_element(By.NAME, "image").send_keys(row['image'])
        driver.find_element(By.NAME, "carousel_image").send_keys(row['carousel_image'])
        Select(driver.find_element(By.NAME, "created_by")).select_by_visible_text(row['created_by'])

        # Sauvegarde
        driver.find_element(By.NAME, "_save").click()
        print(f"Ajouté : {row['name']}")

        time.sleep(1)

# Fermer
driver.quit()
