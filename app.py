from flask import Flask,request,make_response,jsonify,redirect,url_for,render_template,send_file
from flask_restful import Resource,Api,reqparse
import jwt,datetime,requests,json,validators,random
from functools import wraps
from fake_useragent import UserAgent
from io import BytesIO

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
            "code": 404,
            "creator": "AmmarBN",
            "message": "Masukkan parameter URL"
        })

    api_response = requests.get(f"https://aemt.me/download/igdl?url={url}").json()
    if 'result' in api_response:
        result_data = api_response['result'][0]  # Ambil data dari indeks pertama dalam list result

        return jsonify({
            "code": api_response.get('code', ''),  # Menggunakan get() untuk menghindari KeyError
            "creator": "AmmarBN",
            "result": [
                {
                    "wm": result_data.get('wm', ''),
                    "thumbnail": result_data.get('thumbnail', ''),
                    "url": result_data.get('url', '')
                }
            ],
            "status": "success"
        }), 200, {'Content-Type': 'application/json; charset=utf-8'}
    else:
        # Jika kunci 'result' tidak ada, sesuaikan respons sesuai kebutuhan
        return jsonify({
            "message": "Format respons API tidak valid",
            "status": "error"
        }), 500, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/nsfw/nsfwml', methods=["GET"])
def show_random_image():
    json_links = ["https://telegra.ph/file/c1dad245e498b0353481c.jpg","https://telegra.ph/file/d5d031cf768b7f15b0124.jpg","https://telegra.ph/file/cf77cb63c36c531670468.jpg","https://telegra.ph/file/a70ac31f3396e317e0cf6.jpg","https://telegra.ph/file/b8f847b31c1d6d87a23f5.jpg","https://telegra.ph/file/8b063c809b4a911ee0016.jpg","https://telegra.ph/file/ba2e2d8d3f7f8d447ca73.jpg","https://telegra.ph/file/ecd55a833acd622792f67.jpg","https://telegra.ph/file/0351727b5b03ffef016ba.jpg","https://telegra.ph/file/574fa4efba68c6e54ab66.jpg","https://telegra.ph/file/8a67237ee679868bc4197.jpg","https://telegra.ph/file/f64edeec65da9b29f65bb.jpg","https://telegra.ph/file/9a3d501737a66b6e97353.jpg","https://telegra.ph/file/ccee3a4837b73eab157bf.jpg","https://telegra.ph/file/c4932ab71dafa8419aa8f.jpg","https://telegra.ph/file/60f473f877f24d80b926c.jpg","https://telegra.ph/file/acbb0f0e72e3df51d8aea.jpg","https://telegra.ph/file/21292e56997ca9084feab.jpg","https://telegra.ph/file/48f920d2746b97a2dd112.jpg","https://telegra.ph/file/7ae7ac27602c2aad60d7f.jpg","https://telegra.ph/file/dab8745bbf3496424a940.jpg","https://telegra.ph/file/06df6b37c80078cbe21e2.jpg","https://telegra.ph/file/723a2712449d9eba6f05f.jpg","https://telegra.ph/file/9c7e2c8a4d7863ad3b453.jpg","https://telegra.ph/file/831ac5911f83b10705171.jpg","https://telegra.ph/file/2cd98e857f50d95f02e18.jpg","https://telegra.ph/file/c6ff3f693ccfc1363fb6c.jpg","https://telegra.ph/file/723a2712449d9eba6f05f.jpg","https://telegra.ph/file/b08607c0316203dfd18d6.jpg","https://telegra.ph/file/cd4af91b43caa9721fa6d.jpg","https://telegra.ph/file/9428619ef6e70c2417b81.jpg","https://telegra.ph/file/a12621be8d2c6153c3c3c.jpg","https://telegra.ph/file/b949c94953ac71d434b36.jpg","https://telegra.ph/file/51624a2cecc4a69d625d6.jpg","https://telegra.ph/file/1db376e3ea88659ac4339.jpg","https://telegra.ph/file/a29efbafb3972f537add1.jpg","https://telegra.ph/file/7e3e234957e7518cc2b01.jpg","https://telegra.ph/file/302ddda332b22b595d499.jpg","https://telegra.ph/file/2ed820fb3c06d1135f3a7.jpg","https://telegra.ph/file/b36a1a12cc25b237bebc7.jpg","https://telegra.ph/file/d0808a6d8b6df241648eb.jpg","https://telegra.ph/file/a4ee2bd74789f81739d10.jpg","https://telegra.ph/file/14a159a9ebf3f3011e7be.jpg","https://telegra.ph/file/b7f6b2e6133c8e00ea183.jpg","https://telegra.ph/file/5ecaf535420050ff69424.jpg","https://telegra.ph/file/a3acf9176f37ea46e603d.jpg","https://telegra.ph/file/87d6ca55b0b5c11f82b7b.jpg","https://telegra.ph/file/4abdb85e99c7095c7b776.jpg","https://telegra.ph/file/f5c3ef844a722504ed2b1.jpg","https://telegra.ph/file/d4915000bf8631ce45a89.jpg","https://telegra.ph/file/897cc005abe2ed2af8ca9.jpg","https://telegra.ph/file/ef943a03d5fe87f1b8d87.jpg"]
    try:
        random_image_url = random.choice(json_links)
        image_response = requests.get(random_image_url)
        
        if image_response.status_code == 200:
            image_bytes = image_response.content
            return send_file(BytesIO(image_bytes), mimetype='image/jpeg')

        return jsonify({"error": "Failed to retrieve and display the image."}), 500

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

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

@app.route('/api/call', methods=['POST'])
def spam_call():
    nomor = request.args.get("nomor")
    if not nomor: 
        return jsonify({
            "message": "nomor tidak valid (8xxxx)",
            "response code": 404
        })

	xsrf = requests.get("https://magneto.api.halodoc.com/api/v1/users/status").cookies.get_dict()
	headhaldoc = {"referer": "https://www.halodoc.com","content-type": "application/json","x-xsrf-token": xsrf['XSRF-TOKEN']}
	paylodhaldoc = {"phone_number": "+62"+nomor,"channel": "voice"}
	cokihaldoc = {"cookie": '_gcl_au=1.1.935637007.1686465186; _gid=GA1.2.1888372629.1686465187; ab.storage.deviceId.1cc23a4b-a089-4f67-acbf-d4683ecd0ae7={"g":"9ade8176-03c1-dd87-f8d7-c0c3f60f861a","c":1686465187381,"l":1686465187381}; XSRF-TOKEN='+xsrf['XSRF-TOKEN']+'; afUserId=31b1ff72-9c27-4492-a787-7a895c0d422e-p; AF_SYNC=1686465191318; _ga_02NBJNEKVH=GS1.1.1686465187.1.1.1686465223.0.0.0; amp_394863=WECZG4ZhC4dZKUWVGE4Ogh...1h2kii76k.1h2kiiai8.3.0.3; ab.storage.sessionId.1cc23a4b-a089-4f67-acbf-d4683ecd0ae7={"g":"c13c57ed-4fbf-80d3-7b17-19eb5a8fcedc","e":1686467027367,"c":1686465187365,"l":1686465227367}; _ga=GA1.2.1084460534.1686465187'}
	response = requests.post("https://magneto.api.halodoc.com/api/v1/users/authentication/otp/requests",headers=headhaldoc,data=json.dumps(paylodhaldoc),cookies=cokihaldoc).json()
	if 'otp_id' in response:
		return jsonify({
			"response":"success",
			"message":f"Berhasil Mengirim Call Ke {nomor}",
			"creator":"AmmarBN"
		})
	else:
		return jsonify({
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
