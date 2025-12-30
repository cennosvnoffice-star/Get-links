import dropbox
import requests
import pandas as pd
from tqdm import tqdm
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

# ======= CẤU HÌNH =======
CLIENT_ID = "icwnfnjml3m21c2"
CLIENT_SECRET = "j12579um0i2tget"
REFRESH_TOKEN = "0Ej6wkVJepwAAAAAAAAAAThM0b94S2ew1sLeRsvYyGyWT3zDi3oj1W1Zm5_AYHIK"
FOLDER_PATH = "/Amazon _ Assembly instruction/FOAE250100173 - Amazon Submission - November 2025"
OUTPUT_EXCEL = "dropbox_links.xlsx"
NUM_THREADS = 10

# ======= LẤY ACCESS TOKEN =======
def get_access_token(client_id, client_secret, refresh_token):
    url = "https://api.dropbox.com/oauth2/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

ACCESS_TOKEN = get_access_token(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)

# ======= KẾT NỐI DROPBOX =======
dbx = dropbox.Dropbox(ACCESS_TOKEN)

# ======= LẤY DANH SÁCH FILE =======
entries = []
result = dbx.files_list_folder(FOLDER_PATH)
entries.extend(result.entries)
while result.has_more:
    result = dbx.files_list_folder_continue(result.cursor)
    entries.extend(result.entries)

# ======= LẤY LINK (ĐA LUỒNG) =======
existing_links = {}
links_result = dbx.sharing_list_shared_links(path=FOLDER_PATH, direct_only=True)
for link in links_result.links:
    existing_links[link.path_lower] = link.url.replace("dl=0","dl=1")

def get_link(entry):
    if not isinstance(entry, dropbox.files.FileMetadata):
        return None
    path = entry.path_lower
    name = entry.name
    if path in existing_links:
        return name, existing_links[path]
    try:
        shared_link_metadata = dbx.sharing_create_shared_link_with_settings(path)
        raw_link = shared_link_metadata.url.replace("dl=0", "dl=1")
        existing_links[path] = raw_link
    except dropbox.exceptions.ApiError:
        links = dbx.sharing_list_shared_links(path=path).links
        if links:
            raw_link = links[0].url.replace("dl=0","dl=1")
        else:
            raw_link = "Không tạo được link"
        existing_links[path] = raw_link
    return name, raw_link

ten_anh = []
link_raw = []

with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
    futures = {executor.submit(get_link, e): e for e in entries}
    for future in tqdm(as_completed(futures), total=len(futures), desc="Lấy link ảnh"):
        result = future.result()
        if result:
            ten_anh.append(result[0])
            link_raw.append(result[1])

# ======= TẠO DATAFRAME GỐC =======
df = pd.DataFrame({
    "Tên ảnh": ten_anh,
    "Link dl=1": link_raw
})

# ======= TÁCH TÊN GỐC VÀ SỐ THỨ TỰ =======
def split_name_number(filename):
    m = re.match(r"^(.*?)(?:\s*\((\d+)\))?(\.[^.]+)?$", filename)
    name = m.group(1)
    number = int(m.group(2)) if m.group(2) else 0
    ext = m.group(3) if m.group(3) else ''
    return name, number, ext

df[['Tên gốc đầy đủ', 'Số thứ tự', 'Đuôi']] = df['Tên ảnh'].apply(lambda x: pd.Series(split_name_number(x)))

# ======= SHEET 1: SẮP XẾP THEO TÊN + SỐ =======
df = df.sort_values(['Tên gốc đầy đủ','Số thứ tự']).reset_index(drop=True)

# ======= SHEET 2: TỔNG HỢP LINK =======
# Tên ảnh gốc bỏ đuôi .jpg
df['Tên gốc'] = df['Tên gốc đầy đủ'].str.replace(r'\.jpg$', '', flags=re.IGNORECASE)

grouped = df.groupby('Tên gốc')['Link dl=1'].apply(list).reset_index()

# Tách link ra từng cột (1),(2)...
max_links = grouped['Link dl=1'].apply(len).max()
for i in range(max_links):
    grouped[f'({i+1})'] = grouped['Link dl=1'].apply(lambda x: x[i] if i < len(x) else '')

grouped = grouped.drop(columns=['Link dl=1'])

# ======= XUẤT FILE EXCEL =======
with pd.ExcelWriter(OUTPUT_EXCEL, engine='openpyxl') as writer:
    df[['Tên ảnh','Link dl=1']].to_excel(writer, sheet_name="Danh sách link gốc", index=False)
    grouped.to_excel(writer, sheet_name="Tổng hợp link", index=False)

print(f"Hoàn tất! {len(df)} ảnh đã lưu và tổng hợp link vào {OUTPUT_EXCEL}")
