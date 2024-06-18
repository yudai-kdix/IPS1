import logging
import os
from time import sleep
import cv2
import face_recognition
import numpy as np
import pandas as pd
from flask import Flask, Response, request, send_from_directory, session, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from backend import app
from backend.controller import user_controller
from backend.controller import video_controller

load_dotenv()

CORS(app)

logging.basicConfig(level=logging.DEBUG)
UPLOAD_FOLDER = 'backend/uploads'
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALGORITHM'] = os.environ['ALGORITHM']


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
UPLOAD_FOLDER_STATIC = 'backend/static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER_STATIC):
    os.makedirs(UPLOAD_FOLDER_STATIC)
face_locations_list = {f'frame_{i:02}.jpg': [] for i in range(9)}

def save_thumbnail(video_name):
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_name)
    video = cv2.VideoCapture(video_path)
    ret, frame = video.read()
    if ret:
        thumbnail_path = UPLOAD_FOLDER_STATIC + "/thumbnail/" + video_name.replace('.mp4', '.jpg')
        cv2.imwrite(thumbnail_path, frame)
        return thumbnail_path
    return None

# 既存の動画ファイルでサムネイルが無い場合、サムネイルを作成 ある場合処理しない
files = os.listdir(UPLOAD_FOLDER)
file_names = [f for f in files if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]
for file_name in file_names:
    thumbnail_path = UPLOAD_FOLDER_STATIC + "/thumbnail/" + file_name.replace('.mp4', '.jpg')
    if not os.path.exists(thumbnail_path):
        save_thumbnail(file_name)
print("サムネイル作成完了")


# @app.route('/')
# def index():
#     files = os.listdir(UPLOAD_FOLDER)
#     file_name = [f for f in files if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]

#     return render_template('index.html', video_name=file_name)

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory('uploads', filename)

@app.route('/api/videos')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    file_names = [f for f in files if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]
    return jsonify(file_names)

@app.route('/upload', methods=['POST'])
def update():
    if 'file' not in request.files:
        return jsonify({"error": "ファイルがリクエストに含まれていません。"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "ファイル名がありません。"}), 400

    if file:
        filename = file.filename
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        file_names = [f for f in files if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))]
        return jsonify(file_names)
    

# サムネイルのパスを取得
@app.route('/thumbnail/<video_name>')
def get_thumbnail(video_name):
    # thumbnail_path = UPLOAD_FOLDER_STATIC + "/thumbnail/" + video_name.replace('.mp4', '.jpg')
    # if not os.path.exists(thumbnail_path):
    #     thumbnail_path = save_thumbnail(video_name)
    return send_from_directory("static" + "/thumbnail", video_name.replace('.mp4', '.jpg'))



@app.route('/play/<filename>')
def uploaded_file(filename):
    print("**************************************************************")
    session['filename'] = filename  # セッションにファイル名を保存
    file_list = process_snapshot(0)
    print("************")
    while len(os.listdir('static/images')) < 1:
        sleep(0.1)
    print("リターン")
    return jsonify(file_list)

