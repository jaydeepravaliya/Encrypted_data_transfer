from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from flask import Flask, request
import requests

app = Flask(__name__)
# to host it on different ip 
# we can add below line to command
# --host=127.0.0.11


# Generate RSA key pair
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()

# Endpoint to provide public key to client
@app.route('/public_key', methods=['GET'])
def get_public_key():
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()

# Endpoint to receive encrypted card details from client
@app.route('/card_details', methods=['POST'])
def receive_card_details():
    encrypted_card_details = request.data

    # Decrypt card details with private key
    card_details_bytes = private_key.decrypt(
        encrypted_card_details,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    card_details_str = card_details_bytes.decode()
    card_details = eval(card_details_str)  # Note: this is not a safe way to deserialize data

    # Send card details to bank server for payment
    # bank_response = requests.post('http://<bank_server_ip_address>/payment', json=card_details)
    bank_response = requests.post('http://127.0.0.3/payment', json=card_details)


    return bank_response.text


# if __name__ == '__main__':
#     app.run(host='192.168.1.34', port=5000, debug=True, threaded=False)