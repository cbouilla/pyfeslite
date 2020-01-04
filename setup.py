import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-feslite",
    version="0.0.1",
    author="Charles Bouillaguet",
    author_email="charles.bouillaguet@univ-lille.fr",
    description="A wrapper for libfes-lite",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cbouilla/pyfeslite",
    packages=setuptools.find_packages(),
    setup_requires=["cffi>=1.0.0"],
    cffi_modules=["pyfeslite/build_wrapper.py:ffibuilder"], # "filename:global"
    install_requires=["cffi>=1.0.0"],
    python_requires='>=3.4',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics"
    ],
)
