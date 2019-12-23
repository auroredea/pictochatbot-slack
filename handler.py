# Events API : https://api.slack.com/events-api#events_api_request_urls
# Limit call : https://docs.aws.amazon.com/lambda/latest/dg/scaling.html#increase-concurrent-executions-limit
# Limit call : https://api.slack.com/events-api#rate_limiting
# Puis verifier signature à chaque appel https://github.com/slackapi/python-slack-events-api/blob/master/slackeventsapi/server.py
# https://api.slack.com/docs/verifying-requests-from-slack

import json

def endpoint(event, context):
    body = json.loads(event["body"]) if event["body"] else {}
    print(body)

    if "type" in body :
        if body["type"] == 'url_verification' :
            response = {
            "statusCode": 200,
            "isBase64Encoded": False,
            "headers": {
                "Content-Type": "text/plain"
            },
            "body": body["challenge"]
        }
    else : 
        response = {
        "statusCode": 400,
            "isBase64Encoded": False,
            "headers": {
                "Content-Type": "text/plain"
        }
    }

    return response