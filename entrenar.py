from modelo import  modelomorosidad
test0 = modelomorosidad()
print('AUC test:', test0.entrenar('data/loan_data.csv'))
test0.guardado()
