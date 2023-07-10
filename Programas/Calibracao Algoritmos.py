import fim as pf  # pyfim
import pandas as pd

# import numpy as np

# importando base de dados
database = "enem2020_v8_sample1-100"  # carregar amostra de 1% da base de dados
db = pd.read_csv(database + ".csv", sep=';', header=None, encoding='utf-8')

# base = db.to_dict(orient='index')
base = db.to_numpy()

# parametros do algoritmo
algoritmo = 2  # 1 - Apriori; 2 - FP-Growth
target = 'r'  # minerar regras de associação
supp_lista = [10, 12, 14, 16, 18, 20, 30, 40, 50]  # lista de suporte
conf_lista = [75, 80, 85, 90, 95, 100]  # lista de confiança
supp_lista = [10, 12, 14]  # lista de suporte
conf_lista = [95, 100]  # lista de confiança
zmin = 2  # regras contém pelo menos 2 itens (1 antecedente e 1 consequente)
zmax = 6  # quantidade máxima de itens por regra
report = 'XCL'  # apresentar valor de suporte, confiança e lift das regras
eval = 'l'  # parametro extra de avaliação das regras: lift
thresh = 100  # threshold para o parametro extra: valor mínimo de lift = 1

# teste
matrix = pd.DataFrame()

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
    # 'S': 'support_emptyset',
}

for supp in supp_lista:
    for conf in conf_lista:
        if algoritmo == 1:  # Apriori
            algoritmo_nome = "Apriori"
            result = pf.apriori(tracts=base, target='r', supp=supp, conf=conf, zmin=zmin, zmax=zmax, report=report,
                                eval=eval, thresh=thresh)
        elif algoritmo == 2:  # FP-Growth
            algoritmo_nome = "FP-Growth"
            result = pf.fpgrowth(tracts=base, target='r', supp=supp, conf=conf, zmin=zmin, zmax=zmax, report=report,
                                 eval=eval, thresh=thresh)
        colnames = ['consequent', 'antecedent'] + [report_colnames.get(k, k) for k in list(report)]
        resultado = pd.DataFrame(result, columns=colnames)
        chaveSup = "sup" + str(supp)
        chaveConf = "conf" + str(conf)
        matrix.at[chaveSup, chaveConf] = resultado.shape[0]

matrix.to_csv("Calibracao_" + algoritmo_nome + "_1-100.csv", sep=';')
