import requests
import os

from django.views.generic import TemplateView

def get_env_value(env_file, key, default=""):
    try:
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith(f"{key}="):
                    return line.split('=', 1)[1].strip().strip('"\'')
    except (FileNotFoundError, PermissionError):
        pass
    return default

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
FLY_API_TOKEN = get_env_value(os.path.join(BASE_DIR, ".env"), "FLY_API_TOKEN", "")
FLY_APP_NAME = get_env_value(os.path.join(BASE_DIR, ".env"), "FLY_APP_NAME", "")


class HomepageView(TemplateView):
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch Fly Machines data
        url = f"https://api.machines.dev/v1/apps/{FLY_APP_NAME}/machines"
        headers = {"Authorization": f"Bearer {FLY_API_TOKEN}"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            context["machines"] = response.json()  # Add machines data to context
        else:
            context["machines"] = []  # If API fails, return an empty list

        return context