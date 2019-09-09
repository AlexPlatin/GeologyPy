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
        raise FileExistsError("Can't open file")
    structure = file.structure
    for field, type in zip(list_fields, str_or_num):
        if type == "str":
            structure.add_field(field, MMpy.FieldType.character, 50, 3)
        elif type == "num":
            structure.add_field(field, MMpy.FieldType.real, 0, 3)
    file.structure = structure
    file.close()
    print("Finished")


def create_dat_file(path, list_fields, str_or_num):
    """
    Create new MM.dat file
    :param path: path .dat
    :param list_fields: list cols.

    Example: ["EAST", "NORTH", "RL", "AZ", "NAME"]

    :param str_or_num: type of data (str, num)

    Example: ["num", "num", "num", "num", "str"]

    :return: None
    """
    structure = MMpy.FileStruct()
    for field, type in zip(list_fields, str_or_num):
        if type == "str":
            structure.add_field(field, MMpy.FieldType.character, 50, 3)
        elif type == "num":
            structure.add_field(field, MMpy.FieldType.real, 0, 3)
    MMpy.File.create_from_template(path, "", structure)
    print("Finished")



def get_tridb_names(path_to_tridb):
    """
    Get names of wf from wf type
    :param path_to_tridb: path wf type
    :return: list of wf
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
    Get coordinates from .tridb files
    :param path_to_tridb: path_wf_type
    :param number_tridb_in_base: if -1: get all coordinates in wf type
                                 if not -1: get coordinates of wf with index
    :return: if number_tridb_in_base -1: all coordinates in wf type
             if number_tridb_in_base not -1: coordinates of wf with index
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
