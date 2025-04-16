import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ScheduleService-pkg-nptan2005", # Replace with your own username
    version="0.0.1",
    author="Nguyen Phuoc Tan",
    author_email="nptan2005@gmail.com",
    description="Auto export excel file",
    packages=setuptools.find_packages(),
    python_requires='>=3.12',
)