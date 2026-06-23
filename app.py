import sqlite3
from flask import *
import os
import uuid
from functools import wraps
from werkzeug.utils import secure_filename
from flask import send_file
from report_generator import generate_report
import tensorflow as tf
import numpy as np
from PIL import Image, ImageOps
from disease_info import disease_cards, disease_details, explanations, solutions
from gradcam import save_gradcam

app = Flask(__name__)

app.secret_key = "medvision_ai_secret_key"

DEFAULT_ADMIN_NAME = "Admin"
DEFAULT_ADMIN_EMAIL = "admin@medvision.ai"
DEFAULT_ADMIN_PASSWORD = "admin123"
DATABASE_PATH = "medvision.db"

SUPPORTED_LANGUAGES = {
    "en": "English",
    "kn": "ಕನ್ನಡ"
}

TRANSLATIONS = {
    "kn": {
        "Home": "ಮುಖಪುಟ",
        "Dashboard": "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        "History": "ಇತಿಹಾಸ",
        "Reports": "ವರದಿಗಳು",
        "Camera": "ಕ್ಯಾಮೆರಾ",
        "About Us": "ನಮ್ಮ ಬಗ್ಗೆ",
        "Feedback": "ಪ್ರತಿಕ್ರಿಯೆ",
        "Login": "ಲಾಗಿನ್",
        "Register": "ನೋಂದಣಿ",
        "Admin": "ನಿರ್ವಾಹಕ",
        "Logout": "ಲಾಗ್ ಔಟ್",
        "Language": "ಭಾಷೆ",
        "Admin Dashboard": "ನಿರ್ವಾಹಕ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        "Advanced Admin Control Center": "ಮುನ್ನಡೆದ ನಿರ್ವಾಹಕ ನಿಯಂತ್ರಣ ಕೇಂದ್ರ",
        "Manage users, predictions, feedback, and model review status from one responsive page.": "ಒಂದು ಪ್ರತಿಕ್ರಿಯಾಶೀಲ ಪುಟದಿಂದ ಬಳಕೆದಾರರು, ಊಹೆಗಳು, ಪ್ರತಿಕ್ರಿಯೆ ಮತ್ತು ಮಾದರಿ ಪರಿಶೀಲನೆ ಸ್ಥಿತಿಯನ್ನು ನಿರ್ವಹಿಸಿ.",
        "Total Users": "ಒಟ್ಟು ಬಳಕೆದಾರರು",
        "Total Predictions": "ಒಟ್ಟು ಊಹೆಗಳು",
        "Most Common Disease": "ಅತ್ಯಂತ ಸಾಮಾನ್ಯ ರೋಗ",
        "Verified Accuracy": "ಪರಿಶೀಲಿಸಿದ ನಿಖರತೆ",
        "Needs Review": "ಪರಿಶೀಲನೆ ಅಗತ್ಯ",
        "Search": "ಹುಡುಕಿ",
        "Filter": "ಫಿಲ್ಟರ್",
        "All": "ಎಲ್ಲಾ",
        "Unreviewed": "ಪರಿಶೀಲಿಸಿಲ್ಲ",
        "Correct": "ಸರಿಯಾಗಿದೆ",
        "Incorrect": "ತಪ್ಪಾಗಿದೆ",
        "Update": "ನವೀಕರಿಸಿ",
        "Delete": "ಅಳಿಸಿ",
        "Save": "ಉಳಿಸಿ",
        "Users": "ಬಳಕೆದಾರರು",
        "Predictions": "ಊಹೆಗಳು",
        "Recent Feedback": "ಇತ್ತೀಚಿನ ಪ್ರತಿಕ್ರಿಯೆ",
        "Name": "ಹೆಸರು",
        "Email": "ಇಮೇಲ್",
        "Password": "ಪಾಸ್‌ವರ್ಡ್",
        "Role": "ಪಾತ್ರ",
        "Actions": "ಕ್ರಿಯೆಗಳು",
        "Image": "ಚಿತ್ರ",
        "Disease": "ರೋಗ",
        "Confidence": "ನಂಬಿಕೆ",
        "Date": "ದಿನಾಂಕ",
        "Review": "ಪರಿಶೀಲನೆ",
        "Verified Disease": "ಪರಿಶೀಲಿಸಿದ ರೋಗ",
        "Admin Notes": "ನಿರ್ವಾಹಕ ಟಿಪ್ಪಣಿಗಳು",
        "Model Review": "ಮಾದರಿ ಪರಿಶೀಲನೆ",
        "Reviewed": "ಪರಿಶೀಲಿಸಲಾಗಿದೆ",
        "Model accuracy needs admin-confirmed labels. Mark predictions as correct or incorrect after clinical/user verification.": "ಮಾದರಿ ನಿಖರತೆಗೆ ನಿರ್ವಾಹಕರಿಂದ ದೃಢೀಕರಿಸಿದ ಲೇಬಲ್‌ಗಳು ಬೇಕು. ಕ್ಲಿನಿಕಲ್/ಬಳಕೆದಾರ ಪರಿಶೀಲನೆಯ ನಂತರ ಊಹೆಗಳನ್ನು ಸರಿಯಾಗಿದೆ ಅಥವಾ ತಪ್ಪಾಗಿದೆ ಎಂದು ಗುರುತಿಸಿ.",
        "No data available.": "ಡೇಟಾ ಲಭ್ಯವಿಲ್ಲ.",
        "Upload skin image": "ಚರ್ಮದ ಚಿತ್ರ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
        "Analyze Image": "ಚಿತ್ರ ವಿಶ್ಲೇಷಿಸಿ",
        "Average Confidence": "ಸರಾಸರಿ ನಂಬಿಕೆ",
        "Most Common Result": "ಅತ್ಯಂತ ಸಾಮಾನ್ಯ ಫಲಿತಾಂಶ",
        "Recent Predictions": "ಇತ್ತೀಚಿನ ಊಹೆಗಳು",
        "View All": "ಎಲ್ಲವನ್ನೂ ನೋಡಿ",
        "Download PDF Report": "PDF ವರದಿ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ",
        "Analyze Another Image": "ಮತ್ತೊಂದು ಚಿತ್ರ ವಿಶ್ಲೇಷಿಸಿ",
        "Prediction Summary": "ಊಹೆ ಸಾರಾಂಶ",
        "Explanation": "ವಿವರಣೆ",
        "Suggested Solution": "ಸೂಚಿಸಿದ ಪರಿಹಾರ",
        "Disease Details": "ರೋಗ ವಿವರಗಳು",
        "Medical Use Reminder": "ವೈದ್ಯಕೀಯ ಬಳಕೆ ನೆನಪಿನೋಟ",
        "Submit Feedback": "ಪ್ರತಿಕ್ರಿಯೆ ಕಳುಹಿಸಿ",
        "Create Account": "ಖಾತೆ ರಚಿಸಿ",
        "Email Address": "ಇಮೇಲ್ ವಿಳಾಸ",
        "Full Name": "ಪೂರ್ಣ ಹೆಸರು",
        "Confirm Password": "ಪಾಸ್‌ವರ್ಡ್ ದೃಢೀಕರಿಸಿ",
        "Forgot Password?": "ಪಾಸ್‌ವರ್ಡ್ ಮರೆತಿರಾ?",
        "Reset Password": "ಪಾಸ್‌ವರ್ಡ್ ಮರುಹೊಂದಿಸಿ",
        "Send Reset Link": "ಮರುಹೊಂದಿಸುವ ಲಿಂಕ್ ಕಳುಹಿಸಿ",
        "Back to Login": "ಲಾಗಿನ್‌ಗೆ ಹಿಂತಿರುಗಿ",
        "Download": "ಡೌನ್‌ಲೋಡ್",
        "Report": "ವರದಿ",
        "AI-powered skin disease screening": "AI ಆಧಾರಿತ ಚರ್ಮ ರೋಗ ಪರಿಶೀಲನೆ",
        "Detect possible skin diseases with clearer AI guidance.": "ಸ್ಪಷ್ಟ AI ಮಾರ್ಗದರ್ಶನದೊಂದಿಗೆ ಸಾಧ್ಯವಾದ ಚರ್ಮ ರೋಗಗಳನ್ನು ಪತ್ತೆ ಮಾಡಿ.",
        "Upload a skin image, get an AI-assisted prediction, review disease-specific explanation, and download a structured report for follow-up discussion.": "ಚರ್ಮದ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ, AI ಸಹಾಯದ ಊಹೆ ಪಡೆಯಿರಿ, ರೋಗ-ನಿರ್ದಿಷ್ಟ ವಿವರಣೆಯನ್ನು ನೋಡಿ ಮತ್ತು ಮುಂದಿನ ಚರ್ಚೆಗೆ ವರದಿ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ.",
        "Open Dashboard": "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್ ತೆರೆಯಿರಿ",
        "Start Free Analysis": "ಉಚಿತ ವಿಶ್ಲೇಷಣೆ ಆರಂಭಿಸಿ",
        "Explore Features": "ವೈಶಿಷ್ಟ್ಯಗಳನ್ನು ನೋಡಿ",
        "Disease classes": "ರೋಗ ವರ್ಗಗಳು",
        "Report export": "ವರದಿ ರಫ್ತು",
        "AI availability": "AI ಲಭ್ಯತೆ",
        "Sample AI Result": "ಮಾದರಿ AI ಫಲಿತಾಂಶ",
        "Features": "ವೈಶಿಷ್ಟ್ಯಗಳು",
        "Designed for a complete prediction workflow.": "ಪೂರ್ಣ ಊಹೆ ಕಾರ್ಯಪ್ರವಾಹಕ್ಕಾಗಿ ವಿನ್ಯಾಸಗೊಳಿಸಲಾಗಿದೆ.",
        "Disease Detection": "ರೋಗ ಪತ್ತೆ",
        "Disease Education": "ರೋಗ ಮಾಹಿತಿ",
        "PDF Reports": "PDF ವರದಿಗಳು",
        "Dashboard Charts": "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್ ಚಾರ್ಟ್‌ಗಳು",
        "Disease Guide": "ರೋಗ ಮಾರ್ಗದರ್ಶಿ",
        "Start with the dashboard.": "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ನಿಂದ ಆರಂಭಿಸಿ.",
        "Go to Dashboard": "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್‌ಗೆ ಹೋಗಿ",
        "Welcome": "ಸ್ವಾಗತ",
        "Supported formats: JPG, PNG, JPEG, WEBP": "ಬೆಂಬಲಿತ ರೂಪಗಳು: JPG, PNG, JPEG, WEBP",
        "Disease Pie Chart": "ರೋಗ ಪೈ ಚಾರ್ಟ್",
        "Distribution of your saved predictions.": "ನಿಮ್ಮ ಉಳಿಸಿದ ಊಹೆಗಳ ಹಂಚಿಕೆ.",
        "Pie Chart": "ಪೈ ಚಾರ್ಟ್",
        "No predictions yet": "ಇನ್ನೂ ಊಹೆಗಳಿಲ್ಲ",
        "Your recent results will appear here after analysis.": "ವಿಶ್ಲೇಷಣೆಯ ನಂತರ ನಿಮ್ಮ ಇತ್ತೀಚಿನ ಫಲಿತಾಂಶಗಳು ಇಲ್ಲಿ ಕಾಣುತ್ತವೆ.",
        "Camera Disease Prediction": "ಕ್ಯಾಮೆರಾ ರೋಗ ಊಹೆ",
        "Start Camera": "ಕ್ಯಾಮೆರಾ ಪ್ರಾರಂಭಿಸಿ",
        "Capture Photo": "ಫೋಟೋ ಸೆರೆಹಿಡಿಯಿರಿ",
        "Predict Disease": "ರೋಗ ಊಹಿಸಿ",
        "How to get better results": "ಉತ್ತಮ ಫಲಿತಾಂಶ ಪಡೆಯುವ ವಿಧಾನ",
        "Use clear lighting": "ಸ್ಪಷ್ಟ ಬೆಳಕು ಬಳಸಿ",
        "Frame the lesion": "ಗಾಯವನ್ನು ಸರಿಯಾಗಿ ಫ್ರೇಮ್ ಮಾಡಿ",
        "Follow up clinically": "ವೈದ್ಯಕೀಯವಾಗಿ ಮುಂದುವರಿಸಿ",
        "AI Diagnosis Result": "AI ನಿರ್ಣಯ ಫಲಿತಾಂಶ",
        "Review the confidence score, disease explanation, and recommended next steps.": "ನಂಬಿಕೆ ಅಂಕ, ರೋಗ ವಿವರಣೆ ಮತ್ತು ಶಿಫಾರಸು ಮಾಡಿದ ಮುಂದಿನ ಹಂತಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.",
        "Confidence Score": "ನಂಬಿಕೆ ಅಂಕ",
        "Uploaded Image": "ಅಪ್‌ಲೋಡ್ ಮಾಡಿದ ಚಿತ್ರ",
        "Original Image": "ಮೂಲ ಚಿತ್ರ",
        "AI Attention Map": "AI ಗಮನ ನಕ್ಷೆ",
        "Completed": "ಪೂರ್ಣಗೊಂಡಿದೆ",
        "Common Visible Signs": "ಸಾಮಾನ್ಯ ಗೋಚರ ಲಕ್ಷಣಗಳು",
        "Care Focus": "ಪಾಲನೆಯ ಗಮನ",
        "AI Support": "AI ಬೆಂಬಲ",
        "Clinical Review": "ವೈದ್ಯಕೀಯ ಪರಿಶೀಲನೆ",
        "Follow Changes": "ಬದಲಾವಣೆಗಳನ್ನು ಗಮನಿಸಿ",
        "Help improve MedVision AI": "MedVision AI ಸುಧಾರಿಸಲು ಸಹಾಯ ಮಾಡಿ",
        "Send Feedback": "ಪ್ರತಿಕ್ರಿಯೆ ಕಳುಹಿಸಿ",
        "Rating": "ಮೌಲ್ಯಮಾಪನ",
        "Message": "ಸಂದೇಶ",
        "No feedback yet. Be the first to share your experience.": "ಇನ್ನೂ ಪ್ರತಿಕ್ರಿಯೆ ಇಲ್ಲ. ನಿಮ್ಮ ಅನುಭವವನ್ನು ಮೊದಲಿಗೆ ಹಂಚಿಕೊಳ್ಳಿ.",
        "About MedVision AI": "MedVision AI ಬಗ್ಗೆ",
        "Image Analysis": "ಚಿತ್ರ ವಿಶ್ಲೇಷಣೆ",
        "Disease Guidance": "ರೋಗ ಮಾರ್ಗದರ್ಶನ",
        "Reports & History": "ವರದಿಗಳು ಮತ್ತು ಇತಿಹಾಸ",
        "Important Medical Note": "ಮುಖ್ಯ ವೈದ್ಯಕೀಯ ಸೂಚನೆ",
        "Diseases Covered": "ಒಳಗೊಂಡಿರುವ ರೋಗಗಳು",
        "AI Powered Medical Diagnosis Platform": "AI ಆಧಾರಿತ ವೈದ್ಯಕೀಯ ನಿರ್ಣಯ ವೇದಿಕೆ",
        "Default Admin Login": "ಡೀಫಾಲ್ಟ್ ನಿರ್ವಾಹಕ ಲಾಗಿನ್",
        "Remember Me": "ನನ್ನನ್ನು ನೆನಪಿಡಿ",
        "Don't have an account?": "ಖಾತೆ ಇಲ್ಲವೇ?",
        "Join MedVision AI Healthcare Platform": "MedVision AI ಆರೋಗ್ಯ ವೇದಿಕೆಗೆ ಸೇರಿ",
        "Already have an account?": "ಈಗಾಗಲೇ ಖಾತೆ ಇದೆಯೇ?",
        "Enter your email address": "ನಿಮ್ಮ ಇಮೇಲ್ ವಿಳಾಸ ನಮೂದಿಸಿ",
        "Prediction History": "ಊಹೆ ಇತಿಹಾಸ",
        "Search Disease...": "ರೋಗ ಹುಡುಕಿ...",
        "Download reports from your prediction history after analyzing an image.": "ಚಿತ್ರ ವಿಶ್ಲೇಷಿಸಿದ ನಂತರ ನಿಮ್ಮ ಊಹೆ ಇತಿಹಾಸದಿಂದ ವರದಿಗಳನ್ನು ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ.",
        "View Prediction History": "ಊಹೆ ಇತಿಹಾಸ ನೋಡಿ",
        "Camera Prediction": "ಕ್ಯಾಮೆರಾ ಊಹೆ",
        "Capture a clear image and analyze it instantly.": "ಸ್ಪಷ್ಟ ಚಿತ್ರವನ್ನು ಸೆರೆಹಿಡಿದು ತಕ್ಷಣ ವಿಶ್ಲೇಷಿಸಿ.",
        "Live Camera": "ಲೈವ್ ಕ್ಯಾಮೆರಾ",
        "Camera off": "ಕ್ಯಾಮೆರಾ ಆಫ್",
        "Captured Image": "ಸೆರೆಹಿಡಿದ ಚಿತ್ರ",
        "For better accuracy": "ಉತ್ತಮ ನಿಖರತೆಗೆ"
    }
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "static", "models", "disease_model.h5")
LABEL_PATH = os.path.join(BASE_DIR, "static", "models", "label.txt")
UPLOAD_FOLDER = os.path.join("static", "uploads")
HEATMAP_FOLDER = os.path.join("static", "heatmaps")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(HEATMAP_FOLDER, exist_ok=True)

