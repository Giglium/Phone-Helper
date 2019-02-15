import os, json, xlwt, xlrd, re


class PhoneHelper:
    PARENT_FOLDER = 'file/'
    STATIC_FOLDER = 'static'
    INPUT_DIR = PARENT_FOLDER + 'input'
    OUTPUT_DIR = PARENT_FOLDER + 'output'
    ARCHIVE_DIR = PARENT_FOLDER + 'archive'
    FONTS_DIR = 'fonts'
    SETTINGS_FILE = 'settings.json'

    def __init__(self):
        return

    def setup(self):
        pathlib.Path(self.INPUT_DIR).mkdir(parents=True, exist_ok=True)
        pathlib.Path(self.OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
        pathlib.Path(self.ARCHIVE_DIR).mkdir(parents=True, exist_ok=True)

    def file_list(self):
        data = {}

        if not os.path.exists(self.INPUT_DIR):
            self.setup()

        included_extensions = ['xls', 'xlsx']

        data['input'] = os.listdir(self.INPUT_DIR)
        data['output'] = [fn for fn in os.listdir(self.OUTPUT_DIR)
                          if any(fn.endswith(ext) for ext in included_extensions)]
        data['archive'] = os.listdir(self.ARCHIVE_DIR)

        return data

    def file_upload(self, data):
        error = True

        for file in data:
            filename = file.filename

            if '.xls' in filename or '.xlsx' in filename:
                raw = file.file.read()
                error = False
                if not os.path.exists(self.INPUT_DIR):
                    self.setup()

                with open(self.INPUT_DIR + '/' + filename, 'wb') as save_file:
                    save_file.write(raw)
                    save_file.close()

                with open(self.ARCHIVE_DIR + '/' + filename, 'wb') as save_file:
                    save_file.write(raw)
                    save_file.close()
        return error

    def delete_file(self, filepath):
        path = self.PARENT_FOLDER + filepath
        if os.path.exists(path):
            os.remove(path)
        return

    def read_settings(self):
        data = {}
        try:
            with open(self.SETTINGS_FILE, 'r') as f:
                data = json.load(f)
                data['error'] = False
        except Exception:
            data['error'] = True
        return data

    def save_settings(self, data):
        with open(self.SETTINGS_FILE, 'w') as f:
            f.write(json.dumps(data))
        return

    def get_statistic(self, filename):
        filename = filename.split('.')[0]
        data = {}
        try:
            with open(self.OUTPUT_DIR + '/' + filename + '.json', 'r') as f:
                data = json.load(f)
                data['error'] = False
        except Exception:
            data['error'] = True
        return data

    def run_job(self):
        data = self.read_settings()

        phone_prexif = data['phonePrefix'].replace(" ", "").split(',')
        colums_title = data['columsTitle'].replace(" ", "").upper().split(',')

        for file in os.listdir(self.INPUT_DIR):
            filename = file.split('.')[0]
            col_list = []

            workbook = xlwt.Workbook()
            nice_sheet = workbook.add_sheet(data['validName'])
            wrong_sheet = workbook.add_sheet(data['discardName'])
            nice_sheet_index = 0
            wrong_sheet_index = 0
            valid_number = 0
            discard_number = 0

            wb = xlrd.open_workbook(self.INPUT_DIR + '/' + file)
            sheet = wb.sheet_by_index(0)

            # find column to process
            for col_index in range(sheet.ncols):
                if sheet.cell(0, col_index).value.replace(" ", "").upper() in colums_title:
                    col_list.append(col_index)

            # check number
            for i in range(sheet.nrows):
                if i > 0:
                    nice_sheet_row = sheet.row_values(i).copy()
                    wrong_sheet_row = sheet.row_values(i).copy()

                    for col_index in col_list:
                        phone_number = str(sheet.cell_value(i, col_index)).split(".")[0]
                        valid = True
                        for prefix in phone_prexif:
                            # check min len, max len, prefix and all equals element
                            if len(phone_number) < 7 or len(phone_number) > 13 or re.match(prefix + '*',
                                                                                           phone_number) or re.match(
                                    '^(.)\1*$', phone_number):
                                valid = False

                        if valid:
                            nice_sheet_row[col_index] = phone_number
                            wrong_sheet_row[col_index] = ""
                            valid_number += 1
                        else:
                            nice_sheet_row[col_index] = ""
                            wrong_sheet_row[col_index] = phone_number
                            if phone_number != '' and phone_number != '0':
                                discard_number += 1

                    if data['shifter']:
                        index = len(col_list) - 1
                        while index > 0:
                            if nice_sheet_row[col_list[index]] != "":
                                if nice_sheet_row[col_list[index - 1]] == "":
                                    nice_sheet_row[col_list[index - 1]] = nice_sheet_row[col_list[index]]
                                    nice_sheet_row[col_list[index]] = ""
                            index -= 1

                        index = 0
                        while index < len(col_list) - 1:
                            if nice_sheet_row[col_list[index]] == "":
                                if nice_sheet_row[col_list[index + 1]] != "":
                                    nice_sheet_row[col_list[index + 1]] = nice_sheet_row[col_list[index]]
                                    nice_sheet_row[col_list[index]] = ""
                            index += 1

                    if any(nice_sheet_row[col_index] != "" for col_index in col_list):
                        for index, value in enumerate(nice_sheet_row):
                            nice_sheet.write(nice_sheet_index, index, value)
                        nice_sheet_index += 1

                    if any(wrong_sheet_row[col_index] != "" for col_index in col_list):
                        for index, value in enumerate(wrong_sheet_row):
                            wrong_sheet.write(wrong_sheet_index, index, value)
                        wrong_sheet_index += 1
                else:
                    sheet_row = sheet.row_values(i)

                    for index, value in enumerate(sheet_row):
                        nice_sheet.write(nice_sheet_index, index, value)
                    nice_sheet_index += 1

                    for index, value in enumerate(sheet_row):
                        wrong_sheet.write(wrong_sheet_index, index, value)
                    wrong_sheet_index += 1

            if not data['createDiscardSheet']:
                workbook._Workbook__worksheets = [workbook._Workbook__worksheets[0]]

            workbook.save(self.OUTPUT_DIR + "/" + filename + ".xls")

            statistic = {'validNumber': valid_number, 'discardNumber': discard_number}
            with open(self.OUTPUT_DIR + "/" + filename + ".json", 'w') as f:
                f.write(json.dumps(statistic))

            self.delete_file("input/" + file)
        return
