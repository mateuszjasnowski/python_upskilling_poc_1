from appData import app


@app.route('/get_api_version', methods=['GET'])
def get_api_version():
    return {'api_version': '0.0.1'}