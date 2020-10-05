from contextlib import closing
from datetime import datetime, timedelta

import psutil
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait

from enums.newsItem import NewsItem
from structureNewItem import structureNewItem, structureComment

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


# Scraps the webpage _news_url_ and get all the comments associated to this new.
def getNewItem_Clarin(news_url):
    with closing(Firefox(firefox_options=options,
                         executable_path=GECKODRIVER_PATH)) as browser:
        browser.get(news_url)

        title = browser.find_element_by_id("title").get_attribute("textContent")
        creation_time_section = browser.find_element_by_class_name("breadcrumb").find_element_by_tag_name("span")
        creation_time_str = creation_time_section.get_attribute("textContent").strip()
        creation_time = datetime.strptime(creation_time_str, "%d/%m/%Y - %H:%M")

    pairResult = __getComments_Clarin(news_url, creation_time, None)
    comments_Clarin = pairResult[0]
    last_id_comment = pairResult[1]

    # todo content and text
    return structureNewItem(new_url=news_url, new_title=title, new_content=[], new_text="",
                            new_creation_time=creation_time,
                            comments=comments_Clarin, last_id_comment=last_id_comment)


# Gets the latest comments made in the newItem (since since_id)
def getLatestComments_Clarin(newItem, since_id):
    comments = __getComments_Clarin(newItem[NewsItem.URL], newItem[NewsItem.CREATION_TIME],
                                    since_id)
    return comments


# Scrap the comments_url to get the comments made in the new.
def __getComments_Clarin(comments_url, creation_time, since_id=None):
    comments_Clarin = []

    with closing(Firefox(firefox_options=options,
                         executable_path=GECKODRIVER_PATH)) as browser:
        wait = WebDriverWait(browser, timeout=10)

        browser.get(comments_url)

        try:
            activate_button = wait.until(
                lambda x: browser.find_element_by_id("activateComments"))
            activate_button.click()
        except TimeoutException:
            pass
        except ElementNotInteractableException:
            pass

        while True:
            try:
                more_button = wait.until(
                    lambda x: browser.find_element_by_class_name("gig-comments-more"))
                more_button.click()
            except TimeoutException:
                break
            except ElementNotInteractableException:
                break

        wait.until(lambda comments: browser.find_elements_by_class_name("gig-comment"))

        last_id_comment = ""
        comments = browser.find_elements_by_class_name("gig-comment")

        for comment_body in comments:
            comment_id = comment_body.get_attribute("data-comment-id")
            if last_id_comment == "":
                last_id_comment = comment_id

            if comment_id == since_id:
                break

            text = comment_body.find_element_by_class_name("gig-comment-body").get_attribute("textContent")  # text
            likes = int(
                comment_body.find_element_by_class_name("gig-comment-vote-pos").get_attribute("textContent"))  # pos
            dislikes = int(
                comment_body.find_element_by_class_name("gig-comment-vote-neg").get_attribute("textContent"))  # neg
            time_str = comment_body.find_element_by_class_name("gig-comment-time").get_attribute(
                "textContent").split()  # time

            if len(time_str) > 3:
                time_comment = creation_time
            else:
                time_number = int(time_str[1])
                time_lapse = time_str[2]
                if time_lapse[0] == "m":  # m(inutes)
                    time_comment = creation_time
                else:  # time_lapse[0] == "d" # d(days)
                    time_comment = datetime.today() - timedelta(days=time_number)

            # todo username and improve comments... all thread...
            comment_struc = structureComment(comment_id=comment_id, username="", text=text, time_comment=time_comment,
                                             likes=likes, dislikes=dislikes)

            level = int(comment_body.get_attribute("data-level"))
            if level == 0:
                comments_Clarin.append(comment_struc)
            else:
                comments_Clarin[-1]["replies"].append(comment_struc)

    return (comments_Clarin, last_id_comment)


# structNew = getNewItem_Clarin(
#     news_url="https://www.clarin.com/economia/2021-presion-tributaria-llegara-24-8-pbi-alta-anos_0_a6KiCiEYL.html")
#
# print(structNew)
