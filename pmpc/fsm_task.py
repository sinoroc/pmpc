""" Finite state machine task
"""


from . import fsm
from . import task


class FsmTask(task.Task):
    """ Task with a finite state machine
    """

    def __init__(self, name, states, initial_state_name, threaded=True):
        self._fsm = fsm.Fsm(states, initial_state_name)
        super(FsmTask, self).__init__(name, None, threaded)
        return None

    def _process_event(self, event):
        """ Process an event.
            Forward the event to the FSM's process method.
        """
        self._fsm.handle_event(event)
        return None


# EOF
