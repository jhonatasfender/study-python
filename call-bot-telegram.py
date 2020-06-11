from urllib.parse import urlencode

import requests


def telegram_bot_sendtext(bot_message):
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
        respose = requests.get(send_text)
        print(respose.json())


telegram_bot_sendtext("""
```python
funciona merda nenhuma
```
[-](https://media-exp1.licdn.com/dms/image/C4D12AQFVVv3ppvrwkA/article-cover_image-shrink_423_752/0?e=1597276800&v=beta&t=gZrBegWMacw75lINscNtnB__F1mXjFzEK8pjZD3rCP8)
""")