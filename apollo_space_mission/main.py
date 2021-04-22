from argparse import ArgumentParser
import sys
import os
import simplejson
import pandas as pd
from pathlib import Path


def parse_config():
    my_args = ArgumentParser('ApolloSpaceMission')
    my_args.add_argument('-vid', '--full_visitor_id', dest='visitor_id', help='please provide a visitor id', required=False)
    return my_args.parse_args(sys.argv[1:])

def address_changed(target_client):
    hit_data = target_client.get('hit')
    lats, longs = [], []
    for hit in hit_data:
        custom_dimensions = hit.get('customDimensions', [])
        lats.extend([list(cd.values())[-1] for cd in custom_dimensions if '19' in cd.values()])
        longs.extend([list(cd.values())[-1] for cd in custom_dimensions if '18' in cd.values()])
        if len(set(lats)) > 1 or len(set(longs)) > 1:
            return True
    return False


def get_client_frontendid(target_client):
    pass


def get_client_app_type(target_client):
    pass


def examine_visitor(vid):
    """
    Main calling function to extract client related information
    :param vid: fullvisitorId
    :return: dictionary with client information.
    {
        "vid": int,
        "add_changed": bool,
        "order_placed": bool,
        "order_delv": bool,
        "app_type": str # options: [iOS | Android | BlackBerry]
    }
    """

    # Default return body
    client_info = {
        "vid": -1,
        "add_changed": False,
        "order_placed": False,
        "order_delv": False,
        "app_type": "n/a"
    }

    data_dir = Path(__file__).parent.joinpath('data')

    # input validation
    if vid is None:
        return client_info
    if isinstance(vid, str) and vid.isdigit:
        vid = int(vid)

    # Load the ga-sesion data as DataFrame
    ga_df = pd.read_json(data_dir.joinpath('ga-sessions.json'), orient='records')
    client_data = ga_df[ga_df.fullvisitorid == vid]

    # If no client data, then return default client info since id doesn't exist
    if client_data.empty:
        return client_info

    # Fill information related to ga-session dataset
    target_client = client_data.to_dict(orient='records')[0]
    client_info['add_changed'] = address_changed(target_client)
    client_info['app'] = get_client_app_type(target_client)

    # Fill information related to transaction dataset
    td_df = pd.read_json(data_dir.joinpath('transactionData.json'), orient='records')
    fid = get_client_frontendid(target_client)
    trx_data = td_df[td_df.frontendOrderId == fid]
    client_info['order_placed'] = trx_data.empty
    client_info['order_delv'] = trx_data.get('declinereason_code') is None

    return client_info


def format_output(result):
    """
    format output for individual visitor
    :param result:
    # :return: dictionary with client information.
    {
        "vid": int,
        "add_changed": bool,
        "order_placed": bool,
        "order_delv": bool,
        "app_type": str # options: [iOS | Android | BlackBerry]
    }
    # """
    return {
                "full_visitor_id": result.get("vid"),
                "address_changed": result.get("add_changed"),
                "is_order_placed": result.get("order_placed"),
                "Is_order_delivered": result.get("order_delv"),
                "application_type": result.get("app_type")
            }

if __name__ == '__main__':
    conf = parse_config()
    examine_visitor(conf.visitor_id)
    print(conf.visitor_id)
