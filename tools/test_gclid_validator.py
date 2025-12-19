from gclid_validator import is_valid_gclid_format


def test_valid_gclid():
    valid, _ = is_valid_gclid_format("CjwKCAiA1KL3BRA8EiwAzCfbQxyz123abc")
    assert valid


def test_invalid_gclid():
    valid, _ = is_valid_gclid_format("abc")
    assert not valid
