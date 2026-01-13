import os
import csv
import shutil
from pydub import AudioSegment

raw_dir = "data/raw"
diagnosis_file = "data/patient_diagnosis.csv"
processed_dir = "data/processed"

full_dir = os.path.join(processed_dir, "full_by_label")
copd_full_dir = os.path.join(full_dir, "copd")
healthy_full_dir = os.path.join(full_dir, "healthy")

segments_dir = os.path.join(processed_dir, "segments")
copd_segments_dir = os.path.join(segments_dir, "copd")
healthy_seg_dir = os.path.join(segments_dir, "healthy")


for d in [copd_full_dir, healthy_full_dir, copd_segments_dir, healthy_seg_dir]:
    os.makedirs(d, exist_ok=True)

#Load patient diagnoses
patient_diagnosis = {}
with open(diagnosis_file, newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        patient_id, diagnosis = row
        patient_diagnosis[patient_id] = diagnosis.strip()

#Copy files for COPD and Healthy patients
for filename in os.listdir(raw_dir):
    if not (filename.endswith(".wav") or filename.endswith(".txt")):
        continue

    patient_id = filename.split("_")[0]
    diagnosis = patient_diagnosis.get(patient_id)

    if diagnosis == "COPD":
        shutil.copy2(os.path.join(raw_dir, filename), os.path.join(copd_full_dir, filename))
    elif diagnosis == "Healthy":
        shutil.copy2(os.path.join(raw_dir, filename), os.path.join(healthy_full_dir, filename))

#Segment single file
def segment_file(wav_path, txt_path, out_dir):
    audio = AudioSegment.from_wav(wav_path)

    with open(txt_path, "r") as f:
        for i, line in enumerate(f):
            parts = line.strip().split()
            if len(parts) < 2:
                continue
            start_sec = float(parts[0])
            stop_sec = float(parts[1])

            start_ms = int(start_sec * 1000) 
            stop_ms = int(stop_sec * 1000)

            segment = audio[start_ms:stop_ms]

            base_name = os.path.splitext(os.path.basename(wav_path))[0]
            seg_name = f"{base_name}_seg_{i:03d}.wav"
            segment.export(os.path.join(out_dir, seg_name), format="wav")

#Segment all recordings
for label, full_dir, seg_dir in [("copd", copd_full_dir, copd_segments_dir),
                                 ("healthy", healthy_full_dir, healthy_seg_dir)]:
    for filename in os.listdir(full_dir):
        if filename.endswith(".wav"):
            wav_path = os.path.join(full_dir, filename)
            txt_filename = os.path.splitext(filename)[0] + ".txt"
            txt_path = os.path.join(full_dir, txt_filename)
            
            if os.path.exists(txt_path):
                segment_file(wav_path, txt_path, seg_dir)