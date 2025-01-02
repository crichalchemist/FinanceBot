from setuptools import setup, find_packages

setup(
    name="FinanceBot",
    version="1.0.0",
    description="A modular trading bot integrating MQL5 and Python for real-time trading and analysis",
    author="Courtney Richardson",
    author_email="crichalchemist@gmail.com",
    url="https://github.com/crichalchemist/FinanceBot",
    packages=find_packages(),  # Automatically find and include all packages
    include_package_data=True,
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "scikit-learn>=0.24.2",
        "tensorflow>=2.6.0",
        "flask>=2.0.0",
        "requests>=2.26.0",
        "python-decouple>=3.5",
        "tqdm>=4.61.2",
        "loguru>=0.5.3",
        "psycopg2>=2.9.1",
        "pyyaml>=5.4.1",
        "MetaTrader5>=5.0.39"
    ],
    entry_points={
        "console_scripts": [
            "run-all=run_all:main",
            "start-server=api_server:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
