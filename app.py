from flask import Flask, jsonify, request
from database import Ksb

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
        new_row = Ksb.create(**request.json)
        new_ksb = Ksb.select().where(
            Ksb.ksb_type == new_row.ksb_type,
            Ksb.ksb_code == new_row.ksb_code,
            Ksb.description == new_row.description,
        )
        if len(new_ksb) > 1:
            response = jsonify({"error" : "Ksb already exists in database"})
            response.status_code = 409
            return response
        
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
