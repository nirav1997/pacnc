from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import dash
import dash_core_components as dcc
import dash_html_components as html

from django_plotly_dash import DjangoDash
import plotly.express as px

df = px.data.iris() # iris is a pandas DataFrame
fig = px.scatter(df, x="sepal_width", y="sepal_length")

dcc.Graph(figure=fig)

app = DjangoDash('pacnc') 

def index(request):
    return render(request, 'index.html')

app.layout = html.Div([
        
        
    #html.Br(),
    html.Div([
            dcc.Graph(figure=fig),
            html.Br(),
#            dcc.Dropdown(id='county_dropdown', options=[{'label':'Washington', 'value':'Washington'}], value='Washington'),
    ],style={'float': 'left', 'width': '30%'}),
    
   

])