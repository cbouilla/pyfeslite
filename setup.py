import setuptools

setuptools.setup(
    name="py-feslite",
    version="0.0.1",
    author="Charles Bouillaguet",
    author_email="charles.bouillaguet@univ-lille.fr",
    description="A wrapper for libfes-lite",
    packages=setuptools.find_packages(),
    setup_requires=["cffi>=1.0.0"],
    cffi_modules=["pyfeslite/build_wrapper.py:ffibuilder"], # "filename:global"
    install_requires=["cffi>=1.0.0"],
    python_requires='>=3.4',
)
