import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QRadioButton,
    QVBoxLayout, QHBoxLayout, QMessageBox, QGraphicsDropShadowEffect, QScrollArea
)
from PySide6.QtGui import QFont, QColor, QPalette, QLinearGradient, QBrush
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
import requests
import base64
from io import StringIO

# ---------------- GitHub Credentials ----------------
GITHUB_USERNAME = "Jigneshtest25"
GITHUB_REPO = "demo"
TOKEN = "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"

class DiabetesForm(QWidget):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.setWindowTitle("Diabetes Data Entry")
        self.setGeometry(100, 100, 360, 640)
        self.setAutoFillBackground(True)

        # Gradient Background (Dark Blue → Light)
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, 640)
        gradient.setColorAt(0.0, QColor("#0d1b2a"))
        gradient.setColorAt(1.0, QColor("#e0e8f9"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        # --- Load and Train Model ---
        df = pd.read_csv("https://raw.githubusercontent.com/Jignesh259/Diabetes_Prediction/main/diabetes.csv")
        x = df[['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin',
                'BMI', 'DiabetesPedigreeFunction', 'Age']]
        y = df['Outcome']
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
        self.model = DecisionTreeClassifier()
        self.model.fit(x_train, y_train)

        # Title
        self.title = QLabel("🩸 Diabetes Record Entry")
        self.title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: white; margin: 10px;")

        # Gujarati Mode Radio Button (toggle)
        self.gujarati_toggle = QRadioButton("ગુજરાતી મોડ")
        self.style_radiobutton(self.gujarati_toggle)
        self.gujarati_toggle.toggled.connect(self.toggle_language)

        # Input Fields
        self.inputs = {}
        self.float_fields = ["BMI", "DiabetesPedigreeFunction"]

        # English labels + placeholders
        self.fields_en = {
            "Pregnancies": "Pregnancies:",
            "Glucose": "Glucose:",
            "BloodPressure": "Blood Pressure:",
            "SkinThickness": "Skin Thickness:",
            "Insulin": "Insulin:",
            "BMI": "BMI:",
            "DiabetesPedigreeFunction": "Diabetes Pedigree Function:",
            "Age": "Age:"
        }
        self.placeholders_en = {
            "Pregnancies": "0 if male, otherwise number",
            "Glucose": "Glucose level (mg/dL)",
            "BloodPressure": "Blood pressure (mm Hg)",
            "SkinThickness": "Skin thickness (mm)",
            "Insulin": "Insulin level (μU/mL)",
            "BMI": "Body Mass Index (e.g., 24.5)",
            "DiabetesPedigreeFunction": "Genetic risk (0.0 - 2.5)",
            "Age": "Age in years"
        }

        # Gujarati labels + placeholders
        self.fields_gu = {
            "Pregnancies": "ગર્ભાવસ્થા:",
            "Glucose": "ગ્લૂકોઝ સ્તર:",
            "BloodPressure": "બ્લડ પ્રેશર:",
            "SkinThickness": "ચામડીની જાડાઈ:",
            "Insulin": "ઇન્સ્યુલિન સ્તર:",
            "BMI": "બોડી માસ ઇન્ડેક્સ:",
            "DiabetesPedigreeFunction": "મધુમેહ વંશજ ફંક્શન:",
            "Age": "ઉંમર:"
        }
        self.placeholders_gu = {
            "Pregnancies": "પુરુષ માટે 0, અન્યથા સંખ્યા",
            "Glucose": "ગ્લૂકોઝ લેવલ (mg/dL)",
            "BloodPressure": "બ્લડ પ્રેશર (mm Hg)",
            "SkinThickness": "ચામડીની જાડાઈ (mm)",
            "Insulin": "ઇન્સ્યુલિન સ્તર (μU/mL)",
            "BMI": "બોડી માસ ઇન્ડેક્સ (ઉદાહરણ: 24.5)",
            "DiabetesPedigreeFunction": "વંશજ જોખમ (0.0 - 2.5)",
            "Age": "વય વર્ષોમાં"
        }

        # Layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(20, 15, 20, 15)

        main_layout.addWidget(self.title)
        main_layout.addWidget(self.gujarati_toggle)

        for key in self.fields_en.keys():
            lbl = QLabel(self.fields_en[key])
            lbl.setStyleSheet("color: white; font-size: 13px;")
            inp = QLineEdit()
            inp.setPlaceholderText(self.placeholders_en[key])
            self.style_input(inp)
            self.inputs[key] = (lbl, inp)
            row = QHBoxLayout()
            row.addWidget(lbl)
            row.addWidget(inp)
            main_layout.addLayout(row)

        # Submit Button
        self.btn_submit = QPushButton("Submit Details")
        self.style_button(self.btn_submit)
        self.add_shadow(self.btn_submit)
        self.btn_submit.clicked.connect(self.add_patient)
        main_layout.addWidget(self.btn_submit)

        # Scroll Area
        container = QWidget()
        container.setLayout(main_layout)
        scroll = QScrollArea()
        scroll.setWidget(container)
        scroll.setWidgetResizable(True)

        layout = QVBoxLayout(self)
        layout.addWidget(scroll)

        self.csv_file = "diabetes_records.csv"  # GitHub CSV file

    # ---------------- Styling Functions ----------------
    def style_input(self, widget):
        widget.setFont(QFont("Segoe UI", 10))
        widget.setStyleSheet("""
            QLineEdit {
                color: black;
                background: #f7f9fb;
                border: 2px solid #1e6091;
                border-radius: 8px;
                padding: 6px;
            }
            QLineEdit:focus {
                border: 2px solid #00b4d8;
                background: #ffffff;
            }
            QLineEdit::placeholder {
                color: #6c757d;
                font-style: italic;
            }
        """)
        self.add_shadow(widget)

    def style_button(self, btn):
        btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        btn.setStyleSheet("""
            QPushButton {
                background-color: #1e6091;
                color: white;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1b4965;
            }
        """)

    def style_radiobutton(self, rb):
        rb.setFont(QFont("Segoe UI", 11))
        rb.setStyleSheet("""
            QRadioButton {
                color: white;
                font-weight: bold;
                spacing: 8px;
            }
            QRadioButton::indicator {
                width: 40px;
                height: 20px;
                border-radius: 10px;
                background-color: #6c757d;
            }
            QRadioButton::indicator:checked {
                background-color: #1e6091;
            }
        """)

    def add_shadow(self, widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 120))
        widget.setGraphicsEffect(shadow)

    # ---------------- Animation ----------------
    def animate_button(self, btn):
        anim = QPropertyAnimation(btn, b"geometry")
        anim.setDuration(150)
        start_rect = btn.geometry()
        anim.setStartValue(start_rect)
        anim.setEndValue(QRect(start_rect.x(), start_rect.y() + 3, start_rect.width(), start_rect.height()))
        anim.setEasingCurve(QEasingCurve.OutQuad)
        anim.start()
        btn.animation = anim

    # ---------------- Language Toggle ----------------
    def toggle_language(self):
        if self.gujarati_toggle.isChecked():
            self.title.setText("🩸 મધુમેહ માહિતી દાખલ કરો")
            self.btn_submit.setText("માહિતી તપાસો")
            for key, (lbl, inp) in self.inputs.items():
                lbl.setText(self.fields_gu[key])
                inp.setPlaceholderText(self.placeholders_gu[key])
        else:
            self.title.setText("🩸 Diabetes Record Entry")
            self.btn_submit.setText("Submit Details")
            for key, (lbl, inp) in self.inputs.items():
                lbl.setText(self.fields_en[key])
                inp.setPlaceholderText(self.placeholders_en[key])

    # ---------------- Add Patient + GitHub Save ----------------
    def add_patient(self):
        sender = self.sender()
        self.animate_button(sender)

        # Collect input
        data = {}
        for key, (_, field) in self.inputs.items():
            text = field.text().strip()
            if not text:
                QMessageBox.warning(self, "⚠️", 
                    "Please fill all fields first!" if not self.gujarati_toggle.isChecked() else "કૃપા કરીને બધા ક્ષેત્રો ભરો!")
                return
            data[key] = text

        try:
            # Convert values
            validated_data = [float(data[k]) if k in self.float_fields else int(data[k]) for k in data]

            # Prediction
            columns = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 
                       'BMI', 'DiabetesPedigreeFunction', 'Age']            
            new_data = pd.DataFrame([validated_data], columns=columns)
            prediction = int(self.model.predict(new_data)[0])
            validated_data.append(prediction)  # Add prediction at the end

            # --- Save to GitHub ---
            url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{self.csv_file}"
            headers = {"Authorization": f"token {TOKEN}"}

            # 1. Get existing CSV
            resp = requests.get(url, headers=headers)
            if resp.status_code != 200:
                raise Exception(f"Failed to fetch {self.csv_file} from GitHub. Status: {resp.status_code}")
            file_data = resp.json()
            sha = file_data["sha"]
            csv_content = base64.b64decode(file_data["content"]).decode()
            df = pd.read_csv(StringIO(csv_content))

            # 2. Append new row
            df.loc[len(df)] = validated_data

            # 3. Encode back to base64
            buffer = StringIO()
            df.to_csv(buffer, index=False)
            new_content = base64.b64encode(buffer.getvalue().encode()).decode()

            # 4. Update GitHub
            payload = {
                "message": "Add new diabetes patient record",
                "content": new_content,
                "sha": sha
            }
            put_resp = requests.put(url, headers=headers, json=payload)
            if put_resp.status_code not in [200, 201]:
                raise Exception(f"Failed to update GitHub. Status: {put_resp.status_code}")

            # Show Result
            if prediction == 1:
                msg = ("⚠️ Patient is Diabetic.\n\n➡️ Exercise regularly.\n➡️ Reduce sugar intake.\n➡️ Consult a doctor.") \
                    if not self.gujarati_toggle.isChecked() else \
                    ("⚠️ દર્દીને મધુમેહ છે.\n\n➡️ નિયમિત વ્યાયામ કરો.\n➡️ ખાંડનું સેવન ઓછું કરો.\n➡️ ડોક્ટરની સલાહ લો.")
                QMessageBox.critical(self, "Result", msg)
            else:
                msg = "✅ Patient is not diabetic." if not self.gujarati_toggle.isChecked() else "✅ દર્દીને મધુમેહ નથી."
                QMessageBox.information(self, "Result", msg)

            # Clear fields
            for _, inp in self.inputs.values():
                inp.clear()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


# ---------------- Main ----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiabetesForm()
    window.show()
    sys.exit(app.exec())
