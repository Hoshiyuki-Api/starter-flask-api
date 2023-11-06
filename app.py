from flask import Flask,request,make_response,jsonify
from flask_restful import Resource,Api
import jwt,datetime, redirect, url_for
from functools import wraps
from fake_useragent import UserAgent

app=Flask(__name__)
api=Api(app)
app.config["SECRET_KEY"] = "inirahasianegara"

def kunci_halaman(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token=request.args.get('token')
        if not token:
            return make_response(jsonify({
                "mssg":"Token not valid !!!"
            }), 404)

        try:
            output=jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except:
            return make_response(jsonify({"mssg":"Token Not Valid !!!!!"}))
        return f(*args, **kwargs)
    return decorator

class LoginUser(Resource):
    def post(self):
        user=request.form.get('username')
        pas=request.form.get('password')

        if user and pas == 'superadmin':
            token=jwt.encode(
                {
                    "username":user,
                    "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
                }, app.config["SECRET_KEY"],algorithm="HS256"
            )
            return jsonify({
                "token": token,
                "mssg": "Success Login",
                "response code": 200
            })
            
        return jsonify({"mssg": "Login terlebih dahulu !"})

class Dashboard(Resource):
    @kunci_halaman
    def get(self):
        return jsonify({
            "mssg":"Halo Admin, Rest Flask Berhasil dibuat ©Dusttale"
        })

class HomePage(Resource):
    def get(self):
        return jsonify({"mssg":"Halo Admin, Rest Flask Berhasil dibuat ©Dusttale"})

class Kontol(Resource):
    def get(self):
        return jsonify({"mssg":"Muka Lu Kaya Kontol:V"})

class RandomUa(Resource):
    def get(self):
        useragent=UserAgent()
        ua=useragent.random
        return ({
            "user-agent": ua,
            "response code": 200,
            "creator": "Ammar-Excuted"
        })


api.add_resource(LoginUser, "/apikey/login", methods=["POST"])
api.add_resource(Dashboard, "/apikey/dashboard", methods=["GET"])
api.add_resource(HomePage, "/apikey", methods=["GET"])
api.add_resource(RandomUa, "/api/user-agent", methods=["GET"])
api.add_resource(Kontol, "/testing", methods=["GET"])
if __name__ == "__main__":
    app.run(debug=True)
