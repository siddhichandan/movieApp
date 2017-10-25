from django.conf.urls import include,url
from movieApp.views import (MoviesView,GenreView,MovieListView,MainView,MovieDetailView,loginView,logoutView,registerView)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^add/movie/$', MoviesView.as_view()),
    url(r'^add/genre/$',GenreView.as_view()),
    #url(r'^movies/$',MovieListView.as_view(), name = 'movieList'),
    url(r'^movies/',
        include([
            url(r'^(?P<limit>\d+)$', MovieListView.as_view(), name = 'movieList'),
            url(r'^(?P<featured>featured)$',MovieListView.as_view(), name = 'featuredList')
        ])),
    url(r'^login/$',loginView, name = 'login'),
    url(r'^logout/$', logoutView, name = 'logout'),
    url(r'^register/$', registerView, name = 'register'),
    url(r'^movie/title/(?P<movieId>\d+)/',
    	include([
            url(r'^$', MovieDetailView.as_view(), name = 'movieDetail'),
            url(r'^(?P<jsonResponse>json)$', MovieDetailView.as_view(), name="movie_detail")
        ])),
    url(r'^movie/title/(?P<movieName>[A-Z a-z 0-9]+)/',
        include([
            url(r'^$', MovieDetailView.as_view(), name = 'movieTitleSearch'),
            url(r'^(?P<jsonResponse>json)$', MovieDetailView.as_view(), name="movie_detail")
    ])),
    url(r'^$', MainView.as_view(), name='home')

]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)