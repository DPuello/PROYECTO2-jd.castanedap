def create_db_data(db):
    from models.ingredient import Ingredient
    from models.product import Product
    from models.icecreamshop import IceCreamShop

    db.drop_all()
    db.create_all()

    # Create Ice Cream Shop
    shop = IceCreamShop(
        name="Creamy Delights",
    )
    db.session.add(shop)
    db.session.commit()

    # Create Ingredients
    ingredients = [
        Ingredient(
            name="Milk",
            price=1000,
            calories=100,
            stock=10,
            vegan=False,
            category="Base",
            flavor="Vanilla",
            id_ice_cream_shop=shop.id
        ),
        Ingredient(
            name="Cream",
            price=1500,
            calories=150,
            stock=8,
            vegan=False,
            category="Base",
            flavor="Chocolate",
            id_ice_cream_shop=shop.id
        ),
        Ingredient(
            name="Chocolate",
            price=2000,
            calories=200,
            stock=15,
            vegan=True,
            category="Base",
            flavor="Chocolate",
            id_ice_cream_shop=shop.id
        ),
        Ingredient(
            name="Vanilla Extract",
            price=3000,
            calories=50,
            stock=12,
            vegan=True,
            category="Complement",
            id_ice_cream_shop=shop.id
        ),
        Ingredient(
            name="Strawberries",
            price=1200,
            calories=50,
            stock=20,
            vegan=True,
            category="Complement",
            id_ice_cream_shop=shop.id
        ),
        Ingredient(
            name="Almonds",
            price=2500,
            calories=120,
            stock=10,
            vegan=True,
            category="Complement",
            id_ice_cream_shop=shop.id
        ),
        Ingredient(
            name="Caramel",
            price=1800,
            calories=180,
            stock=7,
            vegan=True,
            category="Complement",
            id_ice_cream_shop=shop.id
        ),
        Ingredient(
            name="Cookie Pieces",
            price=1600,
            calories=160,
            stock=15,
            vegan=False,
            category="Complement",
            id_ice_cream_shop=shop.id
        ),
        Ingredient(
            name="Coconut Milk",
            price=2200,
            calories=80,
            stock=10,
            vegan=True,
            category="Base",
            flavor="Coconut",
            id_ice_cream_shop=shop.id
        ),
        Ingredient(
            name="Mint Leaves",
            price=1000,
            calories=10,
            stock=25,
            vegan=True,
            category="Complement",
            id_ice_cream_shop=shop.id
        )
    ]

    for ingredient in ingredients:
        db.session.add(ingredient)
    db.session.commit()

    # Create Products with their ingredients
    vanilla_ice_cream = Product(
        name="Classic Vanilla",
        category="Milkshake",
        price=5000,
        id_ice_cream_shop=shop.id
    )
    vanilla_ice_cream.ingredients.extend([
        ingredients[0],  # Milk
        ingredients[1],  # Cream
        ingredients[3]   # Vanilla Extract
    ])

    chocolate_dream = Product(
        name="Chocolate Dream",
        category="Milkshake",
        price=5500,
        id_ice_cream_shop=shop.id
    )
    chocolate_dream.ingredients.extend([
        ingredients[0],  # Milk
        ingredients[1],  # Cream
        ingredients[2]   # Chocolate
    ])

    strawberry_delight = Product(
        name="Strawberry Delight",
        category="Cup",
        price=5200,
        id_ice_cream_shop=shop.id
    )
    strawberry_delight.ingredients.extend([
        ingredients[0],  # Milk
        ingredients[1],  # Cream
        ingredients[4]   # Strawberries
    ])

    mint_chocolate = Product(
        name="Mint Chocolate Chip",
        category="Cup",
        price=5800,
        id_ice_cream_shop=shop.id
    )
    mint_chocolate.ingredients.extend([
        ingredients[0],  # Milk
        ingredients[1],  # Cream
        ingredients[2],  # Chocolate
        ingredients[9]   # Mint Leaves
    ])

    products = [vanilla_ice_cream, chocolate_dream,
                strawberry_delight, mint_chocolate]
    for product in products:
        db.session.add(product)
    db.session.commit()
