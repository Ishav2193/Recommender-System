import pandas as pd
import numpy as np
from setuptools import setup,find_packages
from typing import List

def get_packages(filepath)->List:
    req=[]
    e_dot='-e.'
    with open(filepath) as f:
        req=f.readlines()
        req=[r.replace("\n","") for r in req]
        if e_dot in req:
            req.remove(e_dot)
    return req

setup(
    name='Recommender-System',
    version='0.0.1',
    author='Ishav Mahajan',
    author_email='ishvmahajan@gmail.com',
    packages=find_packages(),
    install_requires=get_packages('requirements.txt')
)
