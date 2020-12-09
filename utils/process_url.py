from newspaper import Article
from textblob import TextBlob
from logging import getLogger

log_url = getLogger()


class ContentFromURL:
    def __init__(self, url_str: str, image_url: str = None, article_title_text: str = None,
                 article_date_=None, author_: str = None, keywords_: list = None,
                 summary_: str = None,
                 sentiment_value: float = None,
                 sentiment_subjectivity: float = None):

        # initialize values
        self.url_str = url_str
        self.image_url = image_url
        self.article_title_text = article_title_text
        self.article_date_ = article_date_
        self.author_ = author_
        self.keywords_ = keywords_
        self.summary_ = summary_
        self.sentiment_value = sentiment_value
        self.sentiment_subjectivity = sentiment_subjectivity

        log_url.info('Instantiating Article object')
        self.article = Article(self.url_str)
        log_url.info('Article instantiated')
        # download article
        self.article.download()
        log_url.info('Article downloaded')
        # parse article...
        self.article.parse()
        log_url.info('Article parsed')
        # processing article via NLP
        self.article.nlp()
        log_url.info('Article processed via NLP method')

    def url_top_image(self):
        # get top image
        self.image_url = self.article.top_image
        log_url.info('URL to image=%s', str(self.image_url))
        return self.image_url

    def article_title(self):
        # get article title
        self.article_title_text = self.article.title
        log_url.info('Article title=%s', str(self.article_title_text))
        return self.article_title_text

    def article_date(self):
        # get date
        article_date_aux = self.article.publish_date

        log_url.info('Date from Article class=%s', article_date_aux)
        if not bool(article_date_aux):
            self.article_date_ = 'Not specified'
            log_url.info(
                'Published date was not originally specified in article - it has been replaced to Not Specified')
        else:
            self.article_date_ = article_date_aux.strftime("%d %B %Y")

        log_url.info('Published date=%s', self.article_date_)

        return self.article_date_

    def article_author(self) -> str:
        try:
            # get author from article if possible...
            self.author_ = self.article.authors[0]

        except:
            # otherwise change it to Not specified
            self.author_ = 'Not specified'

        return self.author_

    def article_keywords(self) -> list:
        # get article keywords and summary
        self.keywords_ = self.article.keywords
        log_url.info('Keywords gathered')
        log_url.info('Keywords found=%s', str(self.keywords_))
        return self.keywords_

    def article_summary(self) -> str:
        self.summary_ = self.article.summary
        log_url.info('Summary obtained')
        return self.summary_

    def summary_sentiment(self) -> tuple:
        sentiment_subjectivity = TextBlob(self.summary_).sentiment
        self.sentiment_value = sentiment_subjectivity.polarity
        self.sentiment_subjectivity = sentiment_subjectivity.subjectivity
        if self.sentiment_value > 0:
            return 'Positive', round(self.sentiment_value, 2), round(self.sentiment_subjectivity, 2)
        elif self.sentiment_value < 0:
            return 'Negative', round(self.sentiment_value, 2), round(self.sentiment_subjectivity, 2)
        else:
            return 'Neutral', round(self.sentiment_value, 2), round(self.sentiment_subjectivity, 2)
