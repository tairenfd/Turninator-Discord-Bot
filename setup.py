from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="turninator",
    version="0.0.2",
    description="Turn's Discord bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/tairenfd/turninator",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "discord.py==2.1.1",
        "openai==0.26.5",
        "PyMySQL==1.0.2",
        "requests==2.28.2",
        "SQLAlchemy==2.0.3"
    ],
    extras_require={
        "dev": [],
    },
    classifiers=[
        "Programming Language :: Python :: 3.9",
    ],
    keywords="discord bot python",
    scripts=["src/bot.py"],
    entry_points={
        "console_scripts": ["turninator = bot:main"],
    },
    python_requires=">=3.9",
)
