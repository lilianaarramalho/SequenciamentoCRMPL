from functions import *
import warnings
import csv
warnings.filterwarnings('ignore')

start=time()

alertas=[]

semana_atual=calcular_semana_atual()

importar_materiais,importar_cts=read_arguments()

cts,maquinas,slots=import_cts(importar_cts)

cts=atualizar_caracteristicas_setup(cts)

nomes_cts=[]
for ct in cts:
    nomes_cts.append(ct.nome)

nomes_maquinas=[]
for maquina in maquinas:
    nomes_maquinas.append(maquina.nome)

ofs,alertas=import_ofs(cts,semana_atual,alertas,nomes_cts,maquinas,nomes_maquinas)

descricao_ofs=[]
for of in ofs:
    descricao_ofs.append(of.cod_of)

materiais=import_material(importar_materiais,ofs)

ofs,alertas=identificar_materiais(ofs,materiais,alertas)

ofs,materiais=importar_stocks(ofs,materiais)

grupos,ofs=criar_grupos(cts,ofs,materiais)

codigo_ofs=[]
for of in ofs:
    codigo_ofs.append(of.cod_of)

df = pd.DataFrame(data={"col1": codigo_ofs})
df.to_csv("ofs_lidas.csv", sep=',',index=False)

grupos=limpar_stocks(ofs,materiais,grupos)

id_grupos=gerar_combinacoes(grupos,cts)

for combinacao in id_grupos:

    maquinas,ofs=gerar_plano(combinacao,cts,ofs,materiais,maquinas,slots)
    print('fim')

end=time()

total=round(end-start)

print('total ' + str(total))

print(grupos)
