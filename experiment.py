from GoogleNews import GoogleNews
googlenews = GoogleNews()

#googlenews.get_news('APPLE')
googlenews.search('Microsoft')
link_x = googlenews.get_links()
print(link_x)
list_ = googlenews.results()
link_0 = list_[0]['link']
#list_links = [x['link'] for x in list_]
#print(len(list_links))
print(link_0)

#googlenews.clear()