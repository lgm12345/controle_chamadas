import dash 
from dash import html,dcc,Input,Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import filtro
import datetime
from datetime import date,datetime

#intanciação do app
app = dash.Dash(__name__)
#leitura de dados com o arquivo que faz a filtragem no banco de dados
df_atendimentos_encerrados_ano = filtro.monta_tabela_chamadas_fechadas()
df_atendimentos_encerrados_store = df_atendimentos_encerrados_ano.to_dict()
df_atendimentos_nao_iniciados = filtro.monta_tabela_atendimentos_nao_iniciados()
df_atendimentos_nao_iniciados_store = df_atendimentos_nao_iniciados.to_dict()
df_atendimentos_em_andamento = filtro.monta_tabela_chamadas_em_aberto()
df_atendimentos_em_aberto_store = df_atendimentos_em_andamento.to_dict()
#variaveis auxiliares
clientes = df_atendimentos_encerrados_ano["empresa"].unique()
meses_nome = ["janeiro","fevereiro","março","abril","maio","junho","julho","agosto","setembro","outubro","novembro","dezembro"]


#instanciação do layout

app.layout = dbc.Container(children=[
    dcc.Store(id="df_encerrados",data=df_atendimentos_encerrados_store),
    dcc.Store(id="df_nao_iniciado",data=df_atendimentos_nao_iniciados_store),
    dcc.Store(id="df_em_aberto",data=df_atendimentos_em_aberto_store),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Img(id="logo-recours",src=app.get_asset_url("logo_recours.jpeg"),className="card-image")
                        ])
                    ])
                    ],width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H1("Dashbord de Chamadas")
                        ])
                    ])
                ],width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.P("Selecione o/os clientes"),
                            dcc.Dropdown(
                                id="select-cliente",
                                value=clientes[0],
                                options=clientes,
                                clearable=False,
                                multi=True
                            )
                        ])
                    ])
                ],width=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Legend("Selecione o intervalo de datas"),
                            dcc.DatePickerRange(
                                id="select-data",
                                start_date=date(2023,1,1),
                                end_date=datetime.now().date(),
                                min_date_allowed=date(2023,1,1),
                                max_date_allowed=datetime.now().date(),
                            )
                        ])
                    ])
                ])
            ],className="g-0"),
            dbc.Row([
                dbc.Col([
                   dbc.Row([
                       dbc.Col([
                           dbc.Card([
                               dbc.CardBody([
                                   html.H3("RS encerradas no periodo")
                               ])
                           ])
                       ],width=9),
                       dbc.Col([
                           dbc.Card([
                               dbc.CardBody([
                                   html.H5(id="rs-encerradas text",style={"color":"#adfc92"})
                               ])
                           ])
                       ],width=3)
                   ]),
                   dbc.Row([
                       dbc.Col([
                           dbc.Card([
                               dbc.CardBody([
                                   html.H3("RS nao iniciadas no periodo")
                               ])
                           ])
                       ],width=9),
                       dbc.Col([
                           dbc.Card([
                               dbc.CardBody([
                                   html.H3(id="rs-nao-iniciadas",style={"color": "#DF2935"})
                               ])
                           ])
                       ],width=3)
                   ]),
                   dbc.Row([
                       dbc.Col([
                           dbc.Card([
                               dbc.CardBody([
                                   html.H3("RS em aberto")
                               ])
                           ])
                       ],width=9),
                       dbc.Col([
                           dbc.Card([
                               dbc.CardBody([
                                   html.H3(id="rs-em-aberto-text",style={"color": "#389fd6"})
                               ])
                           ])
                       ],width=3)
                   ]),
                   dbc.Row([
                       dbc.Col([
                           dbc.Card([
                               dbc.CardBody([
                                   html.H3("Indice SLA")
                               ])
                           ])
                       ],width=9),
                       dbc.Col([
                           dbc.Card([
                               dbc.CardBody([
                                   html.H3(id="indice-sla")
                               ])
                           ])
                       ],width=3)
                   ])
                ]),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div(id="tabela-dbas")
                        ])
                    ])
                ],width=8)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            html.H4("Resumo mensal")
                        ]),
                        dbc.Col([
                            html.Span("Selecione o mês"),
                            dcc.Dropdown(
                                id="select-mes",
                                clearable="false",
                                value=meses_nome[0],
                                options=[{}]
                            )
                        ])
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Span("Total RS encerradas no mês"),
                                    html.H3(id="encerrados-no-mes")
                                ])
                            ])
                        ]),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Span("tempo médio para conclusão da RS"),
                                    html.H3(id="tempo-medio-mes-text")
                                ])
                            ])
                        ]) 
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Span("Total RS prioridade crítica"),
                                    html.H3(id="prioridade-critica-mes")
                                ])
                            ])
                        ]),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Span("Total RS prioridade alta"),
                                    html.H3(id="prioridade-alta-mes")
                                ])
                            ])
                        ]),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Span("Total prioridade média"),
                                    html.H3(id="prioridade-média-mes")
                                ])
                            ])
                        ]),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Span("Total prioridade baixa"),
                                    html.H3(id="priorioridade-baixa-mes")
                                ])
                            ])
                        ])
                    ])
                ]),
                dbc.Col([
                    dbc.Row([
                        html.H4("RS abertas e fechadas por mês")
                    ]),
                    dbc.Row([
                        dcc.Graph(id="graph")
                    ])
                ])
            ])
        ])
    ])
],fluid=True)


