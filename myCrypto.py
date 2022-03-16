from Crypto.Hash import SHA256
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from base64 import b64encode, b64decode


def sign(data: str, private: str):
	hash = SHA256.new(data.encode())
	key = ECC.import_key(encoded=private, curve_name="P-521")
	signer = DSS.new(key, "fips-186-3")
	signature = signer.sign(hash)
	encoded = b64encode(signature).decode("utf-8")
	return encoded


def verify(data: str, signature: str, public: str):
	hash = SHA256.new(data.encode())
	key = ECC.import_key(public)
	verifier = DSS.new(key, "fips-186-3")
	try:
		decoded = b64decode(signature.encode("utf-8"))
		verifier.verify(hash, decoded)
		return True
	except:
		return False