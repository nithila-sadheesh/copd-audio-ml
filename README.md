# COPD Detection from Lung Sound Recordings

## Overview

This project investigates whether respiratory cycle–level audio features extracted from lung sound recordings can be used to distinguish COPD patients from healthy individuals.

The project uses the following pipeline:
- Patient-wise data splitting to prevent data leakage
- Cycle-level segmentation using annotated timestamps
- Post-segmentation preprocessing
- Feature extraction
- Class imbalance handling with SMOTE
- Model comparison with hyperparameter tuning

## Dataset

This project uses a public Kaggle Respiratory Sound Dataset. To obtain the data, search for respiratory sound dataset on Kaggle and extract contents into data/raw/ directory. 
Each recording belongs to a single patient diagnosed as one of:
- COPD
- Healthy

Only COPD and Healthy samples are used in this project.

What a “recording” represents: 
- A full .wav file corresponds to a single patient recording
- Each recording is annotated with multiple respiratory cycles
- The cycles, not full recordings, are treated as individual data samples for modeling

## Data Processing Pipeline

1. Label-based organization
- Raw audio files are grouped by patient diagnosis using patient_diagnosis.csv
- Only COPD and Healthy patients are retained

2. Cycle segmentation
- Each .wav file is segmented using start/end times from its annotation .txt
- Each respiratory cycle is saved as an individual .wav file

3. Post-segmentation preprocessing
- Conversion to mono
- Amplitude normalization
- Padding / truncation to fixed length
- Storage as .npy arrays for numerical stability

Preprocessing is intentionally applied after segmentation to avoid cycle boundary distortion.

## Feature Extraction
From each preprocessed respiratory cycle, the following features are extracted:
- MFCCs (mean + standard deviation)
- Spectral centroid (mean + std)
- Spectral bandwidth (mean + std)
- Zero-crossing rate (mean + std)

## Models Evaluated
The following models were trained and evaluated:
- Logistic Regression (baseline)
- Random Forest
- Support Vector Machine (SVM)
- Neural Network

## Results
Best performing model: Random forest
Key metrics: 
- Accuracy: 0.981132
- Precision: 0.983607
- Recall: 0.996678
