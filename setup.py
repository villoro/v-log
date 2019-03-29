import io
from setuptools import setup

setup(
    name="v_log",
    version="1.0.0",
    author="Arnau Villoro",
    author_email="arnau@villoro.com",
    packages=["v_log"],
    install_requires=io.open("requirements.txt", encoding="utf-8").read().splitlines(),
    include_package_data=True,
    license="MIT",
    description=("Colored log that also stores a properly formated csv."),
    long_description=io.open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/villoro/v-log",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
    ],
)
