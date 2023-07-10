import fim as pf  # pyfim
import pandas as pd
import timeit

# make dict for nicer looking column names
report_colnames = {
    'a': 'support_itemset_absolute',
    's': 'support_itemset_relative',
    'S': 'support_itemset_relative_pct',
    'b': 'support_bodyset_absolute',
    'x': 'support_bodyset_relative',
    'X': 'support_bodyset_relative_pct',
    'h': 'support_headitem_absolute',
    'y': 'support_headitem_relative',
    'Y': 'support_headitem_relative_pct',
    'c': 'confidence',
    'C': 'confidence_pct',
    'l': 'lift',
    'L': 'lift_pct',
    'e': 'evaluation',
    'E': 'evaluation_pct',
    'Q': 'xx',
    'S': 'support_emptyset',
}

# parametros do algoritmo
target = 'r'
supp = 10
conf = 90
zmin = 2
report = 'XClL'
eval = 'l'
thresh = 100


def my_apriori(zmax):
    result = pf.apriori(tracts=base, target='r', supp=supp, conf=conf, zmin=zmin, zmax=zmax, report=report, eval=eval,
                        thresh=thresh)
    colnames = ['consequent', 'antecedent'] + [report_colnames.get(k, k) for k in list(report)]
    resultado = pd.DataFrame(result, columns=colnames)
    # Pega a quantidade de regras geradas pelo algoritmo
    matrixAP.at[str(zmax) + " - ", "Qtdd Regras" + str(i[0])] = resultado.shape[0]
    i[0] += 1


def my_fp_growth(zmax):
    result = pf.fpgrowth(tracts=base, target='r', supp=supp, conf=conf, zmin=zmin, zmax=zmax, report=report, eval=eval,
                         thresh=thresh)
    colnames = ['consequent', 'antecedent'] + [report_colnames.get(k, k) for k in list(report)]
    resultado = pd.DataFrame(result, columns=colnames)
    # Pega a quantidade de regras geradas pelo algoritmo
    matrixFP.at[str(zmax) + " - ", "Qtdd Regras" + str(i[0])] = resultado.shape[0]
    i[0] += 1


# Inicializar Matrizes
matrixAP = pd.DataFrame()
matrixFP = pd.DataFrame()

# Auxiliar
i = [1]

# Lista da quantidade máxima de itens por regra para testar
zmaxList = [2, 3, 4, 5, 6]

database = "enem2020_v8"
db = pd.read_csv(database + ".csv", sep=';', header=None, encoding='utf-8')
base = db.to_numpy()

for zmax in zmaxList:
    if i[0] > 2:
        i[0] = 1

    # Pegar tempo de execução pro Apriori
    tempo = timeit.repeat(stmt='my_apriori(zmax)', setup='', repeat=3, number=1, globals=globals())
    # Jogar na matriz o tempo de cada execução
    matrixAP.at[str(zmax) + " - ", "Tempo Exec1"] = tempo[0]
    matrixAP.at[str(zmax) + " - ", "Tempo Exec2"] = tempo[1]
    matrixAP.at[str(zmax) + " - ", "Tempo Exec3"] = tempo[2]

    # Pegar tempo de execução pro FP-Growth
    tempo = timeit.repeat(stmt='my_fp_growth(zmax)', setup='', repeat=3, number=1, globals=globals())
    # Jogar na matriz o tempo de cada execução
    matrixFP.at[str(zmax) + " - ", "Tempo Exec1"] = tempo[0]
    matrixFP.at[str(zmax) + " - ", "Tempo Exec2"] = tempo[1]
    matrixFP.at[str(zmax) + " - ", "Tempo Exec3"] = tempo[2]

# Criar arquivo com as matrizes
matrixAP.to_csv("Desempenho_zmax_Apriori_sup" + str(supp) + "_conf" + str(conf) + ".csv", sep=';', decimal=',')
matrixFP.to_csv("Desempenho_zmax_FP-Growth_sup" + str(supp) + "_conf" + str(conf) + ".csv", sep=';', decimal=',')
