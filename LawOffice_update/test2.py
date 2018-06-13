l1 = [['      (  Chun', '6.0      hr.      0      mins.', '$9900.0  )'],
['      (  Chun', '0      hr.      15.0      mins.', '$412.5  )'],
['      (  Chun', '6.0      hr.      0      mins.', '$9900.0  )']]
reList = list(set([tuple(t) for t in l1]))
reList = [list(v) for v in reList]
print(reList)