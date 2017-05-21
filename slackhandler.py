#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import json
import requests
import traceback
import time
import datetime
from logging import Handler


class SlackHandler(Handler):
    def __init__(self, webhook_url, channel=None):
        # Make sure the url string begins with https://
        webhook_url = re.sub(r'http(?:s*):\/\/', '', webhook_url)
        self.url = 'https://' + webhook_url
        self.channel = channel

        # Finish spinning up the base log handler class
        Handler.__init__(self)

    def get_msg_color(self, record):
        if record.levelname == 'DEBUG':
            return 'good'  # green
        elif record.levelname == 'INFO':
            return '#26d6e5'  # blue
        elif record.levelname == 'WARNING':
            return 'warning'  # Yellow/Orange
        elif record.levelname == 'ERROR':
            return 'danger'  # Red
        elif record.levelname == 'CRITICAL':
            return 'danger'  # Red

    def format_record(self, record):
        import pprint
        pp = pprint.PrettyPrinter(indent=4)

        # Default values
        exception = 'Message logged'
        logline = record.msg
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

        # If there is exception info,
        # get the exception name and the traceback
        if record.exc_info:
            exception = type(record.exc_info[1]).__name__
            logline = traceback.format_exc()
            timestamp = record.asctime

        # Format the message for Slack and make it pretty
        slack_msg = {
            "text": "*" + record.levelname + "*",
            "attachments": [
                {
                    "title": timestamp,
                    "text": "`" + exception + "` in _" + record.pathname + "_\n```" + logline + "```",
                    "color": self.get_msg_color(record),
                    "mrkdwn_in": ["text"]
                }
            ]
        }

        # Return the formatted slack message
        if self.channel:
            slack_msg['channel'] = self.channel

        return json.dumps(slack_msg)

    def emit(self, record):
        try:
            slack_msg = self.format_record(record)
            requests.post(self.url, data=slack_msg)
        except Exception:
            self.handleError(record)
