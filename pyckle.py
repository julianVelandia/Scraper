# -*- coding: utf-8 -*-
import pickle
import numpy as np

result = {}
#names = ['id','data']
#formats = ['f8','f8']
#dtype = dict(names = names, formats=formats)
#array = np.array(list(result.items()), dtype=dtype)

data = list(result.items())
an_array = np.array(data)

pickle_out = open("dataset.pkl","wb")
pickle.dump(an_array, pickle_out)
pickle_out.close()

