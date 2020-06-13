from urllib.parse import urlencode

import requests


class Telegram:

    @staticmethod
    def telegram_bot_send_text(bot_message):
        bot_token = '700094640:AAEKqh3z7e6LfiXTXeFTpRnugSioqMkVA7o'
        bot_chat_id = ('1048049017', '680337670')
        for chat_id in bot_chat_id:
            query = {
                "chat_id": chat_id,
                "parse_mode": "markdown",
                "text": bot_message
            }
            send_text = "https://api.telegram.org/bot{token}/sendMessage?{query}" \
                .format(token=bot_token, query=urlencode(query))
            response = requests.get(send_text)
            print(response.json())

    @staticmethod
    def telegram_bot_delete_conversation():
        chat = requests.get("https://api.telegram.org/bot700094640:AAEKqh3z7e6LfiXTXeFTpRnugSioqMkVA7o/getUpdates")
        result_chat = chat.json()
        for conversation in result_chat.get('result'):
            message_id = conversation.get('message').get('message_id')
            chat_id = conversation.get('message').get('reply_to_message').get('chat').get('id')
            is_bot = conversation.get('message').get('reply_to_message').get('chat').get('is_bot')
            if is_bot:
                response_delete = requests.get(
                    "https://api.telegram.org/bot700094640:AAEKqh3z7e6LfiXTXeFTpRnugSioqMkVA7o/deleteMessage" +
                    "?chat_id=" + str(chat_id) + "&message_id=" + str(message_id)
                )
                print(response_delete.json())
