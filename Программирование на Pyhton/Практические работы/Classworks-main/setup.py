# setup.py

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="calculator-pkg-nmdbls",          # Уникальное имя пакета
    version="0.1.0",                             # Версия пакета
    author="Arsenij",                           # Ваше имя
    author_email="senyasenyasenyaaa@example.com",        # Ваш email
    description="Простой калькулятор на Python",
    long_description=long_description,           # Длинное описание из README.md
    long_description_content_type="text/markdown",
    url="https://github.com/nmdbls/calculator-pkg",  # Ссылка на репозиторий или сайт
    packages=setuptools.find_packages(),         # Поиск всех пакетов внутри проекта
    classifiers=[                                # Классификаторы
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Укажите вашу лицензию
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',                     # Требуемая версия Python
)