import os 
import itertools
import random
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
OUTPUT_CSV = os.path.join(BASE_DIR, "dataset_pairs.csv")

def get_student_folders():
    """Ambil folder siswa di dalam dataset/"""
    return [d for d in os.listdir(DATASET_DIR) if os.path.isdir(os.path.join(DATASET_DIR, d))]

def get_image_paths(student_folder):
    """Ambil path gambar dari folder siswa"""
    folder_path = os.path.join(DATASET_DIR, student_folder)
    return [
        os.path.join(student_folder, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith((".jpg", ".png"))
    ]

def generate_positive_pairs():
    """Generate pasangan dari gambar milik siswa yang sama"""
    positive_pairs = []
    students = get_student_folders()

    for student in students:
        images = get_image_paths(student)
        if len(images) < 2:
            continue
        pairs = list(itertools.combinations(images, 2))
        positive_pairs.extend([(img1, img2, 1) for img1, img2 in pairs])

    return positive_pairs

def generate_negative_pairs(positive_count):
    """Generate pasangan negatif dengan jumlah yang seimbang"""
    negative_pairs = []
    students = get_student_folders()

    while len(negative_pairs) < positive_count:
        student1, student2 = random.sample(students, 2)
        images1 = get_image_paths(student1)
        images2 = get_image_paths(student2)

        if not images1 or not images2:
            continue

        img1 = random.choice(images1)
        img2 = random.choice(images2)
        negative_pairs.append((img1, img2, 0))

    return negative_pairs

def generate_and_save_pairs():
    positive_pairs = generate_positive_pairs()
    print(f"✅ Jumlah pasangan positif: {len(positive_pairs)}")

    negative_pairs = generate_negative_pairs(len(positive_pairs))
    print(f"✅ Jumlah pasangan negatif: {len(negative_pairs)}")

    all_pairs = positive_pairs + negative_pairs
    random.shuffle(all_pairs)

    df = pd.DataFrame(all_pairs, columns=["Image1", "Image2", "Label"])
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"📁 Dataset pairs disimpan ke: {OUTPUT_CSV}")

if __name__ == "__main__":
    generate_and_save_pairs()
