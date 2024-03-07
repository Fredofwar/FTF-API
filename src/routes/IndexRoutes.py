from flask import Blueprint, render_template
from flask_cors import CORS 
import datetime as dt
import locale

main = Blueprint('index_blueprint', __name__)
CORS(main, supports_credentials=True)
locale.setlocale(locale.LC_ALL, "es_MX")

@main.route('/')
def index():
    today = dt.datetime.now()
    fecha_formateada = today.strftime("%A, %d de %B de %Y %H:%M")
    return render_template('index.html', today = fecha_formateada)