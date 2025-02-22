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


if __name__ == "__main__":
    app.run(debug=True)
