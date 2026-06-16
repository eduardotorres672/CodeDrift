"""CodeDrift setup configuration"""

from setuptools import setup, find_packages

setup(
    name="codedrift",
    version="0.1.0",
    description="Keep your code and documentation in perfect sync",
    author="CodeDrift Team",
    author_email="team@codedrift.dev",
    url="https://github.com/codedrift/codedrift",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "typer[all]==0.9.0",
        "click==8.1.7",
        "pydantic==2.4.2",
        "pyyaml==6.0.1",
        "httpx==0.25.0",
        "rich==13.6.0",
    ],
    extras_require={
        "dev": [
            "pytest==7.4.3",
            "black==23.10.1",
            "mypy==1.5.1",
            "pytest-cov==4.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "codedrift=codedrift.cli:app",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Documentation",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="documentation drift sync code quality devex",
)
