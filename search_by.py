import requests
from env_keys.env_secrets import API_KEY


def search_api_by_ingredients(data):
    BASE_URL = 'https://api.spoonacular.com/recipes/findByIngredients'
    ingredients = ','.join([str(elem) for elem in data])
    res = requests.get(BASE_URL, params={
        'apiKey': API_KEY,
        'ingredients': ingredients})
    return res.json()


def search_api_for_instructions(recipe_id):
    BASE_URL = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    res = requests.get(BASE_URL, params={
        'apiKey': API_KEY
    })
    return res.json()


def search_api_random_recipe():
    BASE_URL = 'https://api.spoonacular.com/recipes/random'
    res = requests.get(BASE_URL, params={
        'apiKey': API_KEY,
        'number': 10
    })
    return res.json()


def search_api_complex(cuisine, ingredients, diet, meal_type):
    BASE_URL = 'https://api.spoonacular.com/recipes/complexSearch'
    cuisine_data = cuisine
    ingredients_data = ','.join([str(elem) for elem in ingredients])
    diet_data = diet
    meal_type_data = meal_type
    res = requests.get(BASE_URL, params={
        'apiKey': API_KEY,
        'cuisine': cuisine_data,
        'includeIngredients': ingredients_data,
        'diet': diet_data,
        'type': meal_type_data,
        'number': 8,
        'fillIngredients': True
    })
    return res.json()
