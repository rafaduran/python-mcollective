import base


class TestWithCoilMQIntegration(base.TestCase, base.CoilMQIntegration):
    pass


class TestWithCoilMQ22x(TestWithCoilMQIntegration):
    def setup(self):
        self.get_vendor_rev('2.2.x')
        super(TestWithCoilMQ22x, self).setup()

    def teardown(self):
        base.TestCase.teardown(self)

    def test_something(self):
        assert True


class TestWithCoilMQ20x(TestWithCoilMQIntegration):
    def setup(self):
        self.get_vendor_rev('2.0.x')
        super(TestWithCoilMQ20x, self).setup()

    def teardown(self):
        base.TestCase.teardown(self)

    def test_something(self):
        assert True
