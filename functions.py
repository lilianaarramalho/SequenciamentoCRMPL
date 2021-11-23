import copy

import pandas as pd
import itertools
from tqdm import tqdm
from time import time
from classes import *
import ast
from datetime import date
import datetime
import json
import numpy as np

def read_arguments():

    global importar_materiais

    file = open("data/arguments.txt", "r")

    contents = file.read()

    dictionary = ast.literal_eval(contents)

    file.close()

    importar_materiais = dictionary.get('importar_materiais')
    importar_cts = dictionary.get('importar_cts')

    return importar_materiais,importar_cts

def import_material(importar_materiais,ofs):

    global materiais

    if importar_materiais==1 or importar_materiais==0:
        print('IMPORTAR CARACTERÍSTICAS DOS MATERIAIS')
        start = time()

        df_mara = pd.read_csv('data/01. dimensoes.csv', sep=',', encoding='iso-8859-1')
        df_mara['Material'] = df_mara['Objeto'].astype(str)
        df_mara['Material'] = df_mara['Material'].str.split('.').str[0]
        df_mara = df_mara.sort_values(by='Material')
        df_mara['Nº int.caract.'] = df_mara['Nº int.caract.'].astype(str)
        df_mara['Val.caract.'] = df_mara['Val.caract.'].astype(str)
        materiais_mara = df_mara['Material'].tolist()
        materiais_unique = df_mara['Material'].unique().tolist()
        caracteristicas = df_mara['Nº int.caract.'].tolist()
        valores = df_mara['Val.caract.'].tolist()

        df_bom = pd.read_csv('data/03. bom.csv', sep=",", encoding='iso-8859-1')
        df_bom = df_bom.dropna()

        df_bom['Material'] = df_bom['Material'].astype(str)
        df_bom['Material'] = df_bom['Material'].str.split('.').str[0]
        df_bom = df_bom.sort_values(by='Material')
        df_bom['Descrição Material'] = df_bom['Descrição Material'].astype(str)
        df_bom['Unidade material'] = df_bom['Unidade material'].astype(str)
        df_bom['Centro trabalho'] = df_bom['Centro trabalho'].astype(str)
        df_bom['Componente'] = df_bom['Componente'].astype(str)
        df_bom['Descrição componente'] = df_bom['Descrição componente'].astype(str)
        df_bom['col_bmeng'] = df_bom['col_bmeng'].astype(str)
        df_bom['Quantidade componente'] = df_bom['Quantidade componente'].astype(str)
        df_estabilizacao=pd.read_csv('data/06. tempo estabilizacao.csv',sep=",",encoding='ISO-8859-1')
        df_estabilizacao['material']=df_estabilizacao['material'].astype(str)
        df_estabilizacao['dias'] = df_estabilizacao['dias'].astype(int)
        material_estabilizacao=df_estabilizacao['material'].tolist()
        dias_estabilizacao=df_estabilizacao['dias'].tolist()

        df_bom = df_bom.sort_values(by='Material')

        materiais_bom = df_bom['Material'].tolist()

        last_posicao = -1
        count_materiais = 0
        materiais = []

    if importar_materiais==1 or importar_materiais==0:

        with tqdm(total=len(materiais_unique)) as pbar:
            for material_atual in materiais_unique:
                if material_atual in materiais_bom:
                    caracteristicas_material = {}
                    for posicao in range(last_posicao + 1, len(materiais_mara)):
                        if materiais_mara[posicao] == material_atual:
                            caracteristicas_material[caracteristicas[posicao]] = valores[posicao]
                            last_posicao = posicao

                    try:
                        tipo_material=caracteristicas_material.get('AGL_REFERENCIA')
                    except:
                        tipo_material=""

                    if tipo_material in material_estabilizacao:
                        index_estabilizacao=material_estabilizacao.index(tipo_material)
                        tempo_estabilizacao=dias_estabilizacao[index_estabilizacao]
                    else:
                        tempo_estabilizacao=0

                    new_material = material(count_materiais, material_atual, caracteristicas_material,tempo_estabilizacao)
                    materiais.append(new_material)
                    count_materiais += 1

                pbar.update(1)

        pbar.close()

        end=time()

        print('--Importação concluída em ' + str(round(end-start)) + ' segundos.')

    elif importar_materiais==0:

        codigos = []

        for of in ofs:
            if of.id_material not in codigos:
                codigos.append(str(of.id_material))

        with tqdm(total=len(materiais_unique)) as pbar:
            for material_atual in materiais_unique:
                if material_atual in materiais_bom and material_atual in codigos:
                    caracteristicas_material={}
                    for posicao in range(last_posicao+1,len(materiais_mara)):
                        if materiais_mara[posicao]==material_atual:
                            caracteristicas_material[caracteristicas[posicao]]=valores[posicao]
                            last_posicao=posicao

                    try:
                        tipo_material = caracteristicas_material.get('AGL_REFERENCIA')
                    except:
                        tipo_material = ""

                    if tipo_material in material_estabilizacao:
                        index_estabilizacao = material_estabilizacao.index(tipo_material)
                        tempo_estabilizacao = dias_estabilizacao[index_estabilizacao]
                    else:
                        tempo_estabilizacao = 0

                    new_material = material(count_materiais, str(material_atual), caracteristicas_material,tempo_estabilizacao)
                    materiais.append(new_material)
                    count_materiais += 1

                pbar.update(1)

        pbar.close()

        end=time()

        print('--Importação concluída em ' + str(round(end-start)) + ' segundos.')

    else:
        materiais = []
        output = pd.read_csv('data/101. materiais.csv', sep=",", encoding="ISO-8859-1")
        id_materiais = output['id_material'].tolist()
        codigo_materiais = output['codigo_material'].tolist()
        caracteristicas = output['caracteristicas'].tolist()
        id_precedencias = output['id_precedencias'].tolist()
        fatores_inc = output['fator_inc'].tolist()
        descricao_materiais = output['descricao_material'].tolist()
        unidades_material = output['unidade_material'].tolist()
        centros_trabalho = output['centro trabalho'].tolist()
        tempo_estabilizacao=output['tempo_estabilizacao'].tolist()

        for posicao in range(len(id_materiais)):
            new_material = material(id_materiais[posicao], codigo_materiais[posicao],json.loads(caracteristicas[posicao].replace("\'","\"")),tempo_estabilizacao[posicao])
            new_material.id_precedencias = ast.literal_eval(id_precedencias[posicao])
            new_material.fator_inc = ast.literal_eval(fatores_inc[posicao])
            new_material.descricao_material = descricao_materiais[posicao]
            new_material.unidade_material = unidades_material[posicao]
            new_material.centro_trabalho = centros_trabalho[posicao]
            materiais.append(new_material)


    if importar_materiais==1 or importar_materiais==0:

        print('IMPORTAR BOM')
        start = time()

        materiais_unique = df_bom['Material'].unique().tolist()
        descricao_material_bom =df_bom['Descrição Material'].tolist()
        unidade_material_bom=df_bom['Unidade material'].tolist()
        centro_trabalho_bom=df_bom['Centro trabalho'].tolist()
        componente_bom=df_bom['Componente'].tolist()
        col_bmeng=df_bom['col_bmeng'].tolist()
        quantidade_componenete=df_bom['Quantidade componente'].tolist()

        last_posicao = -1
        count_materiais = 0

        with tqdm(total=len(materiais_unique)) as pbar:
            for material_atual in materiais_unique:

                id_material=-1
                for id_material in range(len(materiais)):
                    material_def=materiais[id_material]
                    if material_def.codigo_material==material_atual:
                        id_material=material_def.id_material
                        break

                if id_material!=-1:

                    for posicao in range(last_posicao + 1, len(materiais_bom)):

                        if materiais_bom[posicao] == material_atual:

                            materiais[id_material].descricao_material = descricao_material_bom[posicao]
                            materiais[id_material].unidade_material = unidade_material_bom[posicao]
                            materiais[id_material].centro_trabalho=centro_trabalho_bom[posicao]

                            componente=componente_bom[posicao]

                            try:
                                fator_inc=float(quantidade_componenete[posicao])/float(col_bmeng[posicao])

                            except:
                                fator_inc = col_bmeng[posicao]

                            id_componente=-1

                            for material_componente in materiais:
                                if material_componente.codigo_material==componente:
                                    id_componente=material_componente.id_material
                                    break

                            if id_componente!=-1:

                                material_def.id_precedencias.append(id_componente)
                                material_def.fator_inc.append(fator_inc)

                            last_posicao = posicao
                        else:
                            break

                pbar.update(1)
                count_materiais += 1

        pbar.close()

        end = time()

        print('--Importação concluída em ' + str(round(end - start)) + ' segundos.')

        print('Guardar nova importação de materiais')
        output_materiais=[]

        for material_output in materiais:
            new_row={'id_material':material_output.id_material,
                     'codigo_material':material_output.codigo_material,
                     'caracteristicas':material_output.caracteristicas,
                     'tempo_estabilizacao':material_output.tempo_estabilizacao,
                     'id_precedencias':material_output.id_precedencias,
                     'fator_inc':material_output.fator_inc,
                     'descricao_material':material_output.descricao_material,
                     'unidade_material':material_output.unidade_material,
                     'centro trabalho':material_output.centro_trabalho,
                     }
            output_materiais.append(new_row)

        df=pd.DataFrame(output_materiais)
        df.to_csv('data/101. materiais.csv',encoding='ISO-8859-1',sep=",")

    return materiais

