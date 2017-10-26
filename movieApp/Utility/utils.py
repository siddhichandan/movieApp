from movieApp.constants.config import Constants
from django.urls import reverse

class Utils:

    @classmethod
    def create_error_payload(
        self,
        message = "Something went wrong",
        responseObject = None
    ):
        print("In creare_error")
        payload = {}
        payload = {
            'status': Constants.API_FAIL,
            'response': {
                'message': message
            }
        }
        if responseObject:
            payload['response'].update(responseObject)
        return payload

    @classmethod
    def create_success_payload(
            self,
     		responseObject
     	):

        print("In creare_success")
        print(responseObject)
        print(type(responseObject))
        payload = {}

        payload = {
            'status': Constants.API_SUCCESS,
            'response': responseObject
        }
        return payload

    @classmethod
    def template_vals_with_web_costants(
        self, results, title="", desc=""
    ):
        return self.merge_two_dicts(
            results,
            self.get_web_constants(
                title,
                desc
            ),
        )

    @classmethod
    def get_web_constants(self, title="", desc=""):
        ASSETS_PATH = '/static/movieApp'
        CSS_PATH = 'css'
        JS_PATH = 'js'
        MAIN_PATH = 'main'

        result = {
            'CSS_PATH': '/'.join([ASSETS_PATH, CSS_PATH]) + '/',
            'CSS_MAIN_PATH': '/'.join(
                [
                    ASSETS_PATH,
                    CSS_PATH,
                    MAIN_PATH
                ]),
            'JS_PATH': '/'.join([ASSETS_PATH, JS_PATH]) + '/',
            'JS_MAIN_PATH': '/'.join(
                [
                    ASSETS_PATH,
                    JS_PATH,
                    MAIN_PATH
                ]),
            'META_TITLE': title,
            'META_DESC': desc,
            'COMPANY_NAME': 'Movie99',
            'TAGLINE': 'The movie Database',
            'LOGIN_URL': reverse("login"),
            'LOGOUT_URL': reverse("logout"),
            'REGISTRATION_URL': reverse("register"),
            'SEARCH_URL': reverse("movieTitleSearch", args=("query",)),
            'HOME_URL': reverse("home"),
            'REVIEW_URL':reverse("reviewPage")
        }
        return result

    @classmethod
    def merge_two_dicts(self, x, y):
        '''Given two dicts, merge them into a new dict as a shallow copy.'''
        z = x.copy()
        z.update(y)
        return z