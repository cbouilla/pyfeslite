import multiprocessing
import itertools
from cffi import FFI
ffi = FFI()

from _feslite_wrapper import ffi, lib

def feslite_solve(n, F, sols, max_solutions, verbose):
    """
    Invoke the solve() function from libfes-lite.
    """
    solutions = ffi.new("uint32_t []", [42] * max_solutions)
    n_solutions = lib.feslite_solve(n, F, solutions, max_solutions, verbose)
    for i in range(n_solutions):
        sols.append(solutions[i])
    return n_solutions

def idx1(i):
    """
    Gives the index of the coefficient in front of X_i in F.
    The variables are X_0, X_1, ...., X_{n-1}.
    """
    return i * (i + 1) // 2 + 1

def idx2(i, j):
    """
    Gives the index of the coefficient in front of X_i * X_j in F.
    The variables are X_0, X_1, ...., X_{n-1}.
    """
    assert i < j
    return idx1(j) + i + 1


def naive_evaluation(n, F, x):
    """
    Naive evaluation of k quadratic polynomials on n variables at input vector x.
    """
    v = []
    n_eqs = max([a.bit_length() for a in F])
    ones = (1 << n_eqs) - 1
    for k in range(n):
        v.append(ones * (x & 1))
        x >>= 1
    y = F[0]
    for idx_0 in range(n):
        v_0 = v[idx_0]
        y ^= F[idx1(idx_0)] & v_0
        for idx_1 in range(idx_0):
            v_1 = v_0 & v[idx_1]
            y ^= F[idx2(idx_1, idx_0)] & v_1
    return y


def flip_leading_variable(n, F):
    """
    in-place flips the leading variable. Involutive
    """
    l = n - 1
    F[0] = F[0] ^ F[idx1(l)]
    for i in range(l):
        F[idx1(i)] ^= F[idx2(i, l)]


def subsystems(n, F):
    """
    Generator that produce the stream of all subsystems.
    
    Returns a stream of triplets (x, n, G). G is a system on n variables
    if y is a solution of G, then (x << 32) + y is a solution of F.
    """
    G = F[:]
    stack = [('fresh', 0, n)]
    n_top = n
    while stack != []:
        (state, prefix, m) = stack.pop()
        if m <= 32:
            # leaf node
            yield prefix, m, G[:idx1(m)]
        else:
            # still more than 32 variables
            if state == 'fresh':
                # push left children
                stack.append(('half', prefix, m))
                stack.append(('fresh', 2*prefix, m-1))
            elif state == 'half':
                # pop left children,
                # push right children
                stack.append(('full', prefix, m))
                flip_leading_variable(m, G)
                stack.append(('fresh', 2*prefix + 1, m-1))
            elif state == 'full':
                # pop right children. Restore the previous state.
                flip_leading_variable(m, G)


def _solve(prefix, n_, G):
    # solve subsystem
    local_solutions = []
    k = feslite_solve(n_, G, local_solutions, 256, 0)
    if k == 256:
        raise Failure("too many solutions in subsystem; Some may be lost")
    for x in local_solutions:
        assert naive_evaluation(n_, G, x) == 0
    return prefix, local_solutions


def full_solve(n, F):
    """
    Simple **parallel** function that returns the list of all solutions, 
    with arbitrary number of functions and variables.
    """   
    F32 = [x & 0xffffffff for x in F]
    pool = multiprocessing.Pool()
    # do the hard work
    sub_solutions = pool.starmap(_solve, subsystems(n, F32))
    # lift solutions
    global_solutions = []
    for (prefix, L) in sub_solutions:
        for x in L:
            y = x + (prefix << 32)
            assert naive_evaluation(n, F32, y) == 0
            if naive_evaluation(n, F, y) == 0:
                global_solutions.append(y)
    return global_solutions