model = tf.keras.models.load_model(MODEL_PATH)

with open(LABEL_PATH, encoding="utf-8") as f:
    class_names = [x.strip() for x in f.readlines()]


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def predict_skin_disease(image_path):

    img = ImageOps.exif_transpose(Image.open(image_path)).convert("RGB")

    img = img.resize((224, 224))

    img = np.array(img) / 255.0

    img = np.expand_dims(img, axis=0)

    prediction = model.predict(img)

    class_index = np.argmax(prediction)

    confidence = float(
        prediction[0][class_index] * 100
    )

    disease = class_names[class_index]

    return disease, round(confidence,2)


def assess_image_quality(image_path):
    img = ImageOps.exif_transpose(Image.open(image_path)).convert("RGB")
    width, height = img.size
    grayscale = np.array(img.convert("L"))
    brightness = float(grayscale.mean())
    contrast = float(grayscale.std())
    warnings = []

    if min(width, height) < 300:
        warnings.append("Image resolution is low. Retake closer with a clearer camera view.")

    if brightness < 45:
        warnings.append("Image is too dark. Use stronger light and avoid shadows.")
    elif brightness > 215:
        warnings.append("Image is too bright. Reduce glare or direct flash.")

    if contrast < 18:
        warnings.append("Image detail is weak or blurry. Hold the camera steady and retake.")

    return warnings


