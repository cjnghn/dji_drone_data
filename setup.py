from setuptools import setup, find_packages

setup(
    name="dji_drone_data",
    version="0.1.0",
    description="A library to parse SRT data and apply Kalman filter to GPS coordinates.",
    author="cjnghn",
    packages=find_packages(),
    install_requires=["numpy", "filterpy"],
)
