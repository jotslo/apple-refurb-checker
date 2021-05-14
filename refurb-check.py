from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from webbrowser import open_new
from notify_run import Notify

found_product = False

expected_price = "£1,019.00"
expected_name = "Refurbished 13.3-inch MacBook Air Apple M1 Chip with 8‑Core CPU and 7‑Core GPU - Space Grey"
refurb_url = "https://www.apple.com/uk/shop/refurbished/mac/2020-13-inch-macbook-air"

notify = Notify()
channel = notify.register()

# output notification url, wait for user to start program
print(channel.endpoint)
input("Press any key once connected...")

# while product has not been found, keep running
while not found_product:
    # wait 5 mins, open refurb webpage via chrome and minimise
    # note: headless window appears to not work for apple website
    sleep(5 * 60)
    driver = webdriver.Chrome()
    driver.get(refurb_url)
    driver.minimize_window()

    # wait 5 seconds for data to load, then grab source
    sleep(5)
    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")

    # iterate through each product, grab data, price and title
    for product in soup.find_all("li", class_="as-producttile"):
        data = product.find("div", class_="as-producttile-info").find("h3", class_="as-producttile-title")
        price = product.find("div", class_="as-price-currentprice").text
        title = data.find("a")

        # if the product title and price match, send mobile notif and open product page
        if title.text == expected_name and price == expected_price:
            found_product = True
            notify.send("MacBook found! Page is ready.")
            open_new("https://apple.com" + title["href"])
    
    # close chrome window
    driver.quit()