import json
from flask import Flask, jsonify, request
from database import Ksb
from utils.check_for_duplicates import check_for_duplicates
from utils.ksb_type_choices import KSB_TYPE_CHOICES
from peewee import DoesNotExist
import uuid

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
    request_json = json.loads(request.data)
    if check_for_duplicates(ksbs, request_json):
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


@app.delete("/<uuid_str>")
def delete_ksb(uuid_str):
        
    try:
        uuid_obj = uuid.UUID(uuid_str)
        ksb_to_delete = Ksb.get(Ksb.id == uuid_obj)

        if ksb_to_delete:
            ksb_to_delete.delete_instance()
            return jsonify({}), 204
        
    except DoesNotExist:
            return jsonify({"error": "ksb cannot be deleted as it does not exist in database"}), 404
    
    except ValueError:
        return jsonify({"error": "uuid is invalid"}), 404
        
       
             
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

@app.put("/<uuid_str>")
def update_ksb(uuid_str):
  
    request_json = json.loads(request.data)
    
 
    try: 
        
        uuid_obj = uuid.UUID(uuid_str)
        ksb_to_update = Ksb.get(Ksb.id == uuid_obj)
     
        if "ksb_type" in request_json:
            ksb_to_update.ksb_type = request_json["ksb_type"].capitalize()
            try:
                ksb_to_update.ksb_type_validator()
            except ValueError as value_error:
                return jsonify({"error": str(value_error)}), 400
            
            
        if "ksb_code" in request_json:    
            ksb_to_update.ksb_code = request_json["ksb_code"]
            try:
                ksb_to_update.ksb_code_validator()
            except ValueError as value_error:
                return jsonify({"error": str(value_error)}), 400
            
                
        if "description" in request_json:
            ksb_to_update.description = request_json["description"]
            try:
                ksb_to_update.ksb_description_validator()
            except ValueError as value_error:
                return jsonify({"error": str(value_error)}), 400
             
        ksbs = Ksb.select()
    
        if check_for_duplicates(ksbs, ksb_to_update):
            return jsonify({"error" : "Ksb already exists in database"}), 409
        else:
            ksb_to_update.save()

        updated_ksb = Ksb.get(Ksb.id == uuid_obj)
        return jsonify(
                {
                "id": updated_ksb.id,
                "type": updated_ksb.ksb_type,
                "code": updated_ksb.ksb_code,
                "description": updated_ksb.description,
            }), 200
       
    except DoesNotExist:
        return jsonify({"error": "ksb with that uuid does not exist in database"}), 404
    except ValueError:
        return jsonify({"error": "uuid is invalid"}), 404
             

if __name__ == "__main__":
    app.run(debug=True)
