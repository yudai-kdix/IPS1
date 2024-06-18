import base64
import cv2
from flask import request, jsonify, send_file
import os
from flask_cors import CORS
from werkzeug.utils import secure_filename
from backend.controller.user_controller import get_user_id_from_token
from backend.models.face import Face
from backend.models.video import Video
from backend import app
import face_recognition

UPLOAD_FOLDER_STATIC = 'backend/static'
CORS(app)

@app.route('/upload_video', methods=['POST'])
def upload_video():
    # ファイルがリクエストに含まれているか確認
    if 'video' not in request.files:
        return jsonify({'message': 'No video file provided'}), 400
    
    file = request.files['video']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    # ファイル名を安全に処理
    filename = secure_filename(file.filename)
    # ビデオファイルをサーバーに保存
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Videoモデルインスタンスを作成
    user_id = get_user_id_from_token()
    if user_id:
        video = Video(name=filename, path=filepath, user_id=user_id)
    else:
        video = Video(name=filename, path=filepath)
    video.save()  # データベースにビデオ情報を保存
    # データベースに保存してないのでidがなかった
    video = Video.find_by_name(filename)
    save_thumbnail(filename)  # サムネイルを保存
    # 9枚の1秒感覚のフレームを作成し、それらをstatic/frame/id/に保存 ファイル名は0.jpg, 1.jpg, ..., 8.jpg
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    video_capture = cv2.VideoCapture(video_path)
    for i in range(9):
        ret, frame = video_capture.read()
        if ret:
            if not os.path.exists(UPLOAD_FOLDER_STATIC + "/frame/" + str(video.id)):
                os.makedirs(UPLOAD_FOLDER_STATIC + "/frame/" + str(video.id))
            frame_path = UPLOAD_FOLDER_STATIC + "/frame/" + str(video.id) + "/" + str(i) + ".jpg"
            tmp = face_find(frame)
            cv2.imwrite(frame_path, tmp['img'])
            for facevec in tmp['face_vecs']:
                if user_id:
                    face = Face(facevec=facevec, user_id=user_id, video_id=video.id)
                    face.save()
                else:
                    face = Face(facevec=facevec,user_id=1, video_id=video.id)
                    face.save()
            
    video_capture.release()
    return jsonify({'message': 'Video uploaded successfully', 'path': filepath}), 201


@app.route('/videos', methods=['GET'])
def get_videos():
    videos = Video.find_all()
    video_list = []
    for video in videos:
        video_list.append({'id': video.id, 'name': video.name, 'path': video.path})
    return jsonify(video_list)


@app.route('/video/<video_id>', methods=['GET'])
def get_video(video_id):
    video = Video.find_by_id(video_id)
    if video:
        video_data = {'id': video.id, 'name': video.name, 'path': video.path}
        return jsonify(video_data)
    else:
        return jsonify({'message': 'Video not found'}), 404
    
@app.route('/play_video/<video_id>', methods=['GET'])
def play_video(video_id):
    video = Video.find_by_id(video_id)
    if video:
        return send_file('uploads/' + video.name)
    else:
        return jsonify({'message': 'Video not found'}), 404

@app.route('/video/<video_id>', methods=['DELETE'])
def delete_video(video_id):
    video = Video.find_by_id(video_id)
    if video:
        video.delete()
        return jsonify({'message': 'Video deleted successfully'})
    else:
        return jsonify({'message': 'Video not found'}), 404
    

@app.route('/video/<video_id>', methods=['PUT'])
def update_video(video_id):
    video = Video.find_by_id(video_id)
    if video:
        data = request.json
        video.name = data.get('name', video.name)
        video.save()
        return jsonify({'message': 'Video updated successfully'})
    else:
        return jsonify({'message': 'Video not found'}), 404


@app.route('/video/<video_id>/faces', methods=['GET'])
def get_faces(video_id):
    video = Video.find_by_id(video_id)
    if video:
        faces = video.faces
        face_list = []
        for face in faces:
            face_list.append({'id': face.id, 'name': face.name, 'facevec': face.facevec})
        return jsonify(face_list)
    else:
        return jsonify({'message': 'Video not found'}), 404

# static/frame/id/に保存された9枚のフレームをbase64エンコードして返す
@app.route('/get_frames/<video_id>')
def get_frames(video_id):
    frames = []
    for i in range(9):
        frame_path = UPLOAD_FOLDER_STATIC + "/frame/" + str(video_id) + "/" + str(i) + ".jpg"
        with open(frame_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            frames.append(encoded_string)
    return jsonify(frames)

def save_thumbnail(video_name):
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], video_name)
    video = cv2.VideoCapture(video_path)
    ret, frame = video.read()
    if ret:
        thumbnail_path = UPLOAD_FOLDER_STATIC + "/thumbnail/" + video_name.replace('.mp4', '.jpg')
        cv2.imwrite(thumbnail_path, frame)
        return thumbnail_path
    return None

# 画像から顔を検出する
# 顔が検出された場合、見つけた顔をstatic/faceに保存。
# また、顔の特徴量を取得し、Faceモデルインスタンスを作成し、データベースに保存
# そして最初の画像に顔の位置を描画し、返す
def face_find(img):
    img_copy = img.copy()
    img_gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
    face_locations = face_recognition.face_locations(img_gray)
    face_encodings = face_recognition.face_encodings(img, face_locations)
    face_vecs = []
    for i, face_location in enumerate(face_locations):
        top, right, bottom, left = face_location
        face = img[top:bottom, left:right]
        face_path = UPLOAD_FOLDER_STATIC + "/face/" + str(i) + ".jpg"
        cv2.imwrite(face_path, face)
        facevec = face_encodings[i].tostring()
        face_vecs.append(facevec)
        face.save()
        cv2.rectangle(img_copy, (left, top), (right, bottom), (0, 0, 255), 2)
    return {'img':img_copy,'face_vecs':face_vecs}