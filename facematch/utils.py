import os
import face_recognition
# from PIL import Image, ImageDraw


def identify(student_data, file_name):

    student_face_encodings = []
    student_face_id = []

    attendance = {}  # Store the attendance value

    for student in student_data:
        student_image = face_recognition.load_image_file(f'.{student.image.url}')
        student_face_encode = face_recognition.face_encodings(student_image)[0]
        student_face_encodings.append(student_face_encode)
        student_face_id.append(student.id)

    # Load test image to find faces in
    test_image = face_recognition.load_image_file(f'./media/raw_files/{file_name}')

    # Find faces in test image
    face_locations = face_recognition.face_locations(test_image)
    face_encodings = face_recognition.face_encodings(test_image, face_locations)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(student_face_encodings, face_encoding)

        # If match
        if True in matches:
            first_match_index = matches.index(True)
            id = student_face_id[first_match_index]

            attendance[id] = True    # Present

    for student in student_data:
        if student.id in attendance.keys():
            continue
        else:
            attendance[student.id] = False  # Absent

    os.remove(f'./media/raw_files/{file_name}')
    return attendance


# def handle_uploaded_file(f):
#     with open('unknown.png', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)
