import pandas as pd
from io import StringIO, BytesIO
import dash_bootstrap_components as dbc
from dash import dcc
from dash import dash_table
from dash import html
from utils import utils_google
from flask import render_template, json

text_example = f"""
1. Sobre el puesto

Este puesto es para un cliente peruano. Estamos trabajando inhouse para un marketplace en Perú y buscamos desarrolladores que se unan al equipo.

El ambiente laboral tiene una positiva combinación de startup y empresa consolidada. Además trabajarás con un equipo amplio y con experiencia.

Harás desarrollos relacionados a e-commerce, pasarelas de pagos, logística, entre otros.

Es deseable la modalidad híbrida yendo a oficina 2 veces por semana (Lima - San Isidro), sin embargo, no es necesario para todas las vacantes.

Los rangos salariales para el puesto son:
Junior: S/1000 - S/2000
Medium: S/2500 - S/4000
Semi Senior: S/4500 - S/6000
Senior: S/6500 - S/8000

Tu rango salarial dependerá de tu experiencia y la resolución del reto así como las condiciones de trabajo pactadas.

Si estás de acuerdo con los términos, ¡adelante con el reto!

2. Reto técnico

Como siguiente paso del proceso, buscaremos validar tus capacidades técnicas a través de un reto que consistirá en:
- Desarrolla una plataforma en .Net (de preferencia versiones recientes) y JavaScript (de preferencia React)
- La plataforma está orientada a freelancers, que puedan crear recibos de manera rápida y sencilla
- La plataforma debe cumplir con las siguientes historias de usuario: https://bit.ly/net-js
- Utiliza componentes de Bootstrap
- Sube tu código a Github con una rama "main" o "master" y una rama "dev"
De completar estas indicaciones, habrás completado el reto satisfactoriamente para pasar a una siguiente etapa de entrevista, donde revisaremos el código y te preguntaremos sobre tu solución.

Podrás sumar puntos extra para el proceso si:
- Guardas la información ingresada por el freelancer en una BBDD
- Haces deploy de tu aplicación utilizando servicios Azure
- Tu app es responsive
Estos últimos puntos no son obligatorios para pasar a la siguiente fase.

Para cualquier duda que tengas puedes responder este correo o escribir a wa.link/qex6h6.

Se evaluará:
- Uso de los lenguajes de programación, herramientas y frameworks requeridos
- Orden del código
- Forma de resolver el reto a nivel lógica-programática y de experiencia de usuario
"""

