#librerías
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
#import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

#dataframes
Salarios_vs_FEES_df = pd.read_csv('Total_Salarios_vs_FEES_anual.csv')
Top5_bechas_2022_df = pd.read_csv('Mediana_Max_2022.csv')
Planilla_UCR_2015_2023_df = pd.read_csv('Planilla_UCR_Final_2015_2023.csv')
Salarios_vs_Antiguedad_df = pd.read_csv('Max_Años_servicio_2022.csv')
Sunburst_df = pd.read_csv('Sunburst_2022.csv')

#app
app = dash.Dash(__name__)

server = app.server #Linea requerida para desplegar la app en render.com

app.layout = html.Div([
    #************************************css************************************
    #html.Link(rel='stylesheet', href='dashboard.css'),
    #leyendo la documentación me di cuenta que no es necesaria esta linea siempre y cuando hagas una carpeta llamada assets y ahí se añadiran todos los css y js que estén dentro de esa carpeta

    #************************************Banner************************************
    html.Div([#0
        html.H1('Planilla UCR (Enero 2015 - Mayo 2023)'),
        html.Div([html.Img(src='https://www.ucr.ac.cr/vistas/webucr_ucr_5/imagenes/firma-ucr-c.svg')]),
    ], className = 'banner'),

    #************************************Intro con graficos estáticos************************************
    html.Div([#1
        html.P("""¡Bienvenido al Dashboard de Análisis de Gastos en Salarios de la Universidad de Costa Rica! 
               Aquí podrá explorar visualmente cómo la universidad asigna sus recursos a los salarios de su personal. 
               Comenzaré con dos gráficos estáticos que le ofrecerán una vista general de los gastos en salarios y las brechas salariales más notables. 
               Luego, podrá sumergirse en los detalles con gráficos dinámicos que le permitirán ajustar los filtros de año, mes y puesto para una comprensión más profunda.""")
    ], className='introduccion'),

    html.Div([#2
        html.Div([
            dcc.Graph(id = "barras_planilla_vs_fees")
        ], className='barras_planilla_vs_fees'),

        html.Div([
            html.P("""En este primer gráfico, muestro cómo se distribuyen los recursos financieros de la Universidad de Costa Rica. 
                   Observe cómo el porcentaje de gastos en salarios en relación con el presupuesto Puesto refleja el compromiso de la universidad con su personal. 
                   Con un promedio del 52% del presupuesto total destinado a salarios, esta visualización te ayudará a comprender la importancia que la universidad otorga a su equipo.""")
        ], className= 'p_planilla_vs_fees')
    ], className= 'container_planilla_vs_fees'),

    html.Div([#3
        html.Div([
            dcc.Graph(id = "barras_max_vs_mediana")
        ], className='barras_max_vs_mediana'),

        html.Div([
            html.P("""Explore este segundo gráfico para descubrir los puestos de trabajo en la Universidad de Costa Rica con las brechas salariales más significativas. 
                   Identifiqué los cinco puestos con diferencias salariales notables entre el salario del percentil 50 y el salario máximo. 
                   Verá cómo algunas posiciones experimentan variaciones considerables en sus compensaciones, lo cual podrá observar más adelante que una buena parte de estas desigualdades pueden ser debido a los años de servicio.
                   Esta visualización arrojará luz sobre las dinámicas salariales dentro de la universidad y le permitirá reflexionar sobre otras posibles razones detrás de estas diferencias""")
        ], className= 'p_max_vs_mediana')
    ], className= 'container_max_vs_mediana'),
    
    #************************************Principales graficos dinámicos, los 3 comparten los mismos filtros************************************
    html.Hr(),#4
    #Primero los filtros
    html.Div([#5
        html.Div([
            html.P('Panel de filtros'),
        ], className= 'panel_filtros_title'),

        html.Div([
            html.P('Puesto:'),
            dcc.Dropdown(id='dropdown-puesto',
                 options=[{'label': puesto, 'value': puesto} for puesto in Planilla_UCR_2015_2023_df['PUESTO_SIMPLIFICADO'].unique()],
                 value='PROFESOR CATEDRATICO',
                 multi=False)
        ], className= 'panel_filtros_dropdown'),

        html.Div([
            html.P('Año:'),
            dcc.Checklist(id="checklist-años",
                options=[{'label': str(año), 'value': año} for año in range(2015, 2024)],
                value=[2022],
                inline=True),

        ], className= 'panel_filtros_chk_year'),

        html.Div([
            html.P('Mes:'),
            dcc.Checklist(id="checklist-meses",
                options=[{'label': str(mes), 'value': mes} for mes in range(1, 13)],
                value=[12],
                inline=True),
        ], className= 'panel_filtros_chk_mes')
    ], className= 'panel_filtros_container'),
    #Segundo los graficos
    html.Div([#6
        html.Div([
            dcc.Graph(id="grafico-dona")
        ], className='dona'),

        html.Div([
            dcc.Graph(id="grafico-histograma")
        ], className='histograma'),

        html.Div([
            dcc.Graph(id="grafico-circular")
        ], className='circulo')
    ], className='graficos_principales'),

    #************************************Conclusión con grafico de puntos, sunburst y un parrafo************************************
    html.Hr(),#7
    html.Div([#8
        html.Div([
            html.P("""La siguiente visualización da una reveladora perspectiva que he construido sobre la influencia de la antigüedad en los salarios de los empleados en la Universidad de Costa Rica durante el año 2022. 
                       A través de un gráfico de línea, podrá explorar cómo la experiencia acumulada a lo largo de los años impacta en la compensación recibida por los trabajadores de un mismo puesto. 
                       He creado un filtro interactivo que le permitirá seleccionar diferentes puestos y, así, observar cómo en algunos roles la antigüedad se convierte en un factor crucial que influye en las diferencias salariales. 
                       """),
            ], className='p_linea'),

        html.Div([
            html.P('Filtro de puesto:'),
            dcc.Dropdown(id='dropdown-puesto2',
                 options=[{'label': puesto, 'value': puesto} for puesto in Salarios_vs_Antiguedad_df['PUESTO_SIMPLIFICADO'].unique()],
                 value='PROFESOR CATEDRATICO',
                 multi=False),
            dcc.Graph(id="grafico-puntos")    
            ], className='grafico_linea'),
    ], className='container_linea'),

    html.Div([#9
        html.P(["""El gráfico Sunburst que presento proporciona una representación visual única de la compleja estructura de puestos de trabajo en la Universidad de Costa Rica durante el año 2022. 
               Dada la diversidad y amplitud de roles, he realizado una agrupación adicional de los puestos (repesentada en el anillo interno) para mejorar la legibilidad de los gráficos. 
               En un esfuerzo por simplificar y resaltar patrones clave, he creado una jerarquía de tres niveles (2 realizados por la UCR) que muestra categorías amplias de puestos, subcategorías y roles individuales. 
               Esta enriquecedora visualización, basada exclusivamente en los datos del 2022, le permitirá explorar cómo los puestos se agrupan y comparten similitudes, lo que brinda una perspectiva más clara de la distribución laboral en la universidad. 
               Al exhibir esta estructura de agrupación, deseo compartir con usted el esfuerzo detrás de la simplificación de datos y cómo esto contribuye a una experiencia de visualización más enriquecedora y comprensible.""",
               html.Br(),html.Br(),
               'Nota: Los valores del grafico corresponden a la suma de salarios pagados durante todo el 2022 por lo que no deben de interpresarse como cantidad de funcionarios.',
               html.Br(),html.Br(),
               """Siéntase libre de hacer click en la agrupación que desee mirar con más detalle."""]),
    
        html.Div([
            dcc.Graph(id = "grafico-sunburst")
        ], className= 'grafico_sunburst')
    ], className='container_sunburst'),

    html.Hr(),
    html.Div([
        html.P([
            """Este dashboard fue desarrollado por """, html.A('Jason Umaña Mata', href='https://linkedin.com/in/jasonu95', target='_blank'), 
            """ como parte de un proyecto independiente de análisis de datos sobre los gastos en salarios de la Universidad de Costa Rica. 
            Las visualizaciones y la interactividad fueron implementadas utilizando la librería Dash de Python. """
        ]),

        html.P([
            'Fuente de datos de planillas: ',
            html.A('https://transparencia.ucr.ac.cr/', href='https://transparencia.ucr.ac.cr/informacion-institucional/recursos-humanos/planillas/pagina-1.html', target='_blank')
        ]),

        html.P([
            'Fuente de datos de montos del FEES: ',
            html.A('https://siesue.conare.ac.cr/', href='https://siesue.conare.ac.cr/wp-content/uploads/2023/07/distribucion_FEES_2010_2023.pdf', target='_blank')
        ]),
    ], className= 'footer')
])

