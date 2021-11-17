import bcrypt, os, json
import creds
import pandas as pd

def loginizer(username, password):
    #print(password)
    password = str.encode(str(password))
    #print(password)
    username = username.lower()
    users = creds.users
    df_user = pd.DataFrame(users)
    df_user["matching"] = df_user.apply(lambda x: True if bcrypt.checkpw(password, str.encode(str(x['password']))) else False, axis = 1)
    df_user = df_user[(df_user["matching"]==True) & (df_user["username"]==username)]
    print(df_user)
    if len(df_user)==0: return False
    df_user.drop(columns=["password", "matching"], inplace=True)
    views = df_user.views.values[0]
    df_user = df_user.to_json(date_format='iso', orient='records')
    user = json.loads(df_user)[0]
    print("user", user)
    return user
