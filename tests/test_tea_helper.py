from helper import get_cid

def assert_response(client, cid,
                    expected_liked_teas_list, disliked_tea, liked_topics_list, disliked_topic, expected_topic_count,
                    final_comments_list, expected_comments_count, answers_list):
    response = client.post('/get_tea_data', json={
        'selected_option': cid,
    })

    for tea in response.json['tea']:
        assert tea['tea'] in expected_liked_teas_list, f'{tea["tea"]} should not be in the response.'
        assert tea['tea'] != disliked_tea, f'{disliked_tea} should not be in the response.'
    assert response.json['tea_count'] == len(expected_liked_teas_list), \
        f'Unexpected tea count. Expected {len(expected_liked_teas_list)}, got {response.json["tea_count"]}.'

    for topic in liked_topics_list:
        assert any(d['topic'] == topic for d in response.json['topics']), f'Expected {topic} to be in the response.'
    assert not any(d['topic'] == disliked_topic for d in response.json['topics']), \
        f'{disliked_topic} should not be in the response.'
    assert len(response.json['topics']) == expected_topic_count, \
        f'Unexpected topic count. Expected {expected_topic_count}, got {len(response.json["topics"])}'

    for comment in final_comments_list:
        assert any(d['comment'] == comment for d in response.json['comments']), \
            f'Expected comment is not in the response: {comment}'
    assert len(response.json['comments']) == expected_comments_count, \
        f'Unexpected comment count. Expected {expected_comments_count}, got {len(response.json["topics"])}'

    for answer in answers_list:
        assert any(d['answer'] == answer for d in response.json['answers']), \
            f'Expected {answer} to be in the response.'
    assert len(response.json['answers']) == expected_comments_count, \
        f'Unexpected answer count. Expected {expected_comments_count}, got {len(response.json["answers"])}'

def test_character1_tea_helper(client, db_context):
    cid = get_cid(db_context, 'Anna')
    char_liked_teas = ['Seiros Tea', 'Dagda Fruit Blend', 'Bergamot']
    char_liked_topics = ['Cats', 'Our first meeting', 'The opera']
    char_final_comments = [
        'Of course I pay my taxes! The fact that I can even do business at all is thanks to the goddess.',
        'The Sreng region is rich in high-quality minerals. Wonder how I can distribute them to a buyer...',
        'War pushes the profit margins up, but at what cost...'
    ]
    char_answers = ['Nod, Commend, Praise', 'Disagree, Sip tea, Blush', 'Laugh, Chat']

    assert_response(client, cid, char_liked_teas, 'Chamomile', char_liked_topics, 'Dimitri',
                    50, char_final_comments, 9, char_answers)

def test_character2_tea_helper(client, db_context):
    cid = get_cid(db_context, 'Caspar')
    char_liked_teas = ['Ginger Tea']
    char_liked_topics = ['A word of advice', 'Perfect recipes', 'The last battle']
    char_final_comments = [
        'Hey, are you getting hungry?',
        "What is justice really? I'm not so sure I know anymore...",
        "I really love fighting alongside you. I can always count on your commands to get us through!"
    ]
    char_answers = ['Laugh, Sigh', 'Commend, Chat', 'Nod, Laugh, Blush']

    assert_response(client, cid, char_liked_teas, 'Bergamot', char_liked_topics, 'The opera',
                    40, char_final_comments, 9, char_answers)

def test_character3_tea_helper(client, db_context):
    cid = get_cid(db_context, 'Constance')
    char_liked_teas = ['Bergamot', 'Rose Petal Blend', 'Sweet-Apple Blend', 'Albinean Berry Blend']
    char_liked_topics = ["Books you've read recently", 'First crushes', 'Relaxing at the sauna']
    char_final_comments = [
        'Tea parties such as this were once so... commonplace for me. And they will be again!',
        "Ever since that fateful day when the Dagdan army took House Nuvelle's territory, I've been on my own.",
        'Tea parties such as this were once so... commonplace for me. I am ashamed to have not appreciated them fully at the time.',
        'How cruel that House Nuvelle, with its long and storied history, should have no heirs left save but me.'
    ]
    char_answers = ['Laugh, Praise', 'Disagree, Sigh, Praise', 'Disagree, Admonish, Praise', 'Sigh, Praise']

    assert_response(client, cid, char_liked_teas, 'Ginger Tea', char_liked_topics, 'Successful plots',
                    31, char_final_comments, 18, char_answers)
