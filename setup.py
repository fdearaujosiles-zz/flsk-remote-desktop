from setuptools import find_packages, setup

setup(
    name='flsk-remote-desktop',
    version='0.1',
    author='Fernando Siles',
    author_email='fdearaujosiles@gmail.com',
    url='https://github.com/fdearaujosiles/flsk-remote-desktop.git',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
