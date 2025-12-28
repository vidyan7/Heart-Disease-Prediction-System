from flask import Flask,render_template,request,redirect,url_for,flash,session #render_template: to display any webpage
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import pickle



app = Flask(__name__)
app.config['SECRET_KEY'] = '1357d'  # Replace with a strong key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DB and Login manager
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Load user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------------- Load Model -------------------
with open("models/HeartDisease_rf_model.pkl", "rb") as f:
    rf_model = pickle.load(f)



# Loading label encoders
with open('models/lb_fasting_blood_sugar.pkl','rb')as file:
    lb_fasting_blood_sugar=pickle.load(file)

with open('models/lb_HeartDisease.pkl','rb')as file:
    lb_HeartDisease=pickle.load(file)






# ------------------- Prediction Function -------------------
def predict_heartdisease(sex='Male', age=56, chest_pain_type='Typical angina',
                         resting_blood_pressure=125, cholestoral=212,
                         fasting_blood_sugar='Lower than 120 mg/ml', rest_ecg='ST-T wave abnormality',
                         Max_heart_rate=168, exercise_induced_angina='No',
                         oldpeak=1.0, slope='Downsloping', thalassemia='Reversable Defect'):
    
    lst = []
    # Encode sex
    lst.append(1 if sex == 'Male' else 0)
    # Age
    lst.append(age)
    # Chest pain type (one-hot)
    chest_pain_types = ['Typical angina', 'Atypical angina', 'Non-anginal pain', 'Asymptomatic']
    for cp in chest_pain_types:
        lst.append(1 if chest_pain_type == cp else 0)
    # Resting blood pressure
    lst.append(resting_blood_pressure)
    # Cholestoral
    lst.append(cholestoral)
    # Fasting blood sugar
    lst.append(0 if fasting_blood_sugar == 'Lower than 120 mg/ml' else 1)
    # Rest ECG
    rest_ecg_types = ['Left ventricular hypertrophy', 'Normal', 'ST-T wave abnormality']
    for ecg in rest_ecg_types:
        lst.append(1 if rest_ecg == ecg else 0)
    # Max heart rate
    lst.append(Max_heart_rate)
    # Exercise induced angina
    lst.append(0 if exercise_induced_angina == 'No' else 1)
    # Oldpeak
    lst.append(oldpeak)
    # Slope
    slope_types = ['Downsloping', 'Flat', 'Upsloping']
    for s in slope_types:
        lst.append(1 if slope == s else 0)
    # Thalassemia
    thal_types = ['Fixed Defect', 'No', 'Normal', 'Reversable Defect']
    for th in thal_types:
        lst.append(1 if thalassemia == th else 0)

    result = rf_model.predict([lst])
    return "Person is not having heart disease" if result == [0] else "Person may be suffering from heart disease"


# ------------------- Routes -------------------
@app.route("/")
@login_required
def home():
    return render_template("index.html", prediction=None, username=current_user.email)


# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if user exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered.', 'warning')
            return redirect(url_for('register'))

        # Create new user
        new_user = User(email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    session.pop("user", None)
    flash("Logout successful!", "info")
    return redirect(url_for("login"))

@app.route("/predict_heart", methods=["POST"])
def predict_heart():
    data = request.form
    prediction = predict_heartdisease(
        sex=data["sex"],
        age=int(data["age"]),
        chest_pain_type=data["chest_pain_type"],
        resting_blood_pressure=int(data["resting_blood_pressure"]),
        cholestoral=float(data["cholestoral"]),
        fasting_blood_sugar=data["fasting_blood_sugar"],
        rest_ecg=data["rest_ecg"],
        Max_heart_rate=int(data["Max_heart_rate"]),
        exercise_induced_angina=data["exercise_induced_angina"],
        oldpeak=float(data["oldpeak"]),
        slope=data["slope"],
        thalassemia=data["thalassemia"],
    )
    return render_template("index.html", prediction=prediction)


if __name__=="__main__":
    with app.app_context():
        if not os.path.exists('users.db'):
            db.create_all()
    app.run(debug=True,port=4500)