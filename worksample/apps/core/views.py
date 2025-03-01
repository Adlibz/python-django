import requests
import os
import environ

from django.views.generic import TemplateView

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


FLY_API_TOKEN = env("FLY_API_TOKEN", default="")  
FLY_APP_NAME = "nganz"

class HomepageView(TemplateView):
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        
        url = f"https://api.machines.dev/v1/apps/{FLY_APP_NAME}/machines"
        headers = {"Authorization": f"Bearer {FLY_API_TOKEN}"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            context["machines"] = response.json()  
        else:
            context["machines"] = []  

        return context
