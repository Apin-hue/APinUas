from flask import Blueprint, request, jsonify, render_template
from src.services import CategoryService, RecipeService, RatingService

bp = Blueprint('api', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


# --- Categories ---
@bp.route('/api/categories', methods=['GET'])
def get_categories():
    categories = CategoryService.get_all()
    return jsonify([c.to_dict() for c in categories]), 200


@bp.route('/api/categories', methods=['POST'])
def create_category():
    data = request.get_json() or {}
    category, errors = CategoryService.create(data)
    if errors:
        return jsonify({'errors': errors}), 400
    return jsonify(category.to_dict()), 201


@bp.route('/api/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    success = CategoryService.delete(category_id)
    if not success:
        return jsonify({'error': 'Category not found'}), 404
    return jsonify({'message': 'Deleted'}), 200


# --- Recipes ---
@bp.route('/api/recipes', methods=['GET'])
def get_recipes():
    category_id = request.args.get('category_id', type=int)
    recipes = RecipeService.get_all(category_id=category_id)
    return jsonify([r.to_dict() for r in recipes]), 200


@bp.route('/api/recipes/search', methods=['GET'])
def search_recipes():
    keyword = request.args.get('q', '')
    recipes = RecipeService.search(keyword)
    return jsonify([r.to_dict() for r in recipes]), 200


@bp.route('/api/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = RecipeService.get_by_id(recipe_id)
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404
    return jsonify(recipe.to_dict()), 200


@bp.route('/api/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json() or {}
    recipe, errors = RecipeService.create(data)
    if errors:
        return jsonify({'errors': errors}), 400
    return jsonify(recipe.to_dict()), 201


@bp.route('/api/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    data = request.get_json() or {}
    recipe, errors = RecipeService.update(recipe_id, data)
    if errors:
        return jsonify({'errors': errors}), 400 if 'not found' not in errors[0] else 404
    return jsonify(recipe.to_dict()), 200


@bp.route('/api/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    success = RecipeService.delete(recipe_id)
    if not success:
        return jsonify({'error': 'Recipe not found'}), 404
    return jsonify({'message': 'Deleted'}), 200


# --- Ratings ---
@bp.route('/api/recipes/<int:recipe_id>/ratings', methods=['POST'])
def add_rating(recipe_id):
    data = request.get_json() or {}
    rating, errors = RatingService.add_rating(recipe_id, data)
    if errors:
        return jsonify({'errors': errors}), 400 if 'not found' not in errors[0] else 404
    return jsonify(rating.to_dict()), 201


@bp.route('/api/recipes/<int:recipe_id>/ratings', methods=['GET'])
def get_ratings(recipe_id):
    ratings = RatingService.get_ratings(recipe_id)
    return jsonify([r.to_dict() for r in ratings]), 200