def import_cts(importar_cts):

    cts = []
    slots = []
    maquinas = []

    if importar_cts==1:

        output = []
        nome_maquinas=[]

        df_cts=pd.read_csv('data/02. cts.csv',sep=",",encoding='ISO-8859-1')
        cts_unique=df_cts['ct'].unique().tolist()
        nome_mes=df_cts['maquina'].tolist()
        caminho_critico=df_cts['caminho_critico'].tolist()
        cts_atual=df_cts['ct'].tolist()
        df_cts=pd.read_csv('data/02. cts total.csv',sep=",",encoding='ISO-8859-1')
        cts_total=df_cts['Centro trabalho'].tolist()
        descricao_total=df_cts['Descrição'].tolist()
        nome_turno=df_cts['Definição Turno'].tolist()

        count_cts=0
        count_maquinas=0
        count_slots=0

        for ct_atual in cts_unique:

            created=False

            for posicao_total in range(len(cts_total)):

                ct_total=cts_total[posicao_total]

                if ct_total==ct_atual:

                    if created==False:

                        new_ct=ct(count_cts,ct_atual,descricao_total[posicao_total])

                        cts.append(new_ct)

                        created=True
                        break

            if created==True:

                for posicao_cts in range(len(nome_mes)):
                    if cts_atual[posicao_cts]==ct_atual:
                        new_maquina=maquina(count_maquinas,count_cts,nome_mes[posicao_cts])
                        maquinas.append(new_maquina)
                        new_ct.id_maquinas.append(count_maquinas)
                        new_ct.is_caminho_critico = caminho_critico[posicao_cts]

                        #todo alterar leitura das slots
                        hora_inicio=0
                        hora_fim=hora_inicio+60*8
                        for index_slot in range(21):
                            new_slot=slot(count_slots,hora_inicio,hora_fim,nome_turno[posicao_cts],count_maquinas)
                            slots.append(new_slot)
                            new_maquina.id_slots.append(count_slots)
                            count_slots+=1
                            hora_inicio=hora_fim
                            hora_fim=hora_inicio+60*8

                        count_maquinas+=1

                new_row = {'id_ct': new_ct.id_ct,
                           'nome': new_ct.nome,
                           'descricao': new_ct.descricao,
                           'id_maquinas': new_ct.id_maquinas,
                           'caracteristicas_setup': new_ct.caracteristicas_setup}
                output.append(new_row)

                count_cts += 1

        df=pd.DataFrame(output)
        df.to_csv('data/102. cts.csv',encoding='ISO-8859-1',sep=",")

    else:

        output=pd.read_csv('data/102. cts.csv',encoding='ISO-8859-1',sep=",")
        id_ct=output['id_ct'].tolist()
        nome=output['nome'].tolist()
        descricao=output['descricao'].tolist()
        id_maquinas=output['id_maquinas'].tolist()
        caracteristicas_setup=output['caracteristicas_setup'].tolist()

        for index in range(len(id_ct)):
            new_ct=ct(id_ct[index],nome[index],descricao[index],id_maquinas[index],caracteristicas_setup[index])
            cts.append(new_ct)

    return cts,maquinas,slots

