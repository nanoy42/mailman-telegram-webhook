# Mailman Telegram Webhook

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Code style black](https://img.shields.io/badge/code%20style-black-000000.svg)]("https://github.com/psf/black)
[![GitHub release](https://img.shields.io/github/release/nanoy42/dinomail.svg)](https://github.com/nanoy42/dinomail/releases/)
[![PyPI version fury.io](https://badge.fury.io/py/mailman-telegram-webhook.svg)](https://pypi.org/project/mailman-telegram-webhook/)

Want to send message to telegram chats when receiving an email on a mailing list ? This script do it for you.

## Installation

### Installation procedure

It is possible to install the package via pip :

```
pip install mailman-telegram-webhook
```

but make sure to install it at good location. The config file is also downloaded with the python file.

Create the folder `/usr/lib/python3/dist-packages/mailman_telegram_webhook` and copy the `__init__.py` file inside.

You will need the python-telegram-bot package (as specified in the dependencies files).

Then copy the `mailam-telegram-webhook.cfg` file to `/ect/mailman3` and edit it :

 * You need to set the token to a valid telegram bot token
 * If you want, you can specify a global chat id. Messages will be sent to this chat when the archiver is enabled for a mailing-list but no specific chat id is defined. If you leave this chat id empty, nothing happens when the archiver is enabled for a list without specific chat id.
 * You can specify specific chat id in `[list.list_name]` sections

Then copy the following code to mailman configuration (`/etc/mailman3/mailman.cfg`) :
```
[archiver.telegram_webhook]
class: mailman_telegram_webhook.Archiver
enable: yes
configuration: /etc/mailman3/mailman-telegram-webhook.cfg
```

Note : By default, the archiver will be enable on every list and if a global chat id is defined, messages will be sent from every list to this chat.

### Configuration examples

```
[global]
token = 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
chat_id = 103

[list.contact]
chat_id = 104
```

We suppose that contact@my.domain and webmaster@my.domain have the archiver enabled and the token `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` (which is an example token) is associated to myBot.

 * A mail sent to contact@my.domain will make myBot send a message to the chat with id 104.
 * A mail sent to webmaster@my.domain will make myBot send a message to the the chat with id 103.

```
[global]
token = 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

[list.contact]
chat_id = 104
```

We suppose that contact@my.domain and webmaster@my.domain have the archiver enabled and the token `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` (which is an example token) is associated to myBot.

 * A mail sent to contact@my.domain will make myBot send a message to the chat with id 104.
 * A mail sent to webmaster@my.domain will make do nothing.

## Under the hood

This little script acts as an archiver (like Hyperkitty). When a message is received by mailman, if the archiver is configured and enabled on the mailing list, the message is passed to the archiver. The `archive_function` function just sends a message to telegram, according to the configuration.

The code is widely adapted from https://github.com/ondrejkolin/mailman_to_rocketchat and from Hyperkitty.

## FAQ

### How do I obtain a telegram bot token ?

You need to create a bot by speaking with @BotFather (see here for more information : https://core.telegram.org/bots)

### How do I find chat ids ?

You can chat with some specific bots to find the chat id or you can use the bot you created. Invite him on the group or chat with him and take a look to `https://api.telegram.org/bot<token>/getUpdates`

### What looks like the message on telegram ?

The message looks like `New message from {from} to {to} : {subject}`.

Example :

`New message from Yoann Pietri <me@nanoy.fr> to webmaster@my.domain : [Webmaster] Unable to access website`.

### Can I change the message on telegram ?

No. You cannot change it in the configuration but you can edit the message in the `__init__.py` file, in the `archive_message` function. 
