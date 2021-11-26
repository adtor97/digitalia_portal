import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
from flask import request, session
from utils.utils_login import loginizer
import paramiko
import os

def serve_layout():
    layout = html.Div([
                        dbc.Row([html.H1("Anti Virus Digitalia", id="title", style={"color":"#1b2b58", "font-size":"28px"})],
                        justify = 'center')
                        , dbc.Row(
                                [
                                dbc.Col(
                                            [
                                            html.Button("Hostgator clean regular virus", id="hostgator-regular-virus-button"),
                                            dcc.Loading(html.Div(id="hostgator-regular-virus-result"))
                                            ],
                                            width=3)
                                ],
                                id="row-buttons")
                        ,
                    ])
    return layout

def init_callbacks(dash_app):
    @dash_app.callback(
                        Output('hostgator-regular-virus-result', 'children'),
                        [Input('hostgator-regular-virus-button', 'n_clicks')],
                        prevent_initial_callback=True
                        )
    def hostgator_regular_virus_cleanup(n_clicks):
        print("start hostgator_regular_virus_cleanup")
        if n_clicks is None:
            return ""
        try:
            if n_clicks<1:
                return ""
        except:
            return ""

        wordpress_folders=["wp-includes\n", "wp-content\n", "wp-admin\n"]
        ssh = paramiko.SSHClient()

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        hostgator_ip = os.environ['hostgator_ip']
        hostgator_username = os.environ['hostgator_username']
        hostgator_password = os.environ['hostgator_password']

        ssh.connect(hostgator_ip, username=hostgator_username, password=hostgator_password, port=2222)
        sftp = ssh.open_sftp()

        stdin1, stdout1, stderr1 = ssh.exec_command('ls')
        folders = stdout1.readlines()

        for folder in folders:
            stdin2, stdout2, stderr2 = ssh.exec_command(f'cd ~/{folder} \n ls')
            folders_inside = stdout2.readlines()
            #stdin, stdout, stderr =  ssh.exec_command('ls')
            if folders_inside!=folders and folders_inside!=[] and folder!='www2':
                #print (folder, folders_inside)
                if "wp-includes\n" in folders_inside and "wp-content\n" in folders_inside and "wp-admin\n" in folders_inside:
                    print("WORDPRESS", folder)

                    stdin3, stdout3, stderr3 = ssh.exec_command(f'cd ~/{folder.strip()}/wp-includes \n ls')
                    folders_wpincludes = stdout3.readlines()
                    #print("folders_wpincludes", folders_wpincludes)

                    if 'header_test\n' in folders_wpincludes:
                        stdin4, stdout4, stderr4 = ssh.exec_command(f'rm -rf  ~/{folder.strip()}/wp-includes/header_test')
                        print("remove header_test", folder)
                    if 'class-wp-http-netfilter.php\n' in folders_wpincludes:
                        stdin5, stdout5, stderr5 = ssh.exec_command(f'rm  ~/{folder.strip()}/wp-includes/class-wp-http-netfilter.php')
                        print("remove class-wp-http-netfilter.php", folder)
                    stdin5, stdout5, stderr5 = ssh.exec_command(f'cd ~/{folder.strip()}/wp-content/themes \n ls')
                    themes_folders = stdout5.readlines()
                    print("themes_folders", themes_folders)
                    for theme_folder in themes_folders:
                        print (theme_folder)
                        print("theme_folder!='index.php\n'", theme_folder!='index.php\n')
                        if theme_folder!='index.php\n':
                            functions_file = f'/home1/digittec/{folder.strip()}/wp-content/themes/{theme_folder.strip()}/functions.php'
                            print(functions_file)
                            functions_file = sftp.open(functions_file)
                            try:
                                for line in functions_file:
                                    if "yup" in line and "zeeta" in line:
                                        print(line)
                            finally:
                                functions_file.close()
        sftp.close()
        ssh.close()

        print("finished hostgator_regular_virus_cleanup correctly")
        return "Hostgator regular virus cleanup ran correctly!"
