import openpyxl
import os
import requests
from PIL import Image
from io import BytesIO

# --- Cấu hình ---
MAX_SIZE_BYTES = 150 * 1024   # 150KB
OUTPUT_FOLDER = "resizenew"
MIN_WIDTH, MIN_HEIGHT = 1600, 900  # Kích thước tối thiểu cho web

# --- Xác định đường dẫn ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_FILE = os.path.join(BASE_DIR, "links.xlsx")
OUTPUT_PATH = os.path.join(BASE_DIR, OUTPUT_FOLDER)
os.makedirs(OUTPUT_PATH, exist_ok=True)

# --- Load Excel ---
wb = openpyxl.load_workbook(EXCEL_FILE)
sheet = wb.active


# --- Hàm nén ảnh ---
def compress_image(img: Image.Image, max_size: int, min_width=1600, min_height=900) -> BytesIO:
    """
    Nén ảnh mà vẫn giữ chất lượng cao.
    - Resize nếu ảnh lớn hơn 1600x900.
    - Giảm chất lượng từ 95 → 90 để đạt dung lượng < max_size.
    """
    width, height = img.size

    # Resize nếu ảnh quá lớn
    if width > min_width or height > min_height:
        img.thumbnail((min_width, min_height), Image.Resampling.LANCZOS)

    # Giảm chất lượng dần để đạt dung lượng mong muốn
    for quality in range(95, 89, -1):
        temp_io = BytesIO()
        img.save(temp_io, format="JPEG", quality=quality, optimize=True)
        if temp_io.tell() <= max_size:
            return temp_io

    # Nếu vẫn nặng, trả bản chất lượng 90
    return temp_io


# --- Xử lý từng link ---
for row in sheet.iter_rows(min_row=2, min_col=1, max_col=1):
    url = row[0].value
    if not url:
        print("⚠️ Ô Excel trống!")
        continue

    try:
        # Tên file đầu ra (ép sang .jpg)
        file_name = url.split("/")[-1].split("?")[0]
        base_name = os.path.splitext(file_name)[0]
        output_file = os.path.join(OUTPUT_PATH, f"{base_name}.jpg")

        # Giả lập trình duyệt thật
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
            "Referer": "https://www.bazango.vn/"
        }

        # Tải ảnh
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"❌ Lỗi tải ảnh ({response.status_code}): {url}")
            continue

        # Mở ảnh
        img_data = response.content
        img = Image.open(BytesIO(img_data))

        # Ép RGB để đảm bảo lưu dạng JPEG hợp lệ
        if img.mode != "RGB":
            img = img.convert("RGB")

        original_size = len(img_data)
        print(f"\n📷 Đang xử lý: {file_name}")
        print(f"   Dung lượng gốc: {original_size // 1024} KB ({img.size[0]}x{img.size[1]})")

        # Nếu ảnh đã nhỏ sẵn
        if original_size <= MAX_SIZE_BYTES:
            img.save(output_file, "JPEG", quality=90, optimize=True)
            print(f"   ✔ Ảnh nhỏ, chỉ chuyển sang JPG: {output_file}")
            continue

        # Nén ảnh
        compressed_io = compress_image(img, MAX_SIZE_BYTES, MIN_WIDTH, MIN_HEIGHT)

        # Lưu file JPG
        with open(output_file, "wb") as f:
            f.write(compressed_io.getvalue())

        print(f"   ✔ Đã nén và lưu: {output_file} ({os.path.getsize(output_file)//1024} KB)")

    except Exception as e:
        print(f"❌ Lỗi khi xử lý {url}: {e}")

print("\n✅ Hoàn tất xử lý tất cả ảnh!")