def get_last_conv_layer_name():
    for layer in reversed(model.layers):
        output_shape = getattr(layer, "output_shape", None)
        if output_shape is None and hasattr(layer, "output"):
            output_shape = getattr(layer.output, "shape", None)
        if output_shape is not None and len(output_shape) == 4:
            return layer.name
    return None


LAST_CONV_LAYER = get_last_conv_layer_name()


def get_locale():
    language = session.get("language", "en")
    if language not in SUPPORTED_LANGUAGES:
        return "en"
    return language


def translate(text):
    return TRANSLATIONS.get(get_locale(), {}).get(text, text)


def is_admin_user():
    if bool(session.get("is_admin")) or session.get("user_email") == DEFAULT_ADMIN_EMAIL:
        return True

    user_id = session.get("user_id")
    if not user_id:
        return False

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT email, COALESCE(role, 'user')
    FROM users
    WHERE id=?
    """, (user_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return False

    session["user_email"] = user[0]
    session["is_admin"] = user[1] == "admin" or user[0] == DEFAULT_ADMIN_EMAIL
    return bool(session["is_admin"])


@app.context_processor
def inject_nav_state():
    return {
        "is_logged_in": "user_id" in session,
        "current_user_name": session.get("user_name"),
        "is_admin": is_admin_user(),
        "current_language": get_locale(),
        "language_options": SUPPORTED_LANGUAGES,
        "_": translate,
        "default_admin_email": DEFAULT_ADMIN_EMAIL,
        "default_admin_password": DEFAULT_ADMIN_PASSWORD
    }


def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)
    return wrapped_view


def admin_required(view_func):
    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        if not is_admin_user():
            flash("Admin access required.")
            return redirect(url_for("dashboard"))
        return view_func(*args, **kwargs)
    return wrapped_view


@app.route("/language/<language_code>")
def set_language(language_code):
    if language_code in SUPPORTED_LANGUAGES:
        session["language"] = language_code

    next_url = request.args.get("next")
    if not next_url or not next_url.startswith("/") or next_url.startswith("//"):
        next_url = url_for("home")

    return redirect(next_url)


@app.route("/")
def home():
    return render_template("index.html", disease_cards=disease_cards)


@app.route("/about")
def about():
    return render_template("about.html", disease_cards=disease_cards)


@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        rating = request.form.get("rating", "5").strip()
        message = request.form.get("message", "").strip()

        if not name:
            name = session.get("user_name", "")

        try:
            rating_value = max(1, min(5, int(rating)))
        except ValueError:
            rating_value = 5

        if not name or not email or not message:
            flash("Please fill name, email, and feedback message.")
        else:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO feedback(user_id, name, email, rating, message)
            VALUES(?,?,?,?,?)
            """, (
                session.get("user_id"),
                name,
                email,
                rating_value,
                message
            ))
            conn.commit()
            conn.close()
            flash("Thank you for sharing your feedback.")
            return redirect(url_for("feedback"))

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT name, rating, message, created_at
    FROM feedback
    ORDER BY created_at DESC
    LIMIT 6
    """)
    feedback_entries = cursor.fetchall()
    conn.close()

    return render_template(
        "feedback.html",
        feedback_entries=feedback_entries,
        prefill_name=session.get("user_name", "")
    )

@app.route("/result")
def result():

    return render_template(
        "result.html",
        image_path="/static/uploads/sample.jpg",
        disease="Melanoma",
        confidence=94.7,
        explanation="The lesion contains irregular borders and pigmentation patterns commonly associated with melanoma.",
        solution="Consult a dermatologist immediately for professional diagnosis and biopsy confirmation.",
        details=disease_details.get("Melanoma"),
        prediction_id=None,
        image_quality_warnings=[]
    )

@app.route("/download_report")
@app.route("/download_report/<int:prediction_id>")
@login_required
def download_report(prediction_id=None):

    disease = "Melanoma"
    confidence = 94.5

    explanation = "Potential skin cancer requiring medical evaluation."

    solution = "Consult a dermatologist immediately."

    if prediction_id is not None:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        SELECT disease, confidence
        FROM predictions
        WHERE id=? AND user_id=?
        """, (prediction_id, session["user_id"]))

        prediction = cursor.fetchone()
        conn.close()

        if prediction is None:
            return "Report not found", 404

        disease = prediction[0]
        confidence = round(prediction[1], 2)
        explanation = explanations.get(disease, "No explanation available.")
        solution = solutions.get(disease, "Consult a healthcare professional.")

    pdf_path = "medical_report.pdf"

    generate_report(
        pdf_path,
        disease,
        confidence,
        explanation,
        solution
    )

    return send_file(
        pdf_path,
        as_attachment=True
    )

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip().lower()
        password = request.form["password"]

        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, name, email, password, COALESCE(role, 'user') FROM users WHERE email=? AND password=?",
            (email,password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            session["user_id"] = user[0]
            session["user_name"] = user[1]
            session["user_email"] = user[2]
            session["is_admin"] = user[4] == "admin" or user[2] == DEFAULT_ADMIN_EMAIL
            return redirect("/dashboard")

        return "Invalid Email or Password"

    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            return "Passwords do not match"

        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO users(name,email,password)
        VALUES(?,?,?)
        """,(name,email,password))

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


def column_exists(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    return any(row[1] == column_name for row in cursor.fetchall())


def ensure_column(cursor, table_name, column_name, column_definition):
    if not column_exists(cursor, table_name, column_name):
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_definition}")


def initialize_database():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT,
    role TEXT DEFAULT 'user'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    image_path TEXT,
    disease TEXT,
    confidence REAL,
    review_status TEXT DEFAULT 'unreviewed',
    verified_disease TEXT,
    admin_notes TEXT,
    reviewed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    name TEXT,
    email TEXT,
    rating INTEGER,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    ensure_column(cursor, "users", "role", "role TEXT DEFAULT 'user'")
    ensure_column(cursor, "predictions", "review_status", "review_status TEXT DEFAULT 'unreviewed'")
    ensure_column(cursor, "predictions", "verified_disease", "verified_disease TEXT")
    ensure_column(cursor, "predictions", "admin_notes", "admin_notes TEXT")
    ensure_column(cursor, "predictions", "reviewed_at", "reviewed_at TIMESTAMP")

    cursor.execute("SELECT id FROM users WHERE email=?", (DEFAULT_ADMIN_EMAIL,))
    default_admin = cursor.fetchone()

    if default_admin is None:
        cursor.execute("""
        INSERT INTO users(name,email,password,role)
        VALUES(?,?,?,?)
        """, (
            DEFAULT_ADMIN_NAME,
            DEFAULT_ADMIN_EMAIL,
            DEFAULT_ADMIN_PASSWORD,
            "admin"
        ))
    else:
        cursor.execute("""
        UPDATE users
        SET role='admin'
        WHERE email=?
        """, (DEFAULT_ADMIN_EMAIL,))

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_predictions_user_id ON predictions(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_predictions_review_status ON predictions(review_status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_feedback_created_at ON feedback(created_at)")

    conn.commit()
    conn.close()


initialize_database()

@app.route("/forgot_password", methods=["GET","POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form["email"]

        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            return "Password reset feature will be added with Email OTP."

        return "Email not found."

    return render_template("forgot_password.html")

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

@app.route("/history")
@login_required
def history():

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, image_path, disease, confidence, created_at
    FROM predictions
    WHERE user_id=?
    ORDER BY created_at DESC
    """, (session["user_id"],))

    predictions = cursor.fetchall()

    conn.close()

    return render_template(
        "history.html",
        predictions=predictions
    )

