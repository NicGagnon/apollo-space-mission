# third party imports
import pandas as pd
import pytest


@pytest.fixture
def fixed_location_client_data():
    """ Will return only the necessary fields that are actually accessed """
    data = \
    {
        'fullvisitorid': '10142370647475443937', 'visitId': 1552353680, 'hits': 273, 'operatingSystem': 'iOS',
        'hit':
             [
                 {'hitNumber': 1,  'customDimensions': [{'index': 11, 'value': 'home'}]},
                 {'hitNumber': 2,  'customDimensions': [{'index': 11, 'value': 'home'}]},
                 {'hitNumber': 3,  'customDimensions': [{'index': 15, 'value': 'CA'}, {'index': 40, 'value': 'true'}, {'index': 11, 'value': 'shop_list'}]},
                 {'hitNumber': 4,  'customDimensions': [{'index': 18, 'value': '-123.2409985'},{'index': 11, 'value': 'shop_list'}, {'index': 15, 'value': 'CA'}, {'index': 19, 'value': '49.2656613'},{'index': 16, 'value': 'Vancouver'}]},
                 {'hitNumber': 5,  'customDimensions': []},
                 {'hitNumber': 6,  'customDimensions': [{'index': 18, 'value': '-123.2409985'}, {'index': 16, 'value': 'Vancouver'}, {'index': 19, 'value': '49.2656613'}, {'index': 15, 'value': 'CA'}]},
                 {'hitNumber': 7,  'customDimensions': [{'index': 15, 'value': 'CA'}, {'index': 40, 'value': 'false'}, {'index': 11, 'value': 'other'}]},
                 {'hitNumber': 8,  'customDimensions': [{'index': 18, 'value': '-123.2409985'}, {'index': 11, 'value': 'other'}, {'index': 15, 'value': 'CA'}, {'index': 19, 'value': '49.2656613'}, {'index': 16, 'value': 'Vancouver'}]},
                 {'hitNumber': 9,  'customDimensions': [{'index': 11, 'value': 'home'}]},
                 {'hitNumber': 10, 'customDimensions': [{'index': 11, 'value': 'home'}]},
                 {'hitNumber': 11, 'customDimensions': [{'index': 15, 'value': 'CA'}, {'index': 40, 'value': 'false'}, {'index': 11, 'value': 'shop_list'}]},
                 {'hitNumber': 12, 'customDimensions': [{'index': 18, 'value': '-123.2409985'}, {'index': 11, 'value': 'shop_list'}, {'index': 15, 'value': 'CA'}, {'index': 19, 'value': '49.2656613'}, {'index': 16, 'value': 'Vancouver'}]},
                 {'hitNumber': 13, 'customDimensions': [{'index': 11, 'value': 'shop_list'}]},
                 {'hitNumber': 14, 'customDimensions': [{'index': 15, 'value': 'CA'}, {'index': 40, 'value': 'false'}, {'index': 11, 'value': 'user_account'}]},
                 {'hitNumber': 15, 'customDimensions': [{'index': 15, 'value': 'CA'}, {'index': 40, 'value': 'false'}, {'index': 11, 'value': 'user_account'}]},
                 {'hitNumber': 16, 'customDimensions': []},
                 {'hitNumber': 17, 'customDimensions': [{'index': 15, 'value': 'CA'}, {'index': 40, 'value': 'false'},{'index': 11, 'value': 'user_account'}]},
                 {'hitNumber': 18, 'customDimensions': [{'index': 18, 'value': '-123.2409985'}, {'index': 16, 'value': 'Vancouver'}, {'index': 19, 'value': '49.2656613'}, {'index': 15, 'value': 'CA'}]},
                 {'hitNumber': 19, 'customDimensions': []},
                 {'hitNumber': 20, 'customDimensions': []},
                 {'hitNumber': 21, 'customDimensions': [{'index': 15, 'value': 'CA'}, {'index': 40, 'value': 'true'}, {'index': 11, 'value': 'shop_list'}]},
                 {'hitNumber': 22, 'customDimensions': [{'index': 15, 'value': 'CA'}, {'index': 40, 'value': 'true'}, {'index': 11, 'value': 'other'}]},
                 {'hitNumber': 23, 'customDimensions': [{'index': 18, 'value': '-123.2409985'}, {'index': 11, 'value': 'other'}, {'index': 15, 'value': 'CA'}, {'index': 19, 'value': '49.2656613'}, {'index': 16, 'value': 'Vancouver'}]},
                 {'hitNumber': 24, 'customDimensions': [{'index': 19, 'value': '49.2656613'}, {'index': 18, 'value': '-123.2409985'}, {'index': 11, 'value': 'shop_list'}, {'index': 16, 'value': 'Vancouver'}, {'index': 15, 'value': 'CA'}]},
                 {'hitNumber': 25, 'customDimensions': [{'index': 15, 'value': 'CA'}]},
                 {'hitNumber': 26, 'customDimensions': [{'index': 15, 'value': 'CA'}]},
                 {'hitNumber': 27, 'customDimensions': [{'index': 15, 'value': 'CA'}, {'index': 40, 'value': 'true'}, {'index': 11, 'value': 'other'}]},
                 {'hitNumber': 28, 'customDimensions': [{'index': 15, 'value': 'CA'}, {'index': 40, 'value': 'true'}, {'index': 11, 'value': 'other'}]},
                 {'hitNumber': 29, 'customDimensions': [{'index': 15, 'value': 'CA'}]},
                 {'hitNumber': 30, 'customDimensions': [{'index': 15, 'value': 'CA'}, {'index': 40, 'value': 'true'}, {'index': 11, 'value': 'other'}]}
             ]
    }
    return data


