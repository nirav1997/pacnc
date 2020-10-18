from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import dash
import dash_core_components as dcc
import dash_html_components as html
import datetime
import requests
from django_plotly_dash import DjangoDash
import plotly.express as px

from plotly.offline import plot
import plotly.graph_objs as go
import random
import json
import numpy as np

df = px.data.iris() # iris is a pandas DataFrame
fig = px.scatter(df, x="sepal_width", y="sepal_length")

dcc.Graph(figure=fig)

app = DjangoDash('pacnc') 

def index(request):
    return render(request, 'confe/index.html')

def risk(request):
    return render(request, 'confe/risk.html')

def submit(request):
    data = request.COOKIES['']
    
    items = data.split(",")
    
    items_with_zipcode = [item.split("zip") for item in items]
    
    zipcodes = [item[-1] for item in items_with_zipcode]
    zip_string = ",".join(zipcodes)
    url = 'http://34.72.27.12:5000/api/v1/risk_analysis?zipcode='+zip_string
    risk_results = requests.get(url)
    risk_results = json.loads(risk_results.content)
    
    risk = risk_results['risk']
    cases = risk_results['Avg Cases']
    cases = np.array(cases)
    
    cases = (cases - min(cases))/(max(cases)-min(cases))*100
    base = datetime.datetime.today()
    date_list = [(base - datetime.timedelta(days=x)).date() for x in range(7)]
    
    bar_dict = {}
    
    for i in range(len(date_list)):
        bar_dict[str(date_list[i])] = cases[i]
        
    
    layout = go.Layout(
                margin=dict(l=5, r=5, t=40, b=5),
                width=375,
                height=250,
                showlegend = False,
                title="Increase Ratio"
            )
    config = {'displayModeBar': False}
    
    fig = go.Figure(layout=layout)
    bar = go.Bar(x=date_list, y=cases, )
    line = go.Scatter(x=date_list, y=cases)
    fig.add_trace(bar)
    fig.add_trace(line)
    plt_div = plot(fig,config=config, output_type='div')
    
    return render(request, 'confe/ris_results.html',  context={'plot_div': plt_div, 'risk':round(risk*100,2)})
    
app.layout = html.Div([
        
        
    #html.Br(),
    html.Div([
            dcc.Graph(figure=fig),
            html.Br(),
#            dcc.Dropdown(id='county_dropdown', options=[{'label':'Washington', 'value':'Washington'}], value='Washington'),
    ],style={'float': 'left', 'width': '30%'}),
    
   

])