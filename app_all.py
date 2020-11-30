from flask import Flask, render_template, request
from GoogleNews import GoogleNews
from newsapi import NewsApiClient
from utils.logging import get_log_object
from utils.get_credentials import get_api_news_credential
from utils.process_url import ContentFromURL
from datetime import date, timedelta
from forms import UrlSearchForm
import sys

# The following import is used the first time to extract data from NLTK and place it
# under the ./nltk_data folder.
# import nltk
# nltk.data.path.append('./nltk_data/')

# Instantiate the app with Flask
app = Flask(__name__)

# get token for APINews
api_key_val = get_api_news_credential()
newsapi_val = NewsApiClient(api_key=api_key_val)
# get todays's date and, from it, get the date corresponding to three days prior to it
todays_date = date.today()
past_date = todays_date - timedelta(1)

# instantiate logging object
log = get_log_object()


# set GET and POST methods for the app
@app.route('/', methods=["GET", "POST"])
def index():
    errors = []
    url_search = UrlSearchForm(request.form)
    log.info('URL to be processed=%s', url_search.data['search'])

    # to display results (POST)
    if request.method == "POST":

        try:
            results_from_req = search_results(url_search)
            log.info('Returning results of the request')
            return results_from_req

        except:
            errors.append(
                "Unable to process request. This event has been logged and it will be tackled in next release"
            )
            log.info('It was not possible to process this URL=%s', url_search.data['search'])
    return render_template("index.html", form=url_search, errors=errors)


def search_results(input_):
    url_search_news = UrlSearchForm(request.form)
    search_string = url_search_news.data['search']
    log.info('String to be processed=%s', search_string)
    log.info('First four characters of the request=%s', search_string[:4])

    # initialize value for search_url
    search_url = None

    # if string provided is candidate to be a URL...
    if search_string[:4] == 'http':
        log.info('Candidate to URL has be provided directly...')
        url_search_news = UrlSearchForm(request.form)
        search_url = url_search_news.data['search']
        log.info('URL to be processed=%s', search_url)
        log.info('Final URL searched=%s', search_url)

    else:
        log.info('An open string has been provided in the search bar...')
        try:
            all_articles = newsapi_val.get_everything(q=search_string,
                                                      sources='bbc-news, the-verge, abc-news, al-jazeera-english,'
                                                              'ars-technica, associated-press, axios,bloomberg,'
                                                              'business-insider, cbc-news, cnn, crypto-coins-news,'
                                                              'financial-post, google-news, google-news-ca, politico,'
                                                              'reuters, the-globe-and-mail, the-wall-street-journal,'
                                                              'the-washington-post, the-washington-times, wired',
                                                      domains='bbc.co.uk, theverge.com, bloomberg.com, nytimes.com,'
                                                              'bnnbloomberg.ca',
                                                      from_param=past_date,
                                                      to=todays_date,
                                                      language='en',
                                                      sort_by='relevancy',
                                                      page=1)
            log.info('Articles have been obtained by means of newsAPI')

            # get total number of articles found
            tot_num_articles = len(all_articles['articles'])
            log.info('Total number of articles found=%i based on search=%s', tot_num_articles, search_string)
            # if call successful and at least one article was found...
            if (all_articles['status'] == 'ok') & (tot_num_articles >= 1):
                # get top 5 news
                top_n_news = all_articles['articles'][:5]
                # log info about URLs
                log.info('Query requested=%s', search_string)
                # initialize list of dictionaries
                list_news_dictionaries = []
                for k, news_ in zip(range(len(top_n_news)), top_n_news):
                    kth_url = news_['url']
                    log.info('URL number=%i from NewsAPI=%s', k+1, kth_url)
                    kth_article_obj = ContentFromURL(kth_url)
                    # get attributes from kth class
                    title_ = kth_article_obj.article_title()
                    log.info('Article title=%s', title_)
                    date_ = kth_article_obj.article_date()
                    log.info('Date article=%s', str(date_))
                    summary_ = kth_article_obj.article_summary()
                    log.info('Summary=%s', summary_)
                    author_ = kth_article_obj.article_author()
                    log.info('Author=%s', author_)
                    url_image_ = kth_article_obj.url_top_image()
                    log.info('URL image=%s', url_image_)
                    key_words_ = kth_article_obj.article_keywords()
                    log.info('Key words=%s', str(key_words_))
                    dict_aux = {'url': kth_url, 'title': title_, 'date': date_, 'author': author_,
                                'url_image': url_image_, 'summary': summary_, 'key_words': key_words_}
                    list_news_dictionaries.append(dict_aux)
                    log.info("==============================================================================")


                # replace search_url with search_string
                # list_search_string = top_5_news


            else:
                log.info('Not relevant result were found from the query %s= ', search_string)

        except:
            log.info('It is likely you have made too many requests recently. Developer accounts are limited to 100')
            log.info('requests over a 24 hour period (50 requests available every 12 hours). Please upgrade to a paid')
            log.info('plan if you need more requests.')


    # render results
    return render_template("results_all_news.html",
                           list_news_dictionaries=list_news_dictionaries)


if __name__ == '__main__':
    app.run()
