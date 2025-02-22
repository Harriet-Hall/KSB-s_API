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


@app.route("/<ksb_type>")
def ksb_by_type(ksb_type):
    print(ksb_type.lower(), "lower")
    filtered_list = Ksb.select().where(Ksb.ksb_type == ksb_type.capitalize())
    print(filtered_list, "!!!!!!!!!!!!!")
    ksb_list = [
        {
            "id": ksb.id,
            "type": ksb.ksb_type,
            "code": ksb.ksb_code,
            "description": ksb.description,
        }
        for ksb in filtered_list
    ]
    return jsonify(ksb_list)
    
    
    

if __name__ == "__main__":
    app.run(debug=True)
