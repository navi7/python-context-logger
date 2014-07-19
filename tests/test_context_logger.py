import unittest
import logging

from mock import (patch,
                  call)

from context_logging import (ContextLogger,
                             log_context,
                             context_logger)


class TestContextLogger(unittest.TestCase):

    def setUp(self):
        pass

    def test_can_instantiate(self):
        cl = ContextLogger(name='test')
        self.assertIsNotNone(cl)

    def test_prefix_works(self):
        pass

    @patch.object(ContextLogger, "_log")
    def test_context_works_on_class(self, logger):
        @context_logger(prefix='ze')
        class ZeObject(object):
            value = 42

        instance = ZeObject()
        self.assertIsNotNone(instance)
        self.assertIsNotNone(instance.log)
        instance.log.info('And the question is?')

        expected = call(logging.INFO, 'And the question is?', ())
        self.assertEqual(expected, logger.call_args)

    @patch.object(logging.root, "_log")
    def test_context_works_on_method(self, logger):
        @log_context(prefix='ze')
        def ze_function():
            value = 42 * 16
            logging.debug('Oh, this is nice and the value is {}'.format(value))

        ze_function()
        expected = call(logging.DEBUG, 'Oh, this is nice and the value is 672', ())
        self.assertEqual(expected, logger.call_args)





