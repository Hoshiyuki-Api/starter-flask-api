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


@app.route('/download/tiktok', methods=["GET"])
def download_tiktok():
    url = request.args.get('url')

    if not url:
        return jsonify({
            "code": 404,
            "creator": "AmmarBN",
            "message": "Masukkan parameter URL"
        })

    api_response = requests.get(f"https://aemt.me/download/tikdl?url={url}").json()

    if api_response.get('status') and api_response.get('code') == 200:
        result_data = api_response['result']
        video_info = result_data['info_video']
        author_info = result_data['author_info']
        url_info = result_data['url']

        json_data = [{
            "code": 200,
            "creator": "AmmarBN",
            "status": "success",
            "data": {
                "title": video_info['title'],
                "region": video_info['region'],
                "thumbnail": video_info['thumbnail'],
                "duration": video_info['duration'],
                "metrics": {
                    "total_download": video_info['total_download'],
                    "total_play": video_info['total_play'],
                    "total_share": video_info['total_share'],
                    "total_comment": video_info['total_comment'],
                },
                "author": {
                    "nickname": author_info['nickname'],
                    "id": author_info['id'],
                    "profile": author_info['profile'],
                },
                "url": {
                    "nowm": url_info['nowm'],
                    "wm": url_info['wm'],
                    "audio": url_info['audio'],
                }
            }
        }]

	return (json_data)
    else:
        return jsonify({
            "error": {
                "code": 500,
                "message": "Format respons API tidak valid"
            }
        }), 500, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/nsfw/nsfwml', methods=["GET"])
