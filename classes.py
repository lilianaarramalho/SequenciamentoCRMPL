class material(object):

    def __init__(self,id_material,codigo_material,caracteristicas,tempo_estabilizacao):
        self.id_material=id_material
        self.codigo_material=str(codigo_material)
        self.caracteristicas=caracteristicas
        self.tempo_estabilizacao=tempo_estabilizacao

        self.id_precedencias=[]
        self.fator_inc=[]

        self.descricao_material=""
        self.unidade_material=""
        self.centro_trabalho=""
        self.stock=[]
        self.dias_lote=[]

    def __repr__(self):
        return str(self.codigo_material)

class ct(object):

    def __init__(self,id_ct,centro_trabalho,descricao):

        self.id_ct=id_ct
        self.nome=centro_trabalho
        self.descricao=descricao
        self.id_maquinas=[]
        self.caracteristicas_setup=[]
        self.is_caminho_critico=-1

    def __repr__(self):
        return str(self.nome)

class maquina(object):

    def __init__(self,id_maquina,id_ct,nome_mes):
        self.id_maquina=id_maquina
        self.id_ct=id_ct
        self.nome=nome_mes
        self.id_slots=[]
        self.ultimo_min_alocado=0

    def __repr__(self):
        return str(self.nome)

class slot(object):

    def __init__(self,id_slot,hora_inicio,hora_fim,nome_turno,id_maquina):

        self.id_slot=id_slot
        self.hora_inicio=hora_inicio
        self.hora_fim=hora_fim
        self.id_maquina=id_maquina
        self.nome_turno=nome_turno

    def __repr__(self):
        return str(self.hora_inicio)

class of(object):

    def __init__(self,id_of,id_maquinas,semana,cod_of,duracao,quantidade,id_material):
        self.id_of=id_of
        self.id_maquinas=id_maquinas
        self.id_material=id_material
        self.semana=semana
        self.id_precedencias=[]
        self.id_sequencias=[]
        self.id_maquina_alocada=-1
        self.id_slot_inicio=-1
        self.cod_of=cod_of
        self.duracao=duracao
        self.quantidade=quantidade
        self.em_producao=0
        self.id_grupo=-1
        self.data_min=0
        self.possivel=0
        self.hora_fim=0

    def __repr__(self):
        return str(self.cod_of)

def limpar_stocks(ofs,materiais,grupos):

    # existe_
    # for grupo in grupos:
    #     for id_of in grupo:

    return grupos