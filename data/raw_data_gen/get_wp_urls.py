"""Had to write a separate function because this takes so long to run."""

import pandas as pd
from selenium import webdriver

def get_wp_urls(min_page: int, max_page: int) -> None:
    link_dict = {}
    driver = webdriver.Chrome()
    for j in range(min_page, max_page):
        driver.implicitly_wait(3)
        web = f"https://whitepaper.io/coins?page={j}"
        for i in range(1, 11):
            try:
                driver.get(web)
                driver.implicitly_wait(3)

                button_path = f'//*[@id="whitePapersList"]/div/div[2]/table/tbody/tr[{i}]/td[2]/a/div/div[1]'  # like button element
                button_location = driver.find_element(by='xpath', value=button_path)  # find the like button
                driver.execute_script("arguments[0].click();", button_location)  # click on like
                driver.implicitly_wait(3)

                button_path = '//*[@id="coin-view"]/div[1]/div[1]/div[1]/div[1]/div/div/div[3]/div/div/div/div[4]/a'  # like button element
                button_location = driver.find_element(by='xpath', value=button_path)  # find the like button
                driver.execute_script("arguments[0].click();", button_location)  # click on like
                driver.implicitly_wait(3)

                url = driver.current_url
                link_dict.update({url[url.rfind("/") + 1:url.rfind("whitepaper") - 1].replace("-", "_"): url})
            except:
                pass

            print(f"Page: {j}, url: {url})")

    # Make a df with all the scraped links
    wp_url_df = pd.DataFrame({'name': link_dict.values(), 'raw_wp_url': link_dict.keys()})
    # Write results to a csv so I don't have to run this again
    wp_url_df.to_csv(f"wp_url_df_{min_page}_{max_page}.csv")

min = input("Enter minimum page:")
max = input("Enter maximum page:")

get_wp_urls(int(min), int(max))
