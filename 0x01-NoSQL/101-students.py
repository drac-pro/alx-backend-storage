#!/usr/bin/env python3
"""defines a function top_students()"""


def top_students(mongo_collection):
    """returns all students sorted by average score
    Args:
        mongo_collection: pymongo collection object
    Return:
        list: of students
    """
    pipeline = [
        {
            '$project': {
                'name': 1,
                'averageScore': {
                    '$avg': '$topics.score'
                }
            }
        },
        {
            '$sort': {'averageScore': -1}
        }
    ]
    return mongo_collection.aggregate(pipeline)
