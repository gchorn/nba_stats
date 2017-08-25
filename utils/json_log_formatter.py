import json
from collections import OrderedDict

from pythonjsonlogger.jsonlogger import JsonFormatter


class BetterJSONFormatter(JsonFormatter):
    """ Adapted from https://github.com/madzak/python-json-logger """

    def get_dict_message(self, record):
        """ Merges any user-supplied args into the `msg` key of
        record.msg
        Similar to the built-in record.getMessage method, but
        expects a record whose msg attribute is a dict containing a
        `msg` key.
        Args:
            record (obj) - The log Record object from which to derive
                the formatted dict message
        Returns:
            The original log message under the `msg` key of record.msg,
        now formatted with any user-supplied args.
        """
        msg = str(record.msg.get('msg', ''))
        if msg and record.args:
            msg = msg % record.args
        return msg

    def format(self, record):
        """ Formats a log record and serializes it to JSON.
        Args:
            record (obj) - The log Record object to parse and format
        Returns:
            A JSON-formatted string representation of the log record
        """
        message_dict = {}
        if isinstance(record.msg, dict):
            message_dict = record.msg
            record.msg = self.get_dict_message(record)
        else:
            record.msg = record.getMessage()

        # only format time if needed
        if "asctime" in self._required_fields:
            record.asctime = self.formatTime(record, self.datefmt)

        # Display formatted exception, but allow overriding it in the
        # user-supplied dict.
        if record.exc_info and not message_dict.get('exc_info'):
            message_dict['exc_info'] = self.formatException(record.exc_info)
        if not message_dict.get('exc_info') and record.exc_text:
            message_dict['exc_info'] = record.exc_text

        log_record = OrderedDict()

        self.add_fields(log_record, record, message_dict)

        return self.jsonify_log_record(log_record)


class PrettyJSONFormatter(BetterJSONFormatter):
    def format(self, record):
        r = super(PrettyJSONFormatter, self).format(record)
        return json.dumps(json.loads(r), indent=4)