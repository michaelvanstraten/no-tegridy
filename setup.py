import setuptools

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setuptools.setup(
    name="no-tegridy",
    version="0.0.1",
    author="Michael van Straten",
    author_email="michael@vanstraten.de",
    license="MIT",
    description="<short description for the tool>",
    long_description=open("./readme.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/michaelvanstraten/no-tegridy",
    packages=setuptools.find_packages(),
    install_requires=[requirements],
    python_requires=">=3.7",
    entry_points={"console_scripts": ["no-tegridy = no_tegridy.cli:cli"]},
)
