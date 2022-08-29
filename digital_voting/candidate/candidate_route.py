from fastapi import APIRouter
import hashlib
import csv
from . import schemas


router = APIRouter(prefix="/candidate", tags=["candidate"])

@router.post("/registration")
def candidate_registration(data : schemas.CandidateRegistration):
    candidate_data = {'first_name': data.first_name,
            'middle_name': data.middle_name,
            'last_name': data.last_name,
            'age': data.age,
            'location': data.location,
            'facial_points': data.face_encoded_list}
    encrypted_data = hashlib.sha512(str(candidate_data).encode()).hexdigest()
    writeable_data = [encrypted_data, data.face_encoded_list]
    with open('candidate_credentials.csv', "a+") as f:
        writer = csv.writer(f)
        writer.writerow(writeable_data)
    return writeable_data
