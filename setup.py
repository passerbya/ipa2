from setuptools import setup, find_packages

setup(
    name='ipa2',
    version='0.9.1',
    package_data={'ipa2': ['data/*', 'ipa-dict/*', 'resources/*', 'resources/*/*', 'dragonmapper/data/*']},
    description='Tools for convert Text to IPA in python',
    long_description="Github : https://github.com/voidful/ipa2",
    url='https://github.com/voidful/ipa2',
    author='voidful',
    author_email='voidful.stack@gmail.com',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Typing :: Typed",
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords='nlp file io string text mining ipa voice',
    install_requires=[
        "nlp2",
        "zhon",
        "hanzidentifier",
        "eng-to-ipa",
        "epitran",
        "fairseq",
        "pykakasi",
        "pinyin-to-ipa",
        "pypinyin"
    ],
    packages=find_packages('.')
)
