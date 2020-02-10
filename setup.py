import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="is_conf_man-t.blackstone",
    version="0.7alpha",
    author="Taylor-Jayde Blackstone",
    author_email="t.blackstone@inspyre.tech",
    description="Package for managing Inspyre Softworks configuration files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://test.pypi.org/legacy/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: System Administrators",
        "Topic :: Utilities",
        "Environment :: X11 Applications :: GTK",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
