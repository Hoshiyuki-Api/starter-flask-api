from flask import Flask,request,make_response,jsonify,redirect,url_for,render_template
from flask_restful import Resource,Api,reqparse
import jwt,datetime,requests,json
from functools import wraps
from fake_useragent import UserAgent

app=Flask(__name__)
api=Api(app)
app.config["SECRET_KEY"] = "inirahasianegara"

@app.route('/')
def index():
    # Redirect to home/index.html
    return redirect(url_for('static', filename='index.html'))
	#return render_template('index.html')

@app.route('/download/igdl', methods=['GET'])
def download_igdl():
    url = request.args.get('url')
    if not url:
        return jsonify({
            "status": "error",
            "code": 404
            "message": "Masukkan Url"
        })
    api_response = requests.get("https://aemt.me/download/igdl?url=" + url).json()
        # Pastikan bahwa respons dari API memiliki kunci 'result'
     if 'result' in api_response:
          result_data = api_response['result'][0]  # Ambil data dari indeks pertama dalam list result

          return jsonify({
              "status": "success",
              "code": api_response.get('code', ''),  # Menggunakan get() untuk menghindari KeyError
              "creator": "AmmarBN",
              "result": [
                  {
                      "wm": result_data.get('wm', ''),
                      "thumbnail": result_data.get('thumbnail', ''),
                      "url": result_data.get('url', '')
                  }
              ]
          })
     else:
            # Jika kunci 'result' tidak ada, sesuaikan respons sesuai kebutuhan
          return jsonify({
              "status": "error",
              "message": "Invalid API response format"
          })

@app.route('/')
def display_image():
    api_url = 'https://api.lolhuman.xyz/api/random/sfw/waifu?apikey=Ichanzx'
    
    # Fetch image URL from the API
    response = requests.get(api_url)
    data = response.json()
    image_url = data.get('result', {}).get('image', '')

    # Render template with the image URL
    return render_template('waifu/waifu.html', image_url=image_url)

@app.route('/')
def index_bak():
	return render_template('index_bak.html')

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

class PinterestDl(Resource):
    def post(self):
        url = request.form.get("url")
        # Menggunakan .json() untuk mendapatkan respons sebagai objek Python
        post_pinterest = requests.get("https://api.betabotz.org/api/download/pinterest?url=" + url + "&apikey=Kontolodon").json()
        # Memastikan bahwa 'image' ada dalam respons JSON sebelum mencoba mengaksesnya
        if 'result' in post_pinterest:
            return {
                "Creator": "AmmarBN",
                "response": 200,
                "data":{
                    "image": post_pinterest['result']['data']['image'],
                    "title": post_pinterest['result']['data']['title']
                }
            }
        else:
            return {
                "response": "error not found",
                "mssg": 404
            }

class SpamCall1(Resource):
	def get(self):
		nomor=request.args.get("nomor")
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
api.add_resource(SpamCall1, "/api/call-tools", methods=["POST"])
api.add_resource(PinterestDl, "/api/pinterest", methods=["POST"])
if __name__ == "__main__":
    app.run(debug=True)
