#!/usr/bin/env python3
"""defines a function list_all(mongo_collection)"""


def list_all(mongo_collection):
    """lists all documents in a collection
    Args:
        mongo_collection(Collection): a database collection
    """
    return [doc for doc in mongo_collection.find()]
