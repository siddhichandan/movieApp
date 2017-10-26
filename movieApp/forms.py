from django import forms
from movieApp.models import Movie,Genre,UserReview
from django.contrib.auth import authenticate,login,logout,get_user_model

User = get_user_model()

class UserLoginForm(forms.Form):

	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput)

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")

		print(username)
		print(password)
		
		if username and password:
			user = authenticate(username=username,password=password)
			print(user)
			if not user:
				raise forms.ValidationError("User does not exist")

			if not user.check_password(password):
				raise forms.ValidationError("Incorrect Password")

			if not user.is_active:
				raise forms.ValidationError("User not active")

		return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegistraterForm(forms.ModelForm):

	password = forms.CharField(widget = forms.PasswordInput)
	email = forms.EmailField()
	class Meta:
		model = User
		fields = [
			'username',
			'password',
			'email'
		]

	def clean(self, *args, **kwargs):
		email = self.cleaned_data.get("email")
		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("Email Already Registered")
		return super(UserRegistraterForm, self).clean(*args, **kwargs)

class movieForm(forms.Form):

	CHOICES=[('HORROR','HORROR'),
         ('COMEDY','COMEDY'),
         ('ACTION','ACTION'),
         ('ANIMATED','ANIMATED'),
         ]

	title = forms.CharField()
	director = forms.CharField(required = False)
	imdb_score = forms.FloatField(max_value=10,min_value=1)
	geners = forms.MultipleChoiceField(choices = CHOICES, widget=forms.CheckboxSelectMultiple())
	popularity = forms.FloatField(max_value=99,min_value=0)
	image_url = forms.URLField(label='Movie Image', required=False)
	movie_description = forms.CharField(widget=forms.Textarea, required=False)
	

class genreForm(forms.ModelForm):

	name = forms.CharField(required=True)
	description = forms.CharField(required=False)
	class Meta:
		model = Genre
		fields = ['name','description']

class userReviewForm(forms.Form):
 
	userReview = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 40,'placeholder': "Review this movie"}),label="")
 
	class Meta:
		model = UserReview
		fields = ['userReview']