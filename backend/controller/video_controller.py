from flask import request, jsonify
import os
from werkzeug.utils import secure_filename

from controller.user_controller import UserController
from backend.models.video import Video
from backend import app

class VideoController:
    @staticmethod
    @app.route('/upload', methods=['POST'])
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
        user_id = UserController.get_user_id_from_token()
        if user_id:
            video = Video(name=filename, path=filepath, user_id=user_id)
        else:
            video = Video(name=filename, path=filepath)
        video.save()  # データベースにビデオ情報を保存

        return jsonify({'message': 'Video uploaded successfully', 'path': filepath}), 201

    @staticmethod
    @app.route('/videos', methods=['GET'])
    def get_videos():
        videos = Video.find_all()
        video_list = []
        for video in videos:
            video_list.append({'id': video.id, 'name': video.name, 'path': video.path})
        return jsonify(video_list)
    
    @staticmethod
    @app.route('/video/<video_id>', methods=['GET'])
    def get_video(video_id):
        video = Video.find_by_id(video_id)
        if video:
            video_data = {'id': video.id, 'name': video.name, 'path': video.path}
            return jsonify(video_data)
        else:
            return jsonify({'message': 'Video not found'}), 404
        
    @staticmethod
    @app.route('/video/<video_id>', methods=['DELETE'])
    def delete_video(video_id):
        video = Video.find_by_id(video_id)
        if video:
            video.delete()
            return jsonify({'message': 'Video deleted successfully'})
        else:
            return jsonify({'message': 'Video not found'}), 404
        
    @staticmethod
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
    
    @staticmethod
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