def import_ofs(cts,semana_atual,alertas,nomes_cts,maquinas,nomes_maquinas):

    ofs=[]

    df_ofs=pd.read_csv('data/04. ofs.csv',sep=",",encoding='ISO-8859-1')
    df_ofs=df_ofs[df_ofs['Centro de trabalho'].isin(nomes_cts)]
    df_ofs['Data-base do fim']=pd.to_datetime(df_ofs['Data-base do fim'],
                                                        format='%d/%m/%Y', errors='coerce')
    df_ofs['semana']=df_ofs['Data-base do fim'].dt.isocalendar()['week']
    #o sort permite que os grupos sejam criados com os atrasos em primeiro lugar
    df_ofs=df_ofs.sort_values(by='semana')
    df_ofs=df_ofs[df_ofs['semana']<=semana_atual]
    df_ofs['Ordem de produção / planeada']=df_ofs['Ordem de produção / planeada'].astype(float)
    df_ofs=df_ofs[(df_ofs['Ordem de produção / planeada']>=1600000000) &(df_ofs['Ordem de produção / planeada']<=1700000000)]
    df_ofs['Duração da operação']=df_ofs['Duração da operação'].str.replace(" ","")
    df_ofs['Duração da operação']=df_ofs['Duração da operação'].astype(float)
    df_ofs['Duração da operação']=round(df_ofs['Duração da operação']*60)
    df_ofs['Quantidade total da ordem'] = df_ofs['Quantidade total da ordem'].str.replace(" ","")
    df_ofs['Quantidade total da ordem']=df_ofs['Quantidade total da ordem'].astype(float)
    df_ofs['Quantidade fornecida ordem de produção']=df_ofs['Quantidade fornecida ordem de produção'].str.replace(" ","")
    df_ofs['Quantidade fornecida ordem de produção']=df_ofs['Quantidade fornecida ordem de produção'].astype(float)
    df_ofs['Qtd.necessária']=df_ofs['Qtd.necessária'].str.replace(" ","")
    df_ofs['Qtd.necessária']=df_ofs['Qtd.necessária'].astype(float)
    df_ofs['quantidade']=df_ofs['Quantidade total da ordem']-df_ofs['Quantidade fornecida ordem de produção']
    df_ofs['quantidade_consumo']=df_ofs['quantidade']/df_ofs['Quantidade total da ordem']*df_ofs['Qtd.necessária']

    df_ofs=df_ofs[df_ofs['quantidade']>0]

    df_ofs=df_ofs.drop_duplicates(subset='Ordem de produção / planeada',keep=("first"))

    df_producao = pd.read_csv('data/07. ofs em producao.csv', sep=",", encoding='iso-8859-1')

    df_producao = df_producao[3:]

    new_header = df_producao.iloc[0]
    df_producao = df_producao[1:]
    df_producao.columns = new_header

    df_producao['AreaSapWorkCenter'] = df_producao['AreaSapWorkCenter'].ffill()

    df_producao = df_producao[df_producao['OrderName'].notnull()]
    df_producao['OrderName'] = df_producao['OrderName'].str.split('.').str[1]
    df_producao['OrderName'] = df_producao['OrderName'].astype(int)

    df_producao['Total'] = df_producao['Total'].str.replace(" ", "")

    df_producao['Total']=df_producao['Total'].astype(float)

    df_producao = df_producao[df_producao['SystemAltName'].isin(nomes_maquinas)]

    try:
        df_producao['TransactionDateTime'] = pd.to_datetime(df_producao['TransactionDateTime'],
                                                            format='%d/%m/%Y %H:%M:%S', errors='coerce')
    except:
        df_producao['TransactionDateTime'] = pd.to_datetime(df_producao['TransactionDateTime'],
                                                            format='%m/%d/%Y %I:%M:%S %p', errors='coerce')

    gb = df_producao[
        df_producao.groupby('SystemAltName').TransactionDateTime.transform('max') == df_producao[
            'TransactionDateTime']]

    df_producao = df_producao.groupby(by=['OrderName'])['Total'].sum()

    df_producao = df_producao.reset_index()

    codigo_of_prod = df_producao['OrderName'].tolist()

    total_of_prod = df_producao['Total'].tolist()

    nome_maquina = gb['SystemAltName'].tolist()
    ordem_maquina = gb['OrderName'].tolist()

    codigo_of=df_ofs['Ordem de produção / planeada'].tolist()
    semana=df_ofs['semana'].tolist()
    codigo_material=df_ofs['Material de produção'].tolist()
    duracao_operacao=df_ofs['Duração da operação'].tolist()
    quantidade_of=df_ofs['quantidade'].tolist()

    centro_trabalho=df_ofs['Centro de trabalho'].tolist()

    count_ofs=0

    for index in range(len(codigo_of)):

        id_ct=-1
        id_material=codigo_material[index]

        quantidade = quantidade_of[index]
        duracao = duracao_operacao[index]

        for ct in cts:
            if ct.nome==centro_trabalho[index]:
                id_ct=ct.id_ct
                break

        if id_ct==-1:
            alertas.append('O centro de trabalho ' + str(centro_trabalho[index]) + ' não se encontra definido.')

        if id_ct!=-1:

            id_maquina=-1
            alocar=False

            for posicao_ordem in range(len(ordem_maquina)):
                if int(codigo_of[index]) == ordem_maquina[posicao_ordem]:
                    alocar=True
                    break

            for maquina in maquinas:
                if maquina.nome == nome_maquina[posicao_ordem]:
                    id_maquina = maquina.id_maquina
                    break

            found=False

            for posicao in range(len(codigo_of_prod)):

                codigo = codigo_of_prod[posicao]

                if codigo_of[index] == codigo:

                    found=True

                    if total_of_prod[posicao]<=0:
                        producao=0
                    else:
                        producao=total_of_prod[posicao]

                    duracao=int((quantidade - producao)/quantidade*duracao)

                    quantidade = quantidade - producao

                    if quantidade > 0 or alocar==True:
                        new_of=of(count_ofs,cts[id_ct].id_maquinas,semana[index],codigo_of[index],duracao,quantidade,id_material)
                        ofs.append(new_of)
                        count_ofs += 1

            if found==False:

                new_of = of(count_ofs, cts[id_ct].id_maquinas, semana[index], codigo_of[index], duracao, quantidade,
                            id_material)
                ofs.append(new_of)
                count_ofs += 1

            if alocar == True:
                new_of.id_maquina_alocada = id_maquina



    return ofs,alertas

