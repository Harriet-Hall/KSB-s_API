from base64 import decode
import json
from flask import Flask, abort, jsonify, request
from database import Ksb
from utils import check_for_duplicates, KSB_TYPE_CHOICES
from peewee import DoesNotExist


app = Flask(__name__)


@app.get("/")
def get_ksbs():

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


@app.post("/")
def post_ksb():

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
            return jsonify(
                {
                    "id": ksb.id,
                    "type": ksb.ksb_type,
                    "code": ksb.ksb_code,
                    "description": ksb.description,
                }
            ), 201

        except ValueError as value_error:
            return jsonify({"error": str(value_error)}), 400


@app.delete("/")
def delete_ksb():
        
    try:
        request_json = json.loads(request.data)
        ksb = Ksb.get(
        Ksb.ksb_code == request_json["ksb_code"],
        Ksb.ksb_type == request_json["ksb_type"].capitalize()
        )
        if ksb:
            ksb.delete_instance()
            return jsonify({}), 204
        
    except DoesNotExist:
            return jsonify({"error": "ksb cannot be deleted as it does not exist in database"}), 404
            
    except: 
        pass
       

            
@app.get("/<ksb_type>")
def get_ksb_by_type(ksb_type):

    if ksb_type not in  KSB_TYPE_CHOICES:
        return  jsonify({"error": "endpoint does not exist"}), 404
        
    try: 
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
        return jsonify(ksb_list), 200
    except:
        pass

@app.put("/<uuid>")
def update_ksb(uuid):
    request_json = json.loads(request.data)
    try: 
        
        ksb_to_update = Ksb.get(Ksb.id == uuid)
    
        if ksb_to_update:
          
            ksb_to_update.ksb_type = request_json["ksb_type"].capitalize()
            ksb_to_update.ksb_code = int(request_json["ksb_code"])
            ksb_to_update.description = request_json["description"]
            ksb_to_update.save()  
    
            updated_ksb = Ksb.get(Ksb.id == uuid)
            return jsonify(
                    {
                    "id": updated_ksb.id,
                    "type": updated_ksb.ksb_type,
                    "code": updated_ksb.ksb_code,
                    "description": updated_ksb.description,
                }), 200
       
    except DoesNotExist:
        return jsonify({"error": "ksb with that uuid does not exist in database"}), 404
            

if __name__ == "__main__":
    app.run(debug=True)
