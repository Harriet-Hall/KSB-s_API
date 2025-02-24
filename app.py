from base64 import decode
import json
from flask import Flask, jsonify, request
from database import Ksb
from utils import check_for_duplicates, KSB_TYPE_CHOICES


app = Flask(__name__)


@app.route("/", methods=["GET", "POST", "DELETE"])
def ksbs():

    if request.method == "GET":

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

    elif request.method == "POST":
        ksbs = Ksb.select()
        
        if check_for_duplicates(ksbs, request):
            return jsonify({"error" : "Ksb already exists in database"}), 409

        else:
            try:

                new_row = Ksb.create(**request.json)

                new_ksb = Ksb.select().where(
                    Ksb.ksb_type == new_row.ksb_type,
                    Ksb.ksb_code == new_row.ksb_code,
                    Ksb.description == new_row.description,
                )

                
                ksb = new_ksb[0]
                response = jsonify(
                    {
                        "id": ksb.id,
                        "type": ksb.ksb_type,
                        "code": ksb.ksb_code,
                        "description": ksb.description,
                    }
                )

                response.status_code = 201
                return response
            except ValueError as value_error:
                return jsonify({"error": str(value_error)}), 400

    elif request.method == "DELETE":
        
        try:
            request_json = json.loads(request.data)
            ksb = Ksb.get(
            Ksb.ksb_code == request_json["ksb_code"],
            Ksb.ksb_type == request_json["ksb_type"].capitalize()
            )
            if ksb:
                ksb.delete_instance()
                return jsonify({}), 204
                        
        except:
            return jsonify({"error": "ksb does not exist"}), 404
    else:
        pass
            
     
@app.route("/<ksb_type>")
def ksb_by_type(ksb_type):

    if ksb_type not in  KSB_TYPE_CHOICES:
        return "endpoint does not exist", 404
        
        
    filtered_list = Ksb.select().where(Ksb.ksb_type == ksb_type.capitalize())

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