def net_react_juntoz():
    div = dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H3("1. Sobre el Puesto", style={"border-bottom": "2px solid #333", "padding-bottom": "10px"}),
                                html.P("¡Se parte de una emocionante empresa en crecimiento! Este puesto es para un cliente en Perú que opera en el espacio de mercado en línea. Nos encontramos en la búsqueda de desarrolladores talentosos para fortalecer nuestro equipo interno."),
                                html.P("Aquí, experimentarás un entorno laboral enriquecedor que fusiona la energía innovadora de una startup con la solidez de una empresa establecida. Además, tendrás la oportunidad de colaborar con un equipo diverso y experimentado."),
                                html.P("Participarás en el desarrollo de soluciones clave para el comercio electrónico, incluyendo integraciones de pasarelas de pago y optimización de la logística."),
                                html.P("Estamos abiertos a un modelo de trabajo híbrido, donde podrás trabajar desde la comodidad de tu hogar y ocasionalmente asistir a nuestras oficinas en Lima - San Isidro. Sin embargo, algunas posiciones pueden ser totalmente remotas."),
                                html.P([
                                    "Nuestra estructura salarial es competitiva y varía según la experiencia:",
                                    html.Ul([
                                        html.Li("Junior: S/1000 - S/2000"),
                                        html.Li("Medium: S/2500 - S/4000"),
                                        html.Li("Semi-Senior: S/4500 - S/6000"),
                                        html.Li("Senior: S/6500 - S/8000")
                                    ], style={"list-style-type": "square"})
                                ]),
                                html.P("Tu compensación se determinará según tu experiencia, habilidades y los términos acordados."),
                                html.P("¡Si estás listo para un desafío gratificante, da el siguiente paso y acepta el reto!", style={"font-weight": "bold"})
                            ],
                            lg=6,
                            md=10,
                            sm=12,
                            style={"padding": "40px", "background-color": "#f9f9f9", "border-radius": "10px"}
                        ),
                    dbc.Col(
                                [
                                    html.H3("2. Reto Técnico", style={"border-bottom": "2px solid #333", "padding-bottom": "10px"}),
                                    html.P("Como parte fundamental de nuestro proceso de selección, queremos evaluar tus habilidades técnicas mediante un reto."),

                                    html.H4("Objetivo General:"),
                                    html.P("Desarrollar una plataforma utilizando .Net y JavaScript (React) orientada a freelancers, que facilite la creación de recibos de manera rápida y eficiente."),

                                    html.H4("Nivel 1: Junior Developer"),
                                    dbc.ListGroup(
                                        [
                                            dbc.ListGroupItem("Implementa un formulario simple para la creación de recibos."),
                                            dbc.ListGroupItem("Utiliza componentes de Bootstrap para un diseño básico."),
                                            dbc.ListGroupItem("Sube tu código a GitHub con ramas 'main' o 'master' y 'dev'.")
                                        ],
                                        flush=True
                                    ),

                                    html.H4("Nivel 2: Medium Developer"),
                                    dbc.ListGroup(
                                        [
                                            dbc.ListGroupItem("Cumple con las historias de usuario (link: https://bit.ly/net-js)."),
                                            dbc.ListGroupItem("Mejora la interfaz utilizando componentes adicionales de Bootstrap."),
                                            dbc.ListGroupItem("Opcional: Almacena la información en una base de datos.")
                                        ],
                                        flush=True
                                    ),

                                    html.H4("Nivel 3: Semi-Senior Developer"),
                                    dbc.ListGroup(
                                        [
                                            dbc.ListGroupItem("Opcional: Despliega la aplicación en Azure."),
                                            dbc.ListGroupItem("Opcional: Implementa un diseño responsivo."),
                                            dbc.ListGroupItem("Prepárate para la revisión de tu código.")
                                        ],
                                        flush=True
                                    ),

                                    html.H4("Nivel 4: Senior Developer"),
                                    dbc.ListGroup(
                                        [
                                            dbc.ListGroupItem("Demuestra dominio de los lenguajes y herramientas."),
                                            dbc.ListGroupItem("Estructura y ordena tu código adecuadamente."),
                                            dbc.ListGroupItem("Enfócate en la lógica de programación y experiencia de usuario.")
                                        ],
                                        flush=True
                                    ),
                                    html.P([
                                        "Para cualquier consulta, contacta a través de ",
                                        html.A("wa.link/qex6h6", href="https://wa.link/qex6h6", target="_blank", style={"color": "#007bff", "text-decoration": "underline"}),
                                        "."
                                    ]),
                                    html.P("Notas: Esta versión del reto se centra en la implementación de funcionalidades clave para facilitar la creación de recibos por parte de freelancers. Los postulantes deben demostrar su capacidad para trabajar con .Net, JavaScript (React) y posiblemente servicios de Azure. Los niveles más avanzados introducen mejoras en la interfaz de usuario y en la estructura del código.", style={"font-style": "italic", "margin-top": "20px"})
                                ],
                                lg=6,
                                md=10,
                                sm=12,
                                style={"padding": "40px", "background-color": "#f9f9f9", "border-radius": "10px"}
                            )
                    ],
                    style={"margin": "20px 0"}
                )
    return div

