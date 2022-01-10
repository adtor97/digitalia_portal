import bcrypt, os, json
import pandas as pd
from utils import utils_google

def loginizer(username, password):
    #print(password)
    password = str.encode(str(password))
    #print(password)
    username = username.lower()

    df_user = utils_google.read_ws_data(utils_google.open_ws("base_1", "usuario"))
    df_user = df_user[(~df_user["usuario_contrasena"].isnull())
                    & (~df_user["usuario_contrasena"].isna())
                    & (df_user["usuario_contrasena"] != "")
                    & (df_user["usuario_email"] == username)
                    ]
    #print(df_user)

    df_user["matching"] = df_user.apply(lambda x: True if bcrypt.checkpw(password, str.encode(str(x['usuario_contrasena']))) else False, axis = 1)
    df_user = df_user[(df_user["matching"]==True)]
    #print(df_user)
    if len(df_user)==0: return False
    df_user.drop(columns=["usuario_contrasena", "matching", "usuario_tipo_doc"], inplace=True)
    views = df_user.usuario_vistas.values[0]
    df_user = df_user.to_json(date_format='iso', orient='records')
    user = json.loads(df_user)[0]
    print("user", user)
    return user
