# créditos: https://www.geeksforgeeks.org/stratified-sampling-in-pandas/
import pandas as pd

# importando base de dados
database = "enem2020_v8"
db = pd.read_csv(database+".csv", sep=';', header=None)

# Stratified Sampling usando Regiões do Brasil
# lista de % da base de dados para amostrar, no caso de 1% a 90%
sampRate_list = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90]

for sampRate in sampRate_list:
    # o atributo de regiões é a 5ª coluna da base de dados
    db2 = db.groupby(5, group_keys=False).apply(lambda x: x.sample(frac=sampRate/100))
    # criar arquivo de cada amostragem
    db2.to_csv(database + "_sample_" + str(sampRate) + "-100.csv", sep=';', header=False, index=False, encoding='utf-8')