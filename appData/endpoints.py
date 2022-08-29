import urllib.request
import zipfile, os
#import jsonify

from appData import app


@app.route('/get_api_version', methods=['GET'])
def get_api_version():
    return {'api_version': '0.0.1'}

@app.route('/routes/update_routes', methods=['GET'])
def routes_update_routes():
    try:
        #download file from url, save as file name
        file_to_download = 'https://www.wroclaw.pl/open-data/87b09b32-f076-4475-8ec9-6020ed1f9ac0/OtwartyWroclaw_rozklad_jazdy_GTFS.zip'
        zip_file_name = 'wroclaw.zip'
        urllib.request.urlretrieve(file_to_download, zip_file_name)

        #extract zip file to directory
        with zipfile.ZipFile(zip_file_name,"r") as zip_ref:
            zip_ref.extractall("./wroclaw/")

        #remove zip file
        os.remove(zip_file_name)

        #get feed info
        with open('./wroclaw/feed_info.txt', 'r') as feed_info:
            feed_info_lines = feed_info.read().replace('"',"").split('\n')
            col_names = feed_info_lines[0].split(',')
            file_content = [dict(zip(col_names, line.split(','))) for line in feed_info_lines[1:] if line != ""]

    except:
        download_status = "FAILED"
        file_content = 'N\A'
    else:
        download_status = "SUCESS"
    finally:
        return {'download_status': download_status, 'feed_info': file_content}

