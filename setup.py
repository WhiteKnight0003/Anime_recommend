from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name = 'Anime_Recommender',
    version = '0.1',
    author='TienChung0003',
    packages = find_packages(),
    install_requires = requirements,
)

# bạn đang muốn chạy file này để cài các gói nên cần chạy lệnh này : 
# uv run python setup.py install