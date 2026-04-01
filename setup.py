from setuptools import setup, find_packages

setup(
    name="solsentry",
    version="0.1.0",
    packages=find_packages(),

    install_requires=[
        "graphviz>=0.20"
    ],

    entry_points={
        "console_scripts": [
            "solsentry=solsentry.main:main",
        ],
    },

    author="Ayush Sharma",
    description="Static Security Analyzer for Solidity Smart Contracts using AST, IR, and CFG",
    python_requires=">=3.9",
)