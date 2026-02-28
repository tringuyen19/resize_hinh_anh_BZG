1️⃣ Tải project về máy

Vào trang GitHub của project

Nhấn nút Code

Chọn Download ZIP

Giải nén file .zip

Mở folder vừa giải nén

2️⃣ Cài Python
🔍 Kiểm tra máy đã có Python chưa

Nhấn:

Command (⌘) + Space

Gõ:

Terminal

Mở Terminal và nhập:

python3 --version

Nếu hiện như:

Python 3.11.x

→ Máy đã có Python. Bỏ qua bước cài đặt.

📥 Nếu chưa có Python

Vào trang chính thức:
👉 https://www.python.org/downloads/

Tải bản mới nhất cho macOS

Mở file .pkg và cài đặt như bình thường

Sau khi cài xong, mở lại Terminal và kiểm tra:

python3 --version
3️⃣ Cài Visual Studio Code (khuyến nghị)

VS Code giúp mở và chạy project dễ dàng hơn.

📥 Tải VS Code

Vào:
👉 https://code.visualstudio.com/

Tải bản cho macOS

Kéo biểu tượng VS Code vào thư mục Applications

🚀 Mở project bằng VS Code

Mở VS Code

Chọn File → Open Folder

Chọn folder project đã giải nén

4️⃣ Tạo môi trường ảo (rất quan trọng)

Trong VS Code:

Chọn:

Terminal → New Terminal

Sau đó chạy:

cd code
🔧 Tạo môi trường ảo
python3 -m venv venv
▶ Kích hoạt môi trường ảo
source venv/bin/activate

Nếu thành công sẽ thấy:

(venv) MacBook:project-name user$
5️⃣ Cài thư viện cần thiết

Chạy:

pip install -r requirements.txt

Chờ cài đặt hoàn tất.

6️⃣ Chạy chương trình
🔗 Resize theo link ảnh
python resize_images.py
📁 Resize theo thư mục đã chứa ảnh
python resize_folder.py