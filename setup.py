import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="urldl",
    version="0.0.1",
    author="Andre Rossi Korol",
    author_email="anrobits@yahoo.com.br",
    description="The easiest way to download files from URLs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrekorol/urldl",
    install_requires=["multipledispatch"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
