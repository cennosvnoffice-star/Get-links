# Get-links-dropbox
B1:Lấy Key API Dropbox: https://www.dropbox.com/developers/apps?_tk=pilot_lp&_ad=topbar4&_camp=myapps
    - Truy cập link -> Log in = sales@enitiallab.com
    - Tìm mục: Generated access token -> Click: Generate
    - Copy + paste vào: ACCESS_TOKEN = '...'
    - Điền đường dẫn Folder, ví dụ: FOLDER_PATH = "/Cennos/Bloomingdale's/08.25.25"

B2: Copy + paste vào Terminal
    1. Cài đặt module cần thiết (chỉ chạy lệnh này vào lần đầu): 
        pip install dropbox pandas openpyxl tqdm

    2. Run:
        python update_get_links.py

Kết quả nằm trong file .xlsx => download.

# File update chỉ cần sửa FOLDER_PATH sau đó chạy luôn.