import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import discord

CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
BOT_TOKEN = os.getenv('BOT_TOKEN')
USERNAME = os.getenv('BGA_USERNAME')
PASSWORD = os.getenv('BGA_PASSWORD')
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

                # Wait for and fill username
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username_input"))
        )
        username_field.send_keys(USERNAME)
        
        password_field = driver.find_element(By.ID, "password_input")
        password_field.send_keys(PASSWORD)
        
        login_button = driver.find_element(By.ID, "submit_login_button")
        login_button.click()

        # wait here for a second
        time.sleep(1)

        driver.get("https://boardgamearena.com/gameinprogress#section-waiting")
        
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "section-waiting"))
        )

        if ("You are up to date" in element.text):
            return
        
        client.run(BOT_TOKEN)

    finally:
        driver.quit()

check_website()
