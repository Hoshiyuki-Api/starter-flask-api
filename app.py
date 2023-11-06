from flask import Flask
from fake_useragent import UserAgent
        
import os

app = Flask(__name__)
api=Api(app)

class RandomUa(Resource):
    def get(self):
        useragent=UserAgent()
        ua=useragent.random
        return ({
            "user-agent": ua,
            "response code": 200,
            "creator": "Ammar-Excuted"
        })
api.add_resource(RandomUa, "/uar", methods=["GET"])
if __name__ == "__main__":
    app.run(debug=True)
