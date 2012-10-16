from visualization.models import Cluster, Article
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
	args = 'none'
	help = 'Task for deleting news'

	def handle(self, *args, **options):
		for c in Cluster.objects.all():
			c.delete()
		for a in Article.objects.all():
			a.delete()
		self.stdout.write('Successfully deleted news')