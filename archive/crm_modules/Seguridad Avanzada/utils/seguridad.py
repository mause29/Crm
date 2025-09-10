import pyotp

def generar_2fa_secret():
    return pyotp.random_base32()

def verificar_2fa(secret, token):
    totp = pyotp.TOTP(secret)
    return totp.verify(token)
