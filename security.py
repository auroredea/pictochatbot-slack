import os


class SecuritySlackAPI:
    def __init__(self):
        self.private_token_api = os.environ.get("BOT_VERIFICATION_TOKEN", "false_token")

    def verifyToken(self, token: str):
        if token == self.private_token_api:
            return True
        else: return False
