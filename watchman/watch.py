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
            reply.append('{} is now at value {}. Check it out!\n\n{}'.format(
                                                    title, current_value, url))
            logging.info('{} meets the condition, now at value: "{}"'.format(
                                                    title, current_value))
        else:
            logging.info('{} does not meet the given condition. '\
                         'Current: "{}", Target: "{}"'.format(title,
                                                current_value, target_value))
    return reply


def main():
    logging_level = logging.INFO
    logging.basicConfig(filename='watch.log',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging_level)

    logging.info('Loading configurations')
    bot_token = config.TELEGRAM.get('botToken')
    chat_id = config.TELEGRAM.get('chatId')
    target_modules = config.TARGET_MODULES
    if not (bot_token and chat_id and target_modules):
        logging.error('Invalid configurations. BotToken: {} ChatId: {} '\
                      'TargetModules: {}'.format(bot_token,
                                                 chat_id, target_modules))
        sys.exit(0)

    logging.info('Starting Watchman for targets {}'.format(target_modules))
    for module in target_modules:
        try:
            target = importlib.import_module('targets.{}'.format(module))
        except ModuleNotFoundError:
            logging.error('Module "{}" not found!'.format(module))
            continue

        reply = get_reply(target)
        if not reply:
            logging.info('No conditions met for {}'.format(module))
            continue

        try:
            client.send_tg_message('\n\n'.join(reply), bot_token, chat_id)
            logging.info('Sent a message to chat %s', chat_id)
        except BaseException:
            logging.exception('Could not send a message')
            continue

    logging.info('Watchman completed')


if __name__ == '__main__':
    main()
