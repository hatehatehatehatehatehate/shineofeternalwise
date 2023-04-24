import base64
import glob
import os
import subprocess
import sys

def convert_images_to_base64():
    img_folder = "img"
    img_files = sorted(glob.glob(os.path.join(img_folder, "*.jpg")))

    images_base64 = []

    for img_file in img_files:
        with open(img_file, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            images_base64.append(encoded_image)

    return images_base64

def update_img_py(images_base64):
    with open("img.py", "w") as file:
        file.write("images_base64 = [\n")
        for img_base64 in images_base64:
            file.write(f"    \"{img_base64}\",\n")
        file.write("]\n")

def build_project():
    build_command = 'pyinstaller -F -w -i "C:\\Users\\Eternity\\Downloads\\iq killa\\Eternity.ico" main.py'
    subprocess.run(build_command, shell=True, check=True)

def main():
    images_base64 = convert_images_to_base64()

    if not os.path.exists("img.py"):
        update_img_py(images_base64)
    else:
        from img import images_base64 as existing_images_base64

        if len(existing_images_base64) != len(images_base64):
            update_img_py(images_base64)

    build_project()

if __name__ == "__main__":
    main()