def calcular_semana_atual():

    dia_atual=date.today()
    dia_da_semana=dia_atual.weekday()
    semana_atual=date.today().isocalendar()[1]
    if dia_da_semana>=3:
        semana_atual+=1

    return semana_atual

def identificar_materiais(ofs,materiais,alertas):

    for of in ofs:

        incluido=False

        for material in materiais:

            if str(of.id_material)==str(material.codigo_material):

                of.id_material=material.id_material

                incluido=True

                break

        if incluido==False:

            alertas.append('O material ' + str(of.id_material) + ' não se encontra definido na tabela MARA. A OF ' + str(of.cod_of) + ' foi removida')

            #ofs.remove(of)

    return ofs,alertas

def importar_stocks(ofs,materiais):

    nomes_materiais=[]
    for material in materiais:
        nomes_materiais.append(str(material.codigo_material))

    df = pd.read_csv('data/05. stock mes.csv', sep=",", encoding="ISO-8859-1")
    new_header = df.iloc[0]
    df = df[1:]
    df.columns = new_header
    df = df.dropna()
    df['MaterialKey']=df['MaterialKey'].astype(str)
    df=df[df['MaterialKey'].isin(nomes_materiais)]
    df['dia'] = df['Lot'].str[4:6]
    df['mes'] = df['Lot'].str[6:8]
    df['ano'] = df['Lot'].str[8:]
    df['data'] = df['dia'] + "/" + df['mes'] + "/" + df['ano']
    unique_materias=df['MaterialKey'].unique().tolist()
    df = df.groupby(by=['MaterialKey', 'data'])['Total'].sum()
    df=df.reset_index()
    materiais_total=df['MaterialKey'].tolist()
    totais=df['Total'].tolist()
    datas=df['data'].tolist()

    last_posicao=0
    for unique in unique_materias:
        id_material=-1
        for material in materiais:
            if material.codigo_material==unique:
                id_material=material.id_material
                break
        for posicao in range(last_posicao,len(totais)):
            if materiais_total[posicao]==unique:
                tempo=0
                if materiais[id_material].tempo_estabilizacao!=0:
                    try:
                        dia=datetime.datetime.strptime(datas[posicao], '%d/%m/%y')
                    except:
                        dia=datetime.datetime.now()
                        tempo=0

                    today = datetime.datetime.now()

                    if (today - dia).days < materiais[id_material].tempo_estabilizacao and (today - dia).days>0 :
                        tempo = materiais[id_material].tempo_estabilizacao - (today - dia).days

                if float(totais[posicao])>0:
                    if tempo in materiais[id_material].dias_lote:
                        posicao_stock=materiais[id_material].dias_lote.index(tempo)
                        materiais[id_material].stock[posicao_stock]=materiais[id_material].stock[posicao_stock]+float(totais[posicao])

                    else:
                        materiais[id_material].stock.append(float(totais[posicao]))
                        materiais[id_material].dias_lote.append(tempo)

                last_posicao+=1

            else:
                break

    return ofs, materiais

