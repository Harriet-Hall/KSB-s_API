from flask import Flask, jsonify
from database import Ksb

app = Flask(__name__)


@app.route("/")
def ksbs():
    ksbs = Ksb.select()

    ksbs = [
        {
            "id": ksb.id,
            "type": ksb.ksb_type,
            "code": ksb.ksb_code,
            "description": ksb.description,
        }
        for ksb in ksbs
    ]
    return jsonify(ksbs)


@app.route("/knowledge")
def knowledge():
    
    knowledge_ksbs = Ksb.select().where(Ksb.ksb_type == "Knowledge")
    knowledge = [
        {
            "id": ksb.id,
            "type": ksb.ksb_type,
            "code": ksb.ksb_code,
            "description": ksb.description,
        }
        for ksb in knowledge_ksbs
    ]
    return jsonify(knowledge)
    
    
    

if __name__ == "__main__":
    app.run(debug=True)
