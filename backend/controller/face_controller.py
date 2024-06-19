from flask import jsonify, send_file
from flask_cors import CORS

from backend.models.face import Face
from backend import app

CORS(app)

# @app.route('/face/<video_id>', methods=['GET'])
# def get_faces_video(video_id):
#     faces = Face.find_by_video_id(video_id)
#     face_list = []
#     for face in faces:
#         face_list.append({'id': face.id, 'name': face.name, 'facevec': face.facevec})
#     return jsonify(face_list)

@app.route('/face/<face_id>', methods=['GET'])
def get_face(face_id):
    face = Face.find_by_id(face_id)
    if face:
        return send_file('static/face/' + str(face.id)+'.jpg')
    else:
        return jsonify({'message': 'Face not found'}), 404
    
@app.route('/faces', methods=['GET'])
def get_face_list():
    faces = Face.find_all()
    face_list = []
    for face in faces:
        face_list.append({'id': face.id, 'name': face.name})
    return jsonify(face_list)
