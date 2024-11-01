from app.models import LostItem
from helper import get_cid

def get_lid(db, name):
    return db.session.query(LostItem).filter_by(name=name).first().id

def assert_response(client, lid, expected_owner, cid, expected_liked_gifts_list):
    response = client.post('/tools/get_item_data', json={
        'lost_item_selected_option': lid,
        'character_selected_option': cid
    })

    owner = response.json['character'][0]['character']
    assert owner == expected_owner, f'Unexpected owner in response. Expected {expected_owner} as owner, got {owner}.'

    for gift in expected_liked_gifts_list:
        assert any(d['name'] == gift for d in response.json['gifts']), f'Expected {gift} to be in the response.'
    assert len(response.json['gifts']) == len(expected_liked_gifts_list), \
        f'Unexpected liked gift count. Expected {len(expected_liked_gifts_list)}, got {len(response.json["gifts"])}.'

def test_items1(client, db_context):
    lid = get_lid(db_context, 'Time-worn Quill Pen')
    cid = get_cid(db_context, 'Rhea')
    char_liked_gifts = ['Landscape Painting', 'Goddess Statuette', 'Ancient Coin']

    assert_response(client, lid, 'Edelgard', cid, char_liked_gifts)

def test_items2(client, db_context):
    lid = get_lid(db_context, 'Dulled Longsword')
    cid = get_cid(db_context, 'Leonie')
    char_liked_gifts = ['Hunting Dagger', 'Training Weight', 'Fishing Float']

    assert_response(client, lid, 'Dimitri', cid, char_liked_gifts)

def test_items3(client, db_context):
    lid = get_lid(db_context, 'Dusty Book of Fables')
    cid = get_cid(db_context, 'Constance')
    char_liked_gifts = ['Lily of the Valley', 'Tea Leaves', 'Arithmetic Textbook', 'Book of Crest Designs']

    assert_response(client, lid, 'Flayn', cid, char_liked_gifts)
