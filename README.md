# newest
newest allows you to recover the information and the comments associated with a news item in a digital newspaper. Implemented in Python and using Selenium as scraper tool, newest can scrap information from the following digital newspapers: [Clarín](https://www.clarin.com/), [Pagina12](https://www.pagina12.com.ar/), [CBC Canada](https://www.cbc.ca/), and [LaNueva](https://www.lanueva.com/). In particular, LaNueva uses the Facebook plugin to allow its users to comment on the web.

### Requirements
```
- psutil === 5.7.2
- selenium === 3.141.0
- python-dateutil === 2.8.1
- tldextract === 2.2.3
- validators === 0.18.1
```

# CLI Usage

You can use newest with an URL running the following commands:
```
cd /path/to/newest/
./main.py -url www.someurl.com
```

or maybe you are interested in getting the latest comments in that news item:

```
cd /path/to/newest/
./main.py -url www.someurl.com -lastComment 213112
```

where `213112` is the ID of the last comment in _someurl.com_.

# Information retrieved

After running the command, you will received the content of the news item structured as follows:
```
{
    URL: news_url,
    TITLE: news_title,
    CONTENT_STRUCTURED: news_content,
    CONTENT_TEXT: news_text,
    CREATION_TIME: news_creation_time,
    COMMENTS: comment_list,
    LAST_COMMENT: last_id_comment
}
```

where each comment in comment_list is structured in this way:
```
{
    ID: comment_id,
    TEXT: comment_text,
    USERNAME: user_username,
    CREATION_TIME: time_comment,
    LIKES: number_likes,
    DISLIKES: number_dislikes,
    REPLIES: comment_list
}
```
