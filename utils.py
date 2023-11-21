import pandas as pd
import numpy as np

'''
THE BELOW FUNCTION WILL CONVERT 'A|B|C|D' TO ['A','B','C','D']
'''
class Utils:
    def convert_into_list(obj):
        l=[]
        s= str(obj)
        if s.count('|')==0:
            l.append(s)
        else:
            l.append(s.split('|'))
            l=[i for t in l for i in t]
        return l 