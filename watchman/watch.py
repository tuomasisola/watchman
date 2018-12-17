import importlib
import logging
import sys
import urllib

import client
import config


def get_reply(target):
    products = target.INFO.get('products')
    base_url = target.INFO.get('baseUrl')

    reply = []
    for path, target_value in products.items():
        try:
            url = urllib.parse.urljoin(base_url, path)
            elements = client.get_site_elements(url)
            current_value = target.get_current_value(elements)
            title = target.get_title(elements)
        except BaseException:
            continue
        if target.condition(current_value, target_value):
            reply.append(f'{title} is now at value {current_value}. '\
                         f'Check it out!\n\n{url}')
            logging.info(f'{title} meets the condition, '\
                          f'now at value: "{current_value}"')
        else:
            logging.info(f'{title} does not meet the given condition. '\
                         f'Current: "{current_value}", Target: "{target_value}"')
    return reply


def main():
    logging.basicConfig(level=logging.INFO)

    logging.info(f'Loading configurations')
    bot_token = config.TELEGRAM.get('botToken')
    chat_id = config.TELEGRAM.get('chatId')
    target_modules = config.TARGET_MODULES
    if not (bot_token and chat_id and target_modules):
        logging.error(f'Invalid configurations. BotToken: {bot_token} '
                        f'ChatId: {chat_id} TargetModules: {target_modules}')
        sys.exit(0)

    logging.info(f'Starting Watchman for targets {target_modules}')
    for module in target_modules:
        try:
            target = importlib.import_module(f'targets.{module}')
        except ModuleNotFoundError:
            logging.error(f'Module "{module}" not found!')
            continue

        reply = get_reply(target)
        if not reply:
            logging.info(f'No conditions met for {module}')
            continue

        try:
            client.send_tg_message('\n\n'.join(reply), bot_token, chat_id)
            logging.info('Sent a message to chat %s', chat_id)
        except BaseException:
            logging.exception('Could not send a message')
            continue

    logging.info(f'Watchman completed')


if __name__ == '__main__':
    main()
