from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import requests

# Generate RSA key pair
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()

# Encrypt card details with shopping website's public key
shopping_website_public_key_pem = requests.get('http://<shopping_website_ip_address>/public_key').text
shopping_website_public_key = serialization.load_pem_public_key(shopping_website_public_key_pem.encode())
card_details = {'card_number': '1234567890123456', 'cvv': '123', 'expiry': '12/23'}
card_details_bytes = str(card_details).encode()
encrypted_card_details = shopping_website_public_key.encrypt(
    card_details_bytes,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Send encrypted card details to shopping website
# requests.post('http://<shopping_website_ip_address>/card_details', data=encrypted_card_details)

requests.post('http://127.0.0.1/card_details', data=encrypted_card_details)

