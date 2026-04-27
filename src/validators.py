def validate_recipe(data):
    errors = []
    if not data.get('title') or not str(data['title']).strip():
        errors.append('Title is required')
    elif len(str(data['title'])) > 200:
        errors.append('Title must be 200 characters or less')

    if not data.get('ingredients') or not str(data['ingredients']).strip():
        errors.append('Ingredients are required')

    if not data.get('instructions') or not str(data['instructions']).strip():
        errors.append('Instructions are required')

    if 'prep_time' in data and data['prep_time'] is not None:
        try:
            pt = int(data['prep_time'])
            if pt < 0:
                errors.append('Prep time must be a positive number')
        except (ValueError, TypeError):
            errors.append('Prep time must be a number')

    if 'servings' in data and data['servings'] is not None:
        try:
            sv = int(data['servings'])
            if sv <= 0:
                errors.append('Servings must be greater than 0')
        except (ValueError, TypeError):
            errors.append('Servings must be a number')

    return errors


def validate_category(data):
    errors = []
    if not data.get('name') or not str(data['name']).strip():
        errors.append('Category name is required')
    elif len(str(data['name'])) > 100:
        errors.append('Category name must be 100 characters or less')
    return errors


def validate_rating(data):
    errors = []
    if 'score' not in data or data['score'] is None:
        errors.append('Score is required')
    else:
        try:
            score = int(data['score'])
            if score < 1 or score > 5:
                errors.append('Score must be between 1 and 5')
        except (ValueError, TypeError):
            errors.append('Score must be a number')
    return errors