@pytest.fixture
def dynamic_location_client_data():
    """ Will return only the necessary fields that are actually accessed """
    data = \
    {
        'fullvisitorid': '10142370647475443937', 'visitId': 1552353680, 'hits': 273, 'operatingSystem': 'iOS',
        'hit':
             [
                 {'hitNumber': 1,  'customDimensions': [{'index': 18, 'value': '-123.2409985'},{'index': 15, 'value': 'CA'}, {'index': 40, 'value': 'true'}, {'index': 11, 'value': 'shop_list'}, {'index': 19, 'value': '49.2656613'}]},
                 {'hitNumber': 2,  'customDimensions': [{'index': 18, 'value': '-125.2409985'},{'index': 11, 'value': 'shop_list'}, {'index': 15, 'value': 'CA'}, {'index': 19, 'value': '59.2656613'},{'index': 16, 'value': 'Vancouver'}]},
                 {'hitNumber': 3, 'customDimensions': [{'index': 15, 'value': 'CA'}, {'index': 40, 'value': 'true'}, {'index': 11, 'value': 'other'}]}
             ]
    }
    return data


@pytest.fixture
def missing_client_data():
    """ Will return only the necessary fields that are actually accessed """
    data = \
    {
        'fullvisitorid': '10142370647475443937', 'visitId': 1552353680, 'hits': 273, 'operatingSystem': 'iOS',
        'hit':
             [
                 {'hitNumber': 1,  'customDimensions': [{'index': 15, 'value': 'CA'}, {'index': 40, 'value': 'true'}, {'index': 11, 'value': 'shop_list'}]},
                 {'hitNumber': 2,  'customDimensions': [{'index': 11, 'value': 'shop_list'}, {'index': 15, 'value': 'CA'},{'index': 16, 'value': 'Vancouver'}]},
                 {'hitNumber': 3, 'customDimensions': [{'index': 15, 'value': 'CA'}, {'index': 40, 'value': 'true'}, {'index': 11, 'value': 'other'}]}
             ]
    }
    return data

@pytest.fixture
def frontendid_client_data():
    """ Will return only the necessary fields that are actually accessed """
    data = \
    {
        'fullvisitorid': '10142370647475443937', 'visitId': 1552353680, 'hits': 273, 'operatingSystem': 'iOS',
        'hit':
             [
                 {'hitNumber': 1,  'customDimensions': [{'index': 15, 'value': 'CA'}, {'index': 40, 'value': 'iOS'}, {'index': 11, 'value': 'shop_list'}]},
                 {'hitNumber': 2,  'customDimensions': [{'index': 11, 'value': 'shop_list'}, {'index': 15, 'value': 'CA'},{'index': 16, 'value': 'Vancouver'}]},
                 {'hitNumber': 3, 'customDimensions': [{'index': 15, 'value': 'CA'}, {'index': 36, 'value': 's4na-atun'}, {'index': 11, 'value': 'other'}]}
             ]
    }
    return data

@pytest.fixture
def multi_frontendid_client_data():
    """ Will return only the necessary fields that are actually accessed """
    data = \
    {
        'fullvisitorid': '10142370647475443937', 'visitId': 1552353680, 'hits': 273, 'operatingSystem': 'iOS',
        'hit':
             [
                 {'hitNumber': 1,  'customDimensions': [{'index': 15, 'value': 'CA'}, {'index': 36, 'value': 's2kb-lr7z'}, {'index': 11, 'value': 'shop_list'}]},
                 {'hitNumber': 2,  'customDimensions': [{'index': 11, 'value': 'shop_list'}, {'index': 15, 'value': 'CA'},{'index': 16, 'value': 'Vancouver'}]},
                 {'hitNumber': 3, 'customDimensions': [{'index': 15, 'value': 'CA'}, {'index': 36, 'value': 's4na-atun'}, {'index': 11, 'value': 'other'}]}
             ]
    }
    return data