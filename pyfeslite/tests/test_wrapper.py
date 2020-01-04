import unittest
import random

import pyfeslite

class WrapperTest(unittest.TestCase):
    """
    Test case used to test the wrapper.
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
        F[0] = pyfeslite.naive_evaluation(n, F, X)
        self.assertEqual(pyfeslite.naive_evaluation(n, F, X), 0, "forged system does NOT contain prescribed solution")
        return (F, X)

    def test_forge(self):
        """
        Forge random quadratic systems with a designated solution and checks that it actually... is a solution.
        """
        self.forge_system(47, 131)
        self.forge_system(131, 47)
    

    def test_solve_random(self):
        """
        Check that solve() from libfes-lite works correctly with n=m on random systems.
        """
        for n in [8, 12, 16, 20, 24, 28, 32]:
            with self.subTest(i=n):
                F, X = self.forge_system(n, n)
                solutions = []
                n_solutions = pyfeslite.feslite_solve(n, F, solutions, 256, 0)
                # check
                self.assertIn(X, solutions, "expected solution NOT found (false negative)")
                for i in range(n_solutions):
                    Y = pyfeslite.naive_evaluation(n, F, solutions[i])
                    self.assertEqual(Y, 0, "solve() reports false positive")

    def test_solve_corner(self):
        """
        Check that solve() from libfes-lite works correctly with n=m on bizarre solutions.
        """
        n = 32
        trials = [0x00000000, 0xffffffff, 
             0xffff0000, 0x0000ffff, 
             0xff00ff00, 0x00ff00ff, 
             0x0f0f0f0f, 0xf0f0f0f0, 
             0x55555555, 0xcccccccc, 
             0x80000000, 0x40000000, 0x20000000, 0x10000000,
             0x08000000, 0x04000000, 0x02000000, 0x01000000,
             0x00800000, 0x00400000, 0x00200000, 0x00100000,
             0x00080000, 0x00040000, 0x00020000, 0x00010000,
             0x00008000, 0x00004000, 0x00002000, 0x00001000,
             0x00000800, 0x00000400, 0x00000200, 0x00000100,
             0x00000080, 0x00000040, 0x00000020, 0x00000010,
             0x00000008, 0x00000004, 0x00000002, 0x00000001,
        ]
        for i, X in enumerate(trials):
            with self.subTest(i=i):
                F, _ = self.forge_system(n, n, X=X)
                solutions = []
                n_solutions = pyfeslite.feslite_solve(n, F, solutions, 256, 0)
                # check
                self.assertIn(X, solutions, "expected solution NOT found (false negative)")
                for i in range(n_solutions):
                    Y = pyfeslite.naive_evaluation(n, F, solutions[i])
                    self.assertEqual(Y, 0, "solve() reports false positive")

    
    def test_solve_underconstrained(self):
        """
        Check that solve() from libfes-lite works correctly with n >> m.
        """
        n, m = 32, 27
        F, X = self.forge_system(n, m)   # we expect 32 solutions
        solutions = []
        n_solutions = pyfeslite.feslite_solve(n, F, solutions, 256, 0)
        # check solutions
        self.assertIn(X, solutions, "expected solution NOT found (false negative)")
        for i in range(n_solutions):
            Y = pyfeslite.naive_evaluation(n, F, solutions[i])
            self.assertEqual(Y, 0, "solve() reports false positive")
        # check solution number
        self.assertGreater(n_solutions, 8)
        self.assertLess(n_solutions, 128)


    def test_solve_overconstrained(self):
        """
        Check that solve() from libfes-lite works correctly with n << m.
        """
        n, m = 27, 32
        F, X = self.forge_system(n, m)   # we expect 32 solutions
        solutions = []
        n_solutions = pyfeslite.feslite_solve(n, F, solutions, 256, 0)
        # check solutions
        self.assertIn(X, solutions, "expected solution NOT found (false negative)")
        for i in range(n_solutions):
            Y = pyfeslite.naive_evaluation(n, F, solutions[i])
            self.assertEqual(Y, 0, "solve() reports false positive")
        # check solution number
        self.assertEqual(n_solutions, 1)
