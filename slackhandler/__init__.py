#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__init__.py

Extension to Python's HTTPHandler that pipes logs to Slack
"""

import re
import json
import requests
from logging import Handler

class SlackHandler(Handler):
    """
    An extension of Python's base logging Handler that will emit logs to Slack
    """
    def __init__(self, webhook_url):
        # Make sure the url string begins with https://
        webhook_url = re.sub(r'http(?:s*):\/\/', '', webhook_url)
        self.url = 'https://' + webhook_url

        # Finish spinning up the base log handler class
        Handler.__init__(self)

    def format_record(self, record):
        try:
            # Format the message and do a splitting and merging to make it pretty
            formatted_rec = self.format(record)

            # If our error record is a full traceback,
            # break it up for proper Slack formatting
            formatted_rec = formatted_rec.split('Exception', 1)
            if len(formatted_rec) > 1:
                formatted_rec = formatted_rec[0] + "```\nException " + formatted_rec[1] + "\n```"
            else:
                formatted_rec = "```" + formatted_rec[0] + "```"
            # formatted_rec = formatted_rec + "\n ```" + request.user_agent.string + "```"

            # Get the exception
            exception = 'Exception'
            if record.exc_info:
                exception = type(record.exc_info[1]).__name__

            # Make the Slack msg string
            msg = "`%s` was thrown at %s" % (
                exception,
                formatted_rec
            )

            # Return the formatted slack message
            return json.dumps({'text': msg})

        except Exception:
            self.handleError(record)

    def emit(self, record):
        try:
            slack_msg = self.format_record(record)
            requests.post(self.url, data=slack_msg)
        except Exception:
            self.handleError(record)
