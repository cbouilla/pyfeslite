from cffi import FFI

"""
This build script builds the FFI wrapper module for libfes-lite.
"""

ffibuilder = FFI()

ffibuilder.cdef("""
size_t feslite_solve(size_t, const uint32_t * const, uint32_t *, size_t, bool);
""")

ffibuilder.set_source("_feslite_wrapper",  # name of the output C extension
"""
    #include "feslite.h"
""",
    libraries=['feslite'],    # link with the feslite library
    include_dirs=["/usr/include", "/usr/local/include"],  # specify the dir for the sources
    library_dirs=["/usr/lib", "/usr/local/lib"],
    #extra_compile_args=["-w"]) # avoids the warnings and add the library path
)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
