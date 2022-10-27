from flask import Flask, render_template, request
from flask_swagger_ui import get_swaggerui_blueprint
from src.alerta_rio_service import AlertaRioService
from src.visualization_map import rio_map

# Starting Flask app
app = Flask(__name__)

# Endpoint for main visualization
@app.route('/')
def index():
    return render_template("index.html", map=rio_map._repr_html_())

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