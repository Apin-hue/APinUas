import pytest
from src.validators import validate_recipe, validate_category, validate_rating


# ── validate_recipe ──────────────────────────────────────────────────────────

class TestValidateRecipe:
    def test_valid_recipe(self):
        data = {'title': 'Nasi Goreng', 'ingredients': 'Nasi, Telur', 'instructions': 'Goreng semua'}
        assert validate_recipe(data) == []

    def test_missing_title(self):
        data = {'ingredients': 'Nasi', 'instructions': 'Goreng'}
        errors = validate_recipe(data)
        assert any('Title' in e for e in errors)

    def test_empty_title(self):
        data = {'title': '   ', 'ingredients': 'Nasi', 'instructions': 'Goreng'}
        errors = validate_recipe(data)
        assert any('Title' in e for e in errors)

    def test_title_too_long(self):
        data = {'title': 'A' * 201, 'ingredients': 'Nasi', 'instructions': 'Goreng'}
        errors = validate_recipe(data)
        assert any('200' in e for e in errors)

    def test_missing_ingredients(self):
        data = {'title': 'Nasi Goreng', 'instructions': 'Goreng'}
        errors = validate_recipe(data)
        assert any('Ingredients' in e for e in errors)

    def test_missing_instructions(self):
        data = {'title': 'Nasi Goreng', 'ingredients': 'Nasi'}
        errors = validate_recipe(data)
        assert any('Instructions' in e for e in errors)

    def test_negative_prep_time(self):
        data = {'title': 'Nasi', 'ingredients': 'Nasi', 'instructions': 'Goreng', 'prep_time': -5}
        errors = validate_recipe(data)
        assert any('positive' in e for e in errors)

    def test_invalid_prep_time(self):
        data = {'title': 'Nasi', 'ingredients': 'Nasi', 'instructions': 'Goreng', 'prep_time': 'abc'}
        errors = validate_recipe(data)
        assert any('number' in e for e in errors)

    def test_zero_servings(self):
        data = {'title': 'Nasi', 'ingredients': 'Nasi', 'instructions': 'Goreng', 'servings': 0}
        errors = validate_recipe(data)
        assert any('Servings' in e for e in errors)

    def test_invalid_servings(self):
        data = {'title': 'Nasi', 'ingredients': 'Nasi', 'instructions': 'Goreng', 'servings': 'banyak'}
        errors = validate_recipe(data)
        assert any('number' in e for e in errors)

    def test_valid_with_optional_fields(self):
        data = {'title': 'Soto', 'ingredients': 'Ayam', 'instructions': 'Rebus', 'prep_time': 30, 'servings': 4}
        assert validate_recipe(data) == []


# ── validate_category ────────────────────────────────────────────────────────

class TestValidateCategory:
    def test_valid_category(self):
        assert validate_category({'name': 'Makanan Berat'}) == []

    def test_missing_name(self):
        errors = validate_category({})
        assert any('name' in e.lower() for e in errors)

    def test_empty_name(self):
        errors = validate_category({'name': '  '})
        assert any('name' in e.lower() for e in errors)

    def test_name_too_long(self):
        errors = validate_category({'name': 'A' * 101})
        assert any('100' in e for e in errors)


# ── validate_rating ──────────────────────────────────────────────────────────

class TestValidateRating:
    def test_valid_rating(self):
        assert validate_rating({'score': 5}) == []

    def test_missing_score(self):
        errors = validate_rating({})
        assert any('Score' in e for e in errors)

    def test_score_too_low(self):
        errors = validate_rating({'score': 0})
        assert any('1 and 5' in e for e in errors)

    def test_score_too_high(self):
        errors = validate_rating({'score': 6})
        assert any('1 and 5' in e for e in errors)

    def test_invalid_score_type(self):
        errors = validate_rating({'score': 'bagus'})
        assert any('number' in e for e in errors)