def atualizar_caracteristicas_setup(cts):

    df=pd.read_csv('data/08. setups a considerar.csv',sep=",",encoding="ISO-8859-1")

    cts_setup=df['ct'].tolist()
    setup=df['caracteristica'].tolist()

    for id_ct in range(len(cts_setup)):

        nome_ct=cts_setup[id_ct]

        for ct in cts:

            if ct.nome==nome_ct:

                ct.caracteristicas_setup.append(setup[id_ct])
                break

    return cts

def criar_grupos(cts,ofs,materiais):

    grupos_ct=[]

    for ct in cts:

        id_ofs=[]

        helper = []

        grupos=[]

        for of in ofs:

            if of.id_maquinas==ct.id_maquinas:

                id_ofs.append(of.id_of)

                caracteristicas_of=ct.nome

                for caracteristica in ct.caracteristicas_setup:

                   id_material=of.id_material

                   try:

                       caracteristica=materiais[id_material].caracteristicas.get(caracteristica)

                   except:

                       caracteristica=""

                   caracteristicas_of=str(caracteristicas_of)+str(caracteristica)

                if caracteristicas_of not in helper:

                    id_grupo=len(helper)

                    helper.append(caracteristicas_of)

                    grupos.append([of.id_of])

                    of.id_grupo=id_grupo

                else:

                    id_grupo=helper.index(caracteristicas_of)

                    temp=copy.deepcopy(grupos[id_grupo])

                    temp.append(of.id_of)

                    grupos[id_grupo]=copy.deepcopy(temp)

                    of.id_grupo=id_grupo


        grupos_ct.append(grupos)

    return grupos_ct,ofs

