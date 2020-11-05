from utils.pager import pager


def test_pager():
    def sample_record(start_index, end_index) -> dict:
        return {'sample_record': [
            {'start_index': start_index, 'end_index': end_index},
        ]}

    response = pager(265, 100, sample_record)

    assert response == {'sample_record': [
        {'start_index': 0, 'end_index': 99},
        {'start_index': 100, 'end_index': 199},
        {'start_index': 200, 'end_index': 265},
    ]}
