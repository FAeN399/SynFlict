from setuptools import setup, find_packages

setup(
    name="cardforge",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "typer>=0.9.0",
        "pillow>=10.0.0",
        "rich>=13.3.5",
    ],
    entry_points={
        "console_scripts": [
            "cardforge=cardforge.cli:app",
        ],
    },
)
