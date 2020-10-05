from enums.newsItem import NewsItem


# Structures a new item, with its url, title, creation date and comments and emotions associated to it.
def structureNewItem(new_url, new_title, new_content, new_text, new_creation_time, comments, last_id_comment):
    newItem = {
        NewsItem.URL: new_url,
        NewsItem.TITLE: new_title,
        NewsItem.CONTENT_STRUCTURED: new_content,
        NewsItem.CONTENT_TEXT: new_text,
        NewsItem.CREATION_TIME: new_creation_time,
        NewsItem.COMMENTS: comments,
        NewsItem.LAST_COMMENT: last_id_comment
    }

    return newItem


def structureComment(comment_id, username, text, time_comment, likes, dislikes, replies=None):
    if replies is None:
        replies = []

    comment_struc = {
        NewsItem.Comments.ID: comment_id,
        NewsItem.Comments.TEXT: text,
        NewsItem.Comments.USERNAME: username,
        NewsItem.Comments.CREATION_TIME: time_comment,
        NewsItem.Comments.LIKES: likes,
        NewsItem.Comments.DISLIKES: dislikes,
        NewsItem.Comments.REPLIES: replies
    }

    return comment_struc
