import curses
import textwrap

from recipe_api import search_recipes
import database


def render_recipe(stdscr, recipe, index, total):
    stdscr.clear()

    height, width = stdscr.getmaxyx()

    def write(y, text, attr=0):
        if 0 <= y < height - 1:
            try:
                stdscr.addnstr(
                    y, 2, str(text),
                    max(0, width - 4),
                    attr
                )
            except curses.error:
                pass

    write(0, " RECIPE FINDER ")
    write(2, f"{index + 1}/{total} recipes")

    title = recipe.get("name", "Untitled").upper()

    write(4, title)

    write(5, "=" * min(width - 4, 60))

    y = 7
    description = recipe.get("description", "No description")

    for line in textwrap.wrap(description, width - 6):
        write(y, line)
        y += 1

    y += 1

    write(y, "RECIPE INFORMATION", curses.A_BOLD)
    y += 1

    info = [
        f"Cuisine: {recipe.get('cuisine', 'N/A')}",
        f"Difficulty: {recipe.get('difficulty', 'N/A')}",
        f"Meal type: {recipe.get('meal_type', 'N/A')}",
        f"Servings: {recipe.get('servings', 'N/A')}",
        f"Prep time: {recipe.get('prep_time', 0)} min",
        f"Cook time: {recipe.get('cook_time', 0)} min",
        f"Calories: {recipe.get('calories_per_serving', 'N/A')} kcal",
        f"Protein: {recipe.get('protein', 'N/A')} g",
    ]

    for item in info:
        write(y, item)
        y += 1

    y += 1

    write(y, "INGREDIENTS", curses.A_BOLD)
    y += 1

    for ingredient in recipe.get("ingredients", []):
        if not isinstance(ingredient, dict):
            continue

        quantity = ingredient.get("quantity", "")
        unit = ingredient.get("unit", "")
        name = ingredient.get("name", "Unknown")

        optional = " (optional)" if ingredient.get("optional") else ""

        write(y, f"  - {quantity} {unit} {name}{optional}")
        y += 1

    y += 1

    write(y, "INSTRUCTIONS", curses.A_BOLD)
    y += 1

    for i, instruction in enumerate(recipe.get("instructions", []), 1):
        wrapped = textwrap.wrap(instruction, width - 8)

        for j, line in enumerate(wrapped):
            prefix = f"{i}. " if j == 0 else "   "
            write(y, prefix + line)
            y += 1

    footer = " UP/DOWN: Navigate | Q: Quit "


    stdscr.addnstr(
        height - 1, 
        0,
        footer.ljust(width - 1),
        width - 1
    )

    stdscr.refresh()


def run(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)

    stdscr.keypad(True)

    ingredients = database.get_ingredients()

    if not ingredients:
        stdscr.addstr(0, 0, "No ingredients saved!")
        stdscr.getch()
        return

    page = 1
    recipes = []
    has_next = True
    loading = False

    try:
        response = search_recipes(ingredients, page=page)

        recipes.extend(response.get("data", []))
        has_next = response.get("links", {}).get("next") is not None

    except Exception as e:
        stdscr.addstr(0, 0, f"API Error: {e}")
        stdscr.getch()
        return

    if not recipes:
        stdscr.addstr(0, 0, "No recipes found.")
        stdscr.getch()
        return

    index = 0

    while True:
        render_recipe(stdscr, recipes[index], index, len(recipes))

        key = stdscr.getch()

        if key in (ord("q"), ord("Q")):
            break

        elif key == curses.KEY_DOWN:
            if index < len(recipes) - 1:
                index += 1

            elif has_next and not loading:
                loading = True

                stdscr.clear()
                stdscr.addstr(0, 0, f"Loading page {page + 1}...")
                stdscr.refresh()

                try:
                    next_page = page + 1

                    response = search_recipes(
                        ingredients,
                        page=next_page
                    )

                    new_recipes = response.get("data", [])

                    if new_recipes:
                        recipes.extend(new_recipes)
                        page = next_page
                        index += 1

                    has_next = (
                        response.get("links", {}).get("next") is not None
                    )

                except Exception as e:
                    stdscr.clear()
                    stdscr.addstr(0, 0, f"API Error: {e}")
                    stdscr.getch()

                finally:
                    loading = False

        elif key == curses.KEY_UP:
            if index > 0:
                index -= 1


def main():
    curses.wrapper(run)


if __name__ == "__main__":
    main()
