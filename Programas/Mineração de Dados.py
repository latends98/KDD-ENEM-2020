import fim as pf  # pyfim
import pandas as pd
# import numpy as np

# importando base de dados
database = "enem2020_v8_sample1-100"
db = pd.read_csv(database+".csv", sep=';', header=None, encoding='utf-8')

# base = db.to_dict(orient='index')
base = db.to_numpy()

# escolher algoritmo para calibrar
algoritmo = 2  # 1 - Apriori; 2 - FP-Growth

# parametros do algoritmo
target = 'r'
supp = 10
conf = 90
zmin = 2
zmax = 6
report = 'XCL'
eval = 'l'
thresh = 100

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

resultado.to_csv("Regras_" + algoritmo_nome + "_sup" + str(supp) + "conf" + str(conf) + ".csv", sep=';')
