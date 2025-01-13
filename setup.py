
from pathlib import Path

import setuptools

def parse_requirements(requirements: str):
    with open(requirements) as f:
        return [
            l.strip('\n') for l in f if l.strip('\n') and not l.startswith('#')
        ]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iabs2rel", 
    version=Path('version.txt').read_text(encoding='utf-8').strip(),
    author="Demetry Pascal",
    author_email="qtckpuhdsa@gmail.com",
    maintainer='Demetry Pascal',
    description="A Python utility / library to convert absolute Python imports to relative",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PasaOpasen/iabs2rel",
    license='MIT',
    keywords=['import', 'absolute', 'relative', 'cli'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=parse_requirements('./requirements.txt'),
    entry_points={
        'console_scripts': [
            'iabs2rel-file=iabs2rel.cli.file:main',
            'iabs2rel=iabs2rel.cli.dir:main'
        ],
    },
)
