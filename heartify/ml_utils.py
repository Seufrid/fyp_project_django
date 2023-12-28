import pickle

def make_prediction(age, sex, chest_pain_type, resting_bp, cholesterol, fasting_bs, resting_ecg, max_hr, exercise_angina, oldpeak, st_slope):
    # Load the trained model from the saved file
    model = pickle.load(open("heart_model.sav", "rb")) 

    # Make the prediction using the loaded model
    prediction = model.predict_proba([[age, sex, chest_pain_type, resting_bp, cholesterol, fasting_bs, resting_ecg, max_hr, exercise_angina, oldpeak, st_slope]])

    # Extract the probability of the positive class (heart disease)
    result = prediction[0][1]

    # Return the resulting probability
    return result