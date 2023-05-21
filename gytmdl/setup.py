from setuptools import setup, find_packages

setup(
    name="gytmdl_ja",  # パッケージ名を指定します
    version="0.1",  # バージョンを指定します
    packages=find_packages(),  # 自動的にパッケージとサブパッケージを見つけます
)

setup(
    # ...
    entry_points={
        'console_scripts': [
            'gytmdl-ja=gytmdl.__main__:main',
        ],
    },
    # ...
)

