import pandas as pd
import cx_Oracle
import sys
import datetime
from datetime import date
query1 = "select rs.cd_rs,replace(replace(replace(substr(rs.ds_rs,1,50),chr(13),''),chr(10),' '),'  ',' ') ds_rs,rs.dt_inicio,f.dt_evento dt_termino,extract(year from f.dt_evento) Ano,extract(month from f.dt_evento) Mês,nvl(pe.nm_pessoa_resumido, pe.nm_fantasia) nm_empresa,nvl(pc.nm_pessoa_resumido, nvl(trim(substr(pc.nm_pessoa,1,instr(pc.nm_pessoa,'',1))),'não informado')) nm_solicitante,decode(rs.cd_tipo_prioridade, 231, 'BAIXA', 232, 'MÉDIA', 233, 'ALTA', 234, 'CRÍTICA')nm_prioridade  from repoman.rs_temppp rs,repoman.pessoa pe,repoman.pessoa pc,repoman.rs_fluxo_temppp f where rs.cd_pessoa_empresa = pe.cd_pessoa and rs.cd_pessoa_solicitante = pc.cd_pessoa and rs.cd_contrato is not null and f.cd_rs = rs.cd_rs and f.cd_tipo_status in (34,230,45,211) and f.dt_evento between TO_DATE('01/01/2023','DD/MM/YYYY') and TO_DATE('31/12/2023 23:59:59','DD/MM/YYYY HH24:mi:ss') and (rs.cd_pessoa_responsavel, rs.cd_pessoa_solicitante) not in (select 2,2 from dual) order by rs.cd_tipo_prioridade desc, f.dt_evento"
query2 = "select rs.cd_rs,replace(replace(replace(substr(rs.ds_rs,1,900),chr(13),''),chr(10),' '),'  ',' ') ds_rs,rs.dt_inicio,nvl(pe.nm_pessoa_resumido, pe.nm_fantasia) nm_empresa,nvl(pc.nm_pessoa_resumido, nvl(trim(substr(pc.nm_pessoa,1,instr(pc.nm_pessoa,' ',1))),'não informado')) nm_solicitante,nvl(pp.nm_pessoa_resumido, nvl(trim(substr(pp.nm_pessoa,1,instr(pc.nm_pessoa,' ',1))),'não informado')) nm_primer,decode(rs.cd_tipo_prioridade, 231, 'BAIXA', 232, 'MÉDIA', 233, 'ALTA', 234, 'CRÍTICA') nm_prioridade from repoman.rs_temppp rs,repoman.pessoa pe,repoman.pessoa pc,repoman.pessoa pp,repoman.contrato_colaborador cc where rs.cd_pessoa_empresa = pe.cd_pessoa and rs.cd_pessoa_solicitante = pc.cd_pessoa and cc.cd_pessoa_colaborador = pp.cd_pessoa and 1 = (select max(f.cd_fluxo) from repoman.rs_fluxo_temppp f where f.cd_rs = rs.cd_rs) and rs.cd_contrato is not null and rs.st_prevista = 0 and (rs.cd_pessoa_responsavel, rs.cd_pessoa_solicitante) not in (select 2,2 from dual) and rs.cd_contrato = cc.cd_contrato and cc.cd_ordem = 1"
query3 = "select rs.cd_rs,replace(replace(replace(substr(rs.ds_rs,1,50),chr(13),''),chr(10),' '),'  ',' ') ds_rs,rs.dt_inicio,nvl(pe.nm_pessoa_resumido, pe.nm_fantasia) nm_empresa,nvl(pc.nm_pessoa_resumido, nvl(trim(substr(pc.nm_pessoa,1,instr(pc.nm_pessoa,' ',1))),'não informado')) nm_solicitante,nvl(pp.nm_pessoa_resumido, nvl(trim(substr(pp.nm_pessoa,1,instr(pp.nm_pessoa,' ',1))),'não informado')) nm_atendente,decode(rs.cd_tipo_prioridade, 231, 'BAIXA', 232, 'MÉDIA', 233, 'ALTA', 234, 'CRÍTICA') nm_prioridade from repoman.rs_temppp rs,repoman.pessoa pe,repoman.pessoa pc,repoman.pessoa pp,repoman.rs_fluxo_temppp f1 where rs.cd_pessoa_empresa = pe.cd_pessoa and rs.cd_pessoa_solicitante = pc.cd_pessoa and f1.cd_pessoa_responsavel = pp.cd_pessoa and rs.cd_contrato is not null and (rs.cd_pessoa_responsavel, rs.cd_pessoa_solicitante) not in (select 2,2 from dual) and f1.cd_fluxo = (select max(cd_fluxo) from repoman.rs_fluxo_temppp f2 where f2.cd_rs = rs.cd_rs and cd_tipo_status in (33,210)) and not exists (select 1 from repoman.rs_fluxo_temppp f3 where f3.cd_rs = rs.cd_rs and f3.cd_tipo_status in (34,230,45,211)) and rs.cd_rs = f1.cd_rs order by rs.cd_tipo_prioridade desc"
def connecting_to_db():
    try:
        dsn_tns = cx_Oracle.makedsn('192.168.33.11','1521', service_name='sgrprod')
        conn = cx_Oracle.connect(user='bi', password='bi#2020#', dsn=dsn_tns)
    except cx_Oracle.DatabaseError:
        print('Banco de dados não encontrado, favor verifique sua conexão.')        
        sys.exit()          
    return conn.cursor()

