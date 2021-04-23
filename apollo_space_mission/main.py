from argparse import ArgumentParser
import sys
import pandas as pd
from pathlib import Path
from glob import glob
import pyarrow.parquet as pq
import dask.dataframe as dd

def parse_config():
    my_args = ArgumentParser('ApolloSpaceMission')
    my_args.add_argument('-vid', '--full_visitor_id', dest='visitor_id', help='please provide a visitor id', required=True)
    return my_args.parse_args(sys.argv[1:])


def did_address_changed(target_client):
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
    hit_data = target_client.get('hit')
    for hit in hit_data:
        custom_dimensions = hit.get('customDimensions', [])
        frontEndId = [list(cd.values())[-1] for cd in custom_dimensions if '36' in cd.values()]
        if len(frontEndId) > 0:
            return frontEndId[0]
    return -1

def load_data(folder_path):
    data_dir = Path(__file__).parent.joinpath('data', folder_path)
    full_df = dd.read_parquet(data_dir, engine='pyarrow')
    return full_df




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

    # input validation
    if vid is None:
        return client_info
    #if isinstance(vid, str) and vid.isdigit:
    #    vid = int(vid)

    # Load the ga-session data as DataFrame
    ga_df = load_data('ga-sessions')
    #todo sort by longest session time or largest session time but still only one record
    client_df = ga_df[ga_df.fullvisitorid == vid]
    # If no client data, then return default client info since id doesn't exist
    if len(client_df.index) == 0:
        return client_info

    # Fill information related to ga-session dataset
    target_client = client_df.compute().to_dict(orient='records')[0]
    client_info['add_changed'] = did_address_changed(target_client)
    client_info['app'] = target_client.get('operatingSystem', 'not found')

    # Fill information related to transaction dataset
    td_df = load_data('transaction-data')
    fid = get_client_frontendid(target_client)
    trx_data = td_df[td_df.frontendOrderId == fid]
    client_info['order_placed'] = trx_data.empty
    client_info['order_delv'] = trx_data.get('declinereason_code') is None

    return client_info


if __name__ == '__main__':
    conf = parse_config()
    result = examine_visitor(conf.visitor_id)
    print(result)
