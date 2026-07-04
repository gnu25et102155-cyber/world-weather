from flask import Flask, request, jsonify
import json
import urllib.error
import urllib.parse
import urllib.request

app = Flask(__name__)
API_KEY = "91e828401c93afe11fefff459b786295"  # Replace with your actual API key from openweathermap.org

@app.route('/weather')
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "Missing 'city' parameter"}), 400
    query = urllib.parse.urlencode({
        "q": city,
        "appid": API_KEY,
        "units": "metric",
    })
    url = f"https://api.openweathermap.org/data/2.5/weather?{query}"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
            status = response.getcode()
    except urllib.error.HTTPError as error:
        data = json.load(error)
        status = error.code
    except urllib.error.URLError as error:
        return jsonify({"error": f"Network error: {error.reason}"}), 500

    if status == 200:
        result = {
            "location": f"{data['name']}, {data['sys']['country']}",
            "temperature": f"{data['main']['temp']} °C",
            "weather": data['weather'][0]['description'],
            "humidity": f"{data['main']['humidity']}%",
            "wind_speed": f"{data['wind']['speed']} m/s"
        }
        return jsonify(result)
    else:
        return jsonify({"error": data.get("message", "Something went wrong")}), status

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)