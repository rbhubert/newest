import time
from contextlib import closing

import psutil
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait

MACOS_ = ""
WINDOWS_ = ""
LINUX_ = ""
GECKODRIVER_PATH_BASE = "./geckodriver/"
GECKODRIVER_PATH = GECKODRIVER_PATH_BASE + "geckodriver_windows.exe"

# Identification of the SO to select and use the appropiate geckodriver to scrap the newspapers.
if psutil.MACOS:
    GECKODRIVER_PATH = GECKODRIVER_PATH_BASE + "geckodriver_macos"
elif psutil.LINUX:
    GECKODRIVER_PATH = GECKODRIVER_PATH_BASE + "geckodriver_linux.exe"

options = FirefoxOptions()
options.add_argument('--headless')


def google_news(newspaper_site, place, keywords, since):
    newsList = []
    # this file will have every new url from SITE with the KEYWORD
    file = open("news_{site}_{keyword}.txt".format(site=newspaper_site, keyword=keywords), "a", encoding='utf-8')

    with closing(Firefox(firefox_options=options,
                         executable_path=GECKODRIVER_PATH)) as browser:
        wait = WebDriverWait(browser, timeout=10)

        # https://google.com/search?q=<Query>&filter=0
        # filter=0 es para que no se omitan resultados
        query = "site:" + newspaper_site + " " + place + " " + keywords
        news_url = "https://google.com/search?q={query}&filter=0&start={since}".format(query=query, since=since)
        browser.get(news_url)

        while True:
            try:
                all_results_in_page = browser.find_elements_by_class_name("g")
                for result in all_results_in_page:
                    result_href = result.find_element_by_class_name("rc").find_element_by_class_name(
                        "r").find_element_by_tag_name("a").get_attribute("href")
                    newsList.append(result_href)
                    file.write(result_href + "\n")

                nextPage = wait.until(
                    lambda x: browser.find_element_by_id(
                        "pnnext"))
                nextPage.click()
                time.sleep(10)
            except NoSuchElementException:
                break
            except TimeoutException:
                break

    file.close()
    return newsList


# todo recover from links/urls...
def recover_from_links(news_items):
    pass


# SEARCH DONE MARCH 29, 2020

# # classify as immigration policies
# google_news("cbc.ca", "nova scotia", "immigration system barriers", 250)
# google_news("cbc.ca", "nova scotia", "immigration system integration", 0)
# google_news("cbc.ca", "nova scotia", "immigration system population growth")
#
# # classify as immigration policies
# google_news("cbc.ca", "nova scotia", "immigration policies barriers")
# google_news("cbc.ca", "nova scotia", "immigration policies integration")
# google_news("cbc.ca", "nova scotia", "immigration policies population growth")

# classify as economic impact
# google_news("cbc.ca", "nova scotia", "economic impact (immigration OR immigrant)",0)

# # classify as health care system
# google_news("cbc.ca", "nova scotia", "health care system (immigration OR immigrant)")
#
# # classify as education system
# google_news("cbc.ca", "nova scotia", "education system (immigration OR immigrant)")
#
#
# # other possible classification is 'other'
