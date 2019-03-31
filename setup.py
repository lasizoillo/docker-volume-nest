import io
import re
from setuptools import setup, find_packages


def get_version_from_changelog():
    try:
        with io.open('debian/changelog', encoding='utf8') as stream:
            return re.search(r'\((.+)\)', next(stream)).group(1)
    except IOError:
        print('No debian/changelog file found, using: 0.0.1 as version')
        return '0.0.1'


setup(
    name='docker_volume_nest',
    description='Manage volumes for a simple docker swarm deploy',
    long_description=io.open('README.md').read(),
    long_description_content_type='text/markdown',
    version=get_version_from_changelog(),
    include_package_data=True,
    author='lasizoillo',
    author_email='myteam@avature.net',
    url='https://github.com/lasizoillo/docker_volume_nest',
    install_requires=io.open('requirements.txt').read().splitlines(),
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'docker_volume_nest = docker_volume_nest.cli:main',
        ]
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