def gerar_combinacoes(grupos,cts):

    combinacoes=[]

    for ct in cts:

        id_posicao_grupo=ct.id_ct

        grupos_a_considerar=grupos[id_posicao_grupo]

        combinacoes_to_append = []
        for id_grupo in range(len(grupos_a_considerar)):
            combinacoes_to_append.append(id_grupo)


        if ct.is_caminho_critico == 0:

            new_list=[]
            combinacoes_to_append=itertools.permutations(combinacoes_to_append,len(combinacoes_to_append))
            for combination in combinacoes_to_append:
                new_list.append(combination)

            combinacoes.append(new_list)

        else:

            combinacoes.append(combinacoes_to_append)

    combinations=(itertools.product(combinacoes[0],combinacoes[1],combinacoes[2],combinacoes[3]))
    lista=[]
    for combination in combinations:
        lista.append(combination)
        print(combination)

    return lista

def calcular_grupos_prontos(combinacao,ofs,materiais,cts):
    possivel=True
    ofs_to_return=[]

    for id_ct in range(len(combinacao)):

        try:
            len(combinacao[id_ct][0])
            ofs_grupo = combinacao[id_ct][0]
        except:
            ofs_grupo = combinacao[id_ct]

        if cts[id_ct].is_caminho_critico!=1:

            for id_of in ofs_grupo:

                alocar=False
                id_materiais_precedencias = materiais[ofs[id_of].id_material].id_precedencias
                of_possivel,materiais = verificar_possivel_stock(ofs, id_of, materiais,alocar)

                if of_possivel==False:

                    of_possivel,ofs=verificar_possivel_precedencias(id_materiais_precedencias,ofs,id_of)

                if of_possivel==True:
                    ofs[id_of].possivel=1

                else:
                    possivel=False
                    ofs_grupo.remove(id_of)

            ofs_to_return.append(ofs_grupo)

        else:

            for id_of in ofs_grupo:

                alocar=False
                id_materiais_precedencias = materiais[ofs[id_of].id_material].id_precedencias
                of_possivel,materiais = verificar_possivel_stock(ofs, id_of, materiais,alocar)

                if of_possivel==False:

                    of_possivel,ofs=verificar_possivel_precedencias(id_materiais_precedencias,ofs,id_of)

                if of_possivel==True:
                    ofs[id_of].possivel=1

                else:
                    ofs_grupo.remove(id_of)
                    possivel=False
            ofs_to_return.append(ofs_grupo)

    return materiais,ofs_to_return,ofs,possivel

