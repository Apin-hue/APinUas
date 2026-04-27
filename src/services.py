from src.models import db, Recipe, Category, Rating
from src.validators import validate_recipe, validate_category, validate_rating


class CategoryService:
    @staticmethod
    def get_all():
        return Category.query.all()

    @staticmethod
    def get_by_id(category_id):
        return Category.query.get(category_id)

    @staticmethod
    def create(data):
        errors = validate_category(data)
        if errors:
            return None, errors
        existing = Category.query.filter_by(name=data['name'].strip()).first()
        if existing:
            return None, ['Category name already exists']
        category = Category(name=data['name'].strip(), description=data.get('description', ''))
        db.session.add(category)
        db.session.commit()
        return category, []

    @staticmethod
    def delete(category_id):
        category = Category.query.get(category_id)
        if not category:
            return False
        db.session.delete(category)
        db.session.commit()
        return True


class RecipeService:
    @staticmethod
    def get_all(category_id=None):
        query = Recipe.query
        if category_id:
            query = query.filter_by(category_id=category_id)
        return query.all()

    @staticmethod
    def get_by_id(recipe_id):
        return Recipe.query.get(recipe_id)

    @staticmethod
    def create(data):
        errors = validate_recipe(data)
        if errors:
            return None, errors
        recipe = Recipe(
            title=data['title'].strip(),
            description=data.get('description', ''),
            ingredients=data['ingredients'].strip(),
            instructions=data['instructions'].strip(),
            prep_time=data.get('prep_time'),
            servings=data.get('servings'),
            category_id=data.get('category_id'),
        )
        db.session.add(recipe)
        db.session.commit()
        return recipe, []

    @staticmethod
    def update(recipe_id, data):
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            return None, ['Recipe not found']
        errors = validate_recipe(data)
        if errors:
            return None, errors
        recipe.title = data['title'].strip()
        recipe.description = data.get('description', recipe.description)
        recipe.ingredients = data['ingredients'].strip()
        recipe.instructions = data['instructions'].strip()
        recipe.prep_time = data.get('prep_time', recipe.prep_time)
        recipe.servings = data.get('servings', recipe.servings)
        recipe.category_id = data.get('category_id', recipe.category_id)
        db.session.commit()
        return recipe, []

    @staticmethod
    def delete(recipe_id):
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            return False
        db.session.delete(recipe)
        db.session.commit()
        return True

    @staticmethod
    def search(keyword):
        return Recipe.query.filter(Recipe.title.ilike(f'%{keyword}%')).all()


class RatingService:
    @staticmethod
    def add_rating(recipe_id, data):
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            return None, ['Recipe not found']
        errors = validate_rating(data)
        if errors:
            return None, errors
        rating = Rating(recipe_id=recipe_id, score=int(data['score']), comment=data.get('comment', ''))
        db.session.add(rating)
        db.session.commit()
        return rating, []

    @staticmethod
    def get_ratings(recipe_id):
        return Rating.query.filter_by(recipe_id=recipe_id).all()
