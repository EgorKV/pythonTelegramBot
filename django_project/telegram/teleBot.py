import logging
import json
import requests
import datetime
from .test import testF

logging.basicConfig(filename="telebot.log", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

testF()


def log_exception(e):
    logging.error(
        "Function raised {exception_class} ({exception_docstring}): {exception_message}".format(
            exception_class=e.__class__,
            exception_docstring=e.__doc__,
            exception_message="error info" + str(e)))


def lod_response_status(response):
    logging.info("response from {response_url} at {time}: {result} with status {status}".format(
        response_url=response.url,
        time=datetime.datetime.now(),
        result=response.text,
        status=response.status_code))


def lod_request_status(request):
    logging.info("request at {time}: {result}".format(
        time=datetime.datetime.now(),
        result=str(request.body)))


class TeleBot:
    def __init__(self, request, botToken, urlT):
        self._botToken = botToken
        self._urlT = urlT
        self._request = request
        self.received_json_data = serialize_json(request.body)
        self.headersBot = {"Content-Type": "application/json"}
        lod_request_status(request)

    def sendMessage(self, text):
        """ sends message to user """
        if "callback_query" in self.received_json_data:
            botBody = {
                "chat_id": self.received_json_data["callback_query"]["message"]["chat"]["id"],
                "text": text
            }
        else:
            botBody = {
                "chat_id": self.received_json_data["message"]["chat"]["id"],
                "text": text
            }
        result = requests.post(self._urlT + "sendMessage",
                               json=botBody, headers=self.headersBot)
        lod_response_status(result)
        return result.status_code

    def sendMessageWithKeyboard(self, text, buttons):
        inlineButtons = initButtons(buttons)
        if "callback_query" in self.received_json_data:
            chat_id = self.received_json_data["callback_query"]["message"]["chat"]["id"]
        else:
            chat_id = self.received_json_data["message"]["chat"]["id"]
        botBody = {
            "chat_id": chat_id,
            "text": text,
            "reply_markup": {
                "inline_keyboard": inlineButtons
            }
        }
        result = requests.post(self._urlT + "sendMessage",
                               json=botBody, headers=self.headersBot)
        lod_response_status(result)
        return result.status_code

    def answerCallbackQuery(self, text="", show_alert=False):
        botBody = {
            "callback_query_id": self.received_json_data["callback_query"]["id"],
            "text": text,
            "show_alert": show_alert
        }
        result = requests.post(
            self._urlT + "answerCallbackQuery", json=botBody, headers=self.headersBot)
        lod_response_status(result)
        return serialize_json(result.text)

    # only for callback_query
    def editMessageText(self, text, buttons=[[]]):
        inlineButtons = initButtons(buttons)
        botBody = {
            "message_id": self.received_json_data["callback_query"]["message"]["message_id"],
            "chat_id": self.received_json_data["callback_query"]["message"]["chat"]["id"],
            "text": text,
            "reply_markup": {
                "inline_keyboard": inlineButtons
            }
        }
        result = requests.post(
            self._urlT + "editMessageText", json=botBody, headers=self.headersBot)
        lod_response_status(result)
        return result.status_code

    def answerInlineQuery(self, result_type):
        query_id = 23422
        query_type = "article"
        title = "hello"
        input_message_content = {"message_text": "well"}
        botBody = {
            "inline_query_id": self.received_json_data["inline_query"]["id"],
            "type": query_type,
            "id": query_id,
            "tittle": title,
            "input_message_content": input_message_content,
        }
        result = requests.post(
            self._urlT + "answerInlineQuery", json=botBody, headers=self.headersBot)
        lod_response_status(result)
        return result.status_code


def serialize_json(json_obj):
    try:
        received_json_data = json.loads(json_obj)
    except json.JSONDecodeError as e:
        log_exception(e)
        received_json_data = {}
    finally:
        return received_json_data


def initButtons(buttons):
    inlineButtons = []
    for row in buttons:
        row_of_buttons = []
        for button in row:
            row_of_buttons.append(
                {"text": button.get("text"), f"{button.get('type')}": button.get("data")})
        inlineButtons.append(row_of_buttons)
    return inlineButtons
