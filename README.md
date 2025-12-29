# Heart Disease Prediction System (Machine Learning + Flask)

A machine learning–based web application that predicts the risk of heart disease using patient health data. The project implements a complete ML pipeline and deploys the trained model using Flask, allowing users to obtain real-time predictions through a web interface.

---

## Project Overview

Heart disease is one of the leading causes of death worldwide. Early detection can significantly reduce health risks and improve patient outcomes.  
This project uses machine learning techniques to analyze patient medical attributes and predict whether a person is at risk of heart disease.

The system combines:
- Machine learning for prediction
- Flask for backend deployment
- HTML and CSS for frontend interaction

---

## Machine Learning Workflow

1. Loading and exploring the heart disease dataset  
2. Data cleaning and preprocessing  
3. Encoding categorical features  
4. Feature selection based on medical relevance  
5. Training the model using **Random Forest Classifier**  
6. Evaluating model performance  
7. Saving trained models using Pickle  
8. Using the trained model for real-time prediction in Flask  

---

## 🛠 Technologies Used

### Backend & Machine Learning
- Python  
- Pandas  
- NumPy  
- Scikit-learn  

### Web Framework
- Flask  

### Frontend
- HTML  
- CSS  
- JavaScript  

---

## Project Structure
```
heartdisease-classification/
│
├── app.py
├── requirements.txt
├── README.md
│
├── dataset/
│ └── HeartDiseaseTrain-Test.csv
│
├── models/
│ ├── HeartDisease_rf_model.pkl
│ ├── lb_fasting_blood_sugar.pkl
│ └── lb_HeartDisease.pkl
│
├── training/
│ ├── HeartDiseaseClassification.ipynb
│ └── README.md
│
├── templates/
│ ├── index.html
│ ├── about.html
│ ├── contact.html
│ ├── login.html
│ ├── register.html
│ ├── doctors.html
│ └── departments.html
│
├── static/
│ ├── css/
│ ├── js/
│ ├── images/
│ └── fonts/

```
## ▶️ How to Run the Project

### Step 1️⃣ Clone the repository
```bash
git clone https://github.com/vidyan7/heartdisease-classification.git
cd heartdisease-classification
```
Step 2️⃣ Create a virtual environment

Step 3️⃣ Install required dependencies
```
pip install -r requirements.txt
```
Step 4️⃣ Run the Flask application
```
python app.py
```
Step 5️⃣ Open the application in browser
```
http://127.0.0.1:5000/
```

### User Instructions 

- Ensure Python 3.8 or higher is installed

- Do not delete the models/ folder (contains trained ML models)

- Dataset must remain inside the dataset/ folder

- HTML files must be inside the templates/ folder

- CSS, JS, images, and fonts must remain inside the static/ folder

- If you retrain the model, replace the .pkl files in the models/ folder

### Model Training (Optional)

- To retrain the model:

- Open training/HeartDiseaseClassification.ipynb

- Run all cells in order

- Save trained models using Pickle

- Update .pkl files inside the models/ folder

### Objective

To apply machine learning techniques for early detection of heart disease and provide an easy-to-use web application for real-time prediction.

### Disclaimer

This project is for educational purposes only and should not be used as a substitute for professional medical diagnosis.

### Future Enhancements

- Improve prediction accuracy with feature engineering

- Add more ML algorithms

- Integrate database support

- Deploy on cloud platforms

### Acknowledgment

This project was developed as part of an academic curriculum to demonstrate the application of machine learning and web development concepts.
