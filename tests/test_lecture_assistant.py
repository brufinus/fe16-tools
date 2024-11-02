

def get_response(client, query):
    return client.post('/tools/get_lecture_data', json={
        'q': query
    })

def assert_response(client, query, expected_question_count):
    response = get_response(client, query)
    for d in response.json['data']:
        assert query.lower() in d['question'].lower(), f'Expected query: {query} to be in the response.'
    assert len(response.json['data']) == expected_question_count, \
        f'Unexpected question count. Expected {expected_question_count}, got {len(response.json["data"])}.'

def test_single_letter(client):
    assert_response(client, 'a', 73)

def test_special_character(client):
    assert_response(client, '?', 55)

def test_short_phrase(client):
    assert_response(client, 'lecture', 5)

def test_long_phrase(client):
    assert_response(client, 'Um. Sorry, but you should', 1)

def test_phrase_case(client):
    assert_response(client, 'sOMetHiNg', 7)

def test_non_phrase(client):
    response = get_response(client, 'foobar')
    assert len(response.json['data']) == 0, f'Unexpected question count. Expected 0, got {len(response.json["data"])}.'

def test_no_phrase(client):
    assert_response(client, '', 0)
