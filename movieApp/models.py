from django.db import models

# Create your models here.

class Genre(models.Model):
	name = models.CharField(max_length=10)
	description = models.TextField()

class Movie(models.Model):
	title = models.CharField(max_length=200,unique = True, db_index=True)
	director = models.CharField(max_length=200)
	imdb_score = models.FloatField(null=True, blank=True, default=None)
	genres = models.ManyToManyField(Genre)
	popularity = models.FloatField(null=True, blank=True, default=None)
	image_url = models.URLField(null=True)
	featured_image = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	movie_description = models.TextField()

	@classmethod
	def get_all_movies(self):
		return Movie.objects.all()

	@classmethod
	def get_all_movies_by_created_by(self, order="asec",limit=10):
		if order=="desc":
			return Movie.objects.order_by('-created_at')[:limit]
		return Movie.objects.order_by('-created_at')[:limit]


	@classmethod
	def get_all_featured_movies(self, limit=None):
		if limit:
			return Movie.objects.filter(featured_image=True)[:limit]
		return Movie.objects.filter(featured_image=True)

	@classmethod
	def get_movies_by_genre(self, page, limit):
		pass


