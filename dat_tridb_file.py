import sqlite3
import MMpy


def add_columns_to_dat_file(path, list_fields, str_or_num):
    """
    Add columns to MM.dat
    :param path: .dat
    :param list_fields: list cols.

    Example: ["EAST", "AZ", "NAME"]

    :param str_or_num: type of data (str, num)

    Example: ["num", "num", "str"]

    :return: None
    """
    file = MMpy.File()
    if not file.open(path):
        raise FileExistsError("Файл не открывается")
    structure = file.structure
    for field, type in zip(list_fields, str_or_num):
        if type == "str":
            structure.add_field(field, MMpy.FieldType.character, 50, 3)
        elif type == "num":
            structure.add_field(field, MMpy.FieldType.real, 0, 3)
    file.structure = structure
    file.close()
    print("Готово")


def create_dat_file(path, list_fields, str_or_num):
    """
    Создание нового .dat файла
    :param path: полный путь к файлу .dat
    :param list_fields: список колонок в новом файле.

    Пример: ["EAST", "NORTH", "RL", "AZ", "NAME"]

    :param str_or_num: список маркировок для колонок - текстовая или численная (str, num)

    Пример: ["num", "num", "num", "num", "str"]

    :return: None
    """
    structure = MMpy.FileStruct()
    for field, type in zip(list_fields, str_or_num):
        if type == "str":
            structure.add_field(field, MMpy.FieldType.character, 50, 3)
        elif type == "num":
            structure.add_field(field, MMpy.FieldType.real, 0, 3)
    MMpy.File.create_from_template(path, "", structure)
    print("Готово")


def export_excel(file_in, file_out):
    """
    Экспорт .dat файла в Excel (.xls) в оригинальном виде
    :param file_in: полный путь до файла .dat
    :param file_out: полный путь до файла .dat
    :return: None
    """
    Export2excel_FormSet20 = MMpy.FormSet("EXPORT2EXCEL", "15.0.5.697")
    Export2excel_FormSet20.set_field("METADATATITLE", "")
    Export2excel_FormSet20.set_field("INPUT_FILTER", "")
    Export2excel_FormSet20.set_field("BOOL_FILTER", "0")
    Export2excel_FormSet20.set_field("INCLUDEMETADATA", "0")
    Export2excel_FormSet20.set_field("BOLDHEADER", "1")
    Export2excel_FormSet20.set_field("INCLUDEHEADER", "1")
    Export2excel_FormSet20.set_field("SHEETNAME", "Report")
    Export2excel_FormSet20.set_field("BOOLEXECUTE", "0")
    Export2excel_FormSet20.set_field("FILETYPEINPUT", "0")
    Export2excel_FormSet20.set_field("FILENAMEINPUT", file_in)
    Export2excel_FormSet20.set_field("FILETYPE", "0")
    Export2excel_FormSet20.set_field("FILENAME", file_out, MMpy.append_flag.none)
    return Export2excel_FormSet20.run()


def get_tridb_names(path_to_tridb):
    """
    Получение списка имен каркасов из набора
    :param path_to_tridb: полный путь к набору каркасов
    :return: список каркасов
    """
    conn = sqlite3.connect(path_to_tridb)
    cur = conn.cursor()
    cur.execute("SELECT * FROM GeneralInformation LIMIT 0")
    cur.execute("SELECT * FROM GeneralInformation ORDER BY ID")
    data = cur.fetchall()
    names = [data[i][1] for i in range(len(data))]
    return names


def get_coordinates_tridb(path_to_tridb, number_tridb_in_base=-1):
    """
    Получение координат из набора каркасов
    :param path_to_tridb: полный путь к набору каркасов
    :param number_tridb_in_base: если значение -1: получение координат по всем каркасам в наборе
                                 если значение отличное от -1: получение координат по каркасу под этим номером
    :return: если значение number_tridb_in_base -1: список из списков координат всех каркасов
             если значение number_tridb_in_base отличное от -1: список координат каркаса под данным номером
    """
    conn = sqlite3.connect(path_to_tridb)
    cur = conn.cursor()
    cur.execute("SELECT * FROM GeneralInformation LIMIT 0")
    cur.execute("SELECT * FROM GeneralInformation ORDER BY ID")
    data = cur.fetchall()
    if number_tridb_in_base == -1:
        exp = []
        for number_tridb_in_base in range(len(data)):
            x_min = data[number_tridb_in_base][13]
            x_max = data[number_tridb_in_base][14]
            y_min = data[number_tridb_in_base][15]
            y_max = data[number_tridb_in_base][16]
            z_min = data[number_tridb_in_base][17]
            z_max = data[number_tridb_in_base][18]
            exp.append([x_min, x_max, y_min, y_max, z_min, z_max])
        return exp
    else:
        x_min = data[number_tridb_in_base][13]
        x_max = data[number_tridb_in_base][14]
        y_min = data[number_tridb_in_base][15]
        y_max = data[number_tridb_in_base][16]
        z_min = data[number_tridb_in_base][17]
        z_max = data[number_tridb_in_base][18]
        return x_min, y_min, z_min, x_max, y_max, z_max
