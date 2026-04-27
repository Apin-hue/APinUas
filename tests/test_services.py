import pytest
from src.services import CategoryService, RecipeService, RatingService


RECIPE_DATA = {
    'title': 'Nasi Goreng',
    'ingredients': 'Nasi, Telur, Kecap',
    'instructions': 'Panaskan wajan, masukkan nasi, aduk rata',
    'prep_time': 15,
    'servings': 2,
}


class TestCategoryService:
    def test_create_category(self, app):
        with app.app_context():
            cat, errors = CategoryService.create({'name': 'Makanan Berat'})
            assert errors == []
            assert cat.name == 'Makanan Berat'

    def test_create_duplicate_category(self, app):
        with app.app_context():
            CategoryService.create({'name': 'Makanan Berat'})
            _, errors = CategoryService.create({'name': 'Makanan Berat'})
            assert errors != []

    def test_create_category_invalid(self, app):
        with app.app_context():
            _, errors = CategoryService.create({'name': ''})
            assert errors != []

    def test_get_all_categories(self, app):
        with app.app_context():
            CategoryService.create({'name': 'Minuman'})
            CategoryService.create({'name': 'Dessert'})
            cats = CategoryService.get_all()
            assert len(cats) == 2

    def test_delete_category(self, app):
        with app.app_context():
            cat, _ = CategoryService.create({'name': 'Snack'})
            result = CategoryService.delete(cat.id)
            assert result is True

    def test_delete_nonexistent_category(self, app):
        with app.app_context():
            result = CategoryService.delete(999)
            assert result is False


class TestRecipeService:
    def test_create_recipe(self, app):
        with app.app_context():
            recipe, errors = RecipeService.create(RECIPE_DATA)
            assert errors == []
            assert recipe.title == 'Nasi Goreng'

    def test_create_recipe_invalid(self, app):
        with app.app_context():
            _, errors = RecipeService.create({'title': ''})
            assert errors != []

    def test_get_all_recipes(self, app):
        with app.app_context():
            RecipeService.create(RECIPE_DATA)
            RecipeService.create({**RECIPE_DATA, 'title': 'Mie Goreng'})
            recipes = RecipeService.get_all()
            assert len(recipes) == 2

    def test_get_recipe_by_id(self, app):
        with app.app_context():
            recipe, _ = RecipeService.create(RECIPE_DATA)
            found = RecipeService.get_by_id(recipe.id)
            assert found.title == 'Nasi Goreng'

    def test_update_recipe(self, app):
        with app.app_context():
            recipe, _ = RecipeService.create(RECIPE_DATA)
            updated, errors = RecipeService.update(recipe.id, {**RECIPE_DATA, 'title': 'Nasi Goreng Spesial'})
            assert errors == []
            assert updated.title == 'Nasi Goreng Spesial'

    def test_update_nonexistent_recipe(self, app):
        with app.app_context():
            _, errors = RecipeService.update(999, RECIPE_DATA)
            assert errors != []

    def test_delete_recipe(self, app):
        with app.app_context():
            recipe, _ = RecipeService.create(RECIPE_DATA)
            result = RecipeService.delete(recipe.id)
            assert result is True

    def test_delete_nonexistent_recipe(self, app):
        with app.app_context():
            result = RecipeService.delete(999)
            assert result is False

    def test_search_recipe(self, app):
        with app.app_context():
            RecipeService.create(RECIPE_DATA)
            RecipeService.create({**RECIPE_DATA, 'title': 'Mie Goreng'})
            results = RecipeService.search('goreng')
            assert len(results) == 2

    def test_search_no_result(self, app):
        with app.app_context():
            RecipeService.create(RECIPE_DATA)
            results = RecipeService.search('pizza')
            assert len(results) == 0

    def test_average_rating(self, app):
        with app.app_context():
            recipe, _ = RecipeService.create(RECIPE_DATA)
            RatingService.add_rating(recipe.id, {'score': 4})
            RatingService.add_rating(recipe.id, {'score': 2})
            found = RecipeService.get_by_id(recipe.id)
            assert found.average_rating() == 3.0

    def test_no_rating_returns_none(self, app):
        with app.app_context():
            recipe, _ = RecipeService.create(RECIPE_DATA)
            assert recipe.average_rating() is None


class TestRatingService:
    def test_add_rating(self, app):
        with app.app_context():
            recipe, _ = RecipeService.create(RECIPE_DATA)
            rating, errors = RatingService.add_rating(recipe.id, {'score': 5, 'comment': 'Enak!'})
            assert errors == []
            assert rating.score == 5

    def test_add_rating_invalid_score(self, app):
        with app.app_context():
            recipe, _ = RecipeService.create(RECIPE_DATA)
            _, errors = RatingService.add_rating(recipe.id, {'score': 10})
            assert errors != []

    def test_add_rating_nonexistent_recipe(self, app):
        with app.app_context():
            _, errors = RatingService.add_rating(999, {'score': 5})
            assert errors != []

    def test_get_ratings(self, app):
        with app.app_context():
            recipe, _ = RecipeService.create(RECIPE_DATA)
            RatingService.add_rating(recipe.id, {'score': 3})
            RatingService.add_rating(recipe.id, {'score': 5})
            ratings = RatingService.get_ratings(recipe.id)
            assert len(ratings) == 2