@app.route("/dashboard")
@login_required
def dashboard():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*), COALESCE(ROUND(AVG(confidence), 2), 0)
    FROM predictions
    WHERE user_id=?
    """, (session["user_id"],))
    total_predictions, average_confidence = cursor.fetchone()

    cursor.execute("""
    SELECT disease, COUNT(*)
    FROM predictions
    WHERE user_id=?
    GROUP BY disease
    ORDER BY COUNT(*) DESC, disease ASC
    """, (session["user_id"],))
    disease_counts = cursor.fetchall()

    cursor.execute("""
    SELECT id, image_path, disease, confidence, created_at
    FROM predictions
    WHERE user_id=?
    ORDER BY created_at DESC
    LIMIT 5
    """, (session["user_id"],))
    recent_predictions = cursor.fetchall()

    conn.close()

    has_chart_data = len(disease_counts) > 0
    chart_labels = [row[0] for row in disease_counts] if has_chart_data else ["No predictions yet"]
    chart_values = [row[1] for row in disease_counts] if has_chart_data else [1]
    top_disease = disease_counts[0][0] if has_chart_data else "No predictions yet"

    return render_template(
        "dashboard.html",
        total_predictions=total_predictions,
        average_confidence=average_confidence,
        top_disease=top_disease,
        recent_predictions=recent_predictions,
        chart_labels=chart_labels,
        chart_values=chart_values,
        has_chart_data=has_chart_data
    )


@app.route("/reports")
@login_required
def reports():
    return render_template("reports.html")


@app.route("/camera")
@login_required
def camera():
    return render_template("camera.html")


def handle_prediction_upload():
    image = request.files.get("image")

    if image is None or image.filename == "":
        return "No image selected"

    if not allowed_file(image.filename):
        return "Unsupported file type. Please upload JPG, PNG, JPEG, or WEBP."

    filename = secure_filename(image.filename)
    filename = f"{session['user_id']}_{uuid.uuid4().hex}_{filename}"

    filepath = os.path.join(UPLOAD_FOLDER, filename)

    image.save(filepath)

    image_quality_warnings = assess_image_quality(filepath)

    # AI Prediction
    disease, confidence = predict_skin_disease(filepath)

    explanation = explanations.get(disease, "No explanation available.")
    solution = solutions.get(disease, "Consult a healthcare professional.")
    image_url = "/" + filepath.replace("\\", "/")

    heatmap_url = None
    if LAST_CONV_LAYER:
        heatmap_path = os.path.join(HEATMAP_FOLDER, filename)
        save_gradcam(filepath, model, LAST_CONV_LAYER, heatmap_path)
        heatmap_url = "/" + heatmap_path.replace("\\", "/")

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO predictions(
        user_id,
        image_path,
        disease,
        confidence
    )
    VALUES(?,?,?,?)
    """, (
        session["user_id"],
        image_url,
        disease,
        confidence
    ))
    prediction_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return render_template(
        "result.html",
        image_path=image_url,
        image=image_url,
        heatmap=heatmap_url,
        disease=disease,
        confidence=round(confidence, 2),
        explanation=explanation,
        solution=solution,
        details=disease_details.get(disease),
        prediction_id=prediction_id,
        image_quality_warnings=image_quality_warnings
    )


