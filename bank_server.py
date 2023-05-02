from flask import Flask, request
# Import SqliteDatabase

# Setup SQLite database named 'bank.db' with table 'card_details' with columns 'card_number', 'cvv', 'expiry' and 'timestamp'
# (timestamp is the time when the card details were received by the bank server)
SqliteDatabase('bank.db').connect()
db = SqliteDatabase('bank.db')

class CardDetails(Model):
    card_number = CharField()
    cvv = CharField()
    expiry = CharField()
    timestamp = DateTimeField()

    class Meta:
        database = db


app = Flask(__name__)

# Endpoint to receive card details from shopping website for payment
@app.route('/payment', methods=['POST'])
def receive_payment():
    card_details = request.json
    # Store the card details to a SQLite database
    CardDetails.create(card_details)
    # Process payment here...
    return 'Payment successful'

