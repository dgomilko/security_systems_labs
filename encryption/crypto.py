from base64 import b64encode, b64decode
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512
from encryption.keys import get_private_key, get_public_key

def encrypt(msg, pub_key):
  message = str.encode(msg)
  cipher = PKCS1_OAEP.new(pub_key)
  encrypted = cipher.encrypt(message)
  return b64encode(encrypted)

def decrypt(msg, priv_key):
  msg_decoded = b64decode(msg)
  cipher = PKCS1_OAEP.new(priv_key)
  decrypted = cipher.decrypt(msg_decoded)
  return decrypted.decode("utf-8")

def sign(msg, priv_key):
  if not isinstance(msg, bytes):
    msg = str.encode(msg)
  signer = PKCS1_v1_5.new(priv_key)
  digest = SHA512.new()
  digest.update(msg)
  signature = signer.sign(digest)
  return b64encode(signature)

def verify(msg, signature, pub_key):
  if not isinstance(msg, bytes):
    msg = str.encode(msg)
  signature_decoded = b64decode(signature)
  signer = PKCS1_v1_5.new(pub_key)
  digest = SHA512.new()
  digest.update(msg)
  return signer.verify(digest, signature_decoded)

def text_encryption(text, path, username):
  private_key = get_private_key(path, username)
  public_key = get_public_key(path, username)
  signature = sign(text, private_key)
  verified = verify(text, signature, public_key)
  if verified: return encrypt(text, public_key)

def text_decryption(text, path, username):
  private_key = get_private_key(path, username)
  public_key = get_public_key(path, username)
  signature = sign(text, private_key)
  verified = verify(text, signature, public_key)
  if verified: return decrypt(text, private_key)

def encrypt_file_contents(file, keys_path, username=None):
  with open(file) as f: text = f.read()
  return text_encryption(text, keys_path, username)

def decrypt_file_contents(file, keys_path, username=None):
  with open(file) as f: text = f.read()
  return text_decryption(text, keys_path, username)

def encrypt_file(file, keys_path, username=None):
  text = encrypt_file_contents(file, keys_path, username)
  if text is None: return None
  with open(file, 'w') as f: return f.write(text.decode("utf-8"))

def decrypt_file(file, keys_path, username=None):
  text = decrypt_file_contents(file, keys_path, username)
  if text is None: return None
  with open(file, 'w') as f: return f.write(text)
