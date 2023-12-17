# heartify/ml_utils.py

import pickle

def make_prediction(age, sex, chest_pain_type, resting_bp, cholesterol, fasting_bs, resting_ecg, max_hr, exercise_angina, oldpeak, st_slope):
    model = pickle.load(open("heart_model.sav", "rb"))
    prediction = model.predict_proba([[age, sex, chest_pain_type, resting_bp, cholesterol, fasting_bs, resting_ecg, max_hr, exercise_angina, oldpeak, st_slope]])
    result = prediction[0][1]
    return result
