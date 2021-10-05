#!/usr/bin/python3
# script per la verifica in pulp del problema del knapsack
# conda activate ROexam
# e lanciare con:
#    ipython ./knapsak/pulp_solution.py
# altrmenti non funziona il seguente import: 
import pulp as p

# Esempio:
# labels ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
#   pesi [15, 16, 18, 11, 13, 5, 7, 3, 1]
# valori [61, 63, 65, 52, 56, 29, 30, 10, 11]
# capacità B dello zaino = 36 

labels = [x.strip() for x in input("array delle etichette: ").replace("'","").replace("[","").replace("]","").split(',')]
pesi = [int(x) for x in input("array dei pesi: ").strip().strip('[').strip(']').strip().split(',')]
assert len(labels) == len(pesi)
valori = [int(x) for x in input("array dei valori: ").strip().strip('[').strip(']').strip().split(',')]
assert len(labels) == len(valori)

while True:
    B = int(input("capacità dello zaino: "))
    
    probLp = p.LpProblem('Knapsack', p.LpMaximize)
    item = []
    obj = 0
    lhs_constraint = 0
    for label, peso, valore in zip(labels, pesi, valori):
        item.append(p.LpVariable(label,lowBound=0,upBound=1,cat='Integer'))
        obj += valore*item[-1]
        lhs_constraint += peso*item[-1]

    probLp += obj
    probLp += lhs_constraint <= B

    print(probLp)
    status = probLp.solve()
    print(p.LpStatus[status])
    print(f"valore ottimo = {p.value(probLp.objective)}")
    print([p.value(x) for x in item])
    print(f"oggetti da prendere: {[labels[i] for i,x in zip(range(len(item)),item) if p.value(x) == 1.0]}")