def startusa_backend_django():
    div = dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H3("1. Sobre el puesto", style={"border-bottom": "2px solid #333", "padding-bottom": "10px"}),
                                html.P("Este puesto es para un cliente que es una startup en Estados Unidos, con un equipo global de colaboradores de diversos países. Estamos en busca de desarrolladores comprometidos y dinámicos para unirse a nuestro equipo de trabajo remoto."),
                                html.P("El entorno de trabajo en la startup es ágil y en constante evolución, lo que requiere adaptabilidad y la capacidad de trabajar bajo presión en situaciones de alto estrés. La comunicación en inglés es esencial, ya que estarás colaborando con colegas de diferentes partes del mundo."),
                                html.P("Trabajarás en un entorno de desarrollo ágil y entrega continua, participando en reuniones diarias (dailies) de lunes a viernes, donde se discuten y planifican las tareas a realizar."),
                                html.P("Es importante destacar que al ser un puesto remoto, recibirás tu remuneración en dólares y tendrás la flexibilidad de trabajar desde Perú."),
                                html.P([
                                    "Los rangos salariales para el puesto son:",
                                    html.Ul([
                                        html.Li("Medium Developer: $1500 - $2500"),
                                        html.Li("SemiSenior Developer: $2600 - $3800"),
                                        html.Li("Senior Developer: $3900 - $5000")
                                    ], style={"list-style-type": "square"})
                                ]),
                                html.P("Tu rango salarial dependerá de tu experiencia, habilidades demostradas en la resolución del reto y las negociaciones de las condiciones de trabajo."),
                                html.P("Si estás de acuerdo con los términos y te sientes emocionado por la oportunidad de trabajar en un ambiente internacional y dinámico, ¡adelante con el reto!", style={"font-weight": "bold"})
                            ],
                            lg=6,
                            md=10,
                            sm=12,
                            style={"padding": "40px", "background-color": "#f9f9f9", "border-radius": "10px"}
                        ),
                        dbc.Col(
                            [
                                html.H3("2. Reto técnico", style={"border-bottom": "2px solid #333", "padding-bottom": "10px"}),
                                html.P("Objetivo General: Desarrollar una aplicación que utilice la API de ChatGPT para realizar una interpretación básica de los datos cargados por el usuario. La interpretación debe ser descriptiva para que el usuario pueda comprender la naturaleza de los datos."),
                                html.P("Nivel 1: Medium Developer"),
                                dbc.ListGroup(
                                    [
                                        dbc.ListGroupItem("Interfaz de Carga de Datos: Implementa un formulario simple para permitir a los usuarios subir archivos de datos en formato CSV."),
                                        dbc.ListGroupItem("Interpretación Básica de Datos con ChatGPT: Usa la API de ChatGPT para leer las columnas del CSV y proporcionar una descripción general de los datos."),
                                        dbc.ListGroupItem("Interfaz de Usuario Básica: Muestra los resultados de la interpretación en una página de resultados simple."),
                                        dbc.ListGroupItem("Pruebas Unitarias: Escribe pruebas unitarias para asegurar que las funcionalidades básicas estén trabajando correctamente.")
                                    ],
                                    flush=True
                                ),
                                html.Br(),
                                html.P("Nivel 2: SemiSenior Developer"),
                                dbc.ListGroup(
                                    [
                                        dbc.ListGroupItem("Interpretación de Datos Mejorada con ChatGPT: ChatGPT debe identificar el tipo de información en cada columna (por ejemplo, numérica, categórica) y sugerir posibles análisis a realizar con los datos."),
                                        dbc.ListGroupItem("Interfaz de Usuario Mejorada: Permite que los usuarios puedan seleccionar columnas específicas del CSV para su interpretación.")
                                    ],
                                    flush=True
                                ),
                                html.Br(),
                                html.P("Nivel 3: Senior Developer"),
                                dbc.ListGroup(
                                    [
                                        dbc.ListGroupItem("Autenticación Simple: Permite que los usuarios ingresen una API Key de ChatGPT para pruebas a través de un campo en la interfaz de usuario."),
                                        dbc.ListGroupItem("Mejores Prácticas de Desarrollo: Asegúrate de que tu enfoque esté basado en las mejores prácticas de desarrollo y pruebas, incluyendo principios SOLID y patrones de diseño.")
                                    ],
                                    flush=True
                                ),
                                html.Br(),
                                html.P("Stack Tecnológico: Python (de preferencia Django)."),
                                html.P("Nota: Esta versión del reto se centra en la implementación de la funcionalidad clave. Los postulantes deben demostrar su capacidad para trabajar con la API de ChatGPT y desarrollar una interfaz de usuario simple. Los niveles más avanzados introducen mejoras incrementales en la interpretación de datos y la interacción del usuario. Las pruebas unitarias son un requerimiento obligatorio para todos los niveles para asegurar la calidad del código.", style={"font-weight": "bold"})
                            ],
                            lg=6,
                            md=10,
                            sm=12,
                            style={"padding": "40px", "background-color": "#f9f9f9", "border-radius": "10px"}
                        )
                    ],
                    style={"margin": "20px 0"}
                )

    return div

