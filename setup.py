from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cm-forms",
    version="0.0.1",
    description="You code the form, we make it accessible",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Lalitha A R",
    author_email="",
    url="https://github.com/comfort-mode-toolkit/cm-forms",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click>=8.1.0",
        "rich>=13.0.0",
        "beautifulsoup4>=4.12.0",
    ],
    entry_points={
        "console_scripts": [
            "cm-forms=cm_forms.cli:main",
        ],
    },
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Text Processing :: Markup :: HTML",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="accessibility, wcag, html, forms, a11y",
)
