# Land Price Prediction System

A Machine Learning–based web application that predicts land price per square foot using historical real estate data.

## 🔍 Overview
This project uses supervised machine learning techniques to estimate land prices based on location and property features. The trained model is deployed using FastAPI and presented through a clean web interface.

## 🚀 Features
- Real-world dataset (Bangalore real estate data)
- Feature engineering and preprocessing
- Random Forest regression model
- FastAPI backend
- Interactive frontend (HTML, CSS, JavaScript)
- REST API + Web UI

## 🧠 Tech Stack
- Python 3.11
- Scikit-learn
- Pandas, NumPy
- FastAPI
- HTML, CSS, JavaScript

Live link:- 
https://land-price-prediction-ml.onrender.com
## 📁 Project Structure

land-price-prediction/
├── app.py
├── train.py
├── preprocessing.py
├── model/
├── data/
├── templates/
├── static/
└── requirements.txt

## Dataset
The dataset used for training is the **Bangalore House Price Dataset** sourced from Kaggle.

Due to GitHub file size limitations, the raw dataset is not included in this repository.

Dataset link:
https://www.kaggle.com/datasets/amitabhajoy/bengaluru-house-price-data


## ▶️ How to Run
```bash
pip install -r requirements.txt
python train.py
uvicorn app:app --reload
then open: http://127.0.0.1:8000

Sample Output: 

    The system predicts land price per square foot based on user input parameters.

Use Case:

    Real estate price estimation

Decision support for buyers and sellers

Academic ML project

Author

Uday Raika
GitHub & LinkedIn links in footer
