import os
from PIL import Image
from io import BytesIO

# --- Cấu hình ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # thư mục chứa file .py
INPUT_FOLDER = os.path.join(BASE_DIR, "..", "input")    # folder input (nằm cùng cấp với code/)
OUTPUT_FOLDER = os.path.join(BASE_DIR, "..", "output")  # folder output

MAX_SIZE_BYTES = 100 * 1024   # 100KB
MIN_WIDTH, MIN_HEIGHT = 1600, 900  # Khung hiển thị web

# Tạo folder output nếu chưa có
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def compress_image(img: Image.Image, max_size: int, min_width=1600, min_height=900) -> BytesIO:
    """
    Nén ảnh xuống dưới max_size nhưng vẫn giữ chất lượng cao (85-90).
    - Resize về tối đa 1600x900 nếu ảnh lớn hơn.
    - Giảm quality từ 90 xuống 85.
    """
    width, height = img.size

    # Resize nếu ảnh lớn hơn khung
    if width > min_width or height > min_height:
        img.thumbnail((min_width, min_height), Image.Resampling.LANCZOS)

    # Thử giảm quality từ 90 → 85
    for quality in range(90, 84, -1):
        temp_io = BytesIO()
        img.save(temp_io, format="JPEG", quality=quality, optimize=True, progressive=True)
        if temp_io.tell() <= max_size:
            return temp_io

    # Nếu vẫn chưa đạt, trả về bản quality=85
    return temp_io



# --- Duyệt tất cả file ảnh trong folder input ---
for file_name in os.listdir(INPUT_FOLDER):
    file_path = os.path.join(INPUT_FOLDER, file_name)

    # Bỏ qua nếu không phải ảnh
    if not file_name.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        continue

    try:
        with Image.open(file_path) as img:
            if img.mode == "RGBA":
                img = img.convert("RGB")

            original_size = os.path.getsize(file_path)
            print(f"\n📷 Đang xử lý: {file_name}")
            print(f"   Dung lượng gốc: {original_size // 1024} KB ({img.size[0]}x{img.size[1]})")

            if original_size <= MAX_SIZE_BYTES:
                print("   ✔ Ảnh đã nhỏ, bỏ qua.")
                continue

            # Nén ảnh
            compressed_io = compress_image(img, MAX_SIZE_BYTES, MIN_WIDTH, MIN_HEIGHT)

            # Lưu ra file .jpg
            output_file = os.path.join(OUTPUT_FOLDER, os.path.splitext(file_name)[0] + ".jpg")
            with open(output_file, "wb") as f:
                f.write(compressed_io.getvalue())

            print(f"   ✔ Đã nén và lưu: {output_file} ({os.path.getsize(output_file)//1024} KB)")

    except Exception as e:
        print(f"❌ Lỗi khi xử lý {file_name}: {e}")

print("\n✅ Hoàn tất xử lý tất cả ảnh trong folder!")
