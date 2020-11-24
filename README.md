# News Summarizer App using Python

News Summarizer App using <strong>Python</strong> and <strong>newspaper3k</strong> to scrape and extract the summary of news data from from a given URL using <strong>requests</strong> and transform and load the extracted data using <strong>WTforms</strong> and <strong>Flask</strong> 

<a href="https://newsdatasummaryapp.herokuapp.com/" target="_blank">View Demo</a>

## About the Project

![About the Project](images/appscreenshot.png)

Previously I built a simple <a href="https://pythonnewsscraper.herokuapp.com/" target="_blank">News Scraper APP</a> on the web using <strong>Python</strong> to scrape the latest news from a specific news site using <strong>Beautiful Soup</strong> and <strong>Flask</strong>.
                
This time, I built slightly more advanced version of the app to scrape news data from a news article using <strong>Python</strong> packages <strong>newspaper3k</strong>, then deployed the app using <strong>Flask</strong> and on <strong>heroku</strong>

First of all, when the URL link form captures the URL link of a news article, the <strong>newspaper3k</strong> package will extract and parse the data of the article.  If the form entry is not for a valid URL of a news site, the error message will appear. For form input handling and validation, I used <strong>WTForms</strong> and <strong>requests</strong> libraries to grab the URL link entered in the form. Then, from the data extracted I extract following data to render on the first part of my result page:

<strong>Title</strong><br>
<strong>Published date</strong><br>
<strong>Author</strong><br>
<strong>Top image (source link)</strong>

(*Please note **WordCloud** is currently disabled due to image storage issue) 

At the same time, using the full text of the article extracted, my app also generates <strong>WordCloud</strong> for the news article. The WordCloud on the result page will display the words that are the most frequent among the news text extracted.<strong>io</strong> library is used to keep the WordCloud image in memory and <strong>base64</strong> to convert the resulting bytes to base64 in order to return the image as part of our HTML response and render the image.
                    
Lastly <strong>newspaper3k</strong> can also run its simple natural language processing to extract keywords from the news and also produce the summary of the article text 

<strong>Keywords (WordCloud image)</strong><br>
<strong>Summary</strong><br>

Keywords(WorldCloud) image and the summary of the news text will be displayed as the second part
of the result page.

## For Deployment on Heroku

The following steps explain how to do deployment of this app on Heroku:

1. In case you do not have a `requirements.txt` file, generate one by typing in the following command in your
conda/virtual environment: `pip freeze -l > requirements.txt`

2. You may want to ensure you have the package `gunicorn==19.9.0` in the list of your requirements.

3. Make sure to include `runtime.txt` to specify the python version used for the deployment with Heroku.

4. Also be sure to include `Procfile` which contains the instructions for Heroku at the time the app will be initiated.

5. Get the [**Heroku CLI**](https://devcenter.heroku.com/articles/heroku-cli) on your local

6. On your local type in `heroku create name-of-app` (in this case we have chosen cib-news-summary to be the name of the app to be created)

7. Upon completion you should be able to see the name of the app in your heroku personal account

   ![app_created](images/heroku-app-created.PNG)
    
   nothing will be displayed in the app as we have not pushed any code to it yet.

8. In order to push your local code to heroku remote, type in `git push heroku add-model:master`. Master here is the
remote (Heroku) master. Upon completion you should be able to see your app working.

