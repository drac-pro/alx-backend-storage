#!/usr/bin/env python3
"""python script that provides some stats about Nginx logs stored in MongoDB"""
from pymongo import MongoClient


def main():
    """main function to execute"""
    client = MongoClient()
    db = client.logs
    print(f'{db.nginx.count_documents({})} logs')

    print('Methods:')
    for method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
        method_count = db.nginx.count_documents({'method': method})
        print(f'\tmethod {method}: {method_count}')

    status_count = db.nginx.count_documents({'method': 'GET', 'path': '/status'})
    print(f'{status_count} status check')

    print('IPs:')
    pipeline = [
        {
            '$group': {
                '_id': '$ip',
                'count': {'$count': {}}
            }
        },
        {
            '$sort': {'count': -1}
        },
        {
            '$limit': 10
        }
    ]

    for addr in db.nginx.aggregate(pipeline):
        print(f'\t{addr["_id"]}: {addr["count"]}')


if __name__ == '__main__':
    main()