#************************************Colocar graficos estáticos************************************
#Creación del gráfico de barras 1
#Puesto_salarios_fees = px.bar(Salarios_vs_FEES_df, x='Año', y=['SALARIO', 'FEES'], title= 'Monto total de salarios vs presupuesto del FEES para la UCR')
trace1 = go.Bar(
    x=Salarios_vs_FEES_df['Año'],
    y=Salarios_vs_FEES_df['SALARIO'],
    hovertext=['52.75% del FEES','52.51% del FEES','50.96% del FEES','52.05% del FEES','53.87% del FEES','56.78% del FEES','52.53% del FEES','48.93% del FEES','20.19% del FEES (Hasta mayo)'],
    marker_color='rgb(65,173,231)',
    name='Salarios',
    showlegend= False
)

trace2 = go.Bar(
    x=Salarios_vs_FEES_df['Año'],
    y=Salarios_vs_FEES_df['FEES'],
    marker_color='rgb(144,196,226)',
    name='UCR_FEES', 
    showlegend= False
)

layout = go.Layout(
    title='Monto total de salarios vs presupuesto del FEES para la UCR',
    title_x=0.5,
    xaxis=dict(title=''),
    yaxis=dict(title='Billones en colones costarricenses'),
    barmode='overlay'
)

Puesto_salarios_fees = go.Figure(data=[trace2, trace1], layout=layout)
#Colocar grafico 1
app.layout.children[2].children[0].children[0].figure = Puesto_salarios_fees