@app.callback(
    [Output(component_id="")]
    [Input(component_id="df_encerrados",component_property="data"),
     Input(component_id="df_nao_iniciado",component_property="data"),
     Input(component_id="df_em_aberto",component_property="data"),
     Input(component_id="select-data",component_property="start_date"),
     Input(component_id="select-data",component_property="end_date"),
     Input(component_id="select-cliente",component_property="value")]
)
#preciso montar a tabela a partir de um dataframe,e passar tudo isso dentro da divisão do html
def monta_tabela(dados_encerrado,dados_nao_iniciado,dados_em_aberto,data_inicio,data_final,clientes):
    df_encerrado = pd.DataFrame(dados_encerrado) 
    df_nao_iniciado =  pd.DataFrame(dados_nao_iniciado)
    df_em_aberto = pd.DataFrame(dados_em_aberto)
    df_encerrado_filt = df_encerrado[(df_encerrado["data de fim"] > data_inicio) & (df_encerrado["data de fim"] < data_final) & (df_encerrado["empresa"].isin(clientes))]
    df_nao_iniciado_filt = df_nao_iniciado[(df_nao_iniciado["data de solicitaçao"] > data_inicio) & (df_nao_iniciado["data de solicitaçao"] < data_final) & (df_nao_iniciado["empresa"].isin(clientes))]
    df_em_aberto_filt = df_em_aberto[(df_em_aberto["data de inicio"] > data_inicio) & (df_em_aberto["data de inicio"] < data_final) & (df_em_aberto["empresa"].isin(clientes))]
    total_encerrados = df_encerrado_filt.shape[0]
    total_nao_iniciados = df_nao_iniciado_filt.shape[0]
    total_em_aberto = df_em_aberto_filt.shape[0]
    sla = (total_encerrados + total_em_aberto) / (total_encerrados + total_nao_iniciados + total_em_aberto)
    return(str(total_encerrados),str(total_nao_iniciados),str(total_em_aberto),str(sla))
    


@app.callback(
        Output(component_id="tabela-dbas",component_property="children"),
        [Input(component_id="df_encerrados",component_property="data"),
         Input(component_id="df_nao_iniciado",component_property="data"),
         Input(component_id="df_em_aberto",component_property="data"),
         Input(component_id="select-data",component_property="start_date"),
         Input(component_id="select-data",component_property="end_date"),
         Input(component_id="select-cliente",component_property="value")],
)



def monta_tabelas_dba(dados_encerrado,dados_nao_iniciado,dados_em_aberto,data_inicial,data_final,clientes):
    df_encerrados = pd.DataFrame(dados_encerrado)
    df_nao_iniciado = pd.DataFrame(dados_nao_iniciado)
    df_em_aberto = pd.DataFrame(dados_em_aberto)
    df_encerrados_filt = df_encerrados[(df_encerrados["data de fim"] > data_inicial) & (df_encerrados["data de fim"] < data_final) & (df_encerrados["empresa"].isin(clientes))]
    df_nao_iniciado_filt = df_nao_iniciado[(df_nao_iniciado["data de solicitacao"]) & (df_nao_iniciado["data de solicitacao"] < data_final) & (df_nao_iniciado["empresa"].isin(clientes))]
    df_em_aberto_filt = df_em_aberto[(df_em_aberto["data de inicio"] > data_inicial) & (df_em_aberto["data de inicio"] < data_final) & (df_em_aberto["empresa"].isin(clientes))]
    lista_dbas = df_encerrados["atendente"].unique()
    atendente = []
    encerrados = []
    nao_iniciados  = []
    em_aberto = []
    for dba in lista_dbas:
       atendente.append(dba)
       encerrados.append(df_encerrados_filt[df_encerrados_filt["atendente"] == dba].shape[0])
       nao_iniciados.append(df_nao_iniciado_filt[df_nao_iniciado_filt["atendente"] == dba].shape[0])
       em_aberto.append(df_em_aberto_filt[df_em_aberto_filt["atendente"] == dba].shape[0])
    df = pd.DataFrame({"DBA":atendente,"RS_ENCERRADAS":encerrados,"RS_NAO_INICIADO":nao_iniciados,"RS_EM_ABERTO":em_aberto})
    children=[
        dbc.Table.from_dataframe(df,bordered=True,striped=True,hover=True)    
    ]
    return children

