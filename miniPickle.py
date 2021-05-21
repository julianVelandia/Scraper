# -*- coding: utf-8 -*-
import pickle
import numpy as np

result={}

data = list(result.items())
an_array = np.array(data)

pickle_out = open("miniarit3.pkl","wb")
pickle.dump(an_array, pickle_out)
pickle_out.close()