#!/usr/bin/env python3
"""defines a function schools_by_topic()"""


def schools_by_topic(mongo_collection, topic):
    """ returns the list of school having a specific topic
    Args:
        mongo_collection: pymongo collection object
        topic(sting): topic searched
    Return:
        list: list of schools having topic
    """
    return [school for school in mongo_collection.find({'topics': topic})]
