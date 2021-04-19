from argparse import ArgumentParser
import sys
import os



def parse_config():
    my_args = ArgumentParser('ApolloSpaceMission')
    my_args.add_argument('-vid', '--full_visitor_id', dest='visitor_id', help='please provide a visitor id', required=False)
    return my_args.parse_args(sys.argv[1:])


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
    print(conf.visitor_id)
