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
zmax = 6
report = 'XClL'
eval = 'l'
thresh = 100


def my_apriori(base, sample):
    result = pf.apriori(tracts=base, target='r', supp=supp, conf=conf, zmin=zmin, zmax=zmax, report=report, eval=eval,
                        thresh=thresh)
    colnames = ['consequent', 'antecedent'] + [report_colnames.get(k, k) for k in list(report)]
    resultado = pd.DataFrame(result, columns=colnames)
    # Pega a quantidade de regras geradas pelo algoritmo
    matrixAP.at[str(sample) + "%", "Qtdd Regras" + str(i[0])] = resultado.shape[0]
    i[0] += 1


def my_fp_growth(base, sample):
    result = pf.fpgrowth(tracts=base, target='r', supp=supp, conf=conf, zmin=zmin, zmax=zmax, report=report, eval=eval,
                         thresh=thresh)
    colnames = ['consequent', 'antecedent'] + [report_colnames.get(k, k) for k in list(report)]
    resultado = pd.DataFrame(result, columns=colnames)
    # Pega a quantidade de regras geradas pelo algoritmo
    matrixFP.at[str(sample) + "%", "Qtdd Regras" + str(i[0])] = resultado.shape[0]
    i[0] += 1


# Inicializar matrizes
matrixFP = pd.DataFrame()
matrixAP = pd.DataFrame()

# Auxiliar
i = [1]

# Lista de tamanhos da base de dados para testar (1% até 100%)
sampleList = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
sampleList = [1, 10]

for sample in sampleList:
    if sample < 100:
        database = "enem2020_v8_sample" + str(sample) + "-100"
    else:
        database = "enem2020_v8"
    db = pd.read_csv(database + ".csv", sep=';', header=None, encoding='utf-8')
    base = db.to_numpy()

    if i[0] > 2:
        i[0] = 1

    # Pegar tempo de execução pro Apriori
    tempo = timeit.repeat(stmt='my_apriori(base, sample)', setup='', repeat=3, number=1, globals=globals())
    # Jogar na matriz o tempo de cada execução
    matrixAP.at[str(sample) + "%", "Tempo Exec1"] = tempo[0]
    matrixAP.at[str(sample) + "%", "Tempo Exec2"] = tempo[1]
    matrixAP.at[str(sample) + "%", "Tempo Exec3"] = tempo[2]

    # Pegar tempo de execução pro FP-Growth
    tempo = timeit.repeat(stmt='my_fp_growth(base, sample)', setup='', repeat=3, number=1, globals=globals())
    # Jogar na matriz o tempo de cada execução
    matrixFP.at[str(sample) + "%", "Tempo Exec1"] = tempo[0]
    matrixFP.at[str(sample) + "%", "Tempo Exec2"] = tempo[1]
    matrixFP.at[str(sample) + "%", "Tempo Exec3"] = tempo[2]

# Criar arquivo com as matrizes
matrixAP.to_csv("Desempenho_tam_Apriori_sup" + str(supp) + "_conf" + str(conf) + ".csv", sep=';', decimal=',')
matrixFP.to_csv("Desempenho_tam_FP-Growth_sup" + str(supp) + "_conf" + str(conf) + ".csv", sep=';', decimal=',')