def gerar_plano(combinacao,cts,ofs,materiais,maquinas,slots):

    ordens_alocadas = 0
    n_impossivel = 0
    n_ofs=0

    for id_ct in range(len(combinacao)):
        n_ofs+=len(combinacao[id_ct])

    while ordens_alocadas + n_impossivel <= n_ofs:

        materiais,grupos,ofs,possivel=calcular_grupos_prontos(combinacao,ofs,materiais,cts)

        for grupo in grupos:
            for id_of in grupo:
                min_atual,id_slot_sugerida,id_maquina_sugerida=alocar(maquinas,id_of,slots)
                hora_fim=min_atual+ofs[id_of].duracao
                maquinas[id_maquina_sugerida].ultimo_min_alocado=hora_fim
                ofs[id_of].id_maquina_alocada=id_maquina_sugerida
                ofs[id_of].id_slot_inicio=id_slot_sugerida
                ofs[id_of].hora_fim=hora_fim
                ofs=atualizar_data_min(ofs,id_of)

    return maquinas,ofs


def verificar_possivel_stock(ofs, id_of, materiais,alocar):

    count_precedencia=0
    id_materiais_precedencias = materiais[ofs[id_of].id_material].id_precedencias
    of_possivel=True

    for id_material_precedencia in id_materiais_precedencias:

        quantidade = ofs[id_of].quantidade * materiais[ofs[id_of].id_material].fator_inc[count_precedencia]

        stock_precedencia = materiais[id_material_precedencia].stock

        count = 0
        total = 0

        while total < quantidade and count < len(stock_precedencia):
            if stock_precedencia[count] > quantidade:
                total = quantidade
            else:
                total += stock_precedencia[count]

        if total < quantidade:
            of_possivel = False

        count_precedencia += 1

    if of_possivel==True and alocar==True:

        for id_material_precedencia in id_materiais_precedencias:

            quantidade = ofs[id_of].quantidade * materiais[ofs[id_of].id_material].fator_inc[count_precedencia]

            stock_precedencia = materiais[id_material_precedencia].stock
            dias_lote = materiais[id_material_precedencia].dias_lote

            count = 0
            total = 0

            while total < quantidade and count < len(stock_precedencia):
                if stock_precedencia[count] > quantidade:
                    total = quantidade
                    materiais[id_material_precedencia].stock[count]-=quantidade
                else:
                    total -= stock_precedencia[count]
                    del materiais[id_material_precedencia].stock[count]
                    del materiais[id_material_precedencia].dias_lote[count]

                if dias_lote[count] > ofs[id_of].data_min:
                    ofs[id_of].data_min = dias_lote[count]

            count_precedencia += 1

    return of_possivel,materiais

