from setuptools import setup


setup(
    name='cldfbench_streitberggothic',
    py_modules=['cldfbench_streitberggothic'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'streitberggothic=cldfbench_streitberggothic:Dataset',
        ]
    },
    install_requires=[
        'cldfbench',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
