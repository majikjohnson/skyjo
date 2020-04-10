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
    extra_require={
        'dev-atom': [
            'flake8',
            'pycodestyle'
        ]
    }
    entry_points = {
        "gui_scripts": [
            "skyjo = skyjo.main:controller"
        ]
    }
)
