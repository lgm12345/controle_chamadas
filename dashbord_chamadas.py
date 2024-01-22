import dash 
from dash import html,dcc,Input,Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import filtro
import datetime
from datetime import date,datetime
import json

#intanciação do app
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.FLATLY])
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
meses = [1,2,3,4,5,6,7,8,8,9,10,11,12]

#montagem do layout frame a frame

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
                            html.Img(id="logo-recours",src=app.get_asset_url("logo_recours.png"),className="card-image")
                        ])
                    ])
                ],md=1),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("Dashbord de Chamadas encerradas,não iniciadas e abertas",style={"font-size":"23px"})
                        ],style={"height":"20vh"})
                    ])
                ],md=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.P("Selecione o/os clientes",style={"font-size":"25px"}),
                            dcc.Dropdown(
                                id="select-cliente",
                                value=[clientes[7],clientes[3],clientes[4]],
                                options=clientes,
                                clearable=False,
                                multi=True,
                                style={"font-size":"12px","margin-top":"-15px"}
                            )
                        ],style={"height":"20vh"})
                    ])
                ],md=4),
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
                        ],style={"height":"20vh"})
                    ])
                ],md=4)
            ],className="g-0"),
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Col([ 
                            dbc.Card([
                                dbc.CardBody([
                                    html.H5("RS encerradas no periodo selecionado")
                                ])
                            ],style={"height":"8vh"})
                        ],md=9),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H3(id="rs-encerradas text",style={"color":"#adfc92","text-align":"center"})
                                ])
                            ],style={"height":"8vh"})
                        ],md=3)
                    ],className="g-0"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H5("RS no iniciadas no periodo selecionado")
                                ])
                            ],style={"height":"8vh"})
                        ],md=9),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H3(id="rs-nao-iniciadas",style={"color": "#DF2935","text-align":"center","padding-bottom":"5px"})
                                ])
                            ],style={"height":"8vh"})
                        ])
                    ],className="g-0"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H5("RS abertas durante o periodo selecionado")
                                ])
                            ],style={"height":"8vh"})
                        ],md=9),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H3(id="rs-em-aberto-text",style={"color": "#389fd6","text-align":"center","font-size":"35px"})
                                ])
                            ],style={"height":"8vh"})
                        ],md=3)
                    ],className="g-0"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H5("Indice SLA")
                                ])
                            ],style={"height":"8vh"})
                        ],md=9),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H3(id="indice-sla",style={"text-align":"center"})
                                ])
                            ],style={"height":"8vh"})
                        ],md=3)
                    ],className="g-0")
                ],md=5),
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Tabela de atendimentos em aberto DBA"),
                        dbc.CardBody([
                            html.Div(id="tabela-dbas")
                        ])
                    ])
                ],md=7)
            ],className="g-0"),
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Card([
                            dbc.CardBody([
                                dbc.Col([
                                    html.H4("Resumo mensal")
                                ]),
                                dbc.Col([
                                    html.Span("Selecione o mês"),
                                    dcc.Dropdown(
                                    id="select-mes",
                                    clearable=False,
                                    value=meses[4],
                                    options=[
                                        {"label":1,"value":1},
                                        {"label":2,"value":2},
                                        {"label":3,"value":3},
                                        {"label":4,"value":4},
                                        {"label":5,"value":5},
                                        {"label":6,"value":6},
                                        {"label":7,"value":7},
                                        {"label":8,"value":8},
                                        {"label":9,"value":9},
                                        {"label":10,"value":10},
                                        {"label":11,"value":11},
                                        {"label":12,"value":12}
                                    ]
                                    )
                            ])
                            ])
                        ])
                        ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Span("Total RS encerradas no mês:"),
                                    html.H3(id="encerrados-no-mes",style={"text-align":"center"})
                                ])
                            ])
                        ]),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Span("Tempo médio para conclusão da RS:"),
                                    html.H3(id="tempo-medio-mes-text",style={"font-size":"15px","text-align":"center"})
                                ])
                            ])
                        ]),
                    ],className="g-0"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Span("Total RS prioridade crítica:",style={"font-size":"15px"}),
                                    html.H3(id="prioridade-critica-mes",style={"text-align":"center","color":"#8B0000"})
                                ])
                            ])
                        ]),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Span("Total RS prioridade alta:"),
                                    html.H3(id="prioridade-alta-mes",style={"text-align":"center","color":"#FF0000"})
                                ])
                            ])
                        ]),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Span("Total prioridade média:"),
                                    html.H3(id="prioridade-média-mes",style={"text-align":"center","color":"#006400"})
                                ])
                            ])
                        ]),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.Span("Total prioridade baixa:"),
                                    html.H3(id="prioridade-baixa-mes",style={"text-align":"center","color": "#389fd6"})
                                ])
                            ])
                        ])
                    ],className="g-0")
                ]),
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id="graph")
                        ])
                    ])
                ])
            ])
        ])
    ])
],fluid=True)

