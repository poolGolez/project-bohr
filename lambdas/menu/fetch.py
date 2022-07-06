from domain import Menu
from marshaller import marshal_menu, marshal_menu_metadata
from repository import deserialize_menu, deserialize_menu_metadata
from request import http_response_ok

import boto3


DB_TABLE_NAME = "bohr-menu"

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(DB_TABLE_NAME)


@http_response_ok
def get_handler(event, _):
    merchant_id = event["pathParameters"]["merchantId"]
    menu_id = event["pathParameters"]["menuId"]
    menu = find_by_merchant_and_menu(merchant_id, menu_id)

    return marshal_menu(menu) if menu is not None else None


@http_response_ok
def list_handler(event, _):
    merchant_id = event["pathParameters"]["merchantId"]
    menus: list = find_all_metadata_by_merchant_id(merchant_id)

    return [marshal_menu_metadata(menu) for menu in menus]


def find_by_merchant_and_menu(merchant_id: str, menu_id: str) -> Menu:
    results = dynamodb.batch_get_item(
        RequestItems={
            DB_TABLE_NAME: {
                "Keys": [
                    {
                        "pk": f"MERCHANT#{merchant_id}",
                        "sk": f"MENU#{menu_id}"
                    },
                    {
                        "pk": f"MENU#{menu_id}",
                        "sk": f"MENU#{menu_id}"
                    }
                ]
            }
        }
    )

    query_results = results["Responses"][DB_TABLE_NAME]
    if(len(query_results) == 0):
        return None

    metadata = [item for item in query_results if item["pk"]
                == f"MERCHANT#{merchant_id}"][0]
    content = [item for item in query_results
               if item["pk"] == f"MENU#{menu_id}"][0]["content"]

    return deserialize_menu(metadata, content)


def find_all_metadata_by_merchant_id(merchant_id: str) -> list:
    results = table.query(
        KeyConditionExpression="#pk = :pk",
        ExpressionAttributeNames={
            "#pk": "pk"
        },
        ExpressionAttributeValues={
            ":pk": f"MERCHANT#{merchant_id}"
        }
    )
    return [deserialize_menu_metadata(item) for item in results["Items"]]
