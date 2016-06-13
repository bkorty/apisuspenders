from unittest import TestCase

import mock

from apisuspenders import install, Suspenders


class TestGlobalInstallMethod(TestCase):
    @classmethod
    def setUp(cls):
        cls.app = mock.Mock()
        cls.patcher = mock.patch('tornado.ioloop.IOLoop.instance')
        cls.mocked_instance = cls.patcher.start()
        cls.mocked_iol = mock.Mock()
        cls.mocked_instance.return_value = cls.mocked_iol

        install(cls.app)

    @classmethod
    def tearDown(cls):
        cls.patcher.stop()

    def test_that_suspenders_is_set_on_app(self):
        self.assertIsInstance(self.app.suspenders, Suspenders)

    def test_that_process_retries_timer_set(self):
        self.mocked_iol.call_later.assert_called_once_with(
            1, self.app.suspenders.process_retries)


class TestThatSuspendersIsInitializedProperly(TestCase):

    @classmethod
    def setUp(cls):
        cls.app = mock.Mock()
        cls.iol = mock.Mock()

    def test_that_reference_to_application_is_cached(self):
        suspenders = Suspenders(self.app, self.iol)
        self.assertEquals(self.app, suspenders.app)

    def test_that_reference_to_application_ioloop_is_cached(self):
        suspenders = Suspenders(self.app, self.iol)
        self.assertEquals(self.iol, suspenders.ioloop)


class TestProcessRetry(TestCase):

    @classmethod
    def setUp(cls):
        cls.app = mock.Mock()
        cls.iol = mock.Mock()
        cls.suspenders = Suspenders(cls.app, cls.iol)
        cls.suspenders.process_retries()

    def test_that_process_process_retries_timer_set(self):
        self.iol.call_later.assert_called_once_with(
            1, self.suspenders.process_retries)