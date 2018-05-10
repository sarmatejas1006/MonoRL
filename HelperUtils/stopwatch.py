import datetime


class Stopwatch(object):
    """A simple timer class"""

    def __init__(self):

        pass

    def start(self):
        """Starts the timer"""
        if self.start is None:
            self.start = datetime.datetime.now()

        return self.start

    def stop(self):
        """Stops the timer.  Returns the time elapsed"""
        self.stop = datetime.datetime.now()
        duration = self.stop - self.start
        self.start = self.stop
        return duration

    def restart(self):
        """Restart the timer.  Returns the time elapsed"""
        self.start = datetime.datetime.now()
        return self.start
