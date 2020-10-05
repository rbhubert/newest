import time
from contextlib import closing
from datetime import datetime

import psutil
from selenium.webdriver import Firefox, FirefoxOptions

from enums.newsItem import NewsItem
from structureNewItem import structureComment

# TODO news title and creationtime of newspapers using FBPlugin


MACOS_ = ""
WINDOWS_ = ""
LINUX_ = ""
GECKODRIVER_PATH_BASE = "./geckodriver/"
GECKODRIVER_PATH = GECKODRIVER_PATH_BASE + "geckodriver_windows.exe"

# Identification of the SO to select and use the appropiate geckodriver to scrap the newspapers.
if psutil.MACOS:
    GECKODRIVER_PATH = GECKODRIVER_PATH_BASE + "geckodriver_macos"
elif psutil.LINUX:
    GECKODRIVER_PATH = GECKODRIVER_PATH_BASE + "geckodriver_linux"

options = FirefoxOptions()
options.add_argument('--headless')


# Scraps for the title and creationDate of the new for newspaper LaNueva.
def getBasicInfo_LaNueva(new_url):
    # todo get content and text

    with closing(Firefox(firefox_options=options, executable_path=GECKODRIVER_PATH)) as browser:
        browser.get(new_url)

        title = browser.find_element_by_css_selector("h2[itemprop='headline']").get_attribute(
            "textContent")
        creation_time_str = browser.find_element_by_class_name("fecha").get_attribute(
            "textContent")
        creation_time = datetime.strptime(creation_time_str, "%d/%m/%Y | %H:%M |")

    return {"title": title, "creation_time": creation_time}


# Scraps the webpage _news_url_ and get all the comments associated to this new.
def getComments_FBPlugin(news_url, since_id=None):
    with closing(Firefox(firefox_options=options,
                         executable_path=GECKODRIVER_PATH)) as browser:
        browser.get(news_url)

        time.sleep(1)

        comments_fbPlugin = []
        frames = browser.find_elements_by_tag_name("iframe")

        for fr in frames:
            if fr.get_attribute("title") == "fb:comments Facebook Social Plugin":
                browser.get(fr.get_attribute("src"))
                # browser.switch_to.frame(fr.get_attribute("name"))
                break

        last_id_comment = ""
        comments = browser.find_element_by_tag_name("body").find_elements_by_class_name("_5nz1")
        for comment_body in comments:
            comment_struc = __structureComment(comment_body)

            comment_id = comment_struc[NewsItem.Comments.ID]
            if last_id_comment == "":
                last_id_comment = comment_id

            if comment_id == since_id:
                break
            replies = []
            replies_uns = comment_body.find_elements_by_class_name("_44ri")

            for reply in replies_uns:
                reply_struc = __structureComment(reply)
                replies.append(reply_struc)

            comment_struc["replies"] = replies
            comments_fbPlugin.append(comment_struc)

    return (comments_fbPlugin, last_id_comment)


# Returns the comment structured.
def __structureComment(comment_body):
    comment_id = comment_body.find_element_by_class_name("img").get_attribute("src").split("&oh=")[1].split("&oe=")[0]
    text = comment_body.find_element_by_class_name("_5mdd").get_attribute("textContent")  # text
    # section of likes and creation date
    section = comment_body.find_element_by_class_name("_2vq9").get_attribute("textContent").split("·")

    if len(section) == 3:
        likes = 0
    else:
        likes = section[2]

    time_utime = comment_body.find_element_by_class_name("livetimestamp").get_attribute("data-utime")
    time_comment = datetime.fromtimestamp(int(time_utime))

    comment_struc = structureComment(comment_id=comment_id, username="", text=text, time_comment=time_comment,
                                     likes=int(likes), dislikes=0)
    return comment_struc
