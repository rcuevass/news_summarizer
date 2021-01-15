from newsapi import NewsApiClient
from datetime import date, timedelta

# Init
newsapi_x = NewsApiClient(api_key='your_key')


# /v2/top-headlines
#top_headlines = newsapi_x.get_top_headlines(q='bitcoin',
#                                          sources='bbc-news,the-verge',
#                                          category='business',
#                                          language='en',
#                                          country='us')

todays_date = date.today()
past_date = todays_date - timedelta(3)

# /v2/everything
'''
all_articles = newsapi_x.get_everything(q='Microsoft',
                                        sources='bbc-news,the-verge,abc-news,al-jazeera-english,ars-technica,'
                                                'associated-press,axios,bloomberg,business-insider,cbc-news,cnn,'
                                                'crypto-coins-news,financial-post,google-news,google-news-ca,politico,'
                                                'reuters,the-globe-and-mail,the-wall-street-journal,'
                                                'the-washington-post,the-washington-times,wired',
                                        domains='bbc.co.uk,theverge.com,bloomberg.com',
                                        from_param=past_date,
                                        to=todays_date,
                                        #from_param='2020-11-01',
                                        #to='2020-11-20',
                                        language='en',
                                        sort_by='popularity',
                                        page=1)
'''

all_articles = newsapi_x.get_everything(q='Amazon',
                                        sources='bbc-news,abc-news,the-wall-street-journal,the-verge',
                                        domains='bbc.co.uk,bloomberg.com,theverge.com',
                                        from_param=past_date,
                                        to=todays_date,
                                        language='en',
                                        sort_by='popularity',
                                        page=1)


print(all_articles)
print(all_articles['articles'][0]['url'])

# /v2/sources
sources = newsapi_x.get_sources()['sources']
source_names = [(x['id'], x['name'], x['country']) if x['country'] in ('us','ca','uk') else None for x in sources ]

print(source_names)