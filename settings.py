from setuptools import setup, find_packages

setup(
    name='package_test',
    version='0.2.0',
    author='tsubamon55',
    author_email='tsubamon55@gmail.com',
    description='package test',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/tsubamon55/kabu-station-api',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=open('requirements.txt').read().splitlines(),
)
