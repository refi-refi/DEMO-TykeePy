""" Setup tool for an easier installation of the package.
"""
import setuptools

VERSION = "1.0.0"
NAME = "DEMO-TykeePy"
DESCRIPTION = "Python package for data analysis and trading."
LONG_DESCRIPTION = """
DEMO-TykeePy is open-source version of TykeePy which is Python package for data analysis and trading.
"""

INSTALL_REQUIRES = [
    "python-dotenv==0.21.0",
    "pandas==1.5.0",
    "fastparquet==0.8.3",
    "pyarrow==9.0.0",
    "sqlalchemy==1.4.41",
    "metatrader5==5.0.37",
    "torch==1.12.1",
    "xgboost==1.6.2",
]

setuptools.setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Artūrs Smiltnieks",
    author_email="smiltnieks.art@gmail.com",
    python_requires=">=3.8",
    license="MIT",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    install_requires=INSTALL_REQUIRES,
)
