from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .teleBot import TeleBot
from .models import Chat
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from .serializer import ChatSerializer
from rest_framework.response import Response
from datetime import datetime
from django.utils.translation import gettext as _, activate
from django.utils.text import _
from django.utils.text import format_lazy
urlT = 'https://api.telegram.org/bot899061394:AAFefj4ey2FMpzOkI08CN1Xri6R9SuiEFRo/'
token = "899061394:AAFefj4ey2FMpzOkI08CN1Xri6R9SuiEFRo"
BOT_NAME = "@noostarBot"


class ListStudents(APIView):

    def get(self, request, format=None):
        chats = Chat.objects.all()
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data, status=200)


@csrf_exempt
def botresponse(request):
    bot = TeleBot(request, token, urlT)
    json_data = bot.received_json_data
    result = 500
    if "message" in json_data:
        chat_id = json_data["message"]["chat"]["id"]
        chat_time = json_data["message"]["date"]
    elif "callback_query" in json_data:
        chat_id = json_data["callback_query"]["message"]["chat"]["id"]
    else:
        return HttpResponse({}, status=200)
    if len(Chat.objects.filter(chat_id=chat_id)) == 0:
        chat = Chat(chat_id=chat_id, time=datetime.fromtimestamp(
            chat_time), place='telegram')
        chat.save()
    else:
        chat = Chat.objects.get(chat_id=chat_id)
    language = chat.language
    activate(language)
    if "message" in json_data:
        if "text" in json_data["message"]:
            if json_data["message"]["text"] == "/start":
                result = bot.sendMessageWithKeyboard(_("Welcome to IT and Engineering School 'Noostar'. Please select language for communication."), [[
                    {"text": "Українська", "data": "uk", "type": "callback_data"}, {"text": "Русский", "data": "ru", "type": "callback_data"}, {"text": "English", "data": "en", "type": "callback_data"}]])
            else:
                text = _("For starting conversation with bot, you can use command'/start'")
                result = bot.sendMessageWithKeyboard(text, [[]])
        elif "contact" in json_data["message"]:
            chat.telephone_number = json_data["message"]["contact"]["phone_number"]
            chat.name = json_data["message"]["contact"]["first_name"]
            if "user_id" in json_data["message"]["contact"]:
                if json_data["message"]["contact"]["user_id"] == json_data["message"]["from"]["id"]:
                    chat.chat_owner_contacts = True
                else:
                    chat.chat_owner_contacts = False
            chat.save()
            text = _("Thank you for your contacts. You can change them in 'menu'")
            button_text = [_("return to menu")]
            result = bot.sendMessageWithKeyboard(text, [[{
                "text": button_text[0], "data": language, "type": "callback_data",
            }]])
        else:
            text = _("For starting conversation with bot, you can use command'/start'")
            result = bot.sendMessageWithKeyboard(text, [[]])
    elif "callback_query" in json_data:
        result = bot.answerCallbackQuery()
        if result["ok"] is True:
            result = 500
            query_data = json_data["callback_query"]["data"]
            if query_data == 'language':
                text = _("Please, choose language")
                button_text = ["Українська", "Русский", "English"]
                result = bot.editMessageText(text, [[
                    {"text": button_text[0], "data": "uk",
                        "type": "callback_data"},
                    {"text": button_text[1], "data": "ru",
                        "type": "callback_data"},
                    {"text": button_text[2], "data": "en",
                        "type": "callback_data"},
                ]])

            elif query_data in ['uk', 'ru', 'en']:
                chat.language = query_data
                chat.save()
                activate(query_data)
                if chat.student is None:
                    text = _("You are interested in")
                    button_text = [_("studying"), _("teaching")]
                    result = bot.editMessageText(text, [[
                        {"text": button_text[0], "data": f"study",
                         "type": "callback_data"},
                        {"text": button_text[1], "data": f"work",
                         "type": "callback_data"}]])
                else:
                    text = _("What do you want to do?")
                    button_text = [
                        _("change information"), _("look through filled in information"), _("change language")]
                    result = bot.editMessageText(text, [
                        [{"text": button_text[0], "data": "start",
                            "type": "callback_data"}],
                        [{"text": button_text[1], "data": "info",
                            "type": "callback_data"}],
                        [{"text": button_text[2], "data": "language", "type": "callback_data"}]])
            elif query_data == 'start':
                text = _("You are interested in")
                button_text = [_("studying"), _("teaching")]
                result = bot.editMessageText(text, [[
                    {"text": button_text[0], "data": f"study",
                     "type": "callback_data"},
                    {"text": button_text[1], "data": f"work",
                     "type": "callback_data"}]])
            elif query_data == 'study':
                chat.student = True
                chat.save()
                text = _("In which direction would you like to develop")
                button_text = [_("programming"), _("system administration"), _("telecommunications"), _("security")]
                result = bot.editMessageText(text, [
                    [{"text": button_text[0],
                        "data": "programming", "type": "callback_data"}],
                    [{"text": button_text[1],
                        "data": "system_administration", "type": "callback_data"}],
                    [{"text": button_text[2],
                        "data": "telecomunication", "type": "callback_data"}],
                    [{"text": button_text[3],
                        "data": "security", "type": "callback_data"}]])
            elif query_data == 'work':
                text = _("we are interested in working with teachers and mentors who specialize in teaching disciplines for IT specialists. In future we want to increase amount of disciplines, that is why we are also interested in cooperation with other teachers, in first place, with teachers of natural sciences. In any case, if you have experience in teaching, teachin materials and a desire to work for a decent pay, write to us. If you are interested, leave you contacts.")
                button_text = [_("return to menu"),
                               _("you dont know how to leave contacts")]
                chat.student = False
                chat.save()
                result = bot.editMessageText(
                    text, [
                        [{"text": button_text[0], "data": language,
                            "type": "callback_data"}],
                        [{"text": button_text[1], "data": "help", "type": "callback_data"}]])
            elif query_data in ['programming', 'system_administration', 'telecomunication', 'security']:
                if query_data == 'system_administration':
                    query_data = 'system administration'
                chat.specialization = query_data
                chat.save()
                text = _("Which level of knowledge would you like to receive?")
                button_text = [_("starter"), _("middle"), _("advanced")]
                result = bot.editMessageText(text, [
                    [{"text": button_text[0], "data": "starter 250",
                        "type": "callback_data"}],
                    [{"text": button_text[1], "data": "middle 350-400",
                      "type": "callback_data"}],
                    [{"text": button_text[2], "data": "advanced 400-500",
                        "type": "callback_data"}]])
            elif query_data in ['starter 250', 'middle 350-400', 'advanced 400-500']:
                chat.knowledge_level = query_data
                chat.save()
                knowledge_level_data = chat.knowledge_level.split(' ')
                knowledge_level = _(knowledge_level_data[0])
                price = _(knowledge_level_data[1])
                text = _("Thank you for your information. We are pleased to offer you our assistance in achieving your goal. We have experience in training professionals in the above fields. The estimated cost of the {} level of knowledge is {} UAH per hour. The specific cost of your training may be determined after the initial communication. So, if you are interested, please leave your contacts.").format(knowledge_level, price)
                button_text = [_('return to menu'),
                               _('you dont know how to leave contacts')]
                result = bot.editMessageText(
                    text, [
                        [{"text": button_text[0], "data": language,
                            "type": "callback_data"}],
                        [{"text": button_text[1], "data": "help", "type": "callback_data"}]])
            elif query_data == 'info':
                name = chat.name
                telephone_number = chat.telephone_number
                wish = _('studying') if chat.student else _('teaching')
                text = _("name - {}\ntelephone number - {}\nYou wish {}\n").format(name, telephone_number, wish)
                if chat.student is True:
                    specialization = _(chat.specialization)
                    knowledge_level = _(chat.knowledge_level.split(' ')[0])
                    text += _("specialization - {}\nknowledge level - {}\n").format(specialization, knowledge_level)
                text += _("To change information, choose in 'menu' - 'change information', if you want to change you telephone number send other contacts to us.")
                button_text = [_("return to menu"),
                               _("you dont know how to leave contacts")]
                result = bot.editMessageText(text, [
                    [{"text": button_text[0], "data": language, "type": "callback_data"}],
                    [{"text": button_text[1], "data": "help", "type": "callback_data"}]])
            elif query_data == 'help':
                text = _("To send contacts, push on 'context meny' button and choose 'send your phone number'")
                button_text = [_("return to menu")]
                result = bot.editMessageText(text, [[{
                    "text": button_text[0], "data": language, "type": "callback_data"
                }]])
            else:
                pass
                # if language == 'uk':
                #     text = "Щоб почати діалог з ботом, скористуйтеся командою /start"
                # else:
                #     text = "Что бы начать диалог с ботом, воспользуйтесь командой /start"
                # result = bot.sendMessageWithKeyboard(text, [[]])
        else:
            pass
            # if language == 'uk':
            #     text = "Щоб почати діалог з ботом, скористуйтеся командою /start"
            # else:
            #     text = "Что бы начать диалог с ботом, воспользуйтесь командой /start"
            # result = bot.sendMessageWithKeyboard(text, [[]])
    else:
        text = _("For starting conversation with bot, you can use command'/start'")
        result = bot.sendMessageWithKeyboard(text, [[]])
    return HttpResponse({}, status=result)
