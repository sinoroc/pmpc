""" Task
"""


import logging
import queue
import threading


LOG = logging.getLogger(__name__)


class Task(object):
    """ Task
        Synchronized on an event queue.
        Can be threaded.
    """

    _tasks = []

    def __init__(self, name, event_handlers, threaded=True):
        self._name = name
        self._event_handlers = event_handlers
        self._event_queue = queue.Queue()
        self._keep_running = False
        self._thread = None
        if threaded:
            self._thread = threading.Thread(name=self._name, target=self._run)
        return None

    def start(self):
        """ Start the task.
            Start the thread if the task is threaded.
            Immediately run the task in the current thread otherwise.
        """
        if self._thread is not None:
            self._thread.start()
        else:
            self._run()
        return None

    def stop(self):
        """ Instruct the task to exit as soon as possible.
        """
        self._keep_running = False
        return None

    def join(self, *args):
        """ Join the thread running this task.
            Return immediately if the task is not threaded.
        """
        if self._thread is not None:
            self._thread.join(*args)
        return None

    def post(self, event):
        """ Post an event to this task's queue and notify the task.
        """
        self._event_queue.put(event)
        self._notify()
        return None

    def _run(self):
        """ This is the target function for the thread.
        """
        self._tasks.append(self)
        self._run_pre()
        self._task()
        self._run_post()
        self._tasks.remove(self)
        return None

    def _run_pre(self):  # pylint: disable=no-self-use
        """ Prepare before the task run.
        """
        return None

    def _run_post(self):  # pylint: disable=no-self-use
        """ Clean up after the task run.
        """
        return None

    def _task(self):
        """ Execute the task loop.
        """
        self._loop()
        return None

    def _loop(self):
        """ Execute the routine in a loop.
        """
        self._keep_running = True
        while self._keep_running:
            self._routine()
        return None

    def _routine(self):
        """ Process the event queue.
        """
        self._process_event_queue()
        return None

    def _process_event_queue(self):
        """ Process the events in the queue.
        """
        while not self._event_queue.empty():
            event = self._event_queue.get()
            self._process_event(event)
        return None

    def _process_event(self, event):
        """ Process one event from the queue.
            Execute the associated handler if any.
        """
        event_type = event.get('type', None)
        if event_type in self._event_handlers:
            self._event_handlers[event_type](event)
        else:
            LOG.debug(
                "Task._process_event no handler for event %s in task %s",
                event_type,
                self._name,
            )
        return None

    def _notify(self):  # pylint: disable=no-self-use
        """ Notify this task that events are waiting.
        """
        return None

    def _emit(self, event):
        """ Broadcast an event to all other tasks.
        """
        receivers = [task for task in self._tasks if task is not self]
        for task in receivers:
            task.post(event)
        return None


# EOF
