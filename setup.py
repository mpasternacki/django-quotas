from setuptools import setup, find_packages

setup(name="django-quotas",
           version="0.1",
           description="Quota permissions for Django",
           author="Maciej Pasternacki",
           author_email="maciej@pasternacki.net",
           packages=find_packages(),
           include_package_data=True,
)

