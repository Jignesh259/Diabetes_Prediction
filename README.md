1 Mini Code
🩺 Diabetes Data Entry and Prediction System
🧠 Overview

The Diabetes Data Entry and Prediction System is a Python desktop application designed to help predict whether a person is diabetic or not based on medical details.
It combines Machine Learning (Decision Tree Classifier) with a PySide6 graphical interface for a smooth and user-friendly experience.
Each record entered by the user is automatically saved to a GitHub CSV file using the GitHub API, allowing easy data storage and access.

🚀 Features

📝 Enter patient medical details

🤖 Predict diabetes result (Yes / No)

☁️ Automatically save data to GitHub CSV

🌐 Supports English and Gujarati languages

🎨 Modern and simple user interface

🧰 Technologies Used

Python 3

PySide6 → for GUI interface

pandas → for data handling

scikit-learn → for machine learning

requests and base64 → for GitHub integration

📊 Machine Learning Model

Algorithm: Decision Tree Classifier

Dataset: Pima Indians Diabetes Dataset

Accuracy: ~78%

Target Variable: Outcome (1 = Diabetic, 0 = Not Diabetic)

⚙️ How It Works

Loads the diabetes dataset from GitHub.

Trains the Decision Tree model.

Takes user input from the form.

Predicts the diabetes result instantly.

Appends the new record to the CSV file on GitHub.

🧩 How to Run

Install required libraries

pip install pandas scikit-learn PySide6 requests


Run the application

python diabetesprediction.py


Fill in the medical details and click Submit Details.

The app will show the prediction and automatically save it to GitHub.

🔐 GitHub Integration

The app connects to GitHub using your Personal Access Token and updates a CSV file.
To enable this feature:

Set your GitHub username, repository name, and token inside the code.

Make sure your repository has an existing CSV file with proper headers (like Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age, Outcome).

📑 Project Report (Summary)

This project demonstrates:

How Machine Learning can be used for medical prediction.

Integration between a desktop GUI (PySide6) and cloud storage (GitHub).

The use of Decision Tree Classification to interpret patient health data.

Result: The system successfully predicts diabetes status with 78% accuracy and stores all results securely for future analysis.

🖼️ Screenshot

<img width="685" height="525" alt="image" src="https://github.com/user-attachments/assets/3088ccb3-10c6-4924-b5fd-1ea96423096e" />


👨‍💻 Developer

Author: Jignesh Jagatiya
Project Type: Machine Learning + GUI Desktop Application
Language Support: English, Gujarati

2 Mini Code
# 🌦 Weather Prediction System (PySide6 + ML)

A modern desktop app that predicts **Weather Type** using **Temperature, Humidity, Wind Speed, and Cloud Cover**.  
Built with **PySide6** for UI and **Scikit-learn** (Decision Tree Classifier) for ML.

---

## 🚀 Features
- 🧠 Machine Learning (Decision Tree Classifier)
- 🎨 Gradient UI with modern design & shadows
- 🧾 Dropdown for Cloud Cover (`partly cloudy`, `clear`, `overcast`)
- ⚡ Instant weather prediction
- 📊 Auto-loads and trains from CSV dataset

---

## 🧩 Tech Stack
**Python**, **PySide6**, **Scikit-learn**, **Pandas**, **NumPy**

---

## 🗂 Dataset
Hosted on GitHub:  
👉 [weather_classification_data.csv](https://raw.githubusercontent.com/Jignesh259/Diabetes_Prediction/main/weather_classification_data.csv)

**Columns:**  
`Temperature`, `Humidity`, `Wind Speed`, `Cloud Cover`, `Weather Type`

---

## 🖥 Setup
```bash
pip install pandas scikit-learn PySide6
python weather_ui.py
