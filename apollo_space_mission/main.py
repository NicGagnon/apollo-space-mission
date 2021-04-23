from argparse import ArgumentParser
from pathlib import Path
import sys
import dask.dataframe as dd


def parse_config():
    """
    Argument parser for the full visitor id
    :return: string - full visitor id
    """
    my_args = ArgumentParser('ApolloSpaceMission')
    my_args.add_argument('-vid', '--full_visitor_id', dest='visitor_id', help='please provide a visitor id', required=True)
    return my_args.parse_args(sys.argv[1:])


def did_address_changed(target_client):
    """
    Check to see if the user changed his address at any point during his session by comparing geopoints
    :param target_client: dictionary with all user data
    :return: boolean value whether there's more than one geopoint for the user session
    """
    hit_data = target_client.get('hit')
    lats, longs = set(), set()
    for hit in hit_data:
        custom_dimensions = hit.get('customDimensions', [])
        lats.update([cd.get('value') for cd in custom_dimensions if cd.get('index') == 19])
        longs.update([cd.get('value') for cd in custom_dimensions if cd.get('index') == 18])
        # If there's ever more than one longitude or latitude, return True
        if len(lats) > 1 or len(longs) > 1:
            return True
    return False


def get_client_frontendid(target_client):
    """
    Retrieve the client front end id for matching against the transactionalData table
    :param target_client: dictionary with all user data
    :return: first front end id encountered or -1 in the case it's not found
    """
    hit_data = target_client.get('hit')
    for hit in hit_data:
        custom_dimensions = hit.get('customDimensions', [])
        frontEndId = [cd.get('value') for cd in custom_dimensions if cd.get('index') == 36]
        # As soon as you find a front end id, return it.
        if len(frontEndId) > 0:
            return frontEndId[0]
    return -1


def load_data(folder_path):
    """
    Return the loaded parquet data as a dask dataframe
    :param folder_path: name of the parquet folder
    :return: dask DataFrame
    """
    data_dir = Path(__file__).parent.joinpath('data', folder_path)
    full_df = dd.read_parquet(data_dir, engine='pyarrow')
    return full_df


def examine_visitor(vid):
    """
    Main calling function to extract client related information
    :param vid: fullvisitorId
    :return: dictionary with client information.
    {
        "vid": str,
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
    if not(isinstance(vid, str) or isinstance(vid, int)):
        return client_info
    client_info['vid'] = str(vid)

    # Load the ga-session data as DataFrame
    ga_df = load_data('ga-sessions')
    client_df = ga_df[ga_df.fullvisitorid == vid]
    # If no client data, then return default client info since id doesn't exist
    if len(client_df.index) == 0:
        return client_info

    # Fill information related to ga-session dataset
    df = client_df.nlargest(1, 'hits').compute()
    target_client = df.to_dict(orient='records')[0]
    client_info['add_changed'] = did_address_changed(target_client)
    client_info['app_type'] = target_client.get('operatingSystem', 'not found')

    # Fill information related to transaction dataset
    td_df = load_data('transaction-data')
    fid = get_client_frontendid(target_client)
    trx_data_df = td_df[td_df.frontendOrderId == fid].compute()
    client_info['order_placed'] = not trx_data_df.empty
    client_info['order_delv'] = False if trx_data_df.empty else trx_data_df.iloc[0]['declinereason_code'] is None

    return client_info


if __name__ == '__main__':
    conf = parse_config()
    result = examine_visitor(conf.visitor_id)
    print(result)