@app.route("/predict", methods=["POST"])
@login_required
def predict():
    return handle_prediction_upload()


def delete_prediction_files(image_path):
    if not image_path or not image_path.startswith("/static/"):
        return

    static_root = os.path.abspath(os.path.join(BASE_DIR, "static"))
    candidate_paths = [image_path]

    if "/uploads/" in image_path:
        candidate_paths.append(image_path.replace("/uploads/", "/heatmaps/"))

    for url_path in candidate_paths:
        relative_path = url_path.lstrip("/").replace("/", os.sep)
        absolute_path = os.path.abspath(os.path.join(BASE_DIR, relative_path))

        if not absolute_path.startswith(static_root + os.sep):
            continue

        if os.path.isfile(absolute_path):
            os.remove(absolute_path)


@app.route("/admin")
@admin_required
def admin():
    search = request.args.get("search", "").strip()
    review_status = request.args.get("review_status", "all").strip()
    allowed_review_statuses = {"all", "unreviewed", "needs_review", "correct", "incorrect"}
    if review_status not in allowed_review_statuses:
        review_status = "all"

    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM predictions")
    total_predictions = cursor.fetchone()[0]

    cursor.execute("""
    SELECT disease, COUNT(*) AS total
    FROM predictions
    GROUP BY disease
    ORDER BY total DESC, disease ASC
    LIMIT 1
    """)
    result = cursor.fetchone()
    common_disease = result["disease"] if result else "N/A"

    cursor.execute("""
    SELECT
        COUNT(*) AS reviewed_total,
        COALESCE(SUM(CASE WHEN review_status='correct' THEN 1 ELSE 0 END), 0) AS correct_total
    FROM predictions
    WHERE review_status IN ('correct', 'incorrect')
    """)
    review_totals = cursor.fetchone()
    reviewed_total = review_totals["reviewed_total"]
    correct_total = review_totals["correct_total"]
    verified_accuracy = round((correct_total / reviewed_total) * 100, 2) if reviewed_total else 0

    cursor.execute("""
    SELECT COUNT(*)
    FROM predictions
    WHERE review_status IN ('unreviewed', 'needs_review')
    """)
    needs_review = cursor.fetchone()[0]

    user_params = []
    user_where = ""
    if search:
        user_where = "WHERE name LIKE ? OR email LIKE ?"
        search_term = f"%{search}%"
        user_params.extend([search_term, search_term])

    cursor.execute(f"""
    SELECT id, name, email, COALESCE(role, 'user') AS role
    FROM users
    {user_where}
    ORDER BY CASE WHEN role='admin' THEN 0 ELSE 1 END, name ASC
    LIMIT 50
    """, user_params)
    users = cursor.fetchall()

    prediction_where = []
    prediction_params = []
    if search:
        search_term = f"%{search}%"
        prediction_where.append("(p.disease LIKE ? OR u.name LIKE ? OR u.email LIKE ?)")
        prediction_params.extend([search_term, search_term, search_term])
    if review_status != "all":
        prediction_where.append("p.review_status=?")
        prediction_params.append(review_status)

    prediction_where_sql = ""
    if prediction_where:
        prediction_where_sql = "WHERE " + " AND ".join(prediction_where)

    cursor.execute(f"""
    SELECT
        p.id,
        p.image_path,
        p.disease,
        p.confidence,
        COALESCE(p.review_status, 'unreviewed') AS review_status,
        COALESCE(p.verified_disease, '') AS verified_disease,
        COALESCE(p.admin_notes, '') AS admin_notes,
        p.reviewed_at,
        p.created_at,
        COALESCE(u.name, 'Deleted user') AS user_name,
        COALESCE(u.email, 'N/A') AS user_email
    FROM predictions p
    LEFT JOIN users u ON u.id = p.user_id
    {prediction_where_sql}
    ORDER BY p.created_at DESC
    LIMIT 80
    """, prediction_params)
    predictions = cursor.fetchall()

    cursor.execute("""
    SELECT id, name, email, rating, message, created_at
    FROM feedback
    ORDER BY created_at DESC
    LIMIT 20
    """)
    feedback_entries = cursor.fetchall()

    conn.close()

    return render_template(
        "admin.html",
        total_users=total_users,
        total_predictions=total_predictions,
        common_disease=common_disease,
        reviewed_total=reviewed_total,
        correct_total=correct_total,
        verified_accuracy=verified_accuracy,
        needs_review=needs_review,
        users=users,
        predictions=predictions,
        feedback_entries=feedback_entries,
        disease_options=class_names,
        review_status=review_status,
        search=search
    )


