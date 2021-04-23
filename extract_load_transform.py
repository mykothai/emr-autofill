import pandas as pd
import message as msg
import tkinter as tk
from tkinter import filedialog


def read_csv(file):
    try:
        return pd.read_csv(file)
    except Exception as e:
        msg.show_error('Unable to read file ERROR: ' + str(e))


def pandarize(env):
    # Do the data things
    if env == 'production':
        msg.show_message('Select patient data csv file...')
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        df = read_csv(file_path)
        msg.show_confirmation('File selected: ' + file_path + '\n')
    elif env == 'dev':
        print('Reading Test Data...')
        df = read_csv('E:../test_data.csv')
    print('============================= PANDARIZING DATA =============================')
    df[' PHN'] = df[' PHN'].astype('str')  # field
    df[' DOB'] = pd.to_datetime(df[' DOB'], format='%d/%m/%Y').astype(str)  # format is the existing data format
    df[' Interpretation Date'] = pd.to_datetime(df[' Interpretation Date'], format='%d/%m/%Y').astype(
        str)  # format is the existing data format
    df[' Ref Doctor BillTo #'] = df[' Ref Doctor BillTo #'].apply(
        lambda x: '{0:0>5}'.format(x))  # add leading zeros to get 5 digits

    return df
