import setuptools

with open('README.md', "r") as fh:
    long_description = fh.read()
    setuptools.setup(
        name="trellowork_client_basics_api-Wilderone", version="0.0.1", author="Wilderone",
        author_email="prims@inbox.ru", description="lern how to work with api",
        long_description=long_description,
        long_description_content_type="text/markdown", url="https://github.com/Wilderone/todoes",
        packages=setuptools.find_packages(), classifiers=["Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License", "Operating System :: OS Independent", ], python_requires='>=3.6',)
