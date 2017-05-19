#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import json
import requests
from logging import Handler


class SlackHandler(Handler):
    def __init__(self, webhook_url):
        # Make sure the url string begins with https://
        webhook_url = re.sub(r'http(?:s*):\/\/', '', webhook_url)
        self.url = 'https://' + webhook_url

        # Finish spinning up the base log handler class
        Handler.__init__(self)

    def format_record(self, record):
        print "Formatting log record"

        try:
            # Get a dict representation of the exception
            record_dict = record.__dict__

            import pprint
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(record_dict)

            # Get the exception
            exception = 'Exception'
            if record.exc_info:
                exception = type(record.exc_info[1]).__name__

            # Format the message and do a splitting and merging to make it pretty
            formatted_record = self.format(record)

            # Make the Slack msg string
            msg = "`%s |  %s`\n```%s\n```" % (
                exception,
                ecord_dict['message'],
                formatted_record
            )

            # Return the formatted slack message
            return json.dumps({'text': msg, 'channel': 'snap-test'})

        except Exception:
            self.handleError(record)

    def emit(self, record):
        print "WHAT"
        try:
            slack_msg = self.format_record(record)
            requests.post(self.url, data=slack_msg)
        except Exception:
            self.handleError(record)