@app.route("/admin/users/<int:user_id>/update", methods=["POST"])
@admin_required
def admin_update_user(user_id):
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    role = request.form.get("role", "user").strip()

    if role not in {"user", "admin"}:
        role = "user"

    if not name or not email:
        flash("Name and email are required.")
        return redirect(url_for("admin"))

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE id=?", (user_id,))
    existing_user = cursor.fetchone()

    if not existing_user:
        conn.close()
        flash("User not found.")
        return redirect(url_for("admin"))

    if existing_user[0] == DEFAULT_ADMIN_EMAIL:
        email = DEFAULT_ADMIN_EMAIL
        role = "admin"

    try:
        if password.strip():
            cursor.execute("""
            UPDATE users
            SET name=?, email=?, password=?, role=?
            WHERE id=?
            """, (name, email, password, role, user_id))
        else:
            cursor.execute("""
            UPDATE users
            SET name=?, email=?, role=?
            WHERE id=?
            """, (name, email, role, user_id))

        conn.commit()
        flash("User saved successfully.")
    except sqlite3.IntegrityError:
        flash("Email already exists.")
    finally:
        conn.close()

    if user_id == session.get("user_id"):
        session["user_name"] = name
        session["user_email"] = email
        session["is_admin"] = role == "admin"

    return redirect(url_for("admin"))


