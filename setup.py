import setuptools

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

setuptools.setup(
    name="tegrity_framework",
    version="0.0.1",
    author="Michael van Straten",
    author_email="michael@vanstraten.de",
    license="MIT",
    description="<short description for the tool>",
    long_description=open("./readme.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/michaelvanstraten/tegrity-framework",
    packages=setuptools.find_packages(),
    install_requires=[requirements],
    python_requires=">=3.7",
    entry_points={"console_scripts": ["tegrity-framework = tegrity_framework.cli:cli"]},
)
