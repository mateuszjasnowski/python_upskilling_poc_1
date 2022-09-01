class CityData():
    def __init__(self, city_name: str) -> None: #, city_url: str
        self.name = city_name

        temp_city_dict = '.temp_city/'

        self.routes = []
        #opening files
        try:
            with open(temp_city_dict+'routes.txt', 'r', encoding="UTF-8") as routes_file:
                file_lines = routes_file.read().replace('"', "").split("\n")
                file_columns = file_lines[0].split(",")
            self.routes.append([dict(zip(file_columns, line.split(','))) for line in file_lines[1:]])

        except:
            pass
        #else:
            #self.routes = []


        '''self.files = {}

        for file in txt_file_list:
            file_path = temp_city_dict + file
            with open(file_path, 'r', encoding="UTF-8") as city_file:
                file_lines = city_file.read().replace('"', "").split("\n")
                file_columns = file_lines[0].split(",")
            self.files[file.replace('.txt', '')] = {i: dict(zip(file_columns, file_lines[i].split(','))) for i in range(1, len(file_lines)) if file_lines[i] != ""}

            #[line for line in file_lines[1:] if line != ""]
            dict(
                zip(
                    file_columns,
                    (
                        line
                        for line in str(file_lines[1:])
                        .replace("['", "")
                        .replace("]'", "")
                        .replace("'", "")
                        .split(",")
                        if line != ""
                    ),
                )
            )'''


        '''for file in txt_file_list:
            file_path = temp_city_dict + file
            with open(file_path, 'r', encoding="UTF-8") as city_file:
                self.file_lines = city_file.read().replace('"', "").split("\n")
                #file_columns = file_lines[0].split(",")

            file_content = dict(
                zip(
                    file_columns,
                    (
                        line
                        for line in str(file_lines[1:])
                        .replace("['", "")
                        .replace("]'", "")
                        .replace("'", "")
                        .split(",")
                        if line != ""
                    ),
                )
            )
            setattr(self, file.replace('.txt',""), file_content'''


class CityAgency():
    def __init__(self, agency_file_location: str) -> None:
        self.file_list = listdir()


        with open(agency_file_location, 'r', encoding="UTF-8") as agency_file:
            agency_file_content = agency_file.read().replace('"', "").split('\n')
            self.agency_columns = agency_file_content[0].split(',')
