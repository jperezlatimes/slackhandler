from setuptools import setup, find_packages

setup(
    name="slackhandler",
    version="0.1.0",
    packages=find_packages(),
    install_requires=(),
    author="James Perez",
    author_email="jdperez04@gmail.com",
    description="Extends Python's base logging Handler that emits logs to Slack",
    long_description="Extends Python's base logging Handler that emits logs to Slack via an Incoming Webhook",
    url="https://github.com/jperezlatimes/SlackHandler/",
    license="GNU GENERAL PUBLIC LICENSE",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Chat',
        'Topic :: System :: Logging',
    ]
)
