import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="phdhelper",  # Replace with your own username
    version="0.0.1",
    author="James Plank",
    author_email="jp5g16@soton.ac.uk",
    description="Helper functions for things to do with SEP trubulence physics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jmsplank/phdhelper.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)