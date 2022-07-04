from setuptools import setup, find_packages


setup(
    name="clean_folder",
    version="0.1",
    author="Nickita",
    entry_points = {
        "console_scripts": ['clean-folder=clean_folder.clean:main']
    },
    license='Free',
    packages=find_packages(),
    description="Folder cleaner"
)