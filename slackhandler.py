#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import json
import requests
import traceback
from logging import Handler

class SlackHandler(Handler):
    def __init__(self, webhook_url, channel=None):
        # Make sure the url string begins with https://
        webhook_url = re.sub(r'http(?:s*):\/\/', '', webhook_url)
        self.url = 'https://' + webhook_url
        self.channel = channel

        # Finish spinning up the base log handler class
        Handler.__init__(self)

    def format_record(self, record):
        # Get a dict representation of the exception
        record_dict = record.__dict__

        # Format the message
        formatted_record = self.format(record)

        # Chop off the traceback from the formatted record string and
        # add it back wrapped in some nice Slack formatting
        split_record_str = formatted_record.split('Traceback', 1)
        try:
            formatted_record = split_record_str[0] + "\n```\n" + traceback.format_exc() + "\n```"
        except Exception as e:
            pass

        # Format the message and do a splitting and merging to make it pretty
        slack_msg = {'text': formatted_record}

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
