# Puis verifier signature à chaque appel https://github.com/slackapi/python-slack-events-api/blob/master/slackeventsapi/server.py
# https://api.slack.com/docs/verifying-requests-from-slack
# Puis CI automatisée CircleCI + Github
# Puis redis contextualisé

import json
import logging
import os
from typing import Any, Dict, Optional
from nlp import PictoNlp

import boto3

import requests
from security import SecuritySlackAPI

BOT_VERIFICATION_TOKEN = os.environ.get(
    "BOT_VERIFICATION_TOKEN", "false_token")
BOT_OAUTH2_TOKEN = os.environ.get("BOT_OAUTH2_TOKEN", "false_token")
security = SecuritySlackAPI()
nlp = PictoNlp()


def endpoint(event: Dict, context: Dict) -> Dict[str, Any]:
    body = json.loads(event["body"]) if event["body"] else {}

    if "type" in body:
        # signature verification
        if body["type"] == "url_verification":
            return _response(status=200, body=body["challenge"])

        if body["type"] == "event_callback":
            # app mentions and im
            if security.verifyToken(body["token"]) and not _event_from_bot(body["event"]):
                _send_to_sqs(event=body["event"])
                return _response(status=200)
            else:
                return _response(status=400)

        return _response(status=200)

    return _response(status=400)


def event_handler(event: Dict, context: Dict) -> None:
    messages = map(_extract_message_from_sqs_record, event["Records"])

    for message in messages:
        _handle_slack_event(event=message)


# Internal functions
def _event_from_bot(event: Dict) -> bool:
    return "subtype" in event and event["subtype"] == "bot_message"


def _handle_slack_event(event: Dict) -> None:
    print(f"RECEIVED EVENT: {event}")
    text = nlp.parse(event["text"])
    print(f"NLP : {text}")
    answer = nlp.intentToResponse(text.intent)

    headers = {
        "Authorization": f"Bearer {BOT_OAUTH2_TOKEN}"
    }

    message = {
        "channel": event["channel"],
        "text": answer,
        "mrkdwn": True
    }
    url = "https://slack.com/api/chat.postMessage"

    response = requests.post(url=url, json=message, headers=headers)
    response.raise_for_status()


def _send_to_sqs(event: Dict) -> None:
    sqs = boto3.client("sqs")
    queue_url = os.environ["EVENT_QUEUE_URL"]
    sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(event))


def _extract_message_from_sqs_record(record: Dict) -> Dict[str, Any]:
    return json.loads(record["body"])


def _response(status: int, body: Optional[Any] = None) -> Dict[str, Any]:
    return {
        "statusCode": status,
        "isBase64Encoded": False,
        "headers": {"Content-Type": "text/plain"},
        "body": body
    }
