import sys
sys.path.append(sys.path[0] + "/..")

import wrapper
import unittest
import random

class PyFesLiteTest(unittest.TestCase):
    """
    Tests everything that is not the interface to libfes-lite.
    """
    def forge_system(self, n, n_eqs, X=None):
        """
        Forge a random quadratic system F with a designated solution X. Returns (F, X)
        """
        N = 1 + n + n * (n - 1) // 2
        F = [0]
        for i in range (1, N):
            F.append(random.getrandbits(n_eqs))
        if X is None:
            X = random.getrandbits(n)
        F[0] = wrapper.naive_evaluation(n, F, X)
        self.assertEqual(wrapper.naive_evaluation(n, F, X), 0, "forged system does NOT contain prescribed solution")
        return (F, X)

    def test_flip_involutive(self):
        """
        Check that flip_leading_variable() is involutive.
        """
        n = 51
        m = 32
        F, _ = self.forge_system(n, m)
        G = F[:]
        wrapper.flip_leading_variable(n, F)
        self.assertNotEqual(F, G)
        wrapper.flip_leading_variable(n, F)
        self.assertEqual(F, G)


    def test_subsystems_small(self):
        n = 24
        m = 32
        F, X = self.forge_system(n, m)
        s = list(wrapper.subsystems(n, F))
        self.assertEqual(1, len(s))
        x, n_, F_ = s[0]
        self.assertEqual(x, 0)
        self.assertEqual(n_, n)
        self.assertEqual(F_, F)


    def test_subsystems_35(self):
        n = 35
        m = 32
        F, X = self.forge_system(n, m)
        s = list(wrapper.subsystems(n, F))
        self.assertEqual(8, len(s))
        good = False
        for prefix, n_, G in s:
            self.assertEqual(32, n_)
            solutions = []
            n_solutions = wrapper.solve(32, G, solutions, 256, 0)
            for x in solutions:
                self.assertTrue(wrapper.naive_evaluation(n, F, x + prefix << 32))

    def test_subsystems_val(self):
        n = 35
        m = 32
        F, X = self.forge_system(n, m)
        for prefix, n_, G in wrapper.subsystems(n, F):
            self.assertEqual(32, n_)
            x = random.getrandbits(32)
            y = wrapper.naive_evaluation(n, F, x + (prefix << 32))
            z = wrapper.naive_evaluation(n_, G, x)
            self.assertEqual(y, z)

    def test_full_solve_32_35(self):
        n = 35
        m = 32
        F, X = self.forge_system(n, m)
        solutions = wrapper.full_solve(n, F)
        self.assertIn(X, solutions, "expected solution NOT found (false negative)")
        for x in solutions:
            Y = wrapper.naive_evaluation(n, F, x)
            self.assertEqual(Y, 0, "full_solve() reports false positive")
