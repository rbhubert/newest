import newspaperClarin
import newspaperPagina12
import newspaper_FBPlugin
from enums.newsItem import NewsItem
from structureNewItem import structureNewItem


# Identify the newspaper and then scraps the corresponding online newspaper.
# Returns the structured newItem
def get_newItem(new_url):
    # do some identification of newspaper with first part of url...
    str_page = new_url.split("www.")[1].split(".com")[0]

    if str_page == "pagina12":
        new_item = newspaperPagina12.getNewItem_Pagina12(new_url)
    elif str_page == "clarin":
        new_item = newspaperClarin.getNewItem_Clarin(new_url)
    elif str_page == "lanueva":
        basicInfo = newspaper_FBPlugin.getBasicInfo_LaNueva(new_url)
        comments = newspaper_FBPlugin.getComments_FBPlugin(new_url)

        # todo get content and text
        new_item = structureNewItem(new_url=new_url, new_title=basicInfo["title"], new_content=[], new_text="",
                                    new_creation_time=basicInfo["creation_time"], comments=comments[0],
                                    last_id_comment=comments[1])
    elif str_page == "cbc":
        new_item = None
        pass
    else:
        comments = newspaper_FBPlugin.getComments_FBPlugin(new_url)
        new_item = structureNewItem(new_url, "", "", comments[0], comments[1])

    return new_item


# Identify the newspaper and scraps for the latest comments to that newItem.
def get_latestComments(newItem):
    since_id = newItem[NewsItem.LAST_COMMENT]
    str_page = newItem[NewsItem.URL].split("www.")[1].split(".com")[0]

    if str_page == "pagina12":
        latestComments = newspaperPagina12.getLatestComments_Pagina12(newItem, since_id)
    elif str_page == "clarin":
        latestComments = newspaperClarin.getLatestComments_Clarin(newItem, since_id)
    elif str_page == "cbc":
        latestComments = None
        pass
    else:
        latestComments = newspaper_FBPlugin.getComments_FBPlugin(newItem[NewsItem.URL],
                                                                 since_id)

    return latestComments

# get_newItem("https://www.pagina12.com.ar/244720-crimen-de-villa-gesell-en-el-penal-de-dolores-a-los-10-rugbi")
# get_newItem("https://www.clarin.com/politica/alberto-fernandez-descarto-hablar-aborto-francisco-temas-importantes-_0_-UfpKgHr.html")
# get_newItem("https://www.lanueva.com/nota/2019-9-12-20-2-0-actrices-argentinas-realizo-una-nueva-denuncia-de-acoso-sexual-en-el-ambiente-artistico")