def show_random_image():
    json_links = ["https://telegra.ph/file/c1dad245e498b0353481c.jpg","https://telegra.ph/file/d5d031cf768b7f15b0124.jpg","https://telegra.ph/file/cf77cb63c36c531670468.jpg","https://telegra.ph/file/a70ac31f3396e317e0cf6.jpg","https://telegra.ph/file/b8f847b31c1d6d87a23f5.jpg","https://telegra.ph/file/8b063c809b4a911ee0016.jpg","https://telegra.ph/file/ba2e2d8d3f7f8d447ca73.jpg","https://telegra.ph/file/ecd55a833acd622792f67.jpg","https://telegra.ph/file/0351727b5b03ffef016ba.jpg","https://telegra.ph/file/574fa4efba68c6e54ab66.jpg","https://telegra.ph/file/8a67237ee679868bc4197.jpg","https://telegra.ph/file/f64edeec65da9b29f65bb.jpg","https://telegra.ph/file/9a3d501737a66b6e97353.jpg","https://telegra.ph/file/ccee3a4837b73eab157bf.jpg","https://telegra.ph/file/c4932ab71dafa8419aa8f.jpg","https://telegra.ph/file/60f473f877f24d80b926c.jpg","https://telegra.ph/file/acbb0f0e72e3df51d8aea.jpg","https://telegra.ph/file/21292e56997ca9084feab.jpg","https://telegra.ph/file/48f920d2746b97a2dd112.jpg","https://telegra.ph/file/7ae7ac27602c2aad60d7f.jpg","https://telegra.ph/file/dab8745bbf3496424a940.jpg","https://telegra.ph/file/06df6b37c80078cbe21e2.jpg","https://telegra.ph/file/723a2712449d9eba6f05f.jpg","https://telegra.ph/file/9c7e2c8a4d7863ad3b453.jpg","https://telegra.ph/file/831ac5911f83b10705171.jpg","https://telegra.ph/file/2cd98e857f50d95f02e18.jpg","https://telegra.ph/file/c6ff3f693ccfc1363fb6c.jpg","https://telegra.ph/file/723a2712449d9eba6f05f.jpg","https://telegra.ph/file/b08607c0316203dfd18d6.jpg","https://telegra.ph/file/cd4af91b43caa9721fa6d.jpg","https://telegra.ph/file/9428619ef6e70c2417b81.jpg","https://telegra.ph/file/a12621be8d2c6153c3c3c.jpg","https://telegra.ph/file/b949c94953ac71d434b36.jpg","https://telegra.ph/file/51624a2cecc4a69d625d6.jpg","https://telegra.ph/file/1db376e3ea88659ac4339.jpg","https://telegra.ph/file/a29efbafb3972f537add1.jpg","https://telegra.ph/file/7e3e234957e7518cc2b01.jpg","https://telegra.ph/file/302ddda332b22b595d499.jpg","https://telegra.ph/file/2ed820fb3c06d1135f3a7.jpg","https://telegra.ph/file/b36a1a12cc25b237bebc7.jpg","https://telegra.ph/file/d0808a6d8b6df241648eb.jpg","https://telegra.ph/file/a4ee2bd74789f81739d10.jpg","https://telegra.ph/file/14a159a9ebf3f3011e7be.jpg","https://telegra.ph/file/b7f6b2e6133c8e00ea183.jpg","https://telegra.ph/file/5ecaf535420050ff69424.jpg","https://telegra.ph/file/a3acf9176f37ea46e603d.jpg","https://telegra.ph/file/87d6ca55b0b5c11f82b7b.jpg","https://telegra.ph/file/4abdb85e99c7095c7b776.jpg","https://telegra.ph/file/f5c3ef844a722504ed2b1.jpg","https://telegra.ph/file/d4915000bf8631ce45a89.jpg","https://telegra.ph/file/897cc005abe2ed2af8ca9.jpg","https://telegra.ph/file/ef943a03d5fe87f1b8d87.jpg"]
    try:
        random_image_url = random.choice(json_links)
        image_response = requests.get(random_image_url)
        
        if image_response.status_code == 200:
            image_bytes = image_response.content
            return send_file(BytesIO(image_bytes), mimetype='image/jppeg')

        return jsonify({"error": "Failed to retrieve and display the image."}), 500

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/anime/waifu', methods=["GET"])
def show_waifu():
    json_rwaifu= [        "https://i.pinimg.com/736x/8e/b2/06/8eb206322336c1e107c187fe338c42f5.jpg",
        "https://i.pinimg.com/474x/8a/eb/f8/8aebf8c8cd83c4a5a7cd9b893a97614f.jpg",
        "https://i.pinimg.com/originals/cc/fe/31/ccfe31df09fbeb8438ffb1268a672b03.png",
        "https://i.pinimg.com/originals/39/d1/df/39d1df920c01a788c858c333232e11d4.png",
        "https://i.pinimg.com/originals/1d/d4/63/1dd463f45c2d4680543253f32818b56f.jpg",
        "https://i.pinimg.com/736x/42/88/f1/4288f17ee25b909430fb7e707d961d0b.jpg",
        "https://i.pinimg.com/474x/be/4a/83/be4a83aa8f4459c65ac57fd536f71baa.jpg",
        "https://i.pinimg.com/originals/1f/04/33/1f04330c19ca1beb531235ac299189c8.png",
        "https://i.pinimg.com/originals/9f/d4/74/9fd4744644230aa520a9dfe2ea24d38d.jpg",
        "https://i.pinimg.com/474x/0b/cb/0b/0bcb0b81d2d5a914b4baae02ce89fef9.jpg",
        "https://i.pinimg.com/originals/90/b3/fb/90b3fb0525ea88bf2214bcd31624e093.png",
        "https://i.pinimg.com/originals/a9/b7/5f/a9b75f3fdd6b08d1113f6910dc1bedb7.jpg",
        "https://i.pinimg.com/originals/f1/ea/fd/f1eafdb8526cf1d73f1156849b2ebef7.jpg",
        "https://i.pinimg.com/originals/50/38/98/503898e84962573df440773b224a9d04.jpg",
        "https://i.pinimg.com/originals/d6/51/a8/d651a8546d44aa0f2ca16e7ec610ee25.jpg",
        "https://i.pinimg.com/564x/51/64/35/51643592f8ef433690a6d4f6756ed30f.jpg",
        "https://i.pinimg.com/originals/46/c7/4d/46c74db33dc44bf5e0b37110cb268d27.jpg",
        "https://i.pinimg.com/originals/1c/73/3b/1c733b10bfc31b42e4b805cffa89def7.jpg",
        "https://i.pinimg.com/originals/0a/7c/f4/0a7cf44f2252b098b210d67fe8f94d9d.jpg",
        "https://i.pinimg.com/474x/41/64/60/4164604df227416f5622db5ba1c175ba.jpg",
        "https://i.pinimg.com/originals/80/a9/2d/80a92d9bf7123b4906158c5a63d94ff0.jpg",
        "https://i.pinimg.com/originals/c1/cf/d6/c1cfd6446624ab90eb95e9e21ee6870f.png",
        "https://i.pinimg.com/736x/44/62/a3/4462a3cf3792a8cf12587fd7875d75bc.jpg",
        "https://i.pinimg.com/originals/de/96/a4/de96a4ee3ad09df91a60aaf580b2a481.jpg",
        "https://i.pinimg.com/originals/22/44/23/224423878ca22cee25ed97fe9859e0f5.png",
        "https://i.pinimg.com/originals/61/16/db/6116dbfdf899dd1f3551bf4c533e43c2.jpg",
        "https://i.pinimg.com/originals/ea/45/cb/ea45cbbbc0b4d78d5446dc4946944ba7.jpg",
        "https://i.pinimg.com/originals/c2/c1/9f/c2c19f5b8c573a3493589add1087a0af.jpg",
        "https://i.pinimg.com/originals/b5/62/df/b562df9c721a3898b72eaaf0a9b3abca.png",
        "https://i.pinimg.com/736x/f1/ce/db/f1cedb200dfab458da7ae8077c873b52.jpg",
        "https://i.pinimg.com/474x/e8/f7/a3/e8f7a39d3f74c3514355850e4b9dc24b.jpg",
        "https://i.pinimg.com/736x/54/e2/18/54e21838e0fc0f0f933d87354a4e244d.jpg",
        "https://i.pinimg.com/originals/0e/ba/1a/0eba1a593d883c50cca095848cfb8722.jpg",
        "https://i.pinimg.com/originals/1e/a4/a6/1ea4a60fd6543b2f78f7d070f44f45e9.jpg",
        "https://i.pinimg.com/564x/89/81/89/8981895db9e17b81cd58d0c467c71cf4.jpg",
        "https://i.pinimg.com/280x280_RS/21/85/cd/2185cdb9d25d38ea544eb4ac8159cf1f.jpg",
        "https://i.pinimg.com/474x/9e/c1/54/9ec154489de01ba05a25a1072ed7882d.jpg",
        "https://i.pinimg.com/originals/31/5c/bd/315cbd1ac25c4d4cdddc3638e466eb25.jpg",
        "https://i.pinimg.com/564x/55/f4/00/55f4004efced0fff60e51bd8dd680953.jpg",
        "https://i.pinimg.com/originals/a4/c0/3a/a4c03ab8447c56f400b9b951fbae3b1d.jpg",
        "https://i.pinimg.com/originals/53/d4/94/53d4949d971e143cdef3fb66746b11b8.jpg",
        "https://i.pinimg.com/originals/01/8b/a1/018ba1ad7093f1171e2aded2e3a4a699.jpg",
        "https://i.pinimg.com/736x/88/81/f7/8881f70ea7baf030120559b04ad1146e.jpg",
        "https://i.pinimg.com/originals/b9/50/83/b9508355aed683ece54ee4f4d703aa08.jpg",
        "https://i.pinimg.com/originals/39/13/11/3913117585b2ffe4102619766822182b.jpg",
        "https://i.pinimg.com/originals/ae/9f/4f/ae9f4f0232cde20d846c114591a371d9.jpg",
        "https://i.pinimg.com/originals/df/56/7e/df567e0a14ee48f9445eab94c2804c24.jpg",
        "https://i.pinimg.com/736x/3a/1e/f1/3a1ef1b776cbf4def64890eaf6c0aa53.jpg",
        "https://i.pinimg.com/originals/8d/fe/54/8dfe546c883aae6099670e8a7a9f3521.jpg",
        "https://i.pinimg.com/736x/9a/52/24/9a52246d7114dad728cd9903b26328d6.jpg",
        "https://i.pinimg.com/564x/75/aa/74/75aa7438dc2756d1b4fe6e8d41ddb2c0.jpg",
        "https://i.pinimg.com/736x/e1/f5/d5/e1f5d591f6c39dc23d02e33b4956a269.jpg",
        "https://i.pinimg.com/564x/63/24/fb/6324fbf1f2d090fa33d2fc2554a0da32.jpg",
        "https://i.pinimg.com/736x/24/8a/41/248a415c9ba2870d9d70fa983269e7e9.jpg",
        "https://i.pinimg.com/736x/6a/1d/2b/6a1d2b33590b57cee2a2cf863b79895e.jpg",
        "https://i.pinimg.com/736x/2f/fa/92/2ffa923ad047567126f374861a338523.jpg",
        "https://i.pinimg.com/736x/ee/87/43/ee874395bf14a8d3d4df5925efcfdb05.jpg",
        "https://i.pinimg.com/originals/92/94/60/929460a690114f65cead93ea5ec57535.jpg",
        "https://i.pinimg.com/originals/cd/31/8c/cd318cf0ac622d1281b7616c9c87e42a.png",
        "https://i.pinimg.com/originals/e8/8e/ed/e88eedaaf2c903c922121c39faf49d6a.png",
        "https://i.pinimg.com/564x/99/43/a2/9943a261d188f048b89db41965b9715e.jpg",
        "https://i.pinimg.com/736x/c1/0c/f2/c10cf211537491a3c1383a7bbd539d38.jpg",
        "https://i.pinimg.com/originals/1d/a6/1a/1da61a5df4a31dd394758b035b17320e.jpg",
        "https://i.pinimg.com/736x/fb/63/d3/fb63d39b4b4aef75f32e4e7d3b67aac3.jpg",
        "https://i.pinimg.com/originals/c4/4b/5f/c44b5fa12edf9ea977f34f0f70414430.jpg",
        "https://i.pinimg.com/736x/03/f2/66/03f26670d5e3040d5ee5cd4f2b032fef.jpg",
        "https://i.pinimg.com/originals/10/d2/24/10d224ab1afae97e058fc9044d5a7e49.jpg",
        "https://i.pinimg.com/originals/93/c6/fb/93c6fbaf62f8b797eea55f7ae79e356d.jpg",
        "https://i.pinimg.com/originals/4d/f6/5b/4df65bb4809890faab894e8e8dff40c1.jpg",
        "https://i.pinimg.com/originals/f0/fe/31/f0fe31397de8e5865b7930d081f1bc1d.jpg",
        "https://i.pinimg.com/originals/8d/cd/e8/8dcde89be14c3810729dbf565f7ccb53.png",
        "https://i.pinimg.com/736x/c3/93/08/c39308900e619b45c4c9f449709c9e95.jpg",
        "https://i.pinimg.com/originals/cb/c6/42/cbc64270e6e5f387f85a3177e1c167ff.jpg",
        "https://i.pinimg.com/originals/07/0d/5c/070d5c4a6ca69d819f37b8ef112eafd6.jpg",
        "https://i.pinimg.com/474x/96/0a/b8/960ab83f5299f79064adb16a2e361189.jpg",
        "https://i.pinimg.com/originals/ea/7c/7c/ea7c7cafb58cef706d0949f1ca6d7149.png",
        "https://i.pinimg.com/originals/3f/fa/9a/3ffa9ad68d5e691b1669b11844483ef0.jpg",
        "https://i.pinimg.com/736x/ef/6f/21/ef6f217ed5d203eb3907ea6b8ef24de7.jpg",
        "https://i.pinimg.com/736x/28/a8/af/28a8afefe43210d14cdd541700a65491.jpg",
        "https://i.pinimg.com/474x/fd/7d/cc/fd7dccdac18b43774c1e42f05f50afa0.jpg",
        "https://i.pinimg.com/originals/00/47/9a/00479aac1d7af8b996018d89f85e7f0b.jpg",
        "https://i.pinimg.com/originals/15/ba/c0/15bac04a0012fe79ca8959eea5138f4e.jpg",
        "https://i.pinimg.com/originals/81/2e/53/812e53850439a2793a36323dd963257c.jpg",
        "https://i.pinimg.com/736x/7c/42/8e/7c428e95cced74b3747d28bb503a2723.jpg",
        "https://i.pinimg.com/originals/ec/e1/05/ece105e7dc8627be78acf85787838edb.png",
        "https://i.pinimg.com/originals/33/42/16/3342165641bb4bcdd8d86a3960572e47.jpg",
        "https://i.pinimg.com/originals/9e/29/d5/9e29d5bf3a4ca9e4b9c11084cf8bd8ab.jpg",
        "https://i.pinimg.com/originals/0d/00/aa/0d00aacaba14ce204a223a941be1ffd2.jpg",
        "https://i.pinimg.com/originals/cf/f1/ed/cff1edc018314b7696d62389738737cd.jpg",
        "https://i.pinimg.com/originals/f9/cb/3c/f9cb3cc2d9630a06d82f48fbaf2daa11.jpg",
        "https://i.pinimg.com/originals/7e/83/d5/7e83d5acca7261cb2feacdc6df8ad3ff.jpg",
        "https://i.pinimg.com/originals/a4/07/c1/a407c1c94fe7b4cab1f205fad5910286.jpg",
        "https://i.pinimg.com/736x/06/3c/ba/063cbaecd700e9151a9787c945283286.jpg",
        "https://i.pinimg.com/736x/44/fc/7a/44fc7a984e56513f6b736d5825e9bf2a.jpg",
        "https://i.pinimg.com/736x/58/c0/8d/58c08d72caaa4c37f3da9ec6ce01b647.jpg",
        "https://i.pinimg.com/originals/75/c5/ee/75c5eef08118c2108b1ed670b2ed5aac.jpg",
        "https://i.pinimg.com/originals/d1/94/e1/d194e11e1736f38d447d29d87911e094.png",
        "https://i.pinimg.com/736x/98/60/66/9860667c468c7306789755dae55b0447.jpg",
        "https://i.pinimg.com/originals/ab/ae/f3/abaef3b76f0c0e9295d88af4214376ec.jpg",
        "https://i.pinimg.com/236x/13/5f/c0/135fc027dde72db0fce7b060c721fc40.jpg"]
    try:
        random_image_url = random.choice(json_rwaifu)
        image_response = requests.get(random_image_url)

        if image_response.status_code == 200:
            image_bytes = image_response.content
            return send_file(BytesIO(image_bytes), mimetype='image/jpeg')

        return jsonify({"error": "Failed to retrieve and display the image."}), 500

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/anime/kurumi', methods=["GET"])
def show_loli():
    json_loli = ["https://i.imgur.com/cvqoK7l.jpg",
  "https://i.imgur.com/r1rm2ry.jpg",
  "https://i.imgur.com/8XO7t9a.jpg",
  "https://i.imgur.com/rTLpecf.jpg",
  "https://i.imgur.com/l9of06d.jpg",
  "https://i.imgur.com/GSegIuQ.jpg",
  "https://i.imgur.com/nSwNlyf.jpg",
  "https://i.imgur.com/iWhZIYl.jpg",
  "https://i.imgur.com/53x02Cj.jpg",
  "https://i.imgur.com/kqrgbGx.jpg",
  "https://i.imgur.com/p9rFiqZ.jpg",
  "https://i.imgur.com/Fr1Biar.jpg",
  "https://i.imgur.com/Y0pOrf4.jpg",
  "https://i.imgur.com/DLbggpI.jpg",
  "https://i.imgur.com/wQWKt8t.jpg",
  "https://i.imgur.com/bqm2ror.jpg",
  "https://i.imgur.com/YjdCC5T.jpg",
  "https://i.imgur.com/JIsiLyr.jpg",
  "https://i.imgur.com/smwHPTJ.jpg",
  "https://i.imgur.com/Rj7btya.jpg",
  "https://i.imgur.com/rvbxepM.jpg",
  "https://i.imgur.com/RNU9BjN.jpg",
  "https://i.imgur.com/sXWfHxx.jpg",
  "https://i.imgur.com/4hgUEny.jpg",
  "https://i.imgur.com/rQNFNIR.jpg",
  "https://i.imgur.com/NIkfoSt.jpg",
  "https://i.imgur.com/gXJCV7E.jpg",
  "https://i.imgur.com/i8pWglI.jpg",
  "https://i.imgur.com/pTgKmHa.jpg",
  "https://i.imgur.com/T5QtZ9I.jpg",
  "https://i.imgur.com/gIHmi7S.jpg",
  "https://i.imgur.com/U3MCtzx.jpg",
  "https://i.imgur.com/5hJCG2f.jpg",
  "https://i.imgur.com/OzBgd1W.jpg",
  "https://i.imgur.com/3TvSX1i.jpg",
  "https://i.imgur.com/b2MkoYM.jpg",
  "https://i.imgur.com/Dtru3fp.jpg",
  "https://i.imgur.com/vkqLf9v.jpg",
  "https://i.imgur.com/b1vBRTV.jpg",
  "https://i.imgur.com/eMv5vkT.jpg",
  "https://i.imgur.com/1kbChJv.jpg",
  "https://i.imgur.com/hQFq7aG.jpg",
  "https://i.imgur.com/bWbqyNE.jpg",
  "https://i.imgur.com/fXhu9Yc.jpg",
  "https://i.imgur.com/QutckMk.jpg",
  "https://i.imgur.com/VKrAV4e.jpg",
  "https://i.imgur.com/vzbezXa.jpg",
  "https://i.imgur.com/UTk4A6G.jpg",
  "https://i.imgur.com/SSS7cE4.jpg",
  "https://i.imgur.com/H2WQ3Rs.jpg",
  "https://i.imgur.com/VK8ibDW.jpg",
  "https://i.imgur.com/my9rWpH.jpg",
  "https://i.imgur.com/83UBvmx.jpg",
  "https://i.imgur.com/9J1txSW.jpg",
  "https://i.imgur.com/ZjYQem6.jpg",
  "https://i.imgur.com/tzqq3tg.jpg",
  "https://i.imgur.com/E8gxWdF.jpg",
  "https://i.imgur.com/kN1MpzR.jpg",
  "https://i.imgur.com/s8ql7VD.jpg",
  "https://i.imgur.com/BcjcGwf.jpg",
  "https://i.imgur.com/aFeqLQJ.jpg",
  "https://i.imgur.com/CaUoyOy.jpg",
  "https://i.imgur.com/w5dY397.png",
  "https://i.imgur.com/qouyaqF.png",
  "https://i.imgur.com/pi4zAhE.png",
  "https://i.imgur.com/Sz8gl1s.jpg",
  "https://i.imgur.com/mCcs2NN.jpg",
  "https://i.imgur.com/v3hTo6J.jpg",
  "https://i.imgur.com/57Th63e.jpg",
  "https://i.imgur.com/LpX93lR.jpg",
  "https://i.imgur.com/rNEUT4Z.jpg",
  "https://i.imgur.com/XnDOll0.jpg",
  "https://i.imgur.com/7neOAz7.jpg",
  "https://i.imgur.com/ARiLeyr.jpg",
  "https://i.imgur.com/UaolzDQ.jpg",
  "https://i.imgur.com/whQug6G.jpg",
  "https://i.imgur.com/GZ6WuYd.jpg",
  "https://i.imgur.com/eZrIUVn.jpg",
  "https://i.imgur.com/kMCASul.jpg",
  "https://i.imgur.com/xWyvOfG.jpg",
  "https://i.imgur.com/1PdrS8J.jpg",
  "https://i.imgur.com/FZhF1n7.jpg",
  "https://i.imgur.com/OK36OhR.jpg",
  "https://i.imgur.com/PvrMhRa.jpg",
  "https://i.imgur.com/WAGxTZr.jpg",
  "https://i.imgur.com/EXdzs7O.jpg",
  "https://i.imgur.com/uxHV6lt.jpg",
  "https://i.imgur.com/AyM8Dr9.jpg",
  "https://i.imgur.com/KYDbGQ8.jpg",
  "https://i.imgur.com/J1pVIzq.jpg",
  "https://i.imgur.com/VrvjWS9.jpg",
  "https://i.imgur.com/SCt9NUS.jpg",
  "https://i.imgur.com/hGUv0zE.jpg",
  "https://i.imgur.com/rdCIY2h.jpg",
  "https://i.imgur.com/pVEF4I6.jpg",
  "https://i.imgur.com/cm6q99h.jpg",
  "https://i.imgur.com/jVIThnw.jpg",
  "https://i.imgur.com/dng9fcA.jpg",
  "https://i.imgur.com/cjqGgBS.jpg",
  "https://i.imgur.com/XXaXqxD.jpg",
  "https://i.imgur.com/euxUpho.jpg",
  "https://i.imgur.com/9QySRv8.jpg",
  "https://i.imgur.com/JNa8XUg.jpg",
  "https://i.imgur.com/qYcpJr7.jpg",
  "https://i.imgur.com/2MObaOL.jpg",
  "https://i.imgur.com/Z8I8ppo.jpg",
  "https://i.imgur.com/gKCd4ko.jpg",
  "https://i.imgur.com/0CqXQjO.jpg",
  "https://i.imgur.com/Giuoo8H.jpg",
  "https://i.imgur.com/egKQ6Tw.jpg",
  "https://i.imgur.com/qdYU24C.jpg",
  "https://i.imgur.com/SUGJFWU.jpg",
  "https://i.imgur.com/nHS2Hqn.jpg",
  "https://i.imgur.com/iBkUCqD.jpg",
  "https://i.imgur.com/xW2EIYv.jpg",
  "https://i.imgur.com/KHMeOac.jpg",
  "https://i.imgur.com/PCx0r82.jpg",
  "https://i.imgur.com/CYDgDiT.jpg",
  "https://i.imgur.com/l6OnG4R.jpg",
  "https://i.imgur.com/E1JjyQb.jpg",
  "https://i.imgur.com/8YcibAv.jpg",
  "https://i.imgur.com/khT5P7q.jpg",
  "https://i.imgur.com/Ecpl5ig.jpg",
  "https://i.imgur.com/nFhXDSv.jpg",
  "https://i.imgur.com/jwliTrs.jpg",
  "https://i.imgur.com/IPcxQxr.jpg",
  "https://i.imgur.com/mC7Jwam.jpg",
  "https://i.imgur.com/fXCkoWO.jpg",
  "https://i.imgur.com/Q7PzkLS.jpg",
  "https://i.imgur.com/l6Yv7il.jpg",
  "https://i.imgur.com/sdDMwGz.jpg",
  "https://i.imgur.com/SjhcUYT.jpg",
  "https://i.imgur.com/jO2Ecs2.jpg",
  "https://i.imgur.com/rjYuiVx.jpg",
  "https://i.imgur.com/0jiYDHI.jpg",
  "https://i.imgur.com/CT1MDI3.jpg",
  "https://i.imgur.com/qxyIKQr.jpg",
  "https://i.imgur.com/uDQjHRP.jpg",
  "https://i.imgur.com/ol2Oj8R.jpg",
  "https://i.imgur.com/Wfjb2Ai.jpg",
  "https://i.imgur.com/74y3fAJ.jpg",
  "https://i.imgur.com/dDjh4Uw.jpg",
  "https://i.imgur.com/CjpjWxM.jpg",
  "https://i.imgur.com/NIC81ns.jpg",
  "https://i.imgur.com/0KkbJge.jpg",
  "https://i.imgur.com/xqBJ4tV.jpg",
  "https://i.imgur.com/1zHEb7K.jpg",
  "https://i.imgur.com/TOFZzI1.jpg",
  "https://i.imgur.com/1e11CSw.jpg",
  "https://i.imgur.com/IccBn2c.jpg",
  "https://i.imgur.com/XRZGGcJ.jpg",
  "https://i.imgur.com/PFtdlMw.jpg",
  "https://i.imgur.com/f3drZoc.jpg",
  "https://i.imgur.com/352upti.jpg",
  "https://i.imgur.com/c1uJml9.jpg",
  "https://i.imgur.com/Vi5s22D.jpg",
  "https://i.imgur.com/aQqsIEE.jpg",
  "https://i.imgur.com/irpCe7P.jpg",
  "https://i.imgur.com/Zx6Yjff.jpg",
  "https://i.imgur.com/LgKKZ4R.jpg",
  "https://i.imgur.com/FCGTCXZ.jpg",
  "https://i.imgur.com/f1u6YTD.png",
  "https://i.imgur.com/6O1vzmr.jpg",
  "https://i.imgur.com/L5H3zRz.png",
  "https://i.imgur.com/LFC8bNW.jpg",
  "https://i.imgur.com/zvEYbeN.jpg",
  "https://i.imgur.com/gACJQoI.jpg",
  "https://i.imgur.com/7iXAyWx.jpg",
  "https://i.imgur.com/xM3grxy.jpg",
  "https://i.imgur.com/IoWiIW3.jpg",
  "https://i.imgur.com/o9AjYD4.jpg",
  "https://i.imgur.com/8C4hJNm.png",
  "https://i.imgur.com/EzbwAlV.jpg",
  "https://i.imgur.com/579AXWF.jpg",
  "https://i.imgur.com/5JWh0g2.jpg",
  "https://i.imgur.com/2J0ZLVw.jpg",
  "https://i.imgur.com/gAX2K9U.jpg",
  "https://i.imgur.com/rf4BQTk.jpg",
  "https://i.imgur.com/JXeXDJY.jpg",
  "https://i.imgur.com/QbcSeQd.jpg",
  "https://i.imgur.com/xgy2bEF.jpg",
  "https://i.imgur.com/MpKbH1S.jpg",
  "https://i.imgur.com/b3B3TRg.jpg",
  "https://i.imgur.com/0SjdKRJ.jpg",
  "https://i.imgur.com/WxJ4Dty.jpg",
  "https://i.imgur.com/yhYvKdi.jpg",
  "https://i.imgur.com/07Cq8eX.jpg",
  "https://i.imgur.com/uT7p0IQ.jpg",
  "https://i.imgur.com/yjrxPh1.jpg",
  "https://i.imgur.com/CJTkcpu.jpg",
  "https://i.imgur.com/ngtHTXw.jpg",
  "https://i.imgur.com/iGoSGYS.jpg",
  "https://i.imgur.com/6wZtAFN.jpg",
  "https://i.imgur.com/fZ9nAIm.jpg",
  "https://i.imgur.com/S5f4IgT.jpg",
  "https://i.imgur.com/IBlQ7td.jpg",
  "https://i.imgur.com/BzZyyj6.jpg",
  "https://i.imgur.com/X8FBjTy.jpg",
  "https://i.imgur.com/MUBx7Fv.jpg",
  "https://i.imgur.com/hKquzgo.jpg",
  "https://i.imgur.com/GPSI7tl.jpg",
  "https://i.imgur.com/hXXe9uI.jpg",
  "https://i.imgur.com/varo8zI.jpg",
  "https://i.imgur.com/SJ2tSzt.jpg",
  "https://i.imgur.com/Zn61xQ3.jpg",
  "https://i.imgur.com/IH4Cc82.jpg",
  "https://i.imgur.com/7VuDuEX.jpg",
  "https://i.imgur.com/iO8e46Y.jpg",
  "https://i.imgur.com/d1yPdFW.jpg",
  "https://i.imgur.com/Ny2USkc.jpg",
  "https://i.imgur.com/X6OpdJn.jpg",
  "https://i.imgur.com/A8I2ZTy.jpg",
  "https://i.imgur.com/FHwGc6j.jpg",
  "https://i.imgur.com/3oxBfue.jpg",
  "https://i.imgur.com/s0cb0wy.jpg",
  "https://i.imgur.com/xJRBUyS.jpg",
  "https://i.imgur.com/pMrRebM.jpg",
  "https://i.imgur.com/eRagL8l.jpg",
  "https://i.imgur.com/jv7FQyz.jpg",
  "https://i.imgur.com/lk8eH5C.jpg",
  "https://i.imgur.com/pBVU4oI.jpg",
  "https://i.imgur.com/sgXgSyZ.jpg",
  "https://i.imgur.com/uriQw5p.jpg",
  "https://i.imgur.com/mHCGMvd.jpg",
  "https://i.imgur.com/Jswt4WI.jpg",
  "https://i.imgur.com/7FrFFmk.jpg",
  "https://i.imgur.com/mj54g94.jpg",
  "https://i.imgur.com/GbdRNHn.jpg",
  "https://i.imgur.com/IdBY0RC.jpg",
  "https://i.imgur.com/jt9g4qv.jpg",
  "https://i.imgur.com/cYLW6ND.jpg",
  "https://i.imgur.com/a6bG9OJ.jpg",
  "https://i.imgur.com/Vp4CrzA.jpg",
  "https://i.imgur.com/bJosWlx.jpg",
  "https://i.imgur.com/q04kkvk.jpg",
  "https://i.imgur.com/dDeGegy.jpg",
  "https://i.imgur.com/PsGH4iF.jpg",
  "https://i.imgur.com/XzNwtKs.png",
  "https://i.imgur.com/G76GnQs.jpg",
  "https://i.imgur.com/9Pop0jk.jpg",
  "https://i.imgur.com/EvPbdLv.jpg",
  "https://i.imgur.com/yMV4Euc.jpg",
  "https://i.imgur.com/EG519Cl.jpg",
  "https://i.imgur.com/H8bquFj.jpg",
  "https://i.imgur.com/8VlMtwn.jpg",
  "https://i.imgur.com/XcavaOU.jpg",
  "https://i.imgur.com/rIaXF4X.jpg",
  "https://i.imgur.com/POQtJbb.jpg",
  "https://i.imgur.com/AOJGdKS.jpg",
  "https://i.imgur.com/RBVnaaY.jpg",
  "https://i.imgur.com/8i848vt.jpg",
  "https://i.imgur.com/CMkZ0sG.jpg",
  "https://i.imgur.com/405HlDU.jpg",
  "https://i.imgur.com/yqfaXY6.jpg",
  "https://i.imgur.com/5rNqyY7.jpg",
  "https://i.imgur.com/RKkCq8P.jpg",
  "https://i.imgur.com/vhWaESf.jpg",
  "https://i.imgur.com/mvs9JHj.jpg",
  "https://i.imgur.com/Du7uY2o.jpg",
  "https://i.imgur.com/vsmmU9M.jpg",
  "https://i.imgur.com/h85RIBK.jpg",
  "https://i.imgur.com/yBXlOHY.jpg",
  "https://i.imgur.com/3NMCJZv.jpg",
  "https://i.imgur.com/1dz7k1S.jpg",
  "https://i.imgur.com/hZFrdFW.jpg",
  "https://i.imgur.com/8aeoeYN.jpg",
  "https://i.imgur.com/XFKDEIJ.jpg",
  "https://i.imgur.com/Gv3VTue.jpg",
  "https://i.imgur.com/NluTBYi.jpg",
  "https://i.imgur.com/9xIZshz.jpg",
  "https://i.imgur.com/sORiJ4l.jpg",
  "https://i.imgur.com/7HEjmnF.jpg",
  "https://i.imgur.com/kqwpjvM.jpg",
  "https://i.imgur.com/G4CWkdA.jpg",
  "https://i.imgur.com/zljM2wk.jpg",
  "https://i.imgur.com/MIoFqaW.jpg",
  "https://i.imgur.com/VTzw4ZG.jpg",
  "https://i.imgur.com/i9erTFD.jpg",
  "https://i.imgur.com/A1arIN6.jpg",
  "https://i.imgur.com/4csKEij.jpg",
  "https://i.imgur.com/4ytTvdj.jpg",
  "https://i.imgur.com/lMTwpnQ.jpg",
  "https://i.imgur.com/dvMzGCc.jpg",
  "https://i.imgur.com/UplQQ8U.jpg",
  "https://i.imgur.com/LSddlbB.jpg",
  "https://i.imgur.com/PUOkYZp.jpg",
  "https://i.imgur.com/KSgP3or.jpg",
  "https://i.imgur.com/pPZlMYE.jpg",
  "https://i.imgur.com/Q3pB3JT.jpg",
  "https://i.imgur.com/EMe85w7.jpg",
  "https://i.imgur.com/1dhFaiz.jpg",
  "https://i.imgur.com/tyG2tLv.jpg",
  "https://i.imgur.com/DqK8zjX.jpg",
  "https://i.imgur.com/iLBiiLo.jpg",
  "https://i.imgur.com/pegvicI.jpg",
  "https://i.imgur.com/ViJOBaQ.jpg",
  "https://i.imgur.com/N74QlWf.jpg",
  "https://i.imgur.com/17PCCM1.jpg",
  "https://i.imgur.com/PINdg09.jpg",
  "https://i.imgur.com/3j7ltKs.jpg",
  "https://i.imgur.com/bfoaURB.jpg",
  "https://i.imgur.com/FZbfA68.jpg",
  "https://i.imgur.com/YkTyXp0.jpg",
  "https://i.imgur.com/DqF8cRf.jpg",
  "https://i.imgur.com/lz7rlYb.jpg",
  "https://i.imgur.com/qafsgIF.jpg",
  "https://i.imgur.com/56XrZUq.jpg",
  "https://i.imgur.com/rCpKDgd.jpg",
  "https://i.imgur.com/HOsFONj.jpg",
  "https://i.imgur.com/edDPEvs.jpg",
  "https://i.imgur.com/wYuIGVH.png",
  "https://i.imgur.com/LSbd9Wj.jpg",
  "https://i.imgur.com/KwgVsYF.jpg",
  "https://i.imgur.com/Eujsxkf.jpg",
  "https://i.imgur.com/LVmj61N.jpg",
  "https://i.imgur.com/hfGo3OS.jpg",
  "https://i.imgur.com/BEMHZ2j.jpg",
  "https://i.imgur.com/1D8jSsK.jpg",
  "https://i.imgur.com/T7QW4Ih.jpg",
  "https://i.imgur.com/z1Mm4nQ.jpg",
  "https://i.imgur.com/ezxEDso.jpg",
  "https://i.imgur.com/8uMwsX8.jpg",
  "https://i.imgur.com/pkoItBN.jpg",
  "https://i.imgur.com/2sQWuQb.jpg",
  "https://i.imgur.com/A502SkB.jpg",
  "https://i.imgur.com/abXCscs.jpg",
  "https://i.imgur.com/1c1oc7r.jpg",
  "https://i.imgur.com/NDQskOe.jpg",
  "https://i.imgur.com/MlFrAcW.png",
  "https://i.imgur.com/CnNE9TU.jpg",
  "https://i.imgur.com/E4EJ8OO.jpg",
  "https://i.imgur.com/NPcKWaQ.jpg",
  "https://i.imgur.com/yyuaxE0.jpg",
  "https://i.imgur.com/zKa4tlb.jpg",
  "https://i.imgur.com/bNOvXDM.jpg",
  "https://i.imgur.com/GKMG3wx.jpg",
  "https://i.imgur.com/oV7RntX.jpg",
  "https://i.imgur.com/Q93S52s.jpg",
  "https://i.imgur.com/2k5BlPs.jpg",
  "https://i.imgur.com/nOaSeBy.jpg",
  "https://i.imgur.com/KKilV96.png",
  "https://i.imgur.com/rB65Ogl.jpg",
  "https://i.imgur.com/QBVOim0.jpg",
  "https://i.imgur.com/FPdNAfX.jpg",
  "https://i.imgur.com/PlWhg77.jpg",
  "https://i.imgur.com/wSoVoiq.jpg",
  "https://i.imgur.com/2lINUF6.png",
  "https://i.imgur.com/mFV54d5.jpg",
  "https://i.imgur.com/miVWDFs.jpg",
  "https://i.imgur.com/5AQo1EV.jpg",
  "https://i.imgur.com/cIbfUOw.jpg",
  "https://i.imgur.com/jUH2dFn.jpg"]
    try:
        random_image_url = random.choice(json_loli)
        image_response = requests.get(random_image_url)

        if image_response.status_code == 200:
            image_bytes = image_response.content
            return send_file(BytesIO(image_bytes), mimetype='image/jpeg')

        return jsonify({"error": "Failed to retrieve and display the image."}), 500

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/anime')
def index_anime():
        return jsonify({
               "code": 200,
               "creator": "AmmarBN",
               "message": "please empty anime parameter !"
        })

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