def monta_tabela_chamadas_fechadas():
    query = query1
    cnxn = connecting_to_db() 
    cnxn.execute(query) 
    dados = cnxn.fetchall()
    lista_codigo_registro = []
    lista_descricao = []
    lista_data_inicio = [] 
    lista_data_final = []
    lista_ano = []
    lista_mes = []
    lista_empresa = []
    lista_solicitante = []
    lista_prioridade  = []
    dic = {}
    for dado in dados:
        lista_codigo_registro.append(dado[0])
        lista_descricao.append(dado[1])
        lista_data_inicio.append(dado[2])
        lista_data_final.append(dado[3])
        lista_ano.append(dado[4])
        lista_mes.append(dado[5])
        lista_empresa.append(dado[6])
        lista_solicitante.append(dado[7])
        lista_prioridade.append(dado[8])
    dic["codigo registro"] = lista_codigo_registro
    dic["descriçao"] = lista_descricao
    dic["data de inicio"] = lista_data_inicio
    dic["data de fim"] = lista_data_final
    dic["ano"] = lista_ano
    dic["mes"] = lista_mes
    dic["empresa"] = lista_empresa
    dic["solicitante"] = lista_solicitante
    dic["prioridade"] = lista_prioridade
    df = pd.DataFrame(dic)
    df["data de inicio(formato date)"] = df["data de inicio"].apply(lambda x: x.date())
    df["data de fim(formato date)"] = df["data de fim"].apply(lambda x: x.date())
    df = df.sort_values("data de fim(formato date)")
    df = df.reset_index(drop=True)
    cnxn.close()
    return df

def monta_tabela_atendimentos_nao_iniciados():
    query = query2
    cnxn = connecting_to_db()
    cnxn.execute(query)
    dados = cnxn.fetchall()
    lista_codigo_registro  = []
    lista_descricao = []
    lista_data_inicio  = []
    lista_empresa  = []
    lista_solicitante = []
    lista_atendente = []
    lista_prioridade = []
    for dado in dados:
        lista_codigo_registro.append(dado[0])
        lista_descricao.append(dado[1])
        lista_data_inicio.append(dado[2])
        lista_empresa.append(dado[3])
        lista_solicitante.append(dado[4])
        lista_atendente.append(dado[5])
        lista_prioridade.append(dado[6])
    dic = {}
    dic["codido registro"] = lista_codigo_registro
    dic["descricao"] = lista_descricao
    dic["data de solicitação"] = lista_data_inicio
    dic["empresa"] = lista_empresa
    dic["solicitante"] = lista_solicitante
    dic["atendente"] = lista_atendente
    dic["prioridade"] = lista_prioridade
    df = pd.DataFrame(dic)
    print(df.shape[0])
    df["data de solicitação"]  = df["data de solicitação"].apply(lambda x: x.date())
    cnxn.close()
    return df

    


def monta_tabela_chamadas_em_aberto():
    query = query3
    cnxn = connecting_to_db() 
    cnxn.execute(query)
    dados = cnxn.fetchall()
    lista_codigo_registro  = []
    lista_descricao = []
    lista_data_inicio  = []
    lista_empresa  = []
    lista_solicitante = []
    lista_atendente = []
    lista_prioridade = []
    for dado in dados:
        lista_codigo_registro.append(dado[0])
        lista_descricao.append(dado[1])
        lista_data_inicio.append(dado[2])
        lista_empresa.append(dado[3])
        lista_solicitante.append(dado[4])
        lista_atendente.append(dado[5])
        lista_prioridade.append(dado[6])
    dic = {}
    dic["codido registro"] = lista_codigo_registro
    dic["descricao"] = lista_descricao
    dic["data de inicio"] = lista_data_inicio
    dic["empresa"] = lista_empresa
    dic["solicitante"] = lista_solicitante
    dic["atendente"] = lista_atendente
    dic["prioridade"] = lista_prioridade
    df = pd.DataFrame(dic)
    df["data de inicio(date)"] = df["data de inicio"].apply(lambda x:x.date())
    df["mes"] = df["data de inicio(date)"].apply(lambda x :x.month)   
    df = df.sort_values("data de inicio(date)")
    df = df.reset_index(drop=True)
    cnxn.close()
    return df





