from setuptools import setup, find_packages

setup(
    name = 'Skyjo',
    version = '0.1',
    package_dir = {
        '': 'src'
    },
    packages=find_packages(),
    install_requires=[
        'pygame'
    ],
    entry_points = {
        "gui_scripts": [
            "skyjo = skyjo.main:gui"
        ]
    }
)