import setuptools

# Read the contents of the README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="mkdocs-zerto-swagger-plugin",
    version="0.0.1",
    author="yuri",
    python_requires='>=3.8',
    author_email="yuri.kretingen@hpe.com",
    description="MKDocs plugin for rendering swagger & openapi files.",
    url="",
    py_modules=["zerto_swagger"],
    install_requires=["mkdocs"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'mkdocs.plugins': [
            'zerto_swagger = zerto_swagger:ZertoSwaggerPlugin',
        ]
    },
    long_description=long_description,
    long_description_content_type='text/markdown'
)