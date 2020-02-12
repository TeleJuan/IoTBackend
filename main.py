
# para correr, instalar las siguientes dependencias 

import logging
import json
import paho.mqtt.client as mqtt  
import pymysql.cursors
from flask import Flask
from flask import request, Response, jsonify
from flask_login import UserMixin
from flask_login import LoginManager
from flask_cors import CORS, cross_origin
from flask import after_this_request
from models import users

#Configuracion flask
app = Flask(__name__)
cors = CORS(app)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
app.config['CORS_HEADERS'] = 'Content-Type'
#login_manager = LoginManager(app)
#cliente mqtt
client = mqtt.Client("P1")  # create new instance
# configuracion log
logging.basicConfig(
    filename='service.log',
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# log inicial
logging.debug('Iniciando Servicio')


# variables importantes
broker_address = "localhost"
port = 1883

def on_message(client, userdata, msg):
    topic = msg.topic.split("/")
    logging.debug("Incoming message!")
    # TODO: dependiendo del topico se realizan diferentes acciones

#################### Implementacion login ####################
"""
@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None
"""

################### Funciones base de datos ####################
def connect_database():
    """
    Genera un cursor para ejecutar querys en la base de datos.
    """
    connection = pymysql.connect(host='localhost',
        user='juan',
        password='manzana',
        db='test',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

def exec_query(query): 
    """
    Ejecuta querys que no implican leer 
    """
    connection = connect_database()

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
        connection.commit()
    except Exception as error:
        logging.debug(error)

    finally:
        connection.close()

def get_conditions(data):
    """
    Convierte un diccionario con restricciones "where" en un string.
    """
    result= ""
    for j,k in data.items():
        if(str(type(k)) == "<class 'int'>"): result+= j + "=" + str(k) + " and "
        else: result+= j + "='" + k + "' and "
    result = result[:-5]
    return result

def get_info(data):
    """
    recibe un diccionario atributos y su correspondiente valor, los transforma en dos strings.
    """
    params = ""
    values = ""
    for j,k in data.items():
        params+= j + ","

        if(str(type(k)) == "<class 'int'>"): values+= str(k) +","
        else: values+= "'" + k + "'" + ","

    params = params[:-1]
    values = values[:-1]        

    return (params,values)

def insert_query(data,table):
    """
    Esta funcion inserta un registro con atributos en forma de diccionario(data) en la tabla especificada
    """
    info = get_info(data)
    query = "insert into %s(%s) values(%s)"%(table,info[0],info[1])
    exec_query(query)

def update_query(data,table,conditions=None):
    """
    Modifica registros en la tabla especificada, requiere un diccionario con los atributos a modificar
    con su correspondiente valor, y otro diccionario con las restricciones correspondientes
    """
    if(conditions!= None):conditions = get_conditions(conditions)
    result = ""
    for j,k in data.items():
        if(str(type(k)) == "<class 'int'>"): result+= j + "=" + str(k) + " , "
        else: result+= j + "='" + k + "' , "  
    
    result = result[:-2]
    if(conditions!= None):query = "update %s set %s where %s"%(table,result,conditions)
    else: query = "update %s set %s"%(table,result)

    exec_query(query)

def delete_query(table,conditions=None):
    """
    elimina registros de la tabla especificada que concuerden con las restricciones dadas.
    """
    if(conditions!= None):conditions = get_conditions(conditions)

    if(conditions!= None):query = "delete from %s where %s"%(table,conditions)
    else:query = "delete from %s"%(table)
    exec_query(query)

def read_query(params,table,conditions=None):
    """
        Lee los parametros indicados en params de la tabla especificada, siguiendo las restricciones entregadas en forma de diccionario
        params puede ser una lista con varios parametros, o un string con un asterisco para leer todos.
        ejemplo formato de salida: ( diccionario de diccionarios )

        {
            'fila_0': {
                'valor_1': 'hola', 
                'valor_2': 123, 
                'valor_3': '23'
            }, 
            
            'fila_1': {
                'valor_1': 'holaaaa', 
                'valor_2': 12, 
                'valor_3': '2334'
            }
        }

    """
    result = dict()
    if(conditions!= None):conditions = get_conditions(conditions)
    select = ""
    if params[0] != "*":
        for j in params:
            select+= j + ","
        select = select[:-1]
    else: select = "*"
    if(conditions!= None):query = "select %s from %s where %s"%(select,table,conditions) 
    else:query = "select %s from %s"%(select,table) 
    connection = connect_database()

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            i = 0
            for row in rows:
                result["fila_"+str(i)] = row
                i+=1
        connection.commit()
    except Exception as error:
        logging.debug(error)

    finally:
        connection.close()
    
    return result


########################## RUTAS API ##########################


#TODO: Definicion rutas
@app.route('/')
def home():
    return 'Hola Ubunlog'
"""
@app.route('/login', methods=['POST'])
def login():
    content = request.get_json()
    user = get_user(content['email'])
    if user is not None and user.check_password(content['password']):
        login_user(user, remember=form.remember_me.data)
"""        
@app.route('/api/device/switch',methods=['POST'])
def switch():
    content = request.get_json()
    if("serial" in content.keys()):
        topic= "down/%s/switch"%(content["serial"])
        payload = {
            "state":content["state"] 
        }
        client.publish(topic,json.dumps(payload))

#################### prueba para ajax con jquery ####################
@app.route('/test', methods=['GET'])
def get_test():

    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    # esto deberia sacarse de algun lugar dependiendo de donde se haga la peticion...
    jsonResp = {'hola': 4098, 'asdf': 4139}
    print(jsonResp)
    return jsonify(jsonResp)

@app.route('/test', methods=['POST'])
def post_test():
    print("llegó un post",request.get_data())
    # req data puede venit de donde sea
    req_data = { 
        "mensaje":"jaja"
    }
    if(request.is_json):
        content = request.get_json()
        # el contenido solo se imprime para verificar que llega bien (llega como bytes)
        print (content)
    # se envia la respuesta
    return Response(json.dumps(req_data, indent=4), mimetype='application/json')
############################################################

def main():
    client.on_message  = on_message
    client.connect(broker_address)  # connect to broker
    logging.debug("Conectando al broker")

    client.subscribe(topic="up/#",qos=2)

    client.loop_start()
    #app.run(host='localhost',port=8080)
    app.run(host='192.168.0.20',port=8080)
    while True:
        try:
            pass
        except KeyboardInterrupt:
            client.disconnect()
            print("Desconectando el cliente y saliendo")
            break
        except Exception as error:
            print(error)


"""
    PRUEBAS FUNCIONES MYSQL

table = "prueba"
data = {
    "valor_3":"castor",
    "valor_2":1245645,
}

conditions = {
    "valor_1":"hola"
}

# probar por separado

insert_query(data,table)

print(read_query("*",table))
update_query(data,table,conditions)
print(read_query("*",table))

"""
main()
