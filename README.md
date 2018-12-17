# Watchman

Tired of keeping track of changes on your favorite website?

Worry no more! Watchman is a Python superhero that will keep track of everything – forever.

Thanks to groundbreaking modular architecture, you can develop your own tracking algorithms, without the need to consider IO, UI, UX or other nonrelevant stuff. Make the internet your `*****` already today!

## How does it work?

Watchman sends you a Telegram message if some of the pre-configured conditions are met. (For example the *comixology* algorithm checks if some of the tracked comics are below the set target price) The message is only sent if the condition is met on the targets, so you can set up [Cron](https://www.raspberrypi.org/documentation/linux/usage/cron.md) to run Watchman daily. This way you will never miss a deal!

The condition function on the algorithm can be arbitrary, so the use cases of Watchman is not limited to price tracking. (Crazy, I know!)

## Algorithms
Algorithm is a special module found in `watchman/targets` folder. Valid algorithm needs to contain four things.

1. `INFO` dictionary
2. `get_current_value()` function
2. `get_title()` function
3. `condition()` function

See example module *comixology* in the folder.

## Configurations
You need to include `config.py` file in the `watchman` folder. There is already `config-example.py` to get you started. Be sure to include your BotToken, chatId, and a set of modules activated.

## Run the module
```
make build
make run
```
