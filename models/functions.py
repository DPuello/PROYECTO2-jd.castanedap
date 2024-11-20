def is_healthy(calories: int, vegan: bool) -> bool:
    return vegan or calories < 100


def calc_calories(calories_by_ingredients: list) -> int:
    total_calories = 0
    for calories in calories_by_ingredients:
        total_calories += calories
    return round(total_calories * 0.95)


def calc_cost(ingredients: list) -> float:
    total_cost = 0
    for ingredient in ingredients:
        total_cost += ingredient["price"]
    return total_cost


def calc_product_earnings(price: float, ingredients: list) -> float:
    return price - calc_cost(ingredients)


def get_best_product(products: list) -> str:
    best_product = products[0]
    for product in products:
        if product["earnings"] > best_product["earnings"]:
            best_product = product
    return best_product["name"]

# Products functions


def calc_milkshake_calories(calories_by_ingredients: list) -> int:
    total_calories = 0
    for calories in calories_by_ingredients:
        total_calories += calories
    return round(total_calories) + 200


def calc_cup_cost(ingredients: list) -> float:
    return calc_cost(ingredients) + 500


def calc_cup_earnings(price: float, ingredients: list) -> float:
    return price - calc_cup_cost(ingredients)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
