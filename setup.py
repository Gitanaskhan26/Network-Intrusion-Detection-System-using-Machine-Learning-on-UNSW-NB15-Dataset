from setuptools import find_packages, setup
from typing import List

def get_requirements() -> List[str]:
    '''
    This function will return list of requirements
    '''
    requirement_list:List[str] = []

    try:
        with open('requirements.txt', "r") as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement != '-e .':
                    requirement_list.append(requirement)
    except FileNotFoundError:
        print("File containing requirements not found")

    return requirement_list

setup(
    name = "NetworkSecurity",
    version = "1.0.0",
    author = "Your Name",
    author_email = "your.email@example.com",
    description = "Network Intrusion Detection System using Machine Learning on UNSW-NB15 Dataset",
    long_description = open("README.md").read(),
    long_description_content_type = "text/markdown",
    url = "https://github.com/yourusername/network_security",
    packages = find_packages(),
    install_requires = get_requirements(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Security",
    ],
    python_requires = ">=3.8",
)