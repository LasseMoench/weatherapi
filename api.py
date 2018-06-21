import connexion
import sqlite3
import time

conn = sqlite3.connect('weather.db')
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS weather(timestamp INTEGER, temperature REAL, pressure INTEGER, humidity REAL, rain INTEGER)')


def report_weather_data(weather):
    print("Temperature: {}, Pressure: {}, Humidity: {}, Rain: {}".format(
          weather["temperature"], weather["pressure"], weather["humidity"], weather["rain"]))
    c.execute("INSERT INTO weather VALUES ({}, {}, {}, {}, {})".format(
        int(time.time()), weather["temperature"], weather["pressure"], weather["humidity"], weather["rain"]))
    conn.commit()


app = connexion.App(__name__)
app.add_api('api.yaml')

# Set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app


def main():
    # Run our standalone gevent server
    app.debug = True
    app.run(port=8080, server='gevent')


if __name__ == '__main__':
    main()