@app.callback(
    [Output(component_id="rs-encerradas text",component_property="children"),
     Output(component_id="rs-nao-iniciadas",component_property="children"),
     Output(component_id="rs-em-aberto-text",component_property="children"),
     Output(component_id="indice-sla",component_property="children")],
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
    if df_encerrado.shape[0] != 0:
        if type(clientes) == str:
           df_encerrado = df_encerrado[(df_encerrado["data de fim"] > data_inicio) & (df_encerrado["data de fim"] < data_final) & (df_encerrado["empresa"].isin([clientes]))]
        else:
           df_encerrado = df_encerrado[(df_encerrado["data de fim"] > data_inicio) & (df_encerrado["data de fim"] < data_final) & (df_encerrado["empresa"].isin(clientes))]
    if df_nao_iniciado.shape[0] != 0:
        if type(clientes) == str:
            df_nao_iniciado = df_nao_iniciado[(df_nao_iniciado["data de solicitação"] > data_inicio) & (df_nao_iniciado["data de solicitação"] < data_final) & (df_nao_iniciado["empresa"].isin([clientes]))]
        else:
            df_nao_iniciado = df_nao_iniciado[(df_nao_iniciado["data de solicitação"] > data_inicio) & (df_nao_iniciado["data de solicitação"] < data_final) & (df_nao_iniciado["empresa"].isin(clientes))]
    if df_em_aberto.shape[0] != 0:
        if type(clientes) == str:
            df_em_aberto = df_em_aberto[(df_em_aberto["data de inicio"] > data_inicio) & (df_em_aberto["data de inicio"] < data_final) & (df_em_aberto["empresa"].isin([clientes]))]
        else:
            df_em_aberto = df_em_aberto[(df_em_aberto["data de inicio"] > data_inicio) & (df_em_aberto["data de inicio"] < data_final) & (df_em_aberto["empresa"].isin(clientes))]
    total_encerrados = df_encerrado.shape[0]
    total_nao_iniciados = df_nao_iniciado.shape[0]
    total_em_aberto = df_em_aberto.shape[0]
    sla = (total_encerrados + total_em_aberto) / (total_encerrados + total_nao_iniciados + total_em_aberto)
    sla_round = round(sla,2)
    return(str(total_encerrados),str(total_nao_iniciados),str(total_em_aberto),str(sla_round))

@app.callback(
        Output(component_id="tabela-dbas",component_property="children"),
        [Input(component_id="df_em_aberto",component_property="data"),
         Input(component_id="select-data",component_property="start_date"),
         Input(component_id="select-data",component_property="end_date"),
         Input(component_id="select-cliente",component_property="value")],
)



def monta_tabelas_dba(dados_em_aberto,data_inicial,data_final,clientes):
    df_em_aberto = pd.DataFrame(dados_em_aberto)
    if (df_em_aberto.shape[0] != 0):
        if (type(clientes) == str):
            df_em_aberto = df_em_aberto[(df_em_aberto["data de inicio"] > data_inicial) & (df_em_aberto["data de inicio"] < data_final) & (df_em_aberto["empresa"].isin([clientes]))]
        else:
            df_em_aberto = df_em_aberto[(df_em_aberto["data de inicio"] > data_inicial) & (df_em_aberto["data de inicio"] < data_final) & (df_em_aberto["empresa"].isin(clientes))]
    lista_dbas = df_em_aberto["atendente"].unique()
    atendente = []
    em_aberto = []
    prioridade_critica = []
    prioridade_alta = []
    prioridade_media = []
    prioridade_baixa = []
    for dba in lista_dbas:
        atendente.append(dba)
        if (df_em_aberto[df_em_aberto["atendente"] == dba].shape[0] == 0):
            em_aberto.append(0)
            prioridade_critica.append(0)
            prioridade_alta.append(0)
            prioridade_media.append(0)
            prioridade_baixa.append(0)
        else:
            df_encerrados_dba = df_em_aberto[df_em_aberto["atendente"] == dba]
            em_aberto.append(df_encerrados_dba.shape[0])
            prioridade_critica.append(df_encerrados_dba[df_encerrados_dba["prioridade"] == "CRÍTICA"].shape[0])
            prioridade_alta.append(df_encerrados_dba[df_encerrados_dba["prioridade"] == "ALTA"].shape[0])
            prioridade_media.append(df_encerrados_dba[df_encerrados_dba["prioridade"] == "MÉDIA"].shape[0])
            prioridade_baixa.append(df_encerrados_dba[df_encerrados_dba["prioridade"] == "BAIXA"].shape[0])
    df = pd.DataFrame({"DBA":atendente,"RS_EM_ABERTO":em_aberto,"PRIORIDADE CRITICA":prioridade_critica,"PRIORIDADE ALTA":prioridade_alta,"PRIORIDADE MÉDIA":prioridade_media,"PRIORIDADE BAIXA":prioridade_baixa})
    #anted de passar para o dbc.Table preciso converter o df em um JSON seriavel,por exexemplo um dicionario
    df["RS_EM_ABERTO"] = df["RS_EM_ABERTO"].astype(int)
    df["PRIORIDADE CRITICA"] = df["PRIORIDADE CRITICA"].astype(int)
    df["PRIORIDADE ALTA"] = df["PRIORIDADE ALTA"].astype(int)
    df["PRIORIDADE MÉDIA"] = df["PRIORIDADE MÉDIA"].astype(int)
    df["PRIORIDADE BAIXA"] = df["PRIORIDADE BAIXA"].astype(int)
    children = dbc.Table.from_dataframe(df,bordered=True,striped=True,hover=True)
    return children


@app.callback(
        [Output(component_id="encerrados-no-mes",component_property="children"),
         Output(component_id="tempo-medio-mes-text",component_property="children"),
         Output(component_id="prioridade-critica-mes",component_property="children"),
         Output(component_id="prioridade-alta-mes",component_property="children"),
         Output(component_id="prioridade-média-mes",component_property="children"),
         Output(component_id="prioridade-baixa-mes",component_property="children")],
        [Input(component_id="df_encerrados",component_property="data"),
        Input(component_id="select-mes",component_property="value"),
        Input(component_id="select-cliente",component_property="value")],
)

def monta_resumo(dados_encerrado,mes,clientes):
    df_encerrado = pd.DataFrame(dados_encerrado)
    if (type(clientes) == str):
        df_encerrado_filt = df_encerrado[(df_encerrado["mes"] == int(mes)) & (df_encerrado["empresa"].isin([clientes]))]
    else :
        df_encerrado_filt = df_encerrado[(df_encerrado["mes"] == int(mes)) & (df_encerrado["empresa"].isin(clientes))]
    prioridade_critica = df_encerrado_filt[df_encerrado_filt["prioridade"] == "CRÍTICA"].shape[0]
    prioridade_alta = df_encerrado_filt[df_encerrado_filt["prioridade"] == "ALTA"].shape[0]
    prioridade_media = df_encerrado_filt[df_encerrado_filt["prioridade"] == "MÉDIA"].shape[0]
    prioridade_baixa = df_encerrado_filt[df_encerrado_filt["prioridade"] == "BAIXA"].shape[0]
    encerrados_no_mes = df_encerrado_filt.shape[0]
    tempo_medio = 0
    df_encerrado_filt["data de fim"] = pd.to_datetime(df_encerrado_filt["data de fim"])
    df_encerrado_filt["data de inicio"] = pd.to_datetime(df_encerrado_filt["data de inicio"])
    for index in df_encerrado_filt.index:
        duracao = df_encerrado_filt["data de fim"][index] - df_encerrado_filt["data de inicio"][index]
        duracao_segundos = duracao.total_seconds()
        tempo_medio = tempo_medio + duracao_segundos
    tempo_medio = tempo_medio / encerrados_no_mes
    total_dias = tempo_medio//86400
    total_horas = (tempo_medio % 86400) //3600
    total_minutos = tempo_medio % 3600 // 60
    if (total_dias != 0):
        tempo = f'Duracao média {total_dias} dias {total_horas} horas e {total_minutos} minutos'
    return (str(encerrados_no_mes),str(tempo),str(prioridade_alta),str(prioridade_critica),str(prioridade_media),str(prioridade_baixa))



@app.callback(
    Output(component_id="graph",component_property="figure"),
    [Input(component_id="df_encerrados",component_property="data"),
     Input(component_id="df_em_aberto",component_property="data"),
     Input(component_id="select-cliente",component_property="value")]
)


def monta_grafico(dados_encerrado,dados_aberto,clientes):
    mes_atual = datetime.now().date().month
    df_encerrado = pd.DataFrame(dados_encerrado)
    df_em_aberto = pd.DataFrame(dados_aberto)
    meses = df_encerrado["mes"].unique()
    if type(clientes) == str:
        df_encerrado_filt = df_encerrado[df_encerrado["empresa"].isin([clientes]) == True]
        df_em_aberto_filt = df_em_aberto[df_em_aberto["empresa"].isin([clientes]) == True]
    else :
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
    df = pd.DataFrame(dic)
    df["mes"] = df["mes"].map(dic_mes_nome)
    fig = px.bar(df,x="mes",y=["encerrados","abertos"],title="RS encerradas e abertas por mês")
    return fig 

if __name__ == "__main__":
    app.run_server(debug=True)