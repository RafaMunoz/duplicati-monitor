import os
import json
import apprise
import logging
from template import parse_report
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.os.getenv("LOGLEVEL", "DEBUG"), format='[%(asctime)s] [%(levelname)s] %(message)s')

app = Flask("duplicati-monitor")
app.logger.info("Start Duplicati Monitor")

# Create an Apprise instance
apobj = apprise.Apprise()
URI_NOTIFICATION = os.getenv("URI_NOTIFICATION")
app.logger.info(f"URI_NOTIFICATION = {URI_NOTIFICATION}")
apobj.add(URI_NOTIFICATION)


@app.route('/')
def default_route():
    text = "Hi, I'm Duplicati-monitor!!"
    return jsonify(mesage=text)


@app.route('/report', methods=['POST'])
def receive_report():
    try:
        # Recibir y procesar el reporte enviado por Duplicati
        app.logger.info(f"Report: {request.data}")
        report = request.get_json()

        message = parse_report.generate_message_report(report)
        app.logger.info(message)

    except Exception as e:
        message = "💾 ⚫ Error processing report backup"
        app.logger.error(f"Error error processing report: {e}")

    # Enviamos notificacioon
    apobj.notify(body=message)

    return 'Report received'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv("PORT", 8000))
