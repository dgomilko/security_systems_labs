from Crypto.Util import number
from Crypto.PublicKey import RSA
#from system_stats import KEY_LENGTH

PUB_NAME = 'pubkey.pem'
PRIV_NAME = 'privkey.pem'

def generate_prime():
  return number.getPrime(56)

def get_key_path(path, username, public):
  name = PUB_NAME if public else PRIV_NAME
  filename = f'{username}_{name}' if username is not None else name
  return f'{path}/{filename}'

def generate_key_pair(path, username=None):
  key = RSA.generate(4096)
  pub_path = get_key_path(path, username, public=True)
  priv_path = get_key_path(path, username, public=False)
  with open(priv_path, 'wb+') as f: f.write(key.exportKey('PEM'))
  pubkey = key.publickey()
  with open(pub_path, 'wb+') as f: f.write(pubkey.exportKey('PEM'))

def get_key(path, public, username):
  path = get_key_path(path, username, public)
  with open(path, 'r') as f: return RSA.importKey(f.read())

get_private_key = lambda path, username=None: get_key(path, False, username)
get_public_key = lambda path, username=None: get_key(path, True, username)