def process_snapshot(start):
    filename = session['filename']

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    video = cv2.VideoCapture(filepath)
    frameAll = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    framerate = int(video.get(cv2.CAP_PROP_FPS))

    idx = 0
    file_list = []


    for i in range(9):
        file_path = f'static/images/frame_{i:02}.jpg'
        if os.path.exists(file_path):
            os.remove(file_path)
            print('Removed:', file_path)



    for i in range(start * framerate, frameAll, framerate):
        
        video.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, image = video.read()
        # 画像に顔の位置を書き込む前にimages_orgに保存
        cv2.imwrite(f'static/images_org/frame_{idx:02}.jpg', image)

        if ret:
            # 画像をBGRからRGBに変換（face_recognitionはRGBを想定）
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # 顔の位置を検出
            face_locations = face_recognition.face_locations(rgb_image)

            # 検出された顔に四角を描画
            # for (top, right, bottom, left) in face_locations:
            #     cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)

            for face_location in face_locations:
                top, right, bottom, left = face_location
                
                
                face_key = f'{top}_{right}_{bottom}_{left}'
                person_name = match_face(filename=f'frame_{idx:02}.jpg', face_location=face_key)

                if person_name != -1:
                    cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.putText(image, person_name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0,255), 2)
                else:
                    # 赤で囲む
                    cv2.rectangle(image, (left, top), (right, bottom), (0, 255,0), 2)


            if face_locations_list[f'frame_{idx:02}.jpg'] == []:
                for (top, right, bottom, left) in face_locations:
                    face_locations_list[f'frame_{idx:02}.jpg'].append(f'{top}_{right}_{bottom}_{left}')
            
            # 画像の保存パス
            if not os.path.exists('static/images'):
                os.makedirs('static/images')
            num = f'{idx:02}'
            url = f'./static/images/frame_{num}.jpg'
            if len(face_locations) == 0:
                session[f'frame_{num}.jpg'] = False
            else:
                session[f'frame_{num}.jpg'] = True
            cv2.imwrite(url, image)  # 四角で囲んだ画像を保存
            print('save:', url)
            file_list.append(url)
            if idx == 8:
                break
            idx += 1

        else:
            break
    session['file_list'] = file_list
    # urlから.を排除
    file_list = [url[1:] for url in file_list]
    return file_list

@app.route('/process_form', methods=['POST'])
def process_form():
    start = int(request.form['start'])  # フォームから'start'パラメータを取得
    file_list = process_snapshot(start)
    # while not all(os.path.exists(file) for file in file_list):
    #     sleep(0.1)
    print("リターン")
    return jsonify(file_list)


@app.route('/person_name_input/<filename>',methods=['GET'])
def person_name_input(filename):
    if request.method == 'GET':
        if session.get(filename, False):
            face_data = face_locations_list.get(filename, [])
            if face_data:
                return jsonify({"photo_name": filename, "face_locations": face_data}), 200
            return jsonify({"error": "No face data available"}), 404
        else:
            # 顔データがないため、エラーレスポンスを返す
            return jsonify({"error": "No face data found"}), 404

    
@app.route('/person_name_input/<filename>',methods=['POST'])
def person_name_input_post(filename):
    if request.method == 'POST':
        print(filename)
        response_data = {}
        for face_location in face_locations_list.get(filename, []):
            person_name = request.form.get(face_location)
            if person_name:
                save_person_face(filename,face_location,person_name)
                response_data[face_location] = person_name
            else:
                response_data[face_location] = 'No name provided'
    return jsonify(response_data)


@app.route('/video/<filename>',methods=['GET'])
def video_play(filename):
    video_dir = 'static/videos'
    output_filename = f'output_hog_{filename}'
    if output_filename in os.listdir(video_dir):
        video_draw_hog(filename)

    video_path = os.path.join(video_dir, output_filename)
    filename = f'output_hog_{filename}'
    return jsonify({'video_path': video_path})

def save_person_face(filename,face_location,person_name):
    
    image = face_recognition.load_image_file(f'static/images_org/{filename}')
    csv_path = './static/data/feature_vectors.csv'

    face_location = tuple(map(int, face_location.split('_')))
    face_encodings = face_recognition.face_encodings(image, [face_location])
    # 特徴ベクトルが存在すれば、それをCSVに保存
    if face_encodings:
        # 特徴ベクトルと人物名をデータフレームに追加
        df = pd.DataFrame(face_encodings)
        df.insert(0, 'person_name', person_name) 
            # CSVファイルに保存（ファイルが存在する場合はデータを追加）
        # CSVファイルに保存（ファイルが存在する場合はデータを追加）
        if os.path.exists(csv_path) and not pd.read_csv(csv_path).empty:
            # ファイルが空でない場合はヘッダーなしで追加
            df.to_csv(csv_path, mode='a', header=False, index=False)
        else:
            # ファイルが空の場合はヘッダーありで新規作成
            df.to_csv(csv_path, mode='w', header=True, index=False)

