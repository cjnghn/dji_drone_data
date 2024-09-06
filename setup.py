from setuptools import setup, find_packages

setup(
    name="dji_drone_data",
    version="0.1.0",
    description="A library to parse SRT data and apply Kalman filter to GPS coordinates.",
    author="cjnghn",
    author_email="chotnt741@gmail.com",
    packages=find_packages(),
    install_requires=["numpy", "filterpy"],
    url="https://github.com/cjnghn/dji_drone_data",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
