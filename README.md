# 🩺 MedVisionAI – AI-Powered Skin Disease Detection System

> An AI-powered **Skin Disease Detection System** built with **Flask**, **TensorFlow/Keras**, **OpenCV**, and **Deep Learning** that analyzes skin lesion images, predicts diseases with confidence scores, generates **Grad-CAM heatmaps**, provides disease information, treatment recommendations, and downloadable PDF medical reports through an intuitive and responsive web interface.

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black)
![TensorFlow](https://img.shields.io/badge/TensorFlow-Deep%20Learning-orange)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-red)
![SQLite](https://img.shields.io/badge/Database-SQLite-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-success)

</p>

---

# 📖 Table of Contents

- Overview
- Features
- Tech Stack
- Project Architecture
- Screenshots
- Installation
- Usage
- Folder Structure
- Model Information
- Future Improvements
- Deployment
- Contributing
- License
- Author

---

# 📖 Overview

**MedVisionAI** is an AI-powered healthcare web application that leverages Deep Learning and Computer Vision to assist in the preliminary detection of skin diseases from uploaded images.

The application uses a trained TensorFlow model to classify skin diseases, visualizes affected regions using Grad-CAM, provides detailed disease information, treatment suggestions, confidence scores, and generates downloadable medical reports.

This project demonstrates the integration of Artificial Intelligence with modern web development using Flask.

> **⚠ Disclaimer**
>
> This project is intended for educational and research purposes only.
> It should **NOT** be used as a replacement for professional medical diagnosis.

---

# ✨ Features

## 🧠 Artificial Intelligence

- Deep Learning-based disease prediction
- High-confidence classification
- TensorFlow/Keras CNN model
- Automatic image preprocessing

---

## 🔥 Explainable AI

- Grad-CAM Heatmap Generation
- Visual explanation of predictions
- Highlight infected regions

---

## 📊 Prediction Results

- Disease Name
- Confidence Score
- Probability Distribution
- Prediction Time

---

## 📚 Disease Information

Displays

- Disease Description
- Causes
- Symptoms
- Risk Factors
- Prevention
- Treatment Suggestions

---

## 📄 PDF Report

Generate downloadable medical reports containing

- Uploaded Image
- Predicted Disease
- Confidence Score
- Heatmap
- Disease Information
- Medical Disclaimer

---

## 👤 User Module

- User Registration
- Login
- Authentication
- Session Management

---

## 🔐 Admin Panel

- Dashboard
- User Management
- Prediction History
- Report Management

---

## 📱 Responsive Design

- Mobile Friendly
- Tablet Friendly
- Desktop Responsive
- Modern UI

---

# 🛠 Tech Stack

## Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript

## Backend

- Python
- Flask

## Machine Learning

- TensorFlow
- Keras
- NumPy
- OpenCV
- Pillow

## Database

- SQLite

## Report Generation

- ReportLab

## Deployment

- Gunicorn
- Render
- PythonAnywhere

---

# 🏗 Project Architecture

```
                User
                  │
                  ▼
          Flask Web Application
                  │
     ┌────────────┼────────────┐
     ▼            ▼            ▼
Image Upload   Authentication  Admin
     │
     ▼
Image Processing
     │
     ▼
TensorFlow Model
     │
     ▼
Disease Prediction
     │
     ▼
Grad-CAM Heatmap
     │
     ▼
Generate PDF Report
```

---

# 📸 Screenshots


```
<img width="1346" height="634" alt="re" src="https://github.com/user-attachments/assets/9a93bb9c-1eb4-424b-8799-af49366d9b51" />
<img width="1342" height="626" alt="login" src="https://github.com/user-attachments/assets/2a9cf1f9-7683-440f-83d2-c247579287ae" />
<img width="1342" height="643" alt="home" src="https://github.com/user-attachments/assets/cf47c0f9-efd7-42cb-8340-d3dbd82cd628" />
<img width="1337" height="638" alt="d1" src="https://github.com/user-attachments/assets/2b50f2d1-1166-41a9-b535-6f2ba67431d0" />
<img width="1336" height="640" alt="d2" src="https://github.com/user-attachments/assets/d220540c-a9bf-4cfd-9a80-4b39e356610d" />
<img width="1342" height="639" alt="d3" src="https://github.com/user-attachments/assets/70733c04-d5e6-4c6e-a6c7-c723e98fca3f" />
<img width="1340" height="640" alt="his" src="https://github.com/user-attachments/assets/b559012d-0da4-42b5-9d51-0a809d3412fd" />
<img width="1337" height="643" alt="Screenshot 2026-06-26 110832" src="https://github.com/user-attachments/assets/21f2ac01-f701-4cb7-a37e-c67031b45663" />
<img width="1339" height="637" alt="cam1" src="https://github.com/user-attachments/assets/747740db-7624-4851-9e63-0d49353acc2a" />
<img width="1340" height="640" alt="cam2" src="https://github.com/user-attachments/assets/665b6d2c-64ab-4aa3-b848-3c5f8982d84c" />
<img width="1337" height="638" alt="cam3" src="https://github.com/user-attachments/assets/a3cbcbdc-565f-42f8-9eaa-c54171a53fdb" />
<img width="1341" height="639" alt="fedd" src="https://github.com/user-attachments/assets/61da639c-767b-4d33-b721-af6f6e11ade4" />
<img width="1339" height="640" alt="ad1" src="https://github.com/user-attachments/assets/a11907b8-d9ae-4fb4-935d-87b370b996e7" />
<img width="1336" height="640" alt="ad2" src="https://github.com/user-attachments/assets/b9991b0a-c2d3-4569-bd8f-a281d96cead5" />
<img width="1344" height="642" alt="ad3" src="https://github.com/user-attachments/assets/7d95d4dc-c94c-4f82-b69f-5313c81ee000" />
<img width="1336" height="640" alt="ad2" src="https://github.com/user-attachments/assets/9ef39f96-eb6b-4d94-bd79-407bf0222b1f" />

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/MedVisionAI.git

cd MedVisionAI
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file

```env
SECRET_KEY=your_secret_key

DATABASE_URL=sqlite:///database.db
```

---

## Run Application

```bash
python app.py
```

Open

```
http://127.0.0.1:5000
```

---

# 💻 Usage

### Upload Image

Upload a skin disease image.

↓

### AI Prediction

The trained model predicts the disease.

↓

### View Results

See

- Disease Name
- Confidence
- Heatmap
- Disease Information

↓

### Download Report

Generate PDF report.

---

# 📂 Folder Structure

```
MedVisionAI/

│

├── app.py

├── database.py

├── predictor.py

├── gradcam.py

├── analytics.py

├── disease_info.py

├── report_generator.py

├── requirements.txt

├── README.md

│

├── static/

│ ├── css/

│ ├── js/

│ ├── images/

│ ├── uploads/

│ ├── heatmaps/

│ └── models/

│

├── templates/

│ ├── index.html

│ ├── login.html

│ ├── register.html

│ ├── dashboard.html

│ └── result.html

│

├── database/

└── screenshots/
```

---

# 🤖 Model Information

| Feature | Details |
|----------|----------|
| Framework | TensorFlow |
| Architecture | CNN |
| Input Size | 224 × 224 |
| Image Processing | OpenCV |
| Output | Disease Prediction |
| Explainability | Grad-CAM |

---

# 🌟 Future Improvements

- Mobile Application
- REST API
- Multi-language Support
- Doctor Consultation
- Email Notifications
- Patient History
- Cloud Database
- Improved AI Accuracy
- Skin Segmentation
- Dark Mode

---

# ☁ Deployment

Supported Platforms

- Render
- PythonAnywhere
- Railway
- Docker
- AWS EC2

---

# 🤝 Contributing

Contributions are welcome!

## Fork Repository

```bash
git fork
```

Create Branch

```bash
git checkout -b feature-name
```

Commit

```bash
git commit -m "Added new feature"
```

Push

```bash
git push origin feature-name
```

Open Pull Request.

---

# 📜 License

This project is licensed under the **MIT License**.

---

# 👨‍💻 Author

## Prajwal T. S.

**Python Developer | AI & Machine Learning Enthusiast | Flask Developer**

### Connect with Me

- GitHub: https://github.com/yourusername
- LinkedIn: https://linkedin.com/in/yourprofile
- Email: yourmail@example.com

---

# ⭐ Support

If you found this project useful,

⭐ Star this repository

🍴 Fork this repository

🐞 Report Issues

💡 Suggest New Features

---

<p align="center">

Made with ❤️ using Python, Flask, TensorFlow & OpenCV

</p>
