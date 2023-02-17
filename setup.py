#!/usr/bin/env python3
import os
from setuptools import setup

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def get_version():
    """ Find the version of the package"""
    version = None
    version_file = os.path.join(BASEDIR, 'PHAL_kinectV1_audio',
                                'version.py')
    major, minor, build, alpha = (None, None, None, None)
    with open(version_file) as f:
        for line in f:
            if 'VERSION_MAJOR' in line:
                major = line.split('=')[1].strip()
            elif 'VERSION_MINOR' in line:
                minor = line.split('=')[1].strip()
            elif 'VERSION_BUILD' in line:
                build = line.split('=')[1].strip()
            elif 'VERSION_ALPHA' in line:
                alpha = line.split('=')[1].strip()

            if ((major and minor and build and alpha) or
                    '# END_VERSION_BLOCK' in line):
                break
    version = f"{major}.{minor}.{build}"
    if alpha and int(alpha) > 0:
        version += f"a{alpha}"
    return version


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


def required(requirements_file):
    """ Read requirements file and remove comments and empty lines. """
    with open(os.path.join(BASEDIR, requirements_file), 'r') as f:
        requirements = f.read().splitlines()
        if 'MYCROFT_LOOSE_REQUIREMENTS' in os.environ:
            print('USING LOOSE REQUIREMENTS!')
            requirements = [r.replace('==', '>=').replace('~=', '>=') for r in requirements]
        return [pkg for pkg in requirements
                if pkg.strip() and not pkg.startswith("#")]


PLUGIN_ENTRY_POINT = 'PHAL-kinectV1-audio=PHAL_kinectV1_audio:KinectAudioPlugin'
UDEV_RULE_FUNC = "ovos_kinect_fw=PHAL_kinectV1_audio:ovos_kinect_fw"
setup(
    name='PHAL-kinectV1-audio',
    version=get_version(),
    description='A plugin allowing Kinect V.1 to be used as microphone',
    url='https://github.com/builderjer/PHAL-kinectV1-audio',
    author='BuilderJer',
    author_email='builderjer@.com',
    license='Apache-2.0',
    packages=['PHAL_kinectV1_audio'],
    package_data={'': package_files('PHAL_kinectV1_audio')},
    install_requires=required("requirements.txt"),
    zip_safe=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'License :: Apache License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.10'
    ],
    entry_points={'ovos.plugin.kinectV1': PLUGIN_ENTRY_POINT,
                  'console_scripts': [UDEV_RULE_FUNC]}
)
