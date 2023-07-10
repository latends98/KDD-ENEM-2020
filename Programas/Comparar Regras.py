import pandas as pd

# Carregar as regras obtidas
aprioriRules = pd.read_csv("Regras_Apriori_sup10conf90.csv", sep=';', index_col=False, encoding='utf-8')
fpgrowthRules = pd.read_csv("Regras_FP-Growth_sup10conf90.csv", sep=';', index_col=False, encoding='utf-8')

# Reordenar as regras do Apriori
aprioriRules = aprioriRules.sort_values(by=['consequent', 'antecedent'])
aprioriRules.reset_index(drop=True, inplace=True)
aprioriRules.drop(columns=['Unnamed: 0'], inplace=True)

# Reordenar as regras do FP-Growth
fpgrowthRules = fpgrowthRules.sort_values(by=['consequent', 'antecedent'])
fpgrowthRules.reset_index(drop=True, inplace= True)
fpgrowthRules.drop(columns=['Unnamed: 0'], inplace=True)

# Gerar matriz contendo todas as regras diferentes entre os conjuntos de regras
compMatrix = aprioriRules.compare(fpgrowthRules)
compMatrix.to_csv("compMatrix.csv", sep=';') # Se a matrix resultante for vazia, significa que as regras são iguais