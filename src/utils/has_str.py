from hashlib import sha256

def has_str(srt):
    return sha256(srt.encode()).hexdigest() 

