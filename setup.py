import setuptools

setuptools.setup(
    name="py-feslite",
    version="0.0.1",
    author="Charles Bouillaguet",
    author_email="charles.bouillaguet@univ-lille.fr",
    description="A wrapper for libfes-lite",
    packages=setuptools.find_packages(),
    setup_requires=["cffi>=1.0.0"],
    cffi_modules=["wrapper_build:ffibuilder"], # "filename:global"
    install_requires=["cffi>=1.0.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
