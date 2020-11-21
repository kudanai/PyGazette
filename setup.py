import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyGazette", # Replace with your own username
    version="0.0.1",
    author="kudanai",
    author_email="kudanai@gmail.com",
    description="Python wrapper for MV Gazette",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kudanai/PyGazette",
    packages=['pygazette', ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License ::  MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)