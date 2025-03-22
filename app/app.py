import json
from flask_cors import CORS
from flask import Flask, jsonify, request
from .database import Ksb, Theme, ThemeKsb
from .utils.check_for_duplicates import check_for_duplicates
from .utils.check_update_is_valid import check_for_valid_updates
from .utils.ksb_type_choices import KSB_TYPE_CHOICES
from peewee import DoesNotExist
import uuid

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'




@app.get("/ksbs")
def get_ksbs():
    try:
     
        ksb_themes = ThemeKsb.select(ThemeKsb.ksb_id, Theme.theme_name).join(Theme).where(Theme.id == ThemeKsb.theme_id)
        ksb = [k.ksb_id.id for k in ksb_themes]
        print(ksb,"here")
        
        
        ksbs = [
            {
                "id": ksb.ksb_id.id,
                "type": ksb.ksb_id.ksb_type,
                "code": ksb.ksb_id.ksb_code,
                "description": ksb.ksb_id.description,
                "created_at": ksb.ksb_id.created_at,
                "updated_at": ksb.ksb_id.updated_at,
                "theme": ksb.theme_id.theme_name
            
            }
            for ksb in ksb_themes
        ] 
        print(ksbs, "ksbo")
        
        return jsonify(ksbs)
    
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500

@app.post("/ksbs/<ksb_type>")
def post_ksb(ksb_type):
      
    
    if ksb_type not in  KSB_TYPE_CHOICES:
        return  jsonify({"error": "endpoint does not exist"}), 404
        
    ksbs = Ksb.select()
    request_data = request.json
    request_dict = {"ksb_type" : ksb_type.capitalize(), 
                    "ksb_code": request_data["code"],
                    "description": request_data["description"]
                    }

    if check_for_duplicates(ksbs, request_dict):
        return jsonify({"error" : "Ksb already exists in database"}), 409

    else:
        try:
                  
            new_row = Ksb.create(**request_dict)

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
                    "created_at": ksb.created_at,
                    
                }
            ), 201

        except ValueError as value_error:
            return jsonify({"error": str(value_error)}), 400
        except Exception:
            return jsonify({"error": "Internal Server Error"}), 500

@app.delete("/ksbs/<uuid_str>")
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
        
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500    

             
@app.get("/ksbs/<ksb_type>")
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
                "created_at": ksb.created_at,
                "updated_at" : ksb.updated_at
                
            }
            for ksb in filtered_list
        ]
        return jsonify(ksb_list), 200
    
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500

@app.put("/ksbs/<uuid_str>")
def update_ksb(uuid_str):
  
    request_json = json.loads(request.data)
    
 
    try: 
        
        uuid_obj = uuid.UUID(uuid_str)
        ksb_to_update = Ksb.get(Ksb.id == uuid_obj)

     
        if "type" in request_json:
            ksb_to_update.ksb_type = request_json["type"].capitalize()
            try:
                ksb_to_update.ksb_type_validator()
            except ValueError as value_error:
                return jsonify({"error": str(value_error)}), 400
            
            
        if "code" in request_json:    
            ksb_to_update.ksb_code = request_json["code"]
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
        
        if check_for_valid_updates(ksbs, ksb_to_update):
            return jsonify({"error" : "Ksb already exists in database with matching value/s"}), 409
        else: 
            ksb_to_update.save() 
            updated_ksb = Ksb.get(Ksb.id == uuid_obj)
            
        return jsonify(
                {
                "id": updated_ksb.id,
                "type": updated_ksb.ksb_type,
                "code": updated_ksb.ksb_code,
                "description": updated_ksb.description,
                "created_at": updated_ksb.created_at,
                "updated_at" : updated_ksb.updated_at
                
            }), 200
       
    except DoesNotExist:
        return jsonify({"error": "ksb with that uuid does not exist in database"}), 404
    except ValueError:
        return jsonify({"error": "uuid is invalid"}), 404   
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500


@app.get("/ksbs/theme/<theme_name>")
def get_ksbs_by_theme(theme_name):
    try:
        name = theme_name.replace("-", " ")
        theme = Theme.get(theme_name = name)
        ksbs_from_chosen_theme = ThemeKsb.select(ThemeKsb.ksb_id).where(ThemeKsb.theme_id == theme.id)
        ksb_list = []
        for ksb in ksbs_from_chosen_theme:
            ksbs = Ksb.get(id = ksb.ksb_id) 
            ksb_list.append(ksbs)

 
        ksbs = [
            {
                "type": ksb.ksb_type,
                "code": ksb.ksb_code,
                "description": ksb.description,
                "updated_at" : ksb.updated_at
                
            }
            for ksb in ksb_list
        ]
        return jsonify(ksbs), 200
   
    except Exception:
        return jsonify({"error": "Internal Server Error"}), 500


@app.post("/ksbs/theme/<theme_name>")
def post_ksbs_to_themeksb(theme_name):
    request_data = request.json
    name = theme_name.replace("-", " ")
    theme = Theme.get(Theme.theme_name == name)
   
    ThemeKsb.create(ksb_id=request_data["ksb_id"], theme_id=theme.id)

        
    new_themeksb = ThemeKsb.get(ksb_id = request_data["ksb_id"], theme_id=theme.id)

    return jsonify(
        {
            "ksb_id" : new_themeksb.ksb_id.id,
            "theme_id" : new_themeksb.theme_id.id,
        } ), 201
    
    
    
    
    
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)