from modelo import  modelomorosidad

test0 = modelomorosidad()
print('AUC test:', test0.entrenar('proyectofinalprogramacion2/data/loan_data.csv'))
test0.guardado()
