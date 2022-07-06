import json


def http_response_ok(handler):
    def wrapper(event, context):
        result = handler(event, context)

        if(result is None):
            return {
                "statusCode": "404",
                "headers": {
                    "Content-type": "application/json"
                },
                "body": None
            }

        return {
            "statusCode": "200",
            "headers": {
                "Content-type": "application/json"
            },
            "body": json.dumps(result)
        }

    return wrapper
