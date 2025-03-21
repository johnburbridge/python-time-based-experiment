from setuptools import setup, find_packages

setup(
    name="time_based_storage",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="John Burbridge",
    author_email="johnburbridge@gmail.com",
    description="A time-based storage system with two implementations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/johnburbridge/time_based_storage",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
) 