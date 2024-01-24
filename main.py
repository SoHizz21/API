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
    

@app.route("/students/<int:std_id>",methods=["GET"])
def get_students(std_id):
    id = collection.find_one({"_id":str(std_id)})
    if not id:
        return jsonify({"error":"Student not found "}),404
    return jsonify(id)

@app.route("/students",method=["POST"])
def post_students():
    data = request.get_json();
    id = collection.find_one({"_id":data.get("_id")})
    if not id:
        return jsonify({"error":"Cannot create new student"}),500
    collection.insert_one(data)
    return jsonify(data)



if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)