from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views import View
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.template.loader import render_to_string
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from movieApp.models import Movie
from movieApp.models import Genre
from movieApp.forms import movieForm,genreForm,UserLoginForm,UserRegistraterForm
from movieApp.Utility.utils import Utils


import json
import os

def loginView(request):
	form = UserLoginForm(request.POST or None)
	title = "Login"
	next = request.GET.get('next')
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		login(request, user)
		if next:
			return redirect(next)
		return redirect("/")
	
	path = os.path.join(
		os.path.dirname(__file__),
			'templates/movieApp/form.html'
		)
	template_values = {"form": form, "title": title }
	template_values = Utils.template_vals_with_web_costants(
			template_values,
			'Movie99'
	)
	return render(request, path, template_values)

def logoutView(request):
	logout(request)
	return redirect("/")

def registerView(request):
	title = 'Register'
	form = UserRegistraterForm(request.POST or None)
	next = request.GET.get('next')
	if form.is_valid():
		user = form.save(commit=False) 
		password = form.cleaned_data.get("password")
		user.set_password(password)
		user.save()
		new_user = authenticate(username=user.username, password=password)
		login(request,user)
		g = Group.objects.get(name='User') 
		g.user_set.add(user)

		if next:
			return redirect(next)
		return redirect("/")

	path = os.path.join(
		os.path.dirname(__file__),
			'templates/movieApp/form.html'
		)
	template_values = {"form": form, "title": title }
	template_values = Utils.template_vals_with_web_costants(
			template_values,
			'Movie99'
	)
	return render(request, path, template_values)


@method_decorator(csrf_exempt, name='dispatch')
class MainView(View):

	def get(self,request):
		
		dataset = Movie.objects.all()
		movies = []
		for movie in dataset:
			new_movie = {}
			new_movie['image_url'] = movie.image_url
			new_movie['open_link'] = reverse('movieDetail',args=(movie.id,))
			movies.append(new_movie)

		print(movies)
		template_values = {
			'movie_list': movies,
			'template_type': 'main'
		}
		template_values = Utils.template_vals_with_web_costants(
			template_values,
			'Movie99'
		)
		path = os.path.join(
		os.path.dirname(__file__),
			'templates/movieApp/index.html'
		)

		return render(request, path, template_values)

#@method_decorator(csrf_exempt, name='dispatch')
class MoviesView(LoginRequiredMixin, View):

	login_url = '/login/'
	def get(self,request):
		form = movieForm()
		return render(request, 'movieApp/addMovie.html', {'form': form})

	def post(self,request):
		form = movieForm(request.POST)

		if not form.is_valid():
			print(form.errors)
			return HttpResponse(json.dumps(Utils.create_error_payload("Form not correct",form.errors)))

		cd = form.cleaned_data
		movie = Movie()
		response = {}
		try:

			movie.title = cd['title']
			movie.director = cd['director']
			movie.imdb_score = cd['imdb_score']
			movie.popularity = cd['popularity']
			movie.image_url = cd['image_url']

			movie.save()

			print(cd['geners'])
			for gen in cd['geners']:
				g = Genre.objects.get(name=gen)
				print(g)
				movie.genres.add(g)
			
			movie.save()
			response = {
				'message': 'Movie Successfully Added to the database',
				'movieId':movie.id
			}
			response = Utils.create_success_payload(response)
		except Exception :
			print("In exception")
			response = Utils.create_error_payload()

		print(response)

		return HttpResponse(json.dumps(response))

@method_decorator(csrf_exempt, name='dispatch')
class GenreView(View):

	def get(self, request):
		form = genreForm()
		return render(request, 'movieApp/addMovie.html', {'form': form})

	def post(self, request):
		form = genreForm(request.POST)

		if not form.is_valid():
			print(form.errors)
			return HttpResponse(Utils.create_error_payload("Form not correct", form.errors))

		response = {}
		try:
			form.save()
			response = {
				'message': 'Genre Successfully Added to the database'
			}
			response = Utils.create_success_payload(response)
		except Exception:
			response = Utils.create_error_payload()

		return HttpResponse(json.dumps(response))


@method_decorator(csrf_exempt, name ='dispatch')
class MovieListView(ListView):
		#model = Movie
		#paginate_by = 10
		context_object_name = 'movie_list'
		template_name = os.path.join(
		os.path.dirname(__file__),
			'templates/movieApp/layout/content/movie_dashboard.html'
		)

		def get_queryset(self):
			limit = self.kwargs.get('limit')
			featured = self.kwargs.get('featured')
			try:
				limit = int(limit)
			except Exception:
				limit = 0

			if limit == 0 and not featured:
				return None

			if limit > 0:
				return  Movie.get_all_movies_by_created_by("desc",10)
			else:
				return Movie.get_all_featured_movies(limit=3)
			

@method_decorator(csrf_exempt, name = 'dispatch')
class MovieDetailView(View):
	
	def get(self, request, movieId=None, movieName=None, jsonResponse=None):

		print(movieId)
		print(movieName)
		print(jsonResponse)

		try:
			movieId = int(movieId)
		except Exception:
			movieId = None

		try:
			movieName = str(movieName)
		except exception:
			movieName = None

		if not movieName and not movieId:
			movie = None

		if movieName or movieId:
			try:
				if movieId:
					movie = Movie.objects.get(pk = movieId)
				else:
					print("name")
					movie = Movie.objects.get(title__icontains = movieName) 
				print(movie)
				template_values = {
					'template_type': 'movieView'
				}
				template_values = Utils.template_vals_with_web_costants(
					template_values,
					'Movie99'
				)
				path = os.path.join(
				os.path.dirname(__file__),
					'templates/movieApp/index.html'
				)
				genre_list = []
				for genre in movie.genres.all():
					genre_list.append(genre.name)

				print(genre_list)

				genre_string = "/".join(genre_list) if genre_list else ""
			except Exception:
				movie = None

		if jsonResponse=='json':
			if not movie:
				return HttpResponse(json.dumps(Utils.create_error_payload(message="No Movie Found")))

			response = {
				'title': movie.title,
				'director': movie.director,
				'genre_string':genre_string,
				'imdb_score': movie.imdb_score
			}
			response = Utils.create_success_payload(response)
			return HttpResponse(json.dumps(response))

		template_values = {
				'template_type': 'movieView',
				'movie': movie,
				'genre_string': genre_string if movie else ""
			}

		template_values = Utils.template_vals_with_web_costants(
			template_values,
			'Movie99'
		)
		path = os.path.join(
		os.path.dirname(__file__),
			'templates/movieApp/index.html'
		)

		return render(request, path, template_values)
