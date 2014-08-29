from setuptools import setup, find_packages
from celerymon import get_version


setup(
    name='django-celery-mon',
    version=get_version(),
    description='App for monitoring Celery workers',
    keywords="django celery monitoring",
    long_description=open('README.rst').read(),
    author="GoTLiuM InSPiRiT",
    author_email='gotlium@gmail.com',
    url='http://github.com/gotlium/django-celery-mon/',
    packages=find_packages(exclude=['demo']),
    package_data={'celerymon': [
        'locale/*/LC_MESSAGES/django.*',
    ]},
    include_package_data=True,
    install_requires=[
        'setuptools',
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
