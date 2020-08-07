from distutils.core import setup

try:
    with open(
        os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8"
    ) as f:
        long_description = f.read()
except:
    long_description = None


setup(
    name = 'mailman-telegram-webhook',
    packages = ['mailman_telegram_webhook'],
    version = '0.1',
    license='GPLv3',
    description = 'A small archiver sending message to telegram chats ',
    long_description=long_description,
    author = 'Yoann Piétri',
    author_email = 'me@nanoy.fr',
    url = 'https://github.com/nanoy42/mailman-telegram-webhook',
    download_url = 'https://github.com/nanoy42/mailman-telegram-webhook/archive/v_01.tar.gz',    # I explain this later on
    keywords = ['mailman', 'telegram', 'webhook'],
    install_requires=[
        'python-telegram-bot'
    ],
    include_package_data=True,
)
