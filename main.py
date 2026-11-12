import argparse
import json

import database
import recipe_api

from tui import main as launch_tui

def display_ingredients():
    ingredients = database.get_ingredients()

    if not ingredients:
        print("Your ingredient database is empty.")
        return

    print("\nYour ingredients:")
    for i, ingredient in enumerate(ingredients, 1):
        print(f"  {i}. {ingredient}")


def display_recipes(response):
    recipes = response.get("data", [])

    if not recipes:
        print("\nNo recipes found.")
        return

    for recipe in recipes:
        print("\n" + "=" * 65)
        print(f"  {recipe['name'].upper()}")
        print("=" * 65)

        print(f"\n{recipe.get('description', 'No description')}")

        print("\n" + "-" * 30)
        print(" RECIPE INFORMATION")
        print("-" * 30)

        print(f"  Cuisine:       {recipe.get('cuisine', 'N/A').title()}")
        print(f"  Meal type:     {recipe.get('meal_type', 'N/A').title()}")
        print(f"  Difficulty:    {recipe.get('difficulty', 'N/A').title()}")
        print(f"  Servings:      {recipe.get('servings', 'N/A')}")
        print(f"  Prep time:     {recipe.get('prep_time', 0)} minutes")
        print(f"  Cook time:     {recipe.get('cook_time', 0)} minutes")
        print(f"  Total time:    {recipe.get('prep_time', 0) + recipe.get('cook_time', 0)} minutes")

        print("\n" + "-" * 30)
        print(" NUTRITION (PER SERVING)")
        print("-" * 30)

        print(f"  Calories:      {recipe.get('calories_per_serving', 'N/A')} kcal")
        print(f"  Protein:       {recipe.get('protein', 'N/A')} g")

        tags = recipe.get("dietary_tags", [])

        if tags:
            print("\n  Dietary tags: " + ", ".join(tags))

        # Ingredients
        print("\n" + "-" * 30)
        print(" INGREDIENTS")
        print("-" * 30)

        for ingredient in recipe.get("ingredients", []):
            if not isinstance(ingredient, dict):
                continue

            quantity = ingredient.get("quantity", "")
            unit = ingredient.get("unit", "")
            name = ingredient.get("name", "Unknown")

            optional = " (optional)" if ingredient.get("optional") else ""

            print(f"  • {quantity} {unit} {name}{optional}")

        # Instructions
        print("\n" + "-" * 30)
        print(" INSTRUCTIONS")
        print("-" * 30)

        for i, instruction in enumerate(recipe.get("instructions", []), 1):
            print(f"  {i}. {instruction}")

        print("\n" + "=" * 65)

    # Pagination
    meta = response.get("meta", {})

    if meta:
        print(
            f"\nPage {meta.get('current_page', 1)}"
            f" of {meta.get('last_page', 1)}"
            f" | Total recipes: {meta.get('total', 0)}"
        )

        if response.get("links", {}).get("next"):
            print("More recipes available. Try implementing pagination!")

def main():
    parser = argparse.ArgumentParser(
        description="Ingredient-based Recipe Finder"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("name")

    remove_parser = subparsers.add_parser("remove")
    remove_parser.add_argument("name")

    subparsers.add_parser("list")

    subparsers.add_parser("search")

    custom_parser = subparsers.add_parser("find")
    custom_parser.add_argument("ingredients", nargs="+")

    args = parser.parse_args()

    database.initialize_db()

    if args.command == "add":
        if database.add_ingredient(args.name):
            print(f"Added: {args.name}")
        else:
            print("Ingredient already exists.")

    elif args.command == "remove":
        if database.remove_ingredient(args.name):
            print(f"Removed: {args.name}")
        else:
            print("Ingredient not found.")

    elif args.command == "list":
        display_ingredients()

    elif args.command == "search":
        # ingredients = database.get_ingredients()

        # if not ingredients:
        #     print("Add some ingredients first!")
        #     return

        # print(f"Searching with: {', '.join(ingredients)}")

        # data = recipe_api.search_recipes(ingredients)
        # display_recipes(data)
        database.initialize_db()
        launch_tui()

    elif args.command == "find":
        ingredients = [i.lower() for i in args.ingredients]

        print(f"Searching with: {', '.join(ingredients)}")

        data = recipe_api.search_recipes(ingredients)
        display_recipes(data)


if __name__ == "__main__":
    main()



