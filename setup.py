from setuptools import setup, find_packages

setup(
    name='connector',
    version='0.1.0',
    author='Teemu Vartiainen',
    author_email='teemu@vartiainen.eu',
    description='Data connector',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dewabe/connector',
    packages=find_packages(),
    install_requires=[
        'pandas>=2.2.0',
        'sqlalchemy>=2.0.25',
        'python-dotenv>=1.0.1',
        'pyodbc>=5.0.1'
    ],
    classifiers=[
        # Choose classifiers from the list: https://pypi.org/classifiers/
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
