import pytest
import json


class TestCategoryAPI:
    def test_create_and_get_category(self, client):
        res = client.post('/api/categories', json={'name': 'Makanan Berat', 'description': 'Nasi dll'})
        assert res.status_code == 201
        data = res.get_json()
        assert data['name'] == 'Makanan Berat'

        res = client.get('/api/categories')
        assert res.status_code == 200
        assert len(res.get_json()) == 1

    def test_create_category_duplicate(self, client):
        client.post('/api/categories', json={'name': 'Minuman'})
        res = client.post('/api/categories', json={'name': 'Minuman'})
        assert res.status_code == 400

    def test_create_category_missing_name(self, client):
        res = client.post('/api/categories', json={})
        assert res.status_code == 400
        assert 'errors' in res.get_json()

    def test_delete_category(self, client):
        res = client.post('/api/categories', json={'name': 'Snack'})
        cat_id = res.get_json()['id']
        res = client.delete(f'/api/categories/{cat_id}')
        assert res.status_code == 200

    def test_delete_nonexistent_category(self, client):
        res = client.delete('/api/categories/999')
        assert res.status_code == 404


class TestRecipeAPI:
    RECIPE = {
        'title': 'Soto Ayam',
        'ingredients': 'Ayam, Kunyit, Serai',
        'instructions': 'Rebus ayam, tambahkan bumbu',
        'prep_time': 45,
        'servings': 4,
    }

    def test_create_and_get_recipe(self, client):
        res = client.post('/api/recipes', json=self.RECIPE)
        assert res.status_code == 201
        assert res.get_json()['title'] == 'Soto Ayam'

        res = client.get('/api/recipes')
        assert res.status_code == 200
        assert len(res.get_json()) == 1

    def test_get_recipe_by_id(self, client):
        res = client.post('/api/recipes', json=self.RECIPE)
        recipe_id = res.get_json()['id']
        res = client.get(f'/api/recipes/{recipe_id}')
        assert res.status_code == 200
        assert res.get_json()['title'] == 'Soto Ayam'

    def test_get_nonexistent_recipe(self, client):
        res = client.get('/api/recipes/999')
        assert res.status_code == 404

    def test_create_recipe_missing_fields(self, client):
        res = client.post('/api/recipes', json={'title': 'Incomplete'})
        assert res.status_code == 400
        assert 'errors' in res.get_json()

    def test_update_recipe(self, client):
        res = client.post('/api/recipes', json=self.RECIPE)
        recipe_id = res.get_json()['id']
        updated = {**self.RECIPE, 'title': 'Soto Betawi'}
        res = client.put(f'/api/recipes/{recipe_id}', json=updated)
        assert res.status_code == 200
        assert res.get_json()['title'] == 'Soto Betawi'

    def test_delete_recipe(self, client):
        res = client.post('/api/recipes', json=self.RECIPE)
        recipe_id = res.get_json()['id']
        res = client.delete(f'/api/recipes/{recipe_id}')
        assert res.status_code == 200

    def test_search_recipe(self, client):
        client.post('/api/recipes', json=self.RECIPE)
        client.post('/api/recipes', json={**self.RECIPE, 'title': 'Soto Mie'})
        res = client.get('/api/recipes/search?q=soto')
        assert res.status_code == 200
        assert len(res.get_json()) == 2

    def test_filter_by_category(self, client):
        cat_res = client.post('/api/categories', json={'name': 'Sup'})
        cat_id = cat_res.get_json()['id']
        client.post('/api/recipes', json={**self.RECIPE, 'category_id': cat_id})
        client.post('/api/recipes', json={**self.RECIPE, 'title': 'Bakso'})
        res = client.get(f'/api/recipes?category_id={cat_id}')
        assert res.status_code == 200
        assert len(res.get_json()) == 1


class TestRatingAPI:
    RECIPE = {
        'title': 'Rendang',
        'ingredients': 'Daging, Santan, Bumbu',
        'instructions': 'Masak hingga kering',
    }

    def test_add_and_get_rating(self, client):
        res = client.post('/api/recipes', json=self.RECIPE)
        recipe_id = res.get_json()['id']

        res = client.post(f'/api/recipes/{recipe_id}/ratings', json={'score': 5, 'comment': 'Mantap!'})
        assert res.status_code == 201
        assert res.get_json()['score'] == 5

        res = client.get(f'/api/recipes/{recipe_id}/ratings')
        assert res.status_code == 200
        assert len(res.get_json()) == 1

    def test_add_rating_invalid_score(self, client):
        res = client.post('/api/recipes', json=self.RECIPE)
        recipe_id = res.get_json()['id']
        res = client.post(f'/api/recipes/{recipe_id}/ratings', json={'score': 0})
        assert res.status_code == 400

    def test_add_rating_nonexistent_recipe(self, client):
        res = client.post('/api/recipes/999/ratings', json={'score': 5})
        assert res.status_code == 404

    def test_average_rating_in_recipe(self, client):
        res = client.post('/api/recipes', json=self.RECIPE)
        recipe_id = res.get_json()['id']
        client.post(f'/api/recipes/{recipe_id}/ratings', json={'score': 4})
        client.post(f'/api/recipes/{recipe_id}/ratings', json={'score': 2})
        res = client.get(f'/api/recipes/{recipe_id}')
        assert res.get_json()['average_rating'] == 3.0

    def test_delete_recipe_cascades_ratings(self, client):
        res = client.post('/api/recipes', json=self.RECIPE)
        recipe_id = res.get_json()['id']
        client.post(f'/api/recipes/{recipe_id}/ratings', json={'score': 5})
        client.delete(f'/api/recipes/{recipe_id}')
        res = client.get(f'/api/recipes/{recipe_id}')
        assert res.status_code == 404
