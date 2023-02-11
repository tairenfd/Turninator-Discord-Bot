from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="turninator",
    version="0.0.1",
    description="Turn's Discord bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/tairenfd/turninator",
    packages=find_packages("src"),
    package_dir={"", "src"},
    include_package_data=True,
    install_requires=[
        "discord.py==1.5.1",
    ],
    extras_require={
        "dev": [],
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
    ],
    keywords="discord bot python",
    scripts=["src/bot.py"],
    entry_points={
        "console_scripts": ["turninator = src.bot:main"],
    },
    python_requires=">=3.8",
)
