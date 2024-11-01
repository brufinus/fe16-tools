from app.models import Seed


def get_sid(db, name, *args):
    sids = [db.session.query(Seed).filter_by(name=name).first().id]
    sids.extend(db.session.query(Seed).filter_by(name=arg).first().id for arg in args)

    return tuple(sids)

def assert_response(client, sid1, sid2, sid3, sid4, sid5, cultivation,
                    expected_score, expected_yield, expected_ratio, expected_coefficient):
    response = client.post('/tools/get_seed_data', json={
        'seed1_selected_option': sid1,
        'seed2_selected_option': sid2,
        'seed3_selected_option': sid3,
        'seed4_selected_option': sid4,
        'seed5_selected_option': sid5,
        'cultivation_selected_option': cultivation
    })

    assert response.json['score'] == expected_score, \
        f'Unexpected score. Expected {expected_score}, got {response.json["score"]}.'
    assert response.json['yield'] == expected_yield, \
        f'Unexpected yield. Expected {expected_yield}, got {response.json["yield"]}.'
    assert response.json['ratio'] == expected_ratio, \
        f'Unexpected ratio. Expected {expected_ratio}, got {response.json["ratio"]}.'
    assert response.json['coefficient'] == expected_coefficient, \
        f'Unexpected coefficient. Expected {expected_coefficient}, got {response.json["coefficient"]}.'

def test_no_seeds1(client, db_context):
    assert_response(client, -1, -1, -1, -1, -1, 0, '0', '0', '', '0')

def test_no_seeds2(client, db_context):
    assert_response(client, -1, -1, -1, -1, -1, 6, '0', '0', '', '0')

def test_seed_pos1(client, db_context):
    sid = get_sid(db_context, 'Mixed Herb Seeds')[0]
    assert_response(client, sid, -1, -1, -1, -1, 0, '53', '2', '7:3', '5')

def test_seed_pos3(client, db_context):
    sid = get_sid(db_context, 'Pale-Blue Flower Seeds')[0]
    assert_response(client, -1, -1, sid, -1, -1, 2, '69', '2', '4:6', '10')

def test_seed_pos5(client, db_context):
    sid = get_sid(db_context, 'Eastern Fodlan Seeds')[0]
    assert_response(client, -1, -1, -1, -1, sid, 6, '51', '2', '7:3', '5')

def test_all_seeds(client, db_context):
    sid1, sid2, sid3, sid4, sid5 = get_sid(db_context, 'Root Vegetable Seeds', 'Southern Fodlan Seeds',
                                           'Purple Flower Seeds', 'Morfis Seeds', 'Mixed Fruit Seeds')
    assert_response(client, sid1, sid2, sid3, sid4, sid5, 3, '76', '2', '4:6', '10')