def match_face( face_location,filename=None,image = None):
    if image is None:
        image = face_recognition.load_image_file(f'static/images_org/{filename}')
    
    face_location = tuple(map(int, face_location.split('_')))

    face_encodings = face_recognition.face_encodings(image, [face_location])

    if not face_encodings:
        return -1  # 顔の特徴ベクトルが抽出できなかった場合

    current_encoding = face_encodings[0]
    csv_path = './static/data/feature_vectors.csv'
    
    if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:

        df = pd.read_csv(csv_path)
        # CSVファイルのデータと比較

        for index, row in df.iterrows():

            stored_encoding = np.array(row[1:].values, dtype=float)  # dtypeを指定して変換
            if face_recognition.compare_faces([stored_encoding], current_encoding, tolerance=0.4)[0]:
                print('match!', row['person_name'])
                return row['person_name']  # 顔が一致した場合、名前を返す

    return -1  # 一致する顔がない場合

def video_draw_cnn(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    video = cv2.VideoCapture(filepath)
    framerate = int(video.get(cv2.CAP_PROP_FPS))
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))  # フレームの幅
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))  # フレームの高さ
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 動画保存時のfourcc設定（mp4形式）
    save_dir = 'static/videos'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_filename = os.path.join(save_dir, f'output_cnn_{filename}')
    out = cv2.VideoWriter(save_filename, fourcc, framerate, (frame_width, frame_height))  # 動画の仕様（ファイル名、fourcc、fps、サイズ）
    count = 0
    while video.isOpened():
        count += 1
        # フレームレートの倍数のときprint
        if count % framerate == 0:
            print(f'frame: {count}')
        ret,frame = video.read()
        if not ret:
            break
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_image, number_of_times_to_upsample=1, model="cnn")
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        out.write(frame)
    
    video.release()
    out.release()

def video_draw_hog(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    video = cv2.VideoCapture(filepath)
    framerate = int(video.get(cv2.CAP_PROP_FPS))
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))  # フレームの幅
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))  # フレームの高さ
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 動画保存時のfourcc設定（mp4形式）
    save_dir = 'static/videos'

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_filename = os.path.join(save_dir, f'output_hog_{filename}')
    out = cv2.VideoWriter(save_filename, fourcc, framerate, (frame_width, frame_height))  # 動画の仕様（ファイル名、fourcc、fps、サイズ）
    count = 0
    while video.isOpened():
        count += 1
        # フレームレートの倍数のときprint
        if count % framerate == 0:
            print(f'frame: {count}')
        ret,frame = video.read()
        if not ret:
            break
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_image)
        for face_location in face_locations:
            top, right, bottom, left = face_location
            face_key = f'{top}_{right}_{bottom}_{left}'
            person_name = match_face(image=rgb_image, face_location=face_key)

            if person_name != -1:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, person_name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0,255), 2)
            else:
                # 赤で囲む
                cv2.rectangle(frame, (left, top), (right, bottom), (255, 0,0), 2)

        out.write(frame)
    
    video.release()
    out.release()


def video_draw_hog_now(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    video = cv2.VideoCapture(filepath)
    framerate = int(video.get(cv2.CAP_PROP_FPS))

    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_image)

        # for (top, right, bottom, left) in face_locations:
        #     cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        for face_location in face_locations:
            top, right, bottom, left = face_location
            face_key = f'{top}_{right}_{bottom}_{left}'
            person_name = match_face(image=rgb_image, face_location=face_key)

            if person_name != -1:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, person_name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0,255), 2)
            else:
                # 赤で囲む
                cv2.rectangle(frame, (left, top), (right, bottom), (255, 0,0), 2)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    video.release()

@app.route('/video_feed/<filename>')
def video_feed(filename):
    return Response(video_draw_hog_now(filename),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)