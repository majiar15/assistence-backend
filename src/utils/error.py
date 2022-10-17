

def errorResponse(statusCode,message,data={}):
    return {
        "StatusCode":statusCode,
        "data":data,
        "message":message,
    }