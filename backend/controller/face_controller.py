from flask import jsonify
from flask_cors import CORS
from backend import app
from backend.models.face import Face

CORS(app)

@app.route('/face/<video_id>', methods=['GET'])
def get_faces(video_id):
    faces = Face.find_by_video_id(video_id)
    face_list = []
    for face in faces:
        face_list.append({'id': face.id, 'name': face.name, 'facevec': face.facevec})
    return jsonify(face_list)
