from flask import jsonify, render_template, request, Blueprint
import face_recognition
from flask_openapi3 import Info, Tag, OpenAPI
from pydantic import BaseModel, Field
import base64
import io
import numpy as np
from PIL import Image
import logging
# import graypy
from deepface import DeepFace
import os

matching = Blueprint("matching", __name__)

info = Info(title="FaceMatch", version="0.0.1")
# app = OpenAPI(__name__, info=info)
logger = logging.getLogger('test_logger')
logger.setLevel(logging.DEBUG)
# handler = graypy.GELFUDPHandler('localhost', 12201)
# logger.addHandler(handler)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

class FacesMatchInput(BaseModel):
    b64image1: str = Field('base64', description="image1")
    b64image2: str = Field('base64', description="image2")


match_tag = Tag(name="FaceMatch", description="FaceMatch")


class FaceMatchResponse(BaseModel):
    match: bool
    score: float


class FaceCropInput(BaseModel):
    b64image: str = Field('base64', description="image")


crop_tag = Tag(name="FaceCrop", description="FaceMatch")


class FaceCropResponse(BaseModel):
    cropped_faces: list


def match_faces(face_encoding1, face_encoding2):
    matches = face_recognition.compare_faces(
        [face_encoding1], face_encoding2, tolerance=0.4)
    score = face_recognition.face_distance([face_encoding1], face_encoding2)[0]
    return matches[0], 1-score

def match_deepfaces(face_encoding1, face_encoding2):
    result = DeepFace.verify(img1_path = face_encoding1, img2_path = face_encoding2)
    return result


def crop_faces(image_array):
    # Find faces in the image
    face_locations = face_recognition.face_locations(image_array)

    cropped_faces = []

    # Crop and append each face found
    for face_location in face_locations:
        top, right, bottom, left = face_location
        face_image = image_array[top:bottom, left:right]
        cropped_faces.append(face_image)

    return cropped_faces


@matching.route("/api/facematch", methods=["GET", "POST"])
def FaceMatch():
    try:
        logger.debug('[facematch]|[BEGIN]|/api/facematch')
        # Predefined image paths
        image1_path = "uploads/face_compare/face_capture.png"
        image2_path = "uploads/face_registers/register_face.png"

        # Load images from paths
        with open(image1_path, "rb") as image_file1, open(image2_path, "rb") as image_file2:
            image_bytes1 = image_file1.read()
            image_bytes2 = image_file2.read()

        logger.debug('[facematch]|[OPERATE]|image_bytes1|image_bytes2')
        # Convert bytes to an image file-like object
        image1 = Image.open(io.BytesIO(image_bytes1)).convert('RGB')
        image2 = Image.open(io.BytesIO(image_bytes2)).convert('RGB')

        face1 = np.array(image1)
        face2 = np.array(image2)

        face_encoding1 = face_recognition.face_encodings(face1)[0]
        face_encoding2 = face_recognition.face_encodings(face2)[0]
        logger.debug('[facematch]|[OPERATE]|face_encoding1|face_encoding2')
        match, score = match_faces(face_encoding1, face_encoding2)
        logger.debug('[facematch]|[OPERATE]|match|score')
        # Do something with the text
        try:
            response_model = FaceMatchResponse(match=match, score=score)
            logger.debug('[facematch]|[OPERATE]|response_model')
            return jsonify(response_model.dict())
        except Exception as e:
            logger.error(f'[facematch]|[error]|{str(e)}')
            return jsonify({"error": str(e)})
    except Exception as e:
        logger.error(f'[facematch]|[error]|{str(e)}')
        return jsonify({"error": str(e)})

@matching.post("/api/facedeepmatch")
def DeepFaceMatch(body: FacesMatchInput):
    try:
        logger.debug('[facematch]|[BEGIN]|/api/facematch')
        # Load base64-encoded images
        image_bytes1 = base64.b64decode(body.b64image1)
        image_bytes2 = base64.b64decode(body.b64image2)
        logger.debug('[facematch]|[OPERATE]|image_bytes1|image_bytes2')
        # Convert bytes to an image file-like object
        image1 = Image.open(io.BytesIO(image_bytes1)).convert('RGB')
        image2 = Image.open(io.BytesIO(image_bytes2)).convert('RGB')

        face1 = np.array(image1)
        face2 = np.array(image2)

        logger.debug('[facematch]|[OPERATE]|face_encoding1|face_encoding2')
        result = match_deepfaces(face1, face2)
        print(result)
        logger.debug('[facematch]|[OPERATE]|match|score')
        # Do something with the text
        try:
            response_model = FaceMatchResponse(match=result['verified'], score=1-result['distance'])
            logger.debug('[facematch]|[OPERATE]|response_model')
            return jsonify(response_model.dict())
        except Exception as e:
            logger.error(f'[facematch]|[error]|{str(e)}')
            return jsonify({"error": str(e)})
    except Exception as e:
        logger.error(f'[facematch]|[error]|{str(e)}')
        return jsonify({"error": str(e)})

@matching.post("/api/facecrop")
def FaceCrop(body: FaceCropInput):
    try:
        # Load base64-encoded image
        image_bytes = base64.b64decode(body.b64image)

        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_bytes))

        # Convert PIL Image to numpy array
        image_array = np.array(image)

        # Convert color format if needed (face_recognition uses RGB)
        if image_array.shape[2] == 4:  # RGBA format
            image_array = image_array[:, :, :3]  # Discard alpha channel

        # Crop faces
        cropped_faces = crop_faces(image_array)

        # Convert cropped faces to PIL Images
        cropped_images = [Image.fromarray(face) for face in cropped_faces]

        # Convert PIL Images to base64-encoded images
        cropped_base64_images = []
        for face_image in cropped_images:
            # Create an in-memory stream to hold the PNG image data
            image_stream = io.BytesIO()

            # Save the image to the in-memory stream in PNG format
            face_image.save(image_stream, format="PNG")

            # Get the byte data from the stream
            image_bytes = image_stream.getvalue()

            # Encode the byte data as base64
            base64_image = base64.b64encode(image_bytes).decode("utf-8")

            # Append the base64-encoded PNG image to the list
            cropped_base64_images.append(base64_image)

        return jsonify({"cropped_faces": cropped_base64_images})

    except Exception as e:
        return jsonify({"error": str(e)})

@matching.route('/upload_video', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video = request.files['video']
    video_path = os.path.join(UPLOAD_FOLDER, video.filename)
    video.save(video_path)
    return jsonify({"message": "Video uploaded successfully"}), 200


@matching.route('/')
def index():
    return render_template("face_timetrack.html")

@matching.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "error": "No file part"})
        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "error": "No selected file"})
        if file:
            image_path = os.path.join(UPLOAD_FOLDER, 'face_compare', 'face_capture.png')
            file.save(image_path)
            return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
