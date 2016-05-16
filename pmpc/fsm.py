""" Finite state machine
"""


class Fsm(object):  # pylint: disable=too-few-public-methods
    """ Finite state machine
    """

    def __init__(self, states, initial_state_name):
        self._states = states
        self._current_state_name = initial_state_name
        return None

    def handle_event(self, event):
        """ Handle event.
        """
        state = self._find_current_state()
        if state:
            transition = _find_transition(state, event)
            if transition:
                self._do_transition(state, transition, event)
            else:
                handler = _find_handler(state, event)
                if handler:
                    handler(event)
        return None

    def _find_current_state(self):
        """ Find the current state.
        """
        return self._find_state(self._current_state_name)

    def _find_state(self, state_name):
        """ Find state by its name.
        """
        state = None
        if state_name in self._states:
            state = self._states[state_name]
            state['name'] = state_name
        return state

    def _do_transition(self, state, transition, event):
        """ Execute the transition.
        """
        next_state_name = transition['next_state']
        next_state = self._find_state(next_state_name)
        if next_state:
            _leave_state(state, event)
            self._set_current_state(next_state_name)
            _enter_state(next_state, event)
        return None

    def _set_current_state(self, state_name):
        """ Set the new current state.
        """
        self._current_state_name = state_name
        return None


def _find_handler(state, event):
    handler = None
    event_type = event.get('type', None)
    handlers = state.get('handlers', {})
    if event_type in handlers:
        handler = handlers[event_type]
    return handler


def _find_transition(state, event):
    transition = None
    event_type = event.get('type', None)
    transitions = state.get('transitions', {})
    if event_type in transitions:
        transition = transitions[event_type]
    return transition


def _enter_state(state, event):
    handler = state.get('enter', None)
    if handler:
        handler(event)
    return None


def _leave_state(state, event):
    handler = state.get('leave', None)
    if handler:
        handler(event)
    return None


# EOF
