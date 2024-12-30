import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import discord
import pdb

config = configparser.ConfigParser()
config.read('config.ini')
CHANNEL_ID = int(config['credentials']['channel_id'])
BOT_TOKEN = config['credentials']['discordbottoken']
USERNAME = config['credentials']['username']
PASSWORD = config['credentials']['password']
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send('You have a turn to play!')

    await client.close()


def check_website():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    
    try:
        url = "https://en.boardgamearena.com/account"
        driver.get(url)
        time.sleep(4)

        # Wait for and fill username
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Email or username']"))
        )
        username_field.send_keys(USERNAME)

        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Next"))
        )
        next_button.click()
        
        time.sleep(2)
        all_password_fields = driver.find_elements(By.CSS_SELECTOR, "input[type='password']")
        clickable_pwd_fields = [field for field in all_password_fields if field.is_displayed()]

        clickable_pwd_fields[0].send_keys(PASSWORD)
        
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Login"))
        )
        login_button.click()

        # wait here for a second
        time.sleep(1)

        driver.get("https://boardgamearena.com/gameinprogress#section-waiting")
        
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "section-waiting"))
        )

        if ("You are up to date" in element.text):
            client.run(BOT_TOKEN)
            return
        
        client.run(BOT_TOKEN)

    finally:
        driver.quit()

check_website()
