from django.http import HttpResponse

def home(request):
   html = "Siddhu is awesome"
   return HttpResponse(html)
