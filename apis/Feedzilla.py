import urllib2
import simplejson
import mechanize
from BeautifulSoup import BeautifulSoup
from datetime import date

#TOPICS = [1314,13,21,22,5,588,6,17,25,1168,11,14,2,28,15,33,591,20,29,36,3,10,16,18,8,34,4,27,30,31,26,23,12,7,590,9,19]
TOPICS = [21,22,5]#,588,6,17,25,1168,11,14,2,28,15,33,591,20,29,36,3,10,16,18,8,34,4,27,30,31,26,23,12,7,590,9,19]
API_URL = "http://api.feedzilla.com/v1/categories/%(topic)s/articles.json?since=%(since)s&count=%(count)s"
COUNT = 5

def collect():
	today = date.today()
	since = today.isoformat()
	articles = []
	for t in TOPICS:
		url = API_URL % {"topic": t, "since": since, "count": COUNT}
		json = urllib2.urlopen(url).read()
		api_result = simplejson.loads(json)
		i = 1
		for result in api_result["articles"]:
			print result["title"].encode("ascii", "ignore")
			real_url = get_real_url(result["url"])
			result["topic"] = t
			result["check_url"] = False
			if(real_url != None):
				result["url"] = real_url
				result["check_url"] = True
			result["search_place"] = i
			articles.append(result)
			i += 1

	return articles

def get_real_url(url):
	br = mechanize.Browser()
	html = br.open(url).read()

	soup = BeautifulSoup(html)
	meta = soup("meta", {"property": "og:url"})
	return meta[0]["content"]