@app.callback(
        [Output(component_id="encerrados-no-mes",component_property="children"),
         Output(component_id="tempo-medio-mes-text",component_property="children"),
         Output(component_id="prioridade-alta-mes",component_property="children"),
         Output(component_id="prioridade-media-mes",component_property="children"),
         Output(component_id="prioridade-baixa-mes",component_property="children")],
        [Input(component_id="df_encerrados",component_property="data"),
        Input(component_id="select-mes",component_property="value"),
        Input(component_id="select-cliente",component_property="value")],
)

def monta_resumo(dados_encerrado,mes,clientes):
    df_encerrado = pd.DataFrame(dados_encerrado)
    if (type(clientes) == str):
        df_encerrado_filt = df_encerrado[(df_encerrado["mes"] == mes) & (df_encerrado["empresa"].isin([clientes]))]
    else :
        df_encerrado_filt = df_encerrado[(df_encerrado["mes"] == mes) & (df_encerrado["empresa"].isin(clientes))]
    prioridade_critica = df_encerrado_filt[df_encerrado_filt["prioridade"] == "CRÍTICA"].shape[0]
    prioridade_alta = df_encerrado_filt[df_encerrado_filt["prioridade"] == "ALTA"].shape[0]
    prioridade_media = df_encerrado_filt[df_encerrado_filt["prioridade"] == "MÉDIA"].shape[0]
    prioridade_baixa = df_encerrado_filt[df_encerrado_filt["prioridade"] == "BAIXA"].shape[0]
    encerrados_no_mes = df_encerrado_filt.shape[0]
    tempo_medio = 0
    for index in df_encerrado_filt.index:
        duracao = df_encerrado_filt["data de fim(formato date)"][index] - df_encerrado_filt["data de inicio(formato date)"][index]
        duracao_segundos = duracao.total_seconds()
        tempo_medio = tempo_medio + duracao_segundos
    tempo_medio = tempo_medio / df_encerrado_filt.index.size
    total_dias = tempo_medio.days
    total_horas = tempo_medio//3600
    total_minutos = tempo_medio % 3600 // 60
    if (total_dias != 0):
        tempo = f'duracao média {total_dias} dias {total_horas} horas e {total_minutos} minutos'
    return (str(encerrados_no_mes),str(tempo),str(prioridade_alta),str(prioridade_critica),str(prioridade_media),str(prioridade_baixa))


@app.callback(
    Output(component_id="fechados-aberto-graph",component_property="figure"),
    [Input(component_id="df_encerrados",component_property="data"),
     Input(component_id="df_em_aberto",component_property="data"),
     Input(component_id="select-cliente",component_property="value")]
)


def monta_grafico(dados_encerrado,dados_aberto,clientes):
    mes_atual = datetime.now().date().month
    meses = df_encerrado["mes"].unique()
    df_encerrado = pd.DataFrame(dados_encerrado)
    df_em_aberto = pd.DataFrame(dados_aberto)
    df_encerrado_filt = df_encerrado[df_encerrado["empresa"].isin(clientes) == True]
    df_em_aberto_filt = df_em_aberto[df_em_aberto["empresa"].isin(clientes) == True]
    encerrados_no_mes = []
    abertos_no_mes = []
    for mes in meses:
        if (mes <= mes_atual):
            encerrados = df_encerrado_filt[df_encerrado_filt["mes"] == mes].shape[0]
            abertos = df_em_aberto_filt[df_em_aberto_filt["mes"] == mes].shape[0]
            encerrados_no_mes.append(encerrados)
            abertos_no_mes.append(abertos)
    dic = {"mes":meses,"encerrados":encerrados_no_mes,"abertos":abertos_no_mes}
    dic_mes_nome = {1:"janeiro",2:"fevereiro",3:"março",4:"abril",5:"maio",6:"junho",7:"julho",8:"agosto",9:"setembro",10:"outubro",11:"novembro",12:"dezembro"}
    df["mes"] = df["mes"].map(dic_mes_nome)
    df = pd.DataFrame(dic)
    df["mes"] = df["mes"].map(dic_mes_nome)
    fig = px.bar(df,x="mes",y=["encerrados","abertos"],title="RS encerradas e abertas por mês")
    return fig 



if __name__ == "__main__":
    app.run_server(debug=True)