def verificar_possivel_precedencias(id_materiais_precedencias,ofs,id_of):

    of_possivel = True
    for id_material_precedencia in id_materiais_precedencias:
        index_precedencia = id_materiais_precedencias.index(id_material_precedencia)
        quantidade_necessaria = materiais[ofs[id_of].id_material].fator_inc[index_precedencia] * ofs[
            id_of].quantidade

        total = 0
        count = 0
        while total < quantidade_necessaria and count < len(ofs):
            if ofs[count].id_material == id_material_precedencia:
                if ofs[count].quantidade > quantidade_necessaria:
                    total = quantidade_necessaria
                else:
                    total += ofs[count].quantidade

                ofs[id_of].id_precedencias.append(count)
                ofs[count].id_sequencias.append(id_of)
            else:
                count += 1

        if total < quantidade_necessaria:
            of_possivel = False

    return of_possivel,ofs

def alocar(id_of,ofs,maquinas,slots):

    id_maquinas_possiveis=ofs[id_of].id_maquinas

    data_min_of=ofs[id_of].data_min*24*60
    min_atual=99999
    id_maquina_sugerida=-1

    for id_maquina in id_maquinas_possiveis:

        if maquinas[id_maquina].ultimo_min_alocado<min_atual:

            min_atual=maquinas[id_maquina].ultimo_min_alocado
            id_maquina_sugerida=id_maquina

    if min_atual<data_min_of:
        min_atual=data_min_of

    id_slots=maquinas[id_maquina_sugerida].id_slots
    id_slot_sugerida=id_slots[0]
    for posicao in range(1,len(id_slots)):
        id_slot=id_slots[posicao]
        id_slot_anterior=id_slots[posicao-1]
        if slots[id_slot_anterior].hora_fim>min_atual and slots[id_slot].hora_fim<min_atual:
            id_slot_sugerida=id_slot
            break

    return min_atual,id_slot_sugerida,id_maquina_sugerida

def atualizar_data_min(ofs,id_of):

    id_sequencias=ofs[id_of].id_sequencias

    for id_of_sequente in id_sequencias:
        ofs[id_of_sequente].data_min=ofs[id_of].hora_fim/60

    return ofs




