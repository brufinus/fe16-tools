from helper import get_cid


def assert_response(client, cid1, cid2,
                    expected_liked_meals_list, disliked_meal, expected_char_count):
    response = client.post('tools/get_meal_data', json={
        'selected_option1': cid1,
        'selected_option2': cid2,
    })

    for meal in response.json['meals']:
        assert meal['meal'] in expected_liked_meals_list, f'{meal["meal"]} should not be in the response.'
        assert meal['meal'] != disliked_meal, f'{disliked_meal} should not be in the response.'
    assert response.json['meals_count'] == len(expected_liked_meals_list), \
        f'Unexpected meal count. Expected {len(expected_liked_meals_list)}, got {response.json["meals_count"]}.'
    assert response.json['num_chars'] == expected_char_count, \
        f'Unexpected character count. Expected {expected_char_count}, got {response.json["num_chars"]}.'

def test_single_character(client, db_context):
    cid = get_cid(db_context, 'Dimitri')
    char_liked_meals = ['Saghert and Cream', 'Sweet Bun Trio', 'Onion Gratin Soup',
                   'Sauteed Jerky', 'Cheesy Verona Stew', 'Gautier Cheese Gratin']

    assert_response(client, cid, cid, char_liked_meals, 'Fried Crayfish', 1)

def test_multiple_shared(client, db_context):
    cid1, cid2 = get_cid(db_context, 'Edelgard', 'Lysithea')
    shared_liked_meals = ['Saghert and Cream', 'Sweet Bun Trio', 'Peach Sorbet']

    assert_response(client, cid1, cid2, shared_liked_meals, 'Sauteed Jerky', 2)

def test_one_shared(client, db_context):
    cid1, cid2 = get_cid(db_context, 'Ferdinand', 'Hubert')
    shared_liked_meal = ['Sauteed Pheasant and Eggs']

    assert_response(client, cid1, cid2, shared_liked_meal, 'Saeghert and Cream', 2)

def test_no_shared(client, db_context):
    cid1, cid2 = get_cid(db_context, 'Balthus', 'Constance')

    assert_response(client, cid1, cid2, [], 'Daphnel Stew', 2)
