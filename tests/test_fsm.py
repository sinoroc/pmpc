""" Tests for finite state machine
"""


import unittest

import pmpc.fsm


class Machine:  # pylint: disable=too-few-public-methods
    """ FSM test subject
    """

    def __init__(self):
        states = {
            'one': {
                'transitions': {
                    'switch': {
                        'next_state': 'two',
                    },
                },
                'handlers': {
                    'toggle': self._handle_toggle,
                    'set': self._handle_set,
                },
                'leave': self._leaving_one,
            },
            'two': {
                'enter': self._entering_two,
            },
        }
        self.fsm = pmpc.fsm.Fsm(states, 'one')
        self.toggle_flag = False
        self.register = None
        self.left_one_register = None
        self.entered_two_register = None
        return None

    def _handle_toggle(self, dummy_event):
        self.toggle_flag = True
        return None

    def _handle_set(self, event):
        self.register = event['value']
        return None

    def _leaving_one(self, event):
        self.left_one_register = event['value']
        return None

    def _entering_two(self, event):
        self.entered_two_register = event['value']
        return None


class TestFsm(unittest.TestCase):
    """ Test cases for finite state machine
    """

    VALUE = 1

    def setUp(self):
        self.machine = Machine()
        self.fsm = self.machine.fsm
        return None

    def test_00_inital_state(self):
        """ Test initial state
        """
        now = self.fsm._current_state_name  # pylint: disable=protected-access
        self.assertEqual(now, 'one')
        return None

    def test_01_transition(self):
        """ Test transition from one state to another on event
        """
        event = {
            'type': 'switch',
            'value': None,
        }
        now = self.fsm._current_state_name  # pylint: disable=protected-access
        self.assertEqual(now, 'one')
        self.fsm.handle_event(event)
        now = self.fsm._current_state_name  # pylint: disable=protected-access
        self.assertEqual(now, 'two')
        return None

    def test_02_handler(self):
        """ Test call of handler on event
        """
        event = {
            'type': 'toggle',
            'value': None,
        }
        self.assertEqual(self.machine.toggle_flag, False)
        self.fsm.handle_event(event)
        self.assertEqual(self.machine.toggle_flag, True)
        return None

    def test_03_event(self):
        """ Test transmission of event to handler
        """
        event = {
            'type': 'set',
            'value': self.VALUE,
        }
        self.assertNotEqual(self.machine.register, self.VALUE)
        self.fsm.handle_event(event)
        self.assertEqual(self.machine.register, self.VALUE)
        return None

    def test_04_leave(self):
        """ Test call of handler on leaving a state
        """
        event = {
            'type': 'switch',
            'value': self.VALUE,
        }
        self.assertNotEqual(self.machine.left_one_register, self.VALUE)
        self.fsm.handle_event(event)
        self.assertEqual(self.machine.left_one_register, self.VALUE)
        return None

    def test_05_enter(self):
        """ Test call of handler on entering a state
        """
        event = {
            'type': 'switch',
            'value': self.VALUE,
        }
        self.assertNotEqual(self.machine.entered_two_register, self.VALUE)
        self.fsm.handle_event(event)
        self.assertEqual(self.machine.entered_two_register, self.VALUE)
        return None


# EOF
