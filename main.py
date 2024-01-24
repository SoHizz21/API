from flask import Flask,jsonify,request
from flask_basicauth import BasicAuth
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://Peerapat_Sent_work:u1LqjH7nGhbIlnTC@cluster0.aj79tau.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri)
app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME']='username'
app.config['BASIC_AUTH_PASSWORD']='password'
basic_auth = BasicAuth(app)

client.admin.command('ping')
db = client["students"]
collection = db["std_info"]
        
@app.route("/")
def Greet():
    return "<p>Welcome to Student Management API</p>" 

@app.route("/students",methods=["GET"])
@basic_auth.required
def get_all_books():
    data = list(collection.find())
    return jsonify(data)
    

@app.route("/students/<int:std_id>",methods=["GET"])
@basic_auth.required
def get_students(std_id):
    id = collection.find_one({"_id":str(std_id)})
    if not id:
        return jsonify({"error":"Student not found "}),404
    return jsonify(id)

@app.route("/students",methods=["POST"])
@basic_auth.required
def post_students():
    data = request.get_json();
    id = collection.find_one({"_id":data.get("_id")})
    if id:
        return jsonify({"error":"Cannot create new student"}),500
    collection.insert_one(data)
    return jsonify(data),200

@app.route("/students/<int:std_id>",methods=["PUT"])
@basic_auth.required
def put_students(std_id):
    data = request.get_json();
    id = collection.find_one({"_id":str(std_id)})
    if not id:
        return jsonify({"error":"Student not found"}),404
    collection.update_one({"_id": str(std_id)}, {"$set": data})
    return jsonify(data),200

@app.route("/students/<int:std_id>",methods=["DELETE"])
@basic_auth.required
def delete_students(std_id):
    id = collection.find_one({"_id":str(std_id)})
    if not id:
        return jsonify({"error":"Student not found"}),404
    collection.delete_one({"_id": str(std_id)})
    return jsonify({"message":"Student deleted successfully"}),200

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)