from numpy.testing import TestCase, run_module_suite, assert_ 
from numpy import random
import numpy as np


class TestMultinomial(TestCase):
    def test_basic(self):
        random.multinomial(100, [0.2, 0.8])

    def test_zero_probability(self):
        random.multinomial(100, [0.2, 0.8, 0.0, 0.0, 0.0])

    def test_int_negative_interval(self):
        assert_( -5 <= random.randint(-5,-1) < -1)
        x = random.randint(-5,-1,5)
        assert_(np.all(-5 <= x))
        assert_(np.all(x < -1))


class TestSetState(TestCase):
    def setUp(self):
        self.seed = 1234567890
        self.prng = random.RandomState(self.seed)
        self.state = self.prng.get_state()

    def test_basic(self):
        old = self.prng.tomaxint(16)
        self.prng.set_state(self.state)
        new = self.prng.tomaxint(16)
        assert_(np.all(old == new))

    def test_gaussian_reset(self):
        """ Make sure the cached every-other-Gaussian is reset.
        """
        old = self.prng.standard_normal(size=3)
        self.prng.set_state(self.state)
        new = self.prng.standard_normal(size=3)
        assert_(np.all(old == new))

    def test_gaussian_reset_in_media_res(self):
        """ When the state is saved with a cached Gaussian, make sure the cached
        Gaussian is restored.
        """
        self.prng.standard_normal()
        state = self.prng.get_state()
        old = self.prng.standard_normal(size=3)
        self.prng.set_state(state)
        new = self.prng.standard_normal(size=3)
        assert_(np.all(old == new))

    def test_backwards_compatibility(self):
        """ Make sure we can accept old state tuples that do not have the cached
        Gaussian value.
        """
        old_state = self.state[:-2]
        x1 = self.prng.standard_normal(size=16)
        self.prng.set_state(old_state)
        x2 = self.prng.standard_normal(size=16)
        self.prng.set_state(self.state)
        x3 = self.prng.standard_normal(size=16)
        assert_(np.all(x1 == x2))
        assert_(np.all(x1 == x3))

    def test_negative_binomial(self):
        """ Ensure that the negative binomial results take floating point
        arguments without truncation.
        """
        self.prng.negative_binomial(0.5, 0.5)


if __name__ == "__main__":
    run_module_suite()
