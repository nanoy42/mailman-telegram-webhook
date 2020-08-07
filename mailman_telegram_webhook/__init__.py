"""
Archiver sending message to telegram chats.
"""

import logging
from configparser import NoOptionError

from telegram.ext import Updater

from mailman.config import config
from mailman.config.config import external_configuration
from mailman.interfaces.archiver import IArchiver
from zope.interface import implementer

logger = logging.getLogger("mailman.archiver")


def _log_error(exc):
    logger.error("Telegram webhook: %s", exc)


@implementer(IArchiver)
class Archiver(object):

    name = "telegram webhook"
    keys = [
        "archived-at",
        "delivered-to",
        "from",
        "cc",
        "to",
        "in-reply-to",
        "message-id",
        "subject",
        "x-message-id-hash",
        "references",
        "x-mailman-rule-hits",
        "x-mailman-rule-misses",
    ]
    config = None

    def _load_config(self):
        """Load configuration."""
        # Read our specific configuration file
        archiver_config = external_configuration(
            config.archiver.telegram_webhook.configuration
        )
        try:
            self.token = archiver_config.get("global", "token")
        except (KeyError, NoOptionError):
            self.token = None
            _log_error("No telegram token found in configuration")

        try:
            self.chat_id = archiver_config.get("global", "chat_id")
        except (KeyError, NoOptionError):
            self.chat_id = None

        try:
            self.filter_spam = archiver_config.get("global", "filter_spam")
        except (KeyError, NoOptionError):
            self.filter_spam = False

        try:
            for section in archiver_config.sections():
                if section.startswith("list."):
                    list_name = section[5:]
                    self.chats_id[list_name] = archiver_config[section]["chat_id"]
                else:
                    continue
        except (KeyError, NoOptionError) as e:
            _log_error(
                "While parsing the config for lists configuration, there was an error "
                + str(e.message)
            )

    def __init__(self):
        """Load config and prepare telegram bot"""
        self.chats_id = {}
        self._load_config()
        try:
            self.updater = Updater(token=self.token, use_context=True)
        except:
            _log_error("Unable to grab bot")

    def archive_message(self, mlist, msg):
        """Compute message and send it to telegram."""
        subject = "No subject"
        msg_content = msg.get_payload(None)
        try:
            subject = msg["subject"]
        except:
            pass

        format_dict = {"from": msg["from"], "to": msg["to"], "subject": subject}

        message = "New message from {from} to {to} : {subject}"

        information_msg = message.format(**format_dict)
        if (self.filter_spam and not "SPAM" in subject) or not self.filter_spam:
            self._send_to_telegram(information_msg, mlist.list_name)

    def _send_to_telegram(self, message, list_name):
        """
        Effectively send message to telegram

        It tries to get a specific chat_id and if it doesn't exists, it takes the general chat id.
        If no general chat id is specified, the messahe is then not sent.
        """
        try:
            chat_id = self.chats_id[list_name]
        except KeyError:
            chat_id = self.chat_id
        if chat_id:
            try:
                self.updater.bot.send_message(chat_id=chat_id, text=message)
            except:
                _log_error("Unable to send message")

    def list_url(self, mlist):
        """
        This doesn't make sense for webhook.
        But we must implement for IArchiver.
        """
        return None

    def permalink(self, mlist, msg):
        """
        This doesn't make sense for webhook. 
        But we must implement for IArchiver.
        """
        return None
