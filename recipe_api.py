import os
import requests

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RECIPE_API")

BASE_URL = "https://recipeapi.io/api/v1/recipes"


# def search_recipes(ingredients):
#     if not API_KEY:
#         raise ValueError("RECIPE_API not found in .env")

#     if not ingredients:
#         return None

#     params = {
#         "ingredients": ",".join(ingredients)
#     }

#     headers = {
#         "Authorization": f"Bearer {API_KEY}"
#     }

#     try:
#         response = requests.get(
#             BASE_URL,
#             params=params,
#             headers=headers,
#             timeout=15
#         )

#         response.raise_for_status()
#         return response.json()

#     except requests.RequestException as e:
#         print(f"API request failed: {e}")
#         return None

def search_recipes(ingredients, page=1):
    if not API_KEY:
        raise ValueError("RECIPE_API not found in .env")

    params = {
        "ingredients": ",".join(ingredients),
        "page": page,
        "per_page": 15
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    response = requests.get(
        BASE_URL,
        params=params,
        headers=headers,
        timeout=15
    )

    response.raise_for_status()
    return response.json()