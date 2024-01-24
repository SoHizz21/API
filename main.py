from flask import Flask,jsonify
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://Peerapat_Sent_work:u1LqjH7nGhbIlnTC@cluster0.aj79tau.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri)

app = Flask(__name__)


client.admin.command('ping')
print("Pinged your deployment. You successfully connected to MongoDB!")
db = client["students"]
collection = db["std_info"]
        
@app.route("/")
def Greet():
    return "<p>Welcome to Student Management API</p>" 

@app.route("/students",methods=["GET"])
def get_all_books():
    data = list(collection.find())
    return jsonify(data)
    

@app.route("/books/<int:book_id>",methods=["GET"])
def get_book(book_id):
    book=next( (b for b in books if b["id"]==book_id),None)
    if book:
        return jsonify(book)
    else:
        return jsonify({"error":"Book not found"}),404

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
''
