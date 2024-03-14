import pandas as pd
import logging

def interval_from_string(s: str) -> tuple:
    """Translate bracket-notation percent intervals to arithmetic mean

    The input format is assumed to be given in the format
    "[ 90 - 100% ]", #"[ 80 - 90% [", #"[ 30 - 40% [", "] 0 - 10% [" #"]0 - 5%["
    or as "None" (string)

    :param s: string of interval boundaries
    :return: mean of interval
    """

    if not isinstance(s, str):
        logging.error("interval_from_string: didnt get a string: %s", str(s))
        return (0, 0)
    elif s == "None":
        return (0, 0)

    try:
        z1, z2 = s.replace("[", "").replace("]", "").replace("%", "").split("-")
    except Exception:
        logging.error("interval_from_string: Unable to convert %s.", s)
        raise
    return (int(z1), int(z2))

def string_to_lower_upper(s: str) -> pd.Series:
    lower, upper = interval_from_string(s)
    return pd.Series({"lower": lower, "upper": upper})


def dbref2id(field: str) -> dict: 
    """Replacing a {"_ref": bson.DBRef, ...} object by the encapsulated ObjectId.
    This is for example necessary to retrieve the ObjectId from a mongoengine.DynamicField.

    :param field: fiel where the original reference shall be replaced by the respective ObjectId.
    :return: the stage which replaces the reference inplace.
    """
    rv = {
        "$addFields": {
            field: {
                "$let": {
                    "vars": {
                        "a": {
                            "$arrayElemAt": [
                                {"$objectToArray": f"${field}._ref"},
                                1,
                            ]
                        }
                    },
                    "in": "$$a.v",
                }
            }
        }
    }
    return rv


def dereference(field: str, collection: str) -> list[dict]:
    """Aggregation stages to resolve foreign collection link.

    :param field: field in current collection
    :param collection: which collection the field points to
    :param dynamic_field_fix: if the reference is a mongoengine.DynamicField instead
        of a mongoengine.ReferenceField, use this option.
    :return: aggregation stages which resolve the link, i.e., insert the linked object in place of
        the respective ObjectId.
    """
    rv = [
        {
            "$lookup": {
                "from": collection,
                "localField": field,
                "foreignField": "_id",
                "as": field,
            }
        },
        {
            "$addFields": {
                field: {
                    "$cond": {
                        "if": {"$ne": [{"$size": f"${field}"}, 0]},
                        "then": f"${field}",
                        "else": [{}],
                    }
                }
            }
        },
        {"$unwind": f"${field}"},
    ]

    return rv