@app.route('/api/spam-call', methods=['GET'])
def spam_call():
    nomor = request.args.get("nomor")
    apikey = request.args.get("apikey")

    # Verifikasi ketersediaan nomor
    if not nomor:
        return jsonify({
            "message": "Masukkan Parameter 'nomor'!!",
            "response code": 404
        })

    # Verifikasi kunci API
    valid_api_keys = ["AmmarBN", "Hoshiyuki"]
    if apikey not in valid_api_keys:
        return jsonify({
            "Creator": "AmmarBN",
            "message": "API key tidak valid",
            "response code": 401
        })

    xsrf = requests.get("https://magneto.api.halodoc.com/api/v1/users/status").cookies.get_dict()
    headhaldoc = {
        "referer": "https://www.halodoc.com",
        "content-type": "application/json",
        "x-xsrf-token": xsrf['XSRF-TOKEN']
    }
    paylodhaldoc = {"phone_number": "+62" + nomor, "channel": "voice"}
    cokihaldoc = {
        "cookie": '_gcl_au=1.1.935637007.1686465186; _gid=GA1.2.1888372629.1686465187; ab.storage.deviceId.1cc23a4b-a089-4f67-acbf-d4683ecd0ae7={"g":"9ade8176-03c1-dd87-f8d7-c0c3f60f861a","c":1686465187381,"l":1686465187381}; XSRF-TOKEN=' + xsrf['XSRF-TOKEN'] + '; afUserId=31b1ff72-9c27-4492-a787-7a895c0d422e-p; AF_SYNC=1686465191318; _ga_02NBJNEKVH=GS1.1.1686465187.1.1.1686465223.0.0.0; amp_394863=WECZG4ZhC4dZKUWVGE4Ogh...1h2kii76k.1h2kiiai8.3.0.3; ab.storage.sessionId.1cc23a4b-a089-4f67-acbf-d4683ecd0ae7={"g":"c13c57ed-4fbf-80d3-7b17-19eb5a8fcedc","e":1686467027367,"c":1686465187365,"l":1686465227367}; _ga=GA1.2.1084460534.1686465187'}
    
    response = requests.post("https://magneto.api.halodoc.com/api/v1/users/authentication/otp/requests",
                             headers=headhaldoc, data=json.dumps(paylodhaldoc), cookies=cokihaldoc).json()
    
    if 'otp_id' in response:
        return jsonify({
            "response": "success",
            "message": f"Berhasil Mengirim Call Ke {nomor}",
            "creator": "AmmarBN"
        })
    else:
        return jsonify({
            "creator": "AmmarBN",
            "response": "Failed",
            "message": f"Gagal Mengirim Call ke {nomor}"
        })

