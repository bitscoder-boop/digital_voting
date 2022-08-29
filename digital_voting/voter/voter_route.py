from fastapi import APIRouter
from typing import Optional, List
import hashlib
import csv
import numpy as np
import ast
import face_recognition
from . import schemas


router = APIRouter(prefix="/voter", tags=["voters"])

@router.post("/registration")
def voter_registration(data : schemas.VoterRegistration):
    user_data = {'first_name': data.first_name,
            'middle_name': data.middle_name,
            'last_name': data.last_name,
            'age': data.age,
            'location': data.location,
            'facial_points': data.face_encoded_list}
    encrypted_data = hashlib.sha512(str(user_data).encode()).hexdigest()
    writeable_data = [encrypted_data, data.face_encoded_list]
    with open('credentials.csv', "a+") as f:
        writer = csv.writer(f)
        writer.writerow(writeable_data)
    return writeable_data

@router.post("/cast_vote")
def cast_vote(data: schemas.CastVote):
    current_facial_points = np.array(data.facial_points)
    user_public_key = data.public_key
    candidate_key = data.candidate_key
    output_data = []
    output_dict = {}
    # read data from credentials.json
    with open('credentials.csv', 'r') as f:
        reader = csv.reader(f)
        for i in reader:
            output_data.append(i)
    for item in output_data:
        output_dict[item[0]] = item[1]
    known_encoding = ast.literal_eval(output_dict[user_public_key])
    match = face_recognition.compare_faces([known_encoding], current_facial_points)
    return str(match[0])
