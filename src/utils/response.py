

def response(statusCode,message,data={}):
    return {
        "data":data,
        "message":message,
    }, statusCode