from setuptools import setup, find_packages

setup(
    include_package_data=True,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={'vorta.i18n': ['qm/*.qm']},
    use_scm_version={'write_to': 'src/vorta/_version.py', 'write_to_template': '__version__ = "{version}"\n'}
)
