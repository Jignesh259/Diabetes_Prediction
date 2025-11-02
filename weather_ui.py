import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QMessageBox, QGraphicsDropShadowEffect, QComboBox
)
from PySide6.QtGui import QFont, QColor, QPalette, QLinearGradient, QBrush
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect


class WeatherPredictor(QWidget):
    def __init__(self):
        super().__init__()

        # ---------- Window Setup ----------
        self.setWindowTitle("🌦 Weather Prediction System")
        self.setGeometry(100, 100, 360, 480)
        self.setAutoFillBackground(True)

        # Background Gradient
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, 480)
        gradient.setColorAt(0.0, QColor("#0d1b2a"))
        gradient.setColorAt(1.0, QColor("#e0e8f9"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        # ---------- Load Data & Train Model ----------
        df = pd.read_csv("https://raw.githubusercontent.com/Jignesh259/Diabetes_Prediction/main/weather_classification_data.csv")

        self.le_cc = LabelEncoder()
        self.le_weather = LabelEncoder()

        df['Cloud Cover'] = self.le_cc.fit_transform(df['Cloud Cover'])
        df['Weather Type'] = self.le_weather.fit_transform(df['Weather Type'])

        X = df[['Temperature', 'Humidity', 'Wind Speed', 'Cloud Cover']]
        y = df['Weather Type']

        x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model = DecisionTreeClassifier()
        self.model.fit(x_train, y_train)

        acc = accuracy_score(y_test, self.model.predict(x_test))
        print(f"Model Accuracy: {acc:.2f}")

        # ---------- Title ----------
        title = QLabel("🌤 Weather Prediction")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; margin: 15px;")

        # ---------- Input Fields ----------
        self.inputs = {}
        layout = QVBoxLayout()
        layout.setSpacing(14)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(title)

        self.inputs["Temperature"] = self.add_input(layout, "Temperature (°C):", "e.g., 25.5")
        self.inputs["Humidity"] = self.add_input(layout, "Humidity (%):", "e.g., 60")
        self.inputs["Wind Speed"] = self.add_input(layout, "Wind Speed (km/h):", "e.g., 10")

        # ---------- Cloud Cover Dropdown ----------
        lbl_cc = QLabel("Cloud Cover:")
        lbl_cc.setStyleSheet("color: white; font-size: 13px;")
        combo = QComboBox()
        combo.addItems(["partly cloudy", "clear", "overcast"])
        combo.setStyleSheet("""
            QComboBox {
                background: #f7f9fb;
                border: 2px solid #1e6091;
                border-radius: 8px;
                padding: 6px;
                color: black;
            }
            QComboBox:hover {
                border: 2px solid #00b4d8;
            }
        """)
        self.add_shadow(combo)
        self.inputs["Cloud Cover"] = combo

        row = QHBoxLayout()
        row.addWidget(lbl_cc)
        row.addWidget(combo)
        layout.addLayout(row)

        # ---------- Predict Button ----------
        btn_predict = QPushButton("Predict Weather")
        self.style_button(btn_predict)
        self.add_shadow(btn_predict)
        btn_predict.clicked.connect(self.predict_weather)
        layout.addWidget(btn_predict)

        self.setLayout(layout)

    # ---------- Helper Functions ----------
    def add_input(self, layout, label, placeholder):
        lbl = QLabel(label)
        lbl.setStyleSheet("color: white; font-size: 13px;")
        inp = QLineEdit()
        inp.setPlaceholderText(placeholder)
        self.style_input(inp)
        row = QHBoxLayout()
        row.addWidget(lbl)
        row.addWidget(inp)
        layout.addLayout(row)
        return inp

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

    def add_shadow(self, widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 120))
        widget.setGraphicsEffect(shadow)

    def animate_button(self, btn):
        anim = QPropertyAnimation(btn, b"geometry")
        anim.setDuration(150)
        start_rect = btn.geometry()
        anim.setStartValue(start_rect)
        anim.setEndValue(QRect(start_rect.x(), start_rect.y() + 3, start_rect.width(), start_rect.height()))
        anim.setEasingCurve(QEasingCurve.OutQuad)
        anim.start()
        btn.animation = anim

    # ---------- Prediction ----------
    def predict_weather(self):
        try:
            temp = float(self.inputs["Temperature"].text())
            humi = float(self.inputs["Humidity"].text())
            ws = float(self.inputs["Wind Speed"].text())
            cc = self.inputs["Cloud Cover"].currentText()

            cc_encoded = self.le_cc.transform([cc])[0]
            predict_df = pd.DataFrame([[temp, humi, ws, cc_encoded]],
                                      columns=['Temperature', 'Humidity', 'Wind Speed', 'Cloud Cover'])

            pred_encoded = self.model.predict(predict_df)[0]
            weather = self.le_weather.inverse_transform([pred_encoded])[0]

            QMessageBox.information(self, "🌤 Predicted Weather", f"Predicted Weather Type: {weather}")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


# ---------- Main ----------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherPredictor()
    window.show()
    sys.exit(app.exec())
