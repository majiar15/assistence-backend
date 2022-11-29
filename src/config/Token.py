import io
import jwt
from datetime import datetime, timedelta, timezone

from config.import_schema import Admin_schema, Admins_schema, Admin, Teacher
def generar_fecha_vencimiento(dias=0, horas=0, minutos=0, segundos=0):
    fecha_actual = datetime.now(tz=timezone.utc)
    tiempo_vencimiento = timedelta(
        days=dias, hours=horas, minutes=minutos, seconds=segundos
    )
    fecha_vencimiento = datetime.timestamp(fecha_actual + tiempo_vencimiento)
    return Out_response(datos=fecha_vencimiento)


# Función para generar token
def generar_token(user_token):
    try:
        fecha_vencimiento = generar_fecha_vencimiento(segundos=8)["token"]
        payload = {
            "exp": fecha_vencimiento,
            "user_id": user_token,
        }
        print(f"Generando Token {payload}")
        
        encoded_jwt = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
        
        return Out_response(False, "Token generado exitosamente", datos=encoded_jwt)

    except Exception as err:
        
        return Out_response(True, err, err.args)


# Función para verificar el token
def verificar_token(token):
    try:
       
        token_verif = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms="HS256")
        if token_verif:
            print("token válido")
            
            return token_verif
        else:
            return Error_response(True, "Token Inválido", 101)
    except Exception as err:
        return Error_response(err, "Token expirado", 101)
    except jwt.ExpiredSignatureError as err:
        return Error_response(err, "Token expirado", 101)
    except jwt.exceptions.InvalidSignatureError as err:
        return Error_response(err, "Firma de Token inválida", 102)
    except jwt.exceptions.InvalidTokenError as err:
        return Error_response(err, "Token inválido", 102)
    except jwt.exceptions.DecodeError as err:
        return Error_response(err, "No se pudo decodificar el token", 103)
    except jwt.exceptions.InvalidKeyError as err:
        return Error_response(err, "LLave secreta de Token inválida", 102)
    except jwt.exceptions.InvalidAlgorithmError as err:
        return Error_response(err, "Algoritmo de Token inválido", 102)


def Out_response(
    error=False,
    mensaje="Operación\
    exitosa",
    datos=None,
):

    res = {
        "error": error,
        "mensaje": mensaje,
        "token": datos,
    }
    return res

from functools import wraps
import jwt
from flask import request, abort
from flask import current_app
import models

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401    
        try:

            data= verificar_token(token)
            # jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            print(data)
            
            current_admin=Admin.query.filter_by(admin_id=data["user_id"], active=True).first() 
            current_user = current_admin
            if current_admin is None:
                current_teacher=Teacher.query.filter_by(teacher_id=data["user_id"], active=True).first() 
                current_user = current_teacher
                if current_teacher is None:
                    return {
                        "message": "Invalid Authentication token!",
                        "data": None,
                        "error": "Unauthorized"
                    }, 401

        except Exception as e:
            print(str(e))
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e),
                "print":str(e)
            }, 500

        return f(*args, **kwargs)

    return decorated
# Funcion para capturar los errores de las excepciones


def Error_response(err, mensaje, codigo_error=None):

    if len(err.args) > 1:

        res = {
            "error": True,
            # "mensaje": f"Error interno en el servidor al procesar esta solicitud",
            "mensaje": f"{mensaje}",
            "token": f"""Codigo interno:{codigo_error}
\n

                Codigo Error: {err.args[0]}
\n

                Mensaje Error: {err.args[1]}
""",
        }

    else:

        res = {
            "error": True,
            "mensaje": mensaje,
            "data": {"Codigo interno": codigo_error, "Mensaje Error": err.args[0]},
        }

    return res
