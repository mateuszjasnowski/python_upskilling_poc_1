"""
Operations on feed
Content:
    Feed class definition
    Download feed function
"""
from datetime import datetime, date
import urllib.request
import zipfile
import os

FEED_URL = ('https://www.wroclaw.pl/open-data/'
            '87b09b32-f076-4475-8ec9-6020ed1f9ac0/'
            'OtwartyWroclaw_rozklad_jazdy_GTFS.zip')


class Feed:
    ''' content of feed '''
    def __init__(self, feed_info_file):
        """feed_info_file is location of feed file"""
        with open(feed_info_file, "r", encoding='UTF-8') as feed_file:
            feed_info_lines = feed_file.read().replace('"', "").split("\n")
            col_names = feed_info_lines[0].split(",")

        file_content = dict(
            zip(
                col_names,
                (
                    line
                    for line in str(feed_info_lines[1:])
                    .replace("['", "")
                    .replace("]'", "")
                    .replace("'", "")
                    .split(",")
                    if line != ""
                ),
            )
        )
        for key, value in file_content.items():
            setattr(self, key, value)

    def is_feed_outdated(self):
        """returns True if feed is outdated"""
        try:
            feed_start_date = datetime.strptime(
                str(self.feed_start_date), "%Y%m%d"
            ).date()  # .strftime("%Y %m, %d")
            feed_end_date = datetime.strptime(
                str(self.feed_end_date), "%Y%m%d"
            ).date()  # .strftime("%Y %m, %d")
            today = date.today()  # .strftime("%Y %m, %d")
        except AttributeError:
            raise Exception('ERROR: Cannot recieve datas from feed')
        else:
            if feed_end_date < today or (today - feed_start_date).days > 15:
                return True
            return False


def download_feed():
    """downloading feed from URL"""
    try:
        print("Downloading file")
        # download file from url, save as file name
        file_to_download = FEED_URL
        zip_file_name = "wroclaw.zip"
        urllib.request.urlretrieve(file_to_download, zip_file_name)

        # extract zip file to directory
        with zipfile.ZipFile(zip_file_name, "r") as zip_ref:
            zip_ref.extractall("./wroclaw/")

        # remove zip file
        os.remove(zip_file_name)

    except:
        return "FAILED: Cannot download feed"
    else:
        return Feed("./wroclaw/feed_info.txt")
