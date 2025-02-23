from flask import Flask, jsonify, request
from database import Ksb
from utils import check_for_duplicates

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
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
            response = jsonify({"error" : "Ksb already exists in database"})
            response.status_code = 409
            return response

        else:
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


@app.route("/<ksb_type>")
def ksb_by_type(ksb_type):

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