@app.route("/admin/users/<int:user_id>/delete", methods=["POST"])
@admin_required
def admin_delete_user(user_id):
    if user_id == session.get("user_id"):
        flash("You cannot delete the active admin account.")
        return redirect(url_for("admin"))

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        flash("User not found.")
        return redirect(url_for("admin"))

    if user[0] == DEFAULT_ADMIN_EMAIL:
        conn.close()
        flash("Default admin account cannot be deleted.")
        return redirect(url_for("admin"))

    cursor.execute("SELECT image_path FROM predictions WHERE user_id=?", (user_id,))
    image_paths = [row[0] for row in cursor.fetchall()]

    cursor.execute("DELETE FROM feedback WHERE user_id=?", (user_id,))
    cursor.execute("DELETE FROM predictions WHERE user_id=?", (user_id,))
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()

    for image_path in image_paths:
        delete_prediction_files(image_path)

    flash("User and related data deleted.")
    return redirect(url_for("admin"))


@app.route("/admin/predictions/<int:prediction_id>/update", methods=["POST"])
@admin_required
def admin_update_prediction(prediction_id):
    disease = request.form.get("disease", "").strip()
    verified_disease = request.form.get("verified_disease", "").strip()
    admin_notes = request.form.get("admin_notes", "").strip()[:1000]
    review_status_value = request.form.get("review_status", "unreviewed").strip()

    if review_status_value not in {"unreviewed", "needs_review", "correct", "incorrect"}:
        review_status_value = "unreviewed"

    try:
        confidence = float(request.form.get("confidence", "0"))
        confidence = max(0, min(100, round(confidence, 2)))
    except ValueError:
        flash("Confidence must be a number.")
        return redirect(url_for("admin"))

    if not disease:
        flash("Disease is required.")
        return redirect(url_for("admin"))

    if review_status_value == "correct" and not verified_disease:
        verified_disease = disease

    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE predictions
    SET disease=?,
        confidence=?,
        review_status=?,
        verified_disease=?,
        admin_notes=?,
        reviewed_at=CASE WHEN ?='unreviewed' THEN NULL ELSE CURRENT_TIMESTAMP END
    WHERE id=?
    """, (
        disease,
        confidence,
        review_status_value,
        verified_disease,
        admin_notes,
        review_status_value,
        prediction_id
    ))
    conn.commit()
    conn.close()

    flash("Prediction review saved.")
    return redirect(url_for("admin"))


@app.route("/admin/predictions/<int:prediction_id>/delete", methods=["POST"])
@admin_required
def admin_delete_prediction(prediction_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT image_path FROM predictions WHERE id=?", (prediction_id,))
    prediction = cursor.fetchone()

    if prediction:
        cursor.execute("DELETE FROM predictions WHERE id=?", (prediction_id,))
        conn.commit()
        image_path = prediction[0]
    else:
        image_path = None

    conn.close()

    if image_path:
        delete_prediction_files(image_path)
        flash("Prediction deleted.")
    else:
        flash("Prediction not found.")

    return redirect(url_for("admin"))


@app.route("/admin/feedback/<int:feedback_id>/delete", methods=["POST"])
@admin_required
def admin_delete_feedback(feedback_id):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM feedback WHERE id=?", (feedback_id,))
    conn.commit()
    conn.close()

    flash("Feedback deleted.")
    return redirect(url_for("admin"))

@app.route("/upload", methods=["POST"])
@login_required
def upload():
    return handle_prediction_upload()

if __name__ == "__main__":
    app.run(debug=True)
