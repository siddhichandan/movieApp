from django.db import models

# Create your models here.

class Genre(models.Model):
	name = models.CharField(max_length=10)
	description = models.TextField()

class Movie(models.Model):
	title = models.CharField(max_length=200,unique = True)
	director = models.CharField(max_length=200)
	imdb_score = models.FloatField(null=True, blank=True, default=None)
	genres = models.ManyToManyField(Genre)
	popularity = models.FloatField(null=True, blank=True, default=None)
	image_url = models.URLField(null=True)
	featured_image = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	movie_description = models.TextField()


