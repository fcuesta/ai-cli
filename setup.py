from setuptools import setup, find_packages

setup(
    name="ai-cli",
    version="0.1.0",
    description="AI CLI tool",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "openai",
        "prompt_toolkit"
    ],
    package_data={
        "ai_cli": ["data/*.json"],
    },
    entry_points={
        "console_scripts": [
            "ai-cli = ai_cli.chat_app:main",
        ],
    },
)