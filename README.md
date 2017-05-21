SlackHandler
===================
![Python versions](https://img.shields.io/badge/python-2.7-blue.svg)

An extension of Python's base `Handler` class that sends log records to a Slack channel via an Incoming Webhook. Written for Python 2.7, if you're using Python 3 you may want to check out [python-slack-logger](https://github.com/junhwi/python-slack-logger)

Installation
------------
Install the slackhandler module from [Pypi](https://pypi.python.org/pypi/slackhandler)
```bash
pip install slackhandler
```

Usage
-------
SlackHandler takes two arguments: `webhook_url` and `channel`. `webhook_url` is a unique url that Slack generates whenever you create a new [Incoming Webhook](https://api.slack.com/incoming-webhooks) integration for your Slack team. `channel` is an optional parameter that lets you override the default Slack channel configured in your Incoming Webhook.

```python
import logging
from slackhandler import SlackHandler

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a new SlackHandler
slack_handler = SlackHandler('<webhook_url>', '<channel>')
slack_handler.setLevel(logging.DEBUG)

# Add it to the logger
logger.addHandler(slack_handler)

# Send a log record
logger.debug('debug message')
```

SlackHandler does not accept any formatter. By default it's messages will have the following format:
![](https://jperezlatimes.github.io/slackhandler.png)
When logging an exception, 'Message Logged' will be replaced with the exception type and 'debug message' will be replaced with the traceback.
