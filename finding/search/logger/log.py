import traceback

from finding.search.telegram import Telegram


class Logger:
    @staticmethod
    def log(i=None, name=None, link=None):
        if i and name and link:
            Telegram.telegram_bot_send_text(
                str(i + 1) + "\n" +
                "*" + name + "*\n" +
                "[link](" + link + ")\n" +
                "```log.py" + traceback.format_exc() + "```"
            )
            print(str([i + 1, name, link]))
        elif name and link:
            Telegram.telegram_bot_send_text(
                "*" + name + "*\n" +
                "[link](" + link + ")\n" +
                "```log.py" + traceback.format_exc() + "```"
            )
            print(str([name, link]))
        else:
            Telegram.telegram_bot_send_text("```log.py" + traceback.format_exc() + "```")

        print(traceback.format_exc())
