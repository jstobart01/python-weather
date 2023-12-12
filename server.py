from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve

app = Flask(__name__)

# Define routes when using Flask

@app.route('/') # This would be the homepage
@app.route('/index') # This would also be the homepage
def index():
    return render_template('index.html')

@app.route('/weather')
def get_weather():
    city = request.args.get('city')

    # Check for empty strings or string with only spaces
    if not bool(city.strip()):
        city = "San Francisco"

    weather_data = get_current_weather(city)
    # City is not found by API
    if not weather_data['cod'] == 200:
        return render_template('city-not-found.html')
    
    # All of the following is what is used in our weather template html file
    return render_template(
        "weather.html",
        title = weather_data["name"],
        status = weather_data["weather"][0]["description"].capitalize(),
        temp = f"{weather_data['main']['temp']:.1f}",
        feels_like = f"{weather_data['main']['feels_like']:.1f}"
        #snow = f"{weather_data["snow"]:.1f}"
    )

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
    # app.run(host="0.0.0.0", port=8000) # 0.0.0.0 will make this run on our local host