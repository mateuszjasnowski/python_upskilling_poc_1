from datetime import datetime, date

class Feed():
    def __init__(self, feed_info_file):
        with open(feed_info_file, 'r') as feed_file:
            feed_info_lines = feed_file.read().replace('"',"").split('\n')
            col_names = feed_info_lines[0].split(',')

        file_content = dict(zip(col_names, (line for line in str(feed_info_lines[1:]).replace("['",'').replace("]'",'').replace("'","").split(',') if line != '')))
        for k,v in file_content.items():
            setattr(self, k, file_content[k])

    def is_feed_outdated(self):
        feed_start_date = datetime.strptime(str(self.feed_start_date), "%Y%m%d").date()#.strftime("%Y %m, %d")
        feed_end_date = datetime.strptime(str(self.feed_end_date), "%Y%m%d").date()#.strftime("%Y %m, %d")
        today = date.today()#.strftime("%Y %m, %d")

        if feed_end_date < today or (today - feed_start_date).days > 15:
            return True
        return False
