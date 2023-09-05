from os import getenv
from json import loads, JSONDecodeError
from logging import basicConfig, info, debug, warning, error

import boto3
from botocore.vendored.requests import get, put, post


PARAMS = {
    "accountIdentifier": getenv("HARNESS_ACCOUNT_ID"),
    "routingId": getenv("HARNESS_ACCOUNT_ID"),
}
HEADERS = {
    "x-api-key": getenv("HARNESS_PLATFORM_API_KEY"),
}

basicConfig(level=getenv("LOGLEVEL", "WARNING").upper())


def connector_exists(identifier: str) -> bool:
    resp = get(
        "https://app.harness.io/ng/api/connectors/" + identifier,
        params=PARAMS,
        headers=HEADERS,
    )

    if resp.status_code == 200:
        debug(f"connector exists: {identifier}")
        return True
    else:
        debug(resp.text)
        return False


def update_connector(payload: dict) -> bool:
    resp = put(
        "https://app.harness.io/gateway/ng/api/connectors",
        params=PARAMS,
        headers=HEADERS,
        json=payload,
    )

    if resp.status_code == 200:
        info(f"updated connector: {payload['connector']['identifier']}")
        return True
    else:
        error(resp.text)
        return False


def create_connector(payload: dict):
    resp = post(
        "https://app.harness.io/gateway/ng/api/connectors",
        params=PARAMS,
        headers=HEADERS,
        json=payload,
    )

    if resp.status_code == 200:
        info(f"created connector: {payload['connector']['identifier']}")
        return True
    else:
        error(resp.text)
        return False


def get_accounts(client: boto3.client) -> list:
    resp = client.list_accounts()

    accounts = resp.get("Accounts", [])

    while resp.get("NextToken"):
        resp = client.list_accounts(NextToken=resp.get("NextToken"))

        accounts.extend(resp.get("Accounts", []))

    return accounts


def get_org_client(role_to_assume: str, session_name: str) -> boto3.client:
    if role_to_assume:
        sts = boto3.client("sts")

        resp = sts.assume_role(RoleArn=role_to_assume, RoleSessionName=session_name)

        credentials = response["Credentials"]

        organizations = boto3.client(
            "organizations",
            aws_access_key_id=credentials["AccessKeyId"],
            aws_secret_access_key=credentials["SecretAccessKey"],
            aws_session_token=credentials["SessionToken"],
        )
    else:
        organizations = boto3.client("organizations")

    return organizations


def build_connector(
    role_name: str,
    account_id: str,
    account_name: str,
    external_id: str,
    features: list,
    gov_cloud: bool,
    tags: dict,
):
    payload = {
        "connector": {
            "name": account_name.replace("-", "_").replace(" ", "_").replace(".", "_"),
            "identifier": f"aws{account_id}",
            "tags": tags,
            "spec": {
                "crossAccountAccess": {
                    "crossAccountRoleArn": f"arn:aws:iam::{account_id}:role/{role_name}",
                    "externalId": external_id,
                },
                "curAttributes": None,
                "awsAccountId": account_id,
                "isAWSGovCloudAccount": gov_cloud,
                "featuresEnabled": features,
            },
            "type": "CEAws",
        },
    }

    if connector_exists(payload["connector"]["identifier"]):
        update_connector(payload)
    else:
        create_connector(payload)


def main():
    cross_account_role_name = getenv("CROSS_ACCOUNT_ROLE_NAME")
    if not cross_account_role_name:
        error(f"Need to set CROSS_ACCOUNT_ROLE_NAME")
        return

    external_id = getenv("EXTERNAL_ID")
    if not external_id:
        error(f"Need to set EXTERNAL_ID")
        return

    try:
        tags = loads(getenv("TAGS", "{}"))
    except json.JSONDecodeError as e:
        warning("Unable to format tags from given json")
        tags = {}

    features = getenv("FEATURES")
    if features:
        features = features.split(",")
    else:
        features = ["GOVERNANCE", "VISIBILITY"]

    gov_cloud = getenv("GOVCLOUD", "false").lower() == "true"

    ignore = getenv("IGNORE", "").split(",")

    role_to_assume = getenv("ROLE_TO_ASSUME")
    session_name = getenv("SESSION_NAME", "harness-ccm-aws-org-connectors")
    organizations = get_org_client(role_to_assume, session_name)

    for account in [
        x
        for x in get_accounts(organizations)
        if (x.get("Status") == "ACTIVE") and (x.get("Id") not in ignore)
    ]:
        build_connector(
            cross_account_role_name,
            account.get("Id"),
            account.get("Name"),
            external_id,
            features,
            gov_cloud,
            tags,
        )


def lambda_handler(event, context):
    main()


if __name__ == "__main__":
    main()
