from newsapi import NewsApiClient

# Init
newsapi_x = NewsApiClient(api_key='your_key')


# /v2/top-headlines
#top_headlines = newsapi_x.get_top_headlines(q='bitcoin',
#                                          sources='bbc-news,the-verge',
#                                          category='business',
#                                          language='en',
#                                          country='us')

# /v2/everything
all_articles = newsapi_x.get_everything(q='Microsoft',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      from_param='2020-11-01',
                                      to='2020-11-20',
                                      language='en',
                                      sort_by='popularity',
                                      page=1)
print(all_articles)

# /v2/sources
sources = newsapi_x.get_sources()['sources']
source_names = [(x['name'], x['country']) for x in sources]

print(source_names)