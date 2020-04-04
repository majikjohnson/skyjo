from setuptools import setup, find_packages

setup(
    name = 'Skyjo',
    version = '0.1',
    package_dir = {
        '': 'src'
    },
    packages=find_packages(),
    entry_points = {
        "console_scripts": [
            "hello = skyjo.sayhello:main"
        ]
    }
)