#Creación del gráfico de barras 2
#brecha_mediana_max = px.bar(Top5_bechas_2022_df, x='PUESTO_SIMPLIFICADO', y=['MEDIANA', 'MAXIMO'], title= 'Top 5 puestos con las mayores brechas entre maximo y mediana en el 2022')
trace1 = go.Bar(
    x=Top5_bechas_2022_df['PUESTO_SIMPLIFICADO'],
    y=Top5_bechas_2022_df['MEDIANA'],
    marker_color='rgb(65,173,231)',
    name='Mediana',
    showlegend= False
)

trace2 = go.Bar(
    x=Top5_bechas_2022_df['PUESTO_SIMPLIFICADO'],
    y=Top5_bechas_2022_df['MAXIMO'],
    hovertext=['18.64 veces la mediana', '2.39 veces la mediana', '2.39 veces la mediana', '1.74 veces la mediana', '1.73 veces la mediana'],
    marker_color='rgb(144,196,226)',
    name='Máximo', 
    showlegend= False
)

layout = go.Layout(
    title='Diferencias salariales absolutas mas grandes del 2022',
    title_x=0.5,
    xaxis=dict(title=''),
    yaxis=dict(title='Colones costarricenses'),
    barmode='overlay'
)

brecha_mediana_max = go.Figure(data=[trace2, trace1], layout=layout)
#Colocar grafico 2
app.layout.children[3].children[0].children[0].figure = brecha_mediana_max

#Creación del Sunburst
levels = ['CARGO ADMINISTRATIVO', 'PUESTO', 'PUESTO_SIMPLIFICADO'] # niveles de jerarquía (de menos a más importantes)
value_column = 'CONTEO'

def build_hierarchical_dataframe(df, levels, value_column):
    df_all_trees = pd.DataFrame(columns=['id', 'parent', 'value'])
    for i, level in enumerate(levels):
        df_tree = pd.DataFrame(columns=['id', 'parent', 'value'])
        dfg = df.groupby(levels[i:]).sum()
        dfg = dfg.reset_index()
        df_tree['id'] = dfg[level].copy()
        if i < len(levels) - 1:
            df_tree['parent'] = dfg[levels[i+1]].copy()
        else:
            df_tree['parent'] = 'Puesto'
        df_tree['value'] = dfg[value_column]
        df_all_trees = pd.concat([df_all_trees,df_tree],ignore_index=True)
    Puesto = pd.Series(dict(id='Puesto', parent='',
                              value=df[value_column].sum()
                              ))
    df_all_trees = pd.concat([df_all_trees,Puesto], ignore_index=True)
    return df_all_trees

#Sunburst_df = Sunburst_df.fillna(" ")
df_all_trees = build_hierarchical_dataframe(Sunburst_df, levels, value_column)
# Crear la figura de Sunburst utilizando los datos del DataFrame
sun = go.Figure(go.Sunburst(
    labels=df_all_trees['id'],
    parents=df_all_trees['parent'],
    values=df_all_trees['value'],
    branchvalues="total",
))
sun.update_layout(margin = dict(t=0, l=0, r=0, b=0))
#Colocar sunburst
app.layout.children[9].children[1].children[0].figure = sun


