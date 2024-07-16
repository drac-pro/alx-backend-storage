#!/usr/bin/env python3
"""defines a function update_topics()"""


def update_topics(mongo_collection, name, topics):
    """changes all topics of a school document based on the name
    Args:
        mongo_collection: the pymongo collection object
        name(string): school name to update
        topics(list[strings]): list of topics approached in the school
    """
    mongo_collection.update_many(
        {'name': name},
        {'$set': {'topics': topics}}
    )
