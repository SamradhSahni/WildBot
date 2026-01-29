import os
import cv2
import numpy as np

# Base paths
images_base = "images"
labels_base = "labels"

# Class mapping (for visualization only)
class_mapping = {
    1: "Zebra", 2: "Tiger", 3: "Rhinoceros", 4: "Ostrich", 5: "Lion",
    6: "Leopard", 7: "Horse", 8: "Jaguar", 9: "Harbor seal", 10: "Goat",
    11: "Giraffe", 12: "Fox", 13: "Elephant", 14: "Eagle", 15: "Deer",
    16: "Crab", 17: "Chicken", 18: "Caterpillar", 19: "Cheetah", 20: "Butterfly"
}

print("🚀 Starting image filtering and replacement...\n")

# Loop through species folders
for species_folder in os.listdir(images_base):
    image_folder = os.path.join(images_base, species_folder)
    label_folder = os.path.join(labels_base, species_folder)

    if not os.path.isdir(image_folder):
        continue

    for image_name in os.listdir(image_folder):
        if not image_name.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        
        image_path = os.path.join(image_folder, image_name)
        label_path = os.path.join(label_folder, os.path.splitext(image_name)[0] + ".txt")

        if not os.path.exists(label_path):
            print(f"⚠️ Label missing for {image_name}")
            continue

        image = cv2.imread(image_path)
        if image is None:
            print(f"❌ Could not read {image_name}")
            continue

        height, width, _ = image.shape

        with open(label_path, "r") as f:
            lines = f.readlines()

        for line in lines:
            parts = line.strip().split()
            if len(parts) != 5:
                continue

            class_id = int(parts[0])
            x_min, y_min, x_max, y_max = map(float, parts[1:])
            x_min, y_min = max(0, int(x_min)), max(0, int(y_min))
            x_max, y_max = min(width, int(x_max)), min(height, int(y_max))

            color = (0, 255, 0)
            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, 2)
            label_text = class_mapping.get(class_id, str(class_id))
            cv2.putText(image, label_text, (x_min, y_min - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # ⚡ Replace original image with filtered version
        cv2.imwrite(image_path, image)
        print(f"✅ Updated: {image_path}")

print("\n🎯 All images updated in-place according to labels!")
