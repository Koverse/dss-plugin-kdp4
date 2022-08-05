from setuptools import setup, find_packages

NAME = "dss-plugin-kdp4"
VERSION = "0.1.0"
DESCRIPTION = 'Connector for Koverse Data Platform (KDP4)'
LONG_DESCRIPTION = 'Dataiku Plugin to connect with Koverse Data Platform (KDP4)'


# Setting up
setup(
        name=NAME,
        version=VERSION,
        author="Koverse development team",
        author_email="developer@koverse.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
        keywords=['python', 'kdp'],
)
