import pandas as pd
import message as msg
import tkinter as tk
from tkinter import filedialog


def read_csv(file):
    try:
        return pd.read_csv(file)
    except Exception as e:
        msg.show_error('Unable to read file ERROR: ' + str(e))


def load_data(env):
    if env == 'production':
        msg.show_message('Select patient data csv file...')
        try:
            root = tk.Tk()
            root.withdraw()
            while True:
                file_path = filedialog.askopenfilename()
                if not file_path:
                    msg.show_prompt('No file selected.')
                else:
                    break
            msg.show_confirmation('File selected: ' + file_path + '\n')
            df = read_csv(file_path)
            return df
        except Exception as e:
            msg.show_error('Somethings wrong with the file selected' + str(e))
    elif env == 'dev':
        print('Reading Test Data...')
        df = read_csv('E:../test_data.csv')
        return df


def pandarize(env):
    df = load_data(env)
    print('============================= PANDARIZING DATA =============================')
    df[' PHN'] = df[' PHN'].astype('str')
    df[' DOB'] = pd.to_datetime(df[' DOB'], format='%d/%m/%Y').astype(str)
    df[' Interpretation Date'] = pd.to_datetime(df[' Interpretation Date'], format='%d/%m/%Y').astype(str)
    df[' Ref Doctor BillTo #'] = df[' Ref Doctor BillTo #'].apply(
        lambda x: '{0:0>5}'.format(x))  # add leading zeros to get 5 digits

    return df