#************************************Graficos dinámicos principales************************************
#Callback para los graficos dinámicos
@app.callback(
    [Output("grafico-dona", "figure"),
     Output("grafico-histograma", "figure"),
     Output("grafico-circular", "figure")],

    [Input("dropdown-puesto", "value"),
     Input("checklist-años", "value"),
     Input("checklist-meses", "value")]
)
def actualizar_graficos(puesto_seleccionado, años_seleccionados, meses_seleccionados):

    #filtrar año(s)
    df_filtrado = Planilla_UCR_2015_2023_df[Planilla_UCR_2015_2023_df['Año'].isin(años_seleccionados)]

    #Filtrar mes(es)
    df_filtrado = df_filtrado[df_filtrado['Mes'].isin(meses_seleccionados)]

    #filtrar puesto
    df_filtrado = df_filtrado[df_filtrado['PUESTO_SIMPLIFICADO'] == puesto_seleccionado]

    #Crear graficos
    #************************************DONA************************************
    Puesto_trabajadores = len(df_filtrado)
    #trabajadores_incompletos = df_filtrado['MES COMPLETO'].notna().sum()
    trabajadores_completos = (df_filtrado['MES COMPLETO'].str.isspace()).sum()
    porcentaje_completos = (trabajadores_completos / Puesto_trabajadores) * 100
    dona = go.Figure(go.Pie(
        labels=['Mes completo', 'Mes incompleto'],
        values=[porcentaje_completos, 100 - porcentaje_completos],
        hole=0.4,  # Agujero para crear un donut chart
        #hoverinfo='label+percent',
        textinfo='label+percent',
        showlegend= False,
        textfont_size=12,
        marker_colors = ['rgb(144,196,226)', 'rgb(65,173,231)']
    ))
    dona.update_layout(
        title=f'¿{puesto_seleccionado.capitalize()} trabajó todo el mes?',
        title_font_size=14,
        title_x=0.5
    )
    #************************************HISTOGRAMA************************************
    histograma = go.Figure(data=[go.Histogram(x=df_filtrado['SALARIO'],
                                              name= 'Rango salarial',
                                              marker_color = '#41ade7')])
    histograma.update_layout(
        title_text = f'Distribución de Salarios para {puesto_seleccionado.capitalize()}',
        title_font_size=14,
        title_x=0.5,
        yaxis_title_text='Cantidad de asalariados',
        xaxis_title_text='Salario en Colones Costarricenses',
        xaxis_title_font_size=12,
        yaxis_title_font_size=12,
        bargap=0.2
    )
    #************************************CIRCULAR************************************
    #Calcular el porcentaje de cada categoría
    porcentaje_completa = (df_filtrado['Categoria'] == 'Jornada completa').sum() / Puesto_trabajadores * 100
    porcentaje_parcial = (df_filtrado['Categoria'] == 'Jornada parcial').sum() / Puesto_trabajadores * 100
    porcentaje_extra = (df_filtrado['Categoria'] == 'Jornada con tiempo extra').sum() / Puesto_trabajadores * 100

    # Crear el gráfico
    circulo = go.Figure(go.Pie(
        labels=['Jornada completa', 'Jornada parcial', 'Jornada con tiempo extra'],
        values=[porcentaje_completa, porcentaje_parcial, porcentaje_extra],
        #hole=0.4,  # Agujero para crear un donut chart
        #hoverinfo='label+percent',
        showlegend= False,
        textinfo='label+percent',
        textfont_size=12,
        marker_colors = ['rgb(144,196,226)', 'rgb(65,173,231)', 'rgb(17,78,143)']
    ))
    circulo.update_layout(
    title=f'Distribución de Jornadas<br>{puesto_seleccionado.capitalize()}',
    title_font_size=14,
    title_x=0.5
)
    #************************************RETORNAR LOS 3 GRÁFICOS************************************
    return dona, histograma, circulo


#************************************Graficos dinámico max salario por años de servicio************************************
@app.callback(
    Output("grafico-puntos", "figure"),
    [Input("dropdown-puesto2", "value")]
)
def actualizar_grafico(puesto_seleccionado):

    #filtrar puesto(s)
    df_filtrado = Salarios_vs_Antiguedad_df[Salarios_vs_Antiguedad_df['PUESTO_SIMPLIFICADO'] == puesto_seleccionado]

    #Crear grafico
    #************************************GRAFICO************************************
    puntos = go.Figure()
    puntos.add_trace(go.Scatter(
        x=df_filtrado['AÑOS DE SERVICIO'],
        y=df_filtrado['SALARIO'],
        name = 'Salario máximo',
        mode='lines',
        line=dict(color='#095fa3')
    ))
    puntos.update_layout(
        title_text = f'Salario maximo para<br>{puesto_seleccionado.capitalize()} en el <b>2022</b><br>en función de sus años de servicio.',
        title_font_size=14,
        title_x=0.5,
        xaxis_title='Años de Servicio',
        yaxis_title='Salario Máximo')
    #************************************RETORNAR GRÁFICO************************************
    return puntos

    
#************************************EJECUTAR************************************
if __name__ == ('__main__'):
    app.run_server(debug = True)