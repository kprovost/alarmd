import logging
from poller import Poller
from notifier import sms
import settings
import s7

class AlarmPoller(Poller):
    def __init__(self):
        self._wasTriggered = False

    def onTriggered(self, s7conn):
        alarmed = [ ]

        msg = "Alarm: overloop pompput kelder"
        logging.warn(msg)
        for dest in settings.SMS_DESTINATIONS:
            if not sms.send(msg, dest):
                logging.error("Failed to send SMS \"%s\" to %s" % (msg, dest))

    def poll(self, s7conn):
        isTriggered = s7conn.readBit(16, 0, 0)

        logging.debug("Alarm trigger status: %s" % isTriggered)

        if not self._wasTriggered and isTriggered:
            self.onTriggered(s7conn)

        self._wasTriggered = isTriggered
