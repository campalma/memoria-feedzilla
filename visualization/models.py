from django.db import models

# APIS
from apis import Feedzilla
from apis import Placemaker
from webarticle2text import extractFromURL
# Date management
import pytz
from datetime import datetime, date
from email.utils import mktime_tz, parsedate_tz

class Continent(models.Model):
	name = models.CharField(max_length=100)

class Location(models.Model):
	name = models.CharField(max_length=100)

class Topic(models.Model):
	name = models.CharField(max_length=100)
	short_name = models.CharField(max_length=500)
	color = models.CharField(max_length=7)

	@staticmethod
	def get_excluded_topics(get_request):
		topics = Topic.objects.all()
		excluded = []
		for t in topics:
			if not (t.short_name in get_request):
				excluded.append(t)
		return excluded

class Cluster(models.Model):
	display_name = models.CharField(max_length=500)
	relevancy = models.IntegerField()
	topic = models.ForeignKey(Topic)
	location = models.ManyToManyField(Location)
	continent_location = models.ManyToManyField(Continent)
	added_date = models.DateTimeField(auto_now_add=True)
	date = models.DateTimeField()

class Article(models.Model):
	title = models.CharField(max_length=500)
	url = models.URLField(max_length=500)
	publisher = models.CharField(max_length=200)
	content = models.CharField(max_length=1000)
	published_date = models.DateTimeField()
	added_date = models.DateTimeField(auto_now_add=True)
	cluster = models.ForeignKey(Cluster)

	@staticmethod
	def collect_with_feedzilla():
		news = Feedzilla.collect()
		for n in news:
			cluster = Cluster()
			cluster.display_name = n["title"]
			cluster.relevancy = 1.0/n["search_place"]*100
			cluster.topic = Topic.objects.get(short_name=str(n["topic"]))
			cluster.date = format_date(n["publish_date"])
			cluster.save()
			if(n["check_url"]):
				try:
					cluster_content = extractFromURL(n["url"])
					cluster_countries = Placemaker.get_countries_from_string(cluster_content)
					for country in cluster_countries:
						try:
							l = Location.objects.get(name=country)
						except Location.DoesNotExist:
							l = Location()
							l.name = country
							l.save()
						cluster.location.add(l)

					cluster_continents = Placemaker.get_continents_from_countries(cluster_countries)
					for continent in cluster_continents:
						try:
							c = Continent.objects.get(name=continent)
						except Continent.DoesNotExist:
							c = Continent()
							c.name = continent
							c.save()
						cluster.continent_location.add(c)
				except TypeError:
					print "webarticle2text Error"


			a = Article()
			a.title = n["title"]
			a.url = n["url"]
			a.publisher = n["source"]
			a.content = n["summary"][:999]
			a.published_date = format_date(n["publish_date"])
			a.cluster = cluster
			a.save()

def format_date(google_date):
	dt = datetime.fromtimestamp(mktime_tz(parsedate_tz(google_date)), pytz.utc)
	return dt.strftime('%Y-%m-%d %H:%M:%S')

