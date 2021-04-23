from apollo_space_mission.main import *
import pytest

def test_check_address_change_false(fixed_location_client_data):
    expected_value = False
    actual_value = did_address_changed(fixed_location_client_data)
    assert expected_value == actual_value, f'Expected: {expected_value}, Actual: {actual_value}'


def test_check_address_change_true(dynamic_location_client_data):
    expected_value = True
    actual_value = did_address_changed(dynamic_location_client_data)
    assert expected_value == actual_value, f'Expected: {expected_value}, Actual: {actual_value}'


def test_check_address_change_no_data(missing_client_data):
    expected_value = False
    actual_value = did_address_changed(missing_client_data)
    assert expected_value == actual_value, f'Expected: {expected_value}, Actual: {actual_value}'


def test_get_client_frontendid(frontendid_client_data):
    expected_value = 's4na-atun'
    actual_value = get_client_frontendid(frontendid_client_data)
    assert expected_value == actual_value, f'Expected: {expected_value}, Actual: {actual_value}'


def test_get_client_missing_frontendid(missing_client_data):
    expected_value = -1
    actual_value = get_client_frontendid(missing_client_data)
    assert expected_value == actual_value, f'Expected: {expected_value}, Actual: {actual_value}'


def test_get_client_multi_frontendid(multi_frontendid_client_data):
    expected_value = 's2kb-lr7z'
    actual_value = get_client_frontendid(multi_frontendid_client_data)
    assert expected_value == actual_value, f'Expected: {expected_value}, Actual: {actual_value}'


def test_examine_visitor_wrong_type():
    expected_value = {
        "vid": -1,
        "add_changed": False,
        "order_placed": False,
        "order_delv": False,
        "app_type": "n/a"
    }
    actual_value = examine_visitor(None)
    assert expected_value == actual_value, f'Expected: {expected_value}, Actual: {actual_value}'


def test_examine_visitor_wrong_type2():
    expected_value = {
        "vid": -1,
        "add_changed": False,
        "order_placed": False,
        "order_delv": False,
        "app_type": "n/a"
    }
    actual_value = examine_visitor([1, 2, 3])
    assert expected_value == actual_value, f'Expected: {expected_value}, Actual: {actual_value}'


def test_examine_visitor_missing_id():
    expected_value = {
        "vid": '234689876543456789876548765456787654345678765456787654',
        "add_changed": False,
        "order_placed": False,
        "order_delv": False,
        "app_type": "n/a"
    }
    actual_value = examine_visitor(234689876543456789876548765456787654345678765456787654)
    assert expected_value == actual_value, f'Expected: {expected_value}, Actual: {actual_value}'


# ----------- END OF UNITTEST AND BEGINNING OF INTEGRATION TESTS ---------------


def test_examine_visitor_success():
    expected_value = {'add_changed': False,
         'app_type': 'iOS',
         'order_delv': True,
         'order_placed': True,
         'vid': '10142370647475443937'
    }
    actual_value = examine_visitor('10142370647475443937')
    assert expected_value == actual_value, f'Expected: {expected_value}, Actual: {actual_value}'


def test_examine_visitor_order_success():
    expected_value = {'add_changed': True,
         'app_type': 'iOS',
         'order_delv': True,
         'order_placed': True,
         'vid': '6548322090645166416'
    }
    actual_value = examine_visitor('6548322090645166416')
    assert expected_value == actual_value, f'Expected: {expected_value}, Actual: {actual_value}'