def startusa_frotend_react():
    div = dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H3("1. Sobre el puesto", style={"border-bottom": "2px solid #333", "padding-bottom": "10px"}),
                                html.P("Este puesto es para un cliente que es una startup en Estados Unidos, con un equipo global de colaboradores de diversos países. Estamos en busca de desarrolladores comprometidos y dinámicos para unirse a nuestro equipo de trabajo remoto."),
                                html.P("El entorno de trabajo en la startup es ágil y en constante evolución, lo que requiere adaptabilidad y la capacidad de trabajar bajo presión en situaciones de alto estrés. La comunicación en inglés es esencial, ya que estarás colaborando con colegas de diferentes partes del mundo."),
                                html.P("Trabajarás en un entorno de desarrollo ágil y entrega continua, participando en reuniones diarias (dailies) de lunes a viernes, donde se discuten y planifican las tareas a realizar."),
                                html.P("Es importante destacar que al ser un puesto remoto, recibirás tu remuneración en dólares y tendrás la flexibilidad de trabajar desde Perú."),
                                html.P([
                                    "Los rangos salariales para el puesto son:",
                                    html.Ul([
                                        html.Li("Medium Developer: $1500 - $2500"),
                                        html.Li("SemiSenior Developer: $2600 - $3800"),
                                        html.Li("Senior Developer: $3900 - $5000")
                                    ], style={"list-style-type": "square"})
                                ]),
                                html.P("Tu rango salarial dependerá de tu experiencia, habilidades demostradas en la resolución del reto y las negociaciones de las condiciones de trabajo."),
                                html.P("Si estás de acuerdo con los términos y te sientes emocionado por la oportunidad de trabajar en un ambiente internacional y dinámico, ¡adelante con el reto!", style={"font-weight": "bold"})
                            ],
                            lg=6,
                            md=10,
                            sm=12,
                            style={"padding": "40px", "background-color": "#f9f9f9", "border-radius": "10px"}
                        ),
                        dbc.Col(
                                    [
                                        html.H3("2. Reto técnico", style={"border-bottom": "2px solid #333", "padding-bottom": "10px"}),
                                        html.P("Objetivo General: Desarrollar una aplicación web o móvil que utilice las APIs de Trello como backend y React o React Native como marco de desarrollo frontend para crear un organizador de proyectos personales."),
                                        html.P("Nivel 1: Medium Developer"),
                                        dbc.ListGroup(
                                            [
                                                dbc.ListGroupItem("Interfaz de Tableros: Implementa una interfaz que liste todos los tableros de Trello del usuario."),
                                                dbc.ListGroupItem("Visualización de Listas y Tarjetas: Dado un tablero seleccionado, muestra las \"listas\" y \"tarjetas\" asociadas al tablero."),
                                                dbc.ListGroupItem("Creación de Tarjetas: Implementa la funcionalidad para crear una tarjeta proporcionando solo el campo \"nombre\"."),
                                                dbc.ListGroupItem("Interfaz de Usuario Básica: Desarrolla una interfaz de usuario simple que permita la visualización de tableros, listas y tarjetas, así como la creación de tarjetas.")
                                            ],
                                            flush=True
                                        ),
                                        html.Br(),
                                        html.P("Nivel 2: SemiSenior Developer"),
                                        dbc.ListGroup(
                                            [
                                                dbc.ListGroupItem("Mover Tarjetas entre Listas: Implementa la funcionalidad para que los usuarios puedan arrastrar y soltar tarjetas de cualquier lista a otra."),
                                                dbc.ListGroupItem("Interfaz de Usuario Mejorada: Optimiza la interfaz de usuario para que sea más intuitiva y atractiva, facilitando la navegación y gestión de tableros, listas y tarjetas.")
                                            ],
                                            flush=True
                                        ),
                                        html.Br(),
                                        html.P("Nivel 3: Senior Developer"),
                                        dbc.ListGroup(
                                            [
                                                dbc.ListGroupItem("Autenticación y Autorización: Implementa un sistema de autenticación y autorización para que los usuarios puedan acceder a sus tableros de Trello de forma segura."),
                                                dbc.ListGroupItem("Mejores Prácticas de Desarrollo: Asegúrate de que tu enfoque esté basado en las mejores prácticas de desarrollo y pruebas, incluyendo principios SOLID y patrones de diseño."),
                                                dbc.ListGroupItem("Despliegue y Optimización: Despliega tu aplicación en un entorno de producción y realiza las optimizaciones necesarias para garantizar un rendimiento óptimo.")
                                            ],
                                            flush=True
                                        ),
                                        html.Br(),
                                        html.P("Stack Tecnológico: React o React Native (de preferencia versiones recientes)."),
                                        html.P("Notas: Esta versión del reto se centra en la implementación de funcionalidades clave. Los postulantes deben demostrar su capacidad para trabajar con las APIs de Trello y desarrollar una interfaz de usuario utilizando React o React Native. Los niveles más avanzados introducen mejoras en la gestión de tarjetas y la interacción del usuario.", style={"font-weight": "bold"})
                                    ],
                                    lg=6,
                                    md=10,
                                    sm=12,
                                    style={"padding": "40px", "background-color": "#f9f9ff9", "border-radius": "10px"}
                                )
                    ],
                    style={"margin": "20px 0"}
                )

    return div




def tests_values(test):
    tests_values = {
                    "net_react_juntoz":net_react_juntoz(),
                    "startusa_backend_django":startusa_backend_django(),
                    "startusa_frotend_react":startusa_frotend_react(),
    }
    try:
        return tests_values[test]
    except:
        return "Test no encontrado"
