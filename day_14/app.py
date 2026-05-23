from flask import Flask, render_template, request
from ultralytics import YOLO
from flask import send_from_directory

app = Flask(__name__)
model = YOLO("yolov8n.pt")

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["image"]           # 获取用户上传的图片
    save_path = "uploads/" + file.filename
    file.save(save_path)
    results = model(save_path)
    result = results[0]
    result_path = "uploads/result_" + file.filename
    result.save(filename=result_path)
    return render_template(
        "result.html",
        original_url=f"/uploads/{file.filename}",
        result_url=f"/uploads/result_{file.filename}"
    )

@app.route("/uploads/<filename>")
def get_file(filename):
    return send_from_directory("uploads", filename)

if __name__ == "__main__":
    app.run(debug=True)