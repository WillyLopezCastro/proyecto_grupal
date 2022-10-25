from flask import Flask
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from pandas_datareader import data as wb
from datetime import datetime as dt
import os
from os.path import join

carpeta = 'uploads'
BASEDIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = join(BASEDIR, carpeta)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.secret_key = "PROYECTO_GRUPAL"
appp = dash.Dash('Mi primer Gráfico')


# Image upload
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 6 * 10000 * 10000 #para cambiar el tamaño de la imagen 2 significa 2megas