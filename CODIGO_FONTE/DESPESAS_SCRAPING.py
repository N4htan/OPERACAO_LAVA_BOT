import requests
import os

URL = 'https://dadosabertos.camara.leg.br/api/v2/deputados'
RESP = requests.get(URL).json()

PASTA_RAIZ = './GASTOS_INDIVIDUAIS'
os.mkdir(PASTA_RAIZ)
FILE_CSV = open('NOME_ID_TOTAL.csv', 'w')  # criando arquivo csv para escrever nome, ID, e total de gastos de cada deputado

CONTADOR = 2
GUIA_SOMA = 2
politicos = {}

while CONTADOR <= 9:

    PASTA_MES = './GASTOS_INDIVIDUAIS/MES_' + str(GUIA_SOMA)
    os.mkdir(PASTA_MES)

    for INFO in RESP['dados']: # for usado para buscar nome, id e as diversas despesas de cada deputado
        NOME_DEPUTADO = str(INFO['nome'])
        ID_DEPUTADO = str(INFO['id'])
        PARTIDO_DEPUTADO = str(INFO['siglaPartido'])
        UF_DEPUTADO = str(INFO['siglaUf'])
        URL = 'https://dadosabertos.camara.leg.br/api/v2/deputados/' + ID_DEPUTADO + '/despesas?ano=2019&mes=0' + str(GUIA_SOMA) + '&ordem=ASC&ordenarPor=ano'
        POST = requests.get(URL).json()
        print(POST)

    # criando arquivo txt para escrever as diversas despesas de cada deputado
        FILE_TXT = open('./GASTOS_INDIVIDUAIS/MES_'+ str(GUIA_SOMA) + '/GASTOS_' + NOME_DEPUTADO + '_' + ID_DEPUTADO + '.txt', 'w')

        SOMA = 0.0

        for INFO in POST['dados']:
            DESPESAS_TXT = (INFO['tipoDespesa'] + " = " + str(INFO['valorDocumento']) + "   (" + str(INFO['dataDocumento']) + ")\n")
            FILE_TXT.writelines(DESPESAS_TXT)      # escrevendo as despesas no arquivo txt

            VALOR_DOC = float(INFO['valorDocumento'])
            SOMA = SOMA + VALOR_DOC
            SOMA = float("%.2f" %SOMA)
            CONTADOR = int(CONTADOR)

        FILE_TXT.writelines("TOTAL DE DESPESAS = " + str(SOMA) + '\n' "PARTIDO DEPUTADO = " + PARTIDO_DEPUTADO + '\n' "UF DEPUTADO = " + UF_DEPUTADO)    #escrevendo o total de despesas no arquivo txt

        if NOME_DEPUTADO in politicos:
            politicos[NOME_DEPUTADO].append(SOMA)
        else:
            politicos[NOME_DEPUTADO] = [NOME_DEPUTADO, ID_DEPUTADO, PARTIDO_DEPUTADO, UF_DEPUTADO, SOMA]

    CONTADOR = CONTADOR + 1
    GUIA_SOMA = GUIA_SOMA + 1

for politico in politicos:
    dados = (';'.join(map(str, politicos[politico])))
    print(dados)
    FILE_CSV.writelines('\n' + dados)

