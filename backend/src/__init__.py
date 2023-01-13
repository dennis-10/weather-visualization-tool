from flask import Flask, render_template, request, make_response, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from src.alerta_rio_service import AlertaRioService
#from src.visualization_line_chart import anim
from src.visualization_map import RioMap
from src.visualization_line_chart import Grafico
from flask_cors import CORS
from src.processing_data import Observacao
from matplotlib import animation

# Starting Flask app
app = Flask(__name__)
CORS(app)

# Instantiate map object
rio_map = RioMap()

# Endpoint for main visualization
@app.route('/')
def index():
  return render_template(
    "index.html",
    map=rio_map.map_visualization._repr_html_()
    #chart1=anim, 
    #chart2=anim2
    )

# Endpoint for setting the data path
@app.route('/chart', methods=["GET"])
def processChart():
  try:
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    start_hour = request.args.get('start_hour')
    end_hour = request.args.get('end_hour')
    select1 = request.args.get('cel_number1')
    select2 = request.args.get('cel_number2')

    intervalo = Observacao(start_date, end_date, start_hour, end_hour)

    sd = intervalo.formataDataInicio()
    ed = intervalo.formataDataFim()
    
    line_chart = Grafico(num_celula=select1, data_inicio=sd, data_fim=ed, 
                hora_inicio=intervalo.hora_inicio, hora_fim=intervalo.hora_fim)
    line_chart.processaObservacao()
    
    line_chart2 = Grafico(num_celula=select2, data_inicio=sd, data_fim=ed, 
                hora_inicio=intervalo.hora_inicio, hora_fim=intervalo.hora_fim)
    line_chart2.processaObservacao()
    
    animations = line_chart.geraGrafico() + line_chart2.geraGrafico()
    
    return make_response(animations)

  except Exception as error:
    raise error

# Endpoint for setting the data path
@app.route('/map', methods=["GET"])
def set_data_path():
  try:
    data_path = request.args.get('data_path')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    start_hour = request.args.get('start_hour')
    end_hour = request.args.get('end_hour')

    intervalo = Observacao(start_date, end_date, start_hour, end_hour)

    sd = intervalo.formataDataInicio()
    ed = intervalo.formataDataFim()

    mapR = rio_map.generate_rio_map(data_path, sd, ed, start_hour, end_hour)

    #return mapR._repr_html_()
    return mapR._repr_html_()
  except Exception as error:
    raise error

# Endpoint for getting alerta rio data
@app.route("/data/")
def get_data():
    try:
      seconds_interval = request.args.get("seconds_interval")

      response = AlertaRioService.get_data(
        request.args.get("start_time"),
        request.args.get("end_time"),
        int(seconds_interval),
        request.args.get("station"))
        
      return response
    except Exception as error:
      raise error

# Swagger DOCS
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
  SWAGGER_URL,
  API_URL,
  config={
    'app_name': 'Weather Visualization Tool'
  }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Path to swagger docs
@app.route('/static/<path:path>')
def send_static(path):
  return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)