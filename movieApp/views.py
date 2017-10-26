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
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.urls import reverse
from django.core.paginator import Paginator
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
		
		dataset = Movie.get_all_movies_created_by("desc",4)
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

class ReviewView(View):

	def get(self, request, genre='HORROR'):

		CHOICES={
			'HORROR':'HORROR',
        	'COMEDY':'COMEDY',
        	'ACTION':'ACTION',
        	'ANIMATED':'ANIMATED'
        }
        

		movies = Movie.get_movies_by_genre(genre)
		genres = Genre.objects.all()

		page = request.GET.get('page', 1)
		paginator = Paginator(movies, 4)
		try:
			movie_list = paginator.page(page)
		except PageNotAnInteger:
			movie_list = paginator.page(1)
		except EmptyPage:
			movie_list = paginator.page(paginator.num_pages)

		template_values = {
			'template_type': 'reviewList',
			'movie_list': movie_list,
			'choices':CHOICES,
			'review_url':reverse("reviewPage"),
			'genre_selected':genre,
			'edit_get_url': '/add/movie/'
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


@method_decorator(csrf_exempt, name='dispatch')
class MoviesView(LoginRequiredMixin, PermissionRequiredMixin, View):

	login_url = '/login/'
	permission_required = "add_movie"

	def get(self,request):
		form = movieForm()

		path = os.path.join(
			os.path.dirname(__file__),
			'templates/movieApp/layout/content/form_info.html'
		)
		template_values = {
							"form": form, 
							"title": "Add movie to the Database" ,
							"form_name": "addMovieForm",
							"submit_type":"button",
							"submit_url":reverse("addMovie")
						  }
		template_values = Utils.template_vals_with_web_costants(
			template_values,
			'Movie99'
		)
		return render(request, path, template_values)
		#return render(request, 'movieApp/addMovie.html', {'form': form})

	def post(self,request):
		form = movieForm(request.POST)

		if not form.is_valid():
			return HttpResponse(json.dumps(Utils.create_error_payload("Form not correct",form.errors)))

		cd = form.cleaned_data
		movie = Movie()
		response = {}
		try:
			movie.title = cd.get('title')
			movie.director = cd.get('director')
			movie.imdb_score = cd.get('imdb_score')
			movie.popularity = cd.get('popularity')
			movie.image_url = cd.get('image_url')
			movie.movie_description = cd.get('movie_description')
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
		except Exception as e :
			print(e)
			response = Utils.create_error_payload("Movie with movie name already exist")

		print(response)

		return HttpResponse(json.dumps(response))

@method_decorator(csrf_exempt, name='dispatch')
class EditMoviesView(LoginRequiredMixin, PermissionRequiredMixin, View):

	login_url = '/login/'
	permission_required = "change_movie"

	def get(self, request, movieId):
		#form = movieForm()
		movie = Movie.get_movie_by_id(movieId)

		if movie:
			genre_list = []
			for genre in movie.genres.all():
				genre_list.append(genre.name)

			print("In editMoviesView")
			print(genre_list)
			data = {
				'title':movie.title,
				'movie_description': movie.movie_description,
				'imdb_score': movie.imdb_score,
				'popularity': movie.popularity,
				'image_url': movie.image_url,
				'geners': genre_list,
				'director': movie.director
			}
			form = movieForm(data)
			path = os.path.join(
				os.path.dirname(__file__),
				'templates/movieApp/layout/content/form_info.html'
			)
			template_values = {
								"form": form, 
								"title": "Edit" ,
								"form_name": "addMovieForm",
								"submit_type":"button",
								"submit_url":"/edit/movie/" + str(movie.id) + "/"
							  }
			template_values = Utils.template_vals_with_web_costants(
				template_values,
				'Movie99'
			)
			return render(request, path, template_values)
		return HttpResponse(json.dumps(Utils.create_error_payload("MovieId does not exist")))

	def post(self, request, movieId):

		form = movieForm(request.POST)

		if not form.is_valid():
			return HttpResponse(json.dumps(Utils.create_error_payload("Form not correct",form.errors)))
		movie = Movie.get_movie_by_id(movieId)
		if not movie:
			return HttpResponse(json.dumps(Utils.create_error_payload("MovieId does not exist")))
		
		cd = form.cleaned_data
		response = {}
		try:
			movie.title = cd.get('title')
			movie.director = cd.get('director')
			movie.imdb_score = cd.get('imdb_score')
			movie.popularity = cd.get('popularity')
			movie.image_url = cd.get('image_url')
			movie.movie_description = cd.get('movie_description')
			movie.save()

			movie.genres.clear()
			for gen in cd['geners']:
				g = Genre.objects.get(name=gen)
				movie.genres.add(g)
			
			movie.save()
			response = {
				'message': 'Movie Successfully Added to the database',
				'movieId':movie.id
			}
			response = Utils.create_success_payload(response)
		except Exception as e :
			response = Utils.create_error_payload()


		return HttpResponse(json.dumps(response))

@method_decorator(csrf_exempt, name='dispatch')
class DeleteMovieView(LoginRequiredMixin, PermissionRequiredMixin, View):
	login_url = '/login/'
	permission_required = "delete_movie"

	def post(self, request, movieId):
		try:
			movieId = int(movieId)
		except Exception:
			movieId = None

		if not movieId:
			return HttpResponse(json.dumps(Utils.create_error_payload(message="Invalid movieId")))
		
		try:
			movie = Movie.get_movie_by_id(movieId)
			if not movie:
				return HttpResponse(json.dumps(Utils.create_error_payload(message="movieId does not exist")))
			movie.delete()
			response = {
				'message': 'Movie Deleted successfully'
			}
			response = Utils.create_success_payload(response)
		except Exception:
			response = Utils.create_error_payload("Something went wrong")

		return HttpResponse(json.dumps(response))

@method_decorator(csrf_exempt, name='dispatch')
class GenreView(View):

	def get(self, request):
		form = genreForm()
		path = os.path.join(
			os.path.dirname(__file__),
			'templates/movieApp/form.html'
		)
		template_values = {"form": form, "title": "Add genre" }
		template_values = Utils.template_vals_with_web_costants(
			template_values,
			'Movie99'
		)
		return render(request, path, template_values)
		#return render(request, 'movieApp/addMovie.html', {'form': form})

	def post(self, request):
		form = genreForm(request.POST)

		if not form.is_valid():
			return HttpResponse(Utils.create_error_payload("Form not correct", form.errors))

		cd = form.cleaned_data
		title = cd.get('title')
		description = cd.get('description')
		response = {}
		try:

			g = Genre()
			g.title = title
			g.description = description
			g.save()
			response = {
				'message': 'Genre Successfully Added to the database'
			}
			response = Utils.create_success_payload(response)
		except Exception:
			response = Utils.create_error_payload("Something went wrong")

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
			genre = self.kwargs.get('genre')
			try:
				limit = int(limit)
			except Exception:
				limit = 0

			if limit == 0 and (not genre or genre == "None"):
				return None

			if limit > 0:
				return  Movie.get_all_movies_by_popularity("desc",limit)
			else:
				return Movie.get_movies_by_genre(genre=genre)

		def get_context_data(self, **kwargs):
			limit = self.kwargs.get('limit')
			genre = self.kwargs.get('genre')
			try:
				limit = int(limit)
			except Exception:
				limit = 0
			# Call the base implementation first to get a context
			context = super(MovieListView, self).get_context_data(**kwargs)
			# Add in a QuerySet of all the books
			context['view'] = limit if "mainView" else "reviewView"
			return context 
			

@method_decorator(csrf_exempt, name = 'dispatch')
class MovieDetailView(View):
	
	def get(self, request, movieId=None, movieName=None, jsonResponse=None):
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
					#movie = Movie.get_movie_by_id(movieId)
					movie = Movie.objects.get(pk = movieId)
				else:
					movie = Movie.objects.get(title__icontains = movieName) 

				genre_list = []
				for genre in movie.genres.all():
					genre_list.append(genre.name)

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
				'genre_string': genre_string if movie else "",
				'edit_get_url': '/edit/movie/' + str(movie.id) + "/" if movie else "",
				'delete_url': '/delete/movie/' + str(movie.id) + "/" if movie else ""
			}

		print("template_value")

		template_values = Utils.template_vals_with_web_costants(
			template_values,
			'Movie99'
		)
		path = os.path.join(
		os.path.dirname(__file__),
			'templates/movieApp/index.html'
		)

		return render(request, path, template_values)