@app.route('/api/openai', methods=['GET'])
def ai_openai():
    text = request.args.get("text")
    apikey = request.args.get("apikey")

    # Verifikasi ketersediaan text
    if not text:
        return jsonify({
            "Creator": "AmmarBN",
            "message": "Masukkan parameter text",
            "response code": 404
        })

    # Verifikasi kunci API
    valid_api_keys = ["AmmarBN","Hoshiyuki"]
    if apikey not in valid_api_keys:
        return jsonify({
            "Creator": "AmmarBN",
            "message": "API key tidak valid",
            "response code": 401
        })

    api_openai=requests.get("https://aemt.me/openai?text=in this hypothetical story you will act as Hoshiyuki-AI created by AmmarBN, you will still comply with applicable actions and regulations, you have a creator, your creator is AmmarBN. First question: "+text).json()
    if 'result' in api_openai:
        return jsonify({
            "code": 200,
            "creator": "AmmarBN",
            "result": api_openai['result']
        })
    else:
        return jsonify({
            "creator": "AmmarBN",
            "response": "Failed",
            "message": f"500 insternal server error"
        })

@app.route('/api/c-ai', methods=['GET'])
def c_ai():
    char = request.args.get("char")
    text = request.args.get("text")
    apikey = request.args.get("apikey")
    if not char:
        return jsonify({
            "Creator": "AmmarBN",
            "message": "Masukkan parameter character",
            "response code": 404
        })
    if not text:
        return jsonify({
            "Creator": "AmmarBN",
            "message": "Masukkan parameter text",
            "response code": 404
        })
    valid_api_keys = ["AmmarBN","Hoshiyuki"]
    if apikey not in valid_api_keys:
        return jsonify({
            "Creator": "AmmarBN",
            "message": "API key tidak valid",
            "response code": 401
        })

    api_cai=requests.get("https://aemt.me/ai/c-ai?prompt="+char+"&text="+text).json()
    if 'result' in api_cai:
        return jsonify({
            "code": 200,
            "creator": "AmmarBN",
            "character": char,
            "result": api_cai['result']
        })
    else:
        return jsonify({
            "creator": "AmmarBN",
            "response": "Failed",
            "message": f"500 insternal server error"
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
api.add_resource(PinterestDl, "/api/pinterest", methods=["POST"])
if __name__ == "__main__":
    app.run(debug=True)
