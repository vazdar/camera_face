from flask import Flask , request
import cv2 , os , face_recognition , csv
from datetime import datetime

known_encoding = []
known_name = []


folder = os.listdir("dataset")

for name in folder :
    image = os.listdir(f"dataset/{name}")

    for image_name in image :
        path = f"dataset/{name}/{image_name}"

        face = face_recognition.load_image_file(path)
        encoding = face_recognition.face_encodings(face)

        if len(encoding)>0 :
            known_encoding.append(encoding[0])
            known_name.append(name)

app = Flask(__name__)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

@app.route("/upload", methods=["POST"])
def upload():
    name_result = "UNKNOWN"
    data = request.data

    file_name = "face_demo.jpg"
    with open(file_name, "wb") as f:
        f.write(data)

    image = cv2.imread(file_name)
    if image is None:
        return "Cannot read image", 400

    # ✅ Dùng face_recognition detect thẳng, bỏ OpenCV cascade
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    face_locations = face_recognition.face_locations(rgb_image)
    encodings = face_recognition.face_encodings(rgb_image, face_locations)

    best_name = "UNKNOWN"
    best_distance = 1.0  # càng nhỏ càng giống

    for encoding in encodings:
        distances = face_recognition.face_distance(known_encoding, encoding)
        
        if len(distances) == 0:
            continue
            
        min_dist = min(distances)
        best_match = distances.argmin()

        # ✅ Chỉ lấy khuôn mặt có độ tương đồng cao nhất
        if min_dist < 0.6 and min_dist < best_distance:
            best_distance = min_dist
            best_name = known_name[best_match]

    mark_attendance(best_name)
    return best_name



@app.route("/attendance")
def attendance():
    html = """
    <h2>Danh sách điểm danh</h2>
    <table border="1" cellpadding="8">
        <tr>
            <th>Tên</th>
            <th>Thời gian</th>
        </tr>
    """

    if os.path.exists("datasheet.csv"):
        with open("datasheet.csv", "r") as f:
            reader = csv.reader(f)

            for row in reader:
                if len(row) >= 2:
                    html += f"""
                    <tr>
                        <td>{row[0]}</td>
                        <td>{row[1]}</td>
                    </tr>
                    """

    html += "</table>"

    return html

def mark_attendance(name):
    if name == "UNKNOWN":
        return

    found = False

    if os.path.exists("datasheet.csv"):
        with open("datasheet.csv", "r") as f:
            reader = csv.reader(f)

            for row in reader:
                if len(row) > 0 and row[0] == name:
                    found = True
                    break

    if not found:
        time_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open("datasheet.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name, time_string])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
