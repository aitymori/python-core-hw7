from setuptools import setup, find_namespace_packages

setup(
    name = 'Clean folder aitymori',
    version = '0.0.1',
    description = 'Script for sorting files in folder',
    author = 'Anastasiia Kholodko',
    author_email = 'anakholodko@gmail.com',
    url = 'https://github.com/aitymori/python-core-hw7',
    license = 'MIT',
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
        ],
    packages = find_namespace_packages(),
    entry_points = {'console_scripts': [
        'clean-folder=clean_folder_aitymori.clean:main'
    ]}

)