# Copyright by Hann-10843 CN 08/24/2025

import dropbox
import pandas as pd
from tqdm import tqdm

# === CẤU HÌNH ===
ACCESS_TOKEN = 'sl.u.AF-SPDzR0Yf_ABIIQZDewDG0rAUHqNzi3hpKldVXZccDD73g63fDFSYpdv_nYedlbKQwJqrclK5V5uFNRjutm393tBJEvIkg4i0brJy5wvdTanQ8bytqg1TFasP6w_49FmK6iELT5oRQschkmsJEEyDFKo9dFNUwPkEut2Mz43yB18_ewqiXTcLvQ7TLPmtGoHrSzaYKLT7kcyQ7BpaWCcGpHTp4TtAX9u71PAfqRd-NTkx_UPXPQjr1SG3AStlJfHm5ExoZBUtPjLJqYV5XTUjpXRGRBc1RueQgcJ8ZhHsWM6X4sqxVoQOZ0UEOFp76BDtdF6B0528PgpRT67as1mcncCIm4UNk_YGRUm5RYn2jEPasaJH0c-lZy9jQdWghK441mSQ01MmAPri6Fecx_QzywTHiaIgY4cgWf9xIiVxV_yuXuFdBkdEg1p8uChpeAO0oanujmYiFNtLcNZRtN1pBFajqw75IQzKGB6qW7F8-xh2kE_4tKDtxHD1MhbFXnC5qIqpyM0ePJPBR5cqDtRiHAvQv8dnkpIEeFCR60u8-9tvb6kOLWsqd0dvrp0rHfVXc21Y1_29mG_95OY_N9_zugRnJV6aVjsBrzGQotMLBReMAd3_FeId-U6T76UWFv1jsBEtkt8JXPSSZ2oNQsyYN3MflsrYZJmCDpOeZt9jVxfgO9NlFmj_bXYIkRQ5NxuEficZbeC0kNfR3wsvocvzmDEPDdJyJL-1Tsb9t3KGRNrso5GkFJxr7zJ3t8x92tDwV1J7ZHLEAUuPmiVLCHLD2o6lQV_MaxqojAnxAOP_tqqB-WnnWr6VaLylfpMLpuNY5EOMHasggNqmN-rMYwvn033YX2qBJ1an-8qAEuZ9bjqW5Yy7dmKipdMQhzXvQYrbC52bHxf9fSdVHTuiFT_gf1KPxisKY9AlPoQXzzMhHrUU0VtpS0GvmmK0OeUNOBAAljrwVcMzVhlwxjgMSAUsooFj1P5CNaVFlOl4vlnhmR7H2ej0SRruuSo1g5ymJb_Re3FlcU2foRdOy54W1uIBRxEliD6tDEN67Cj4Ayw8Rl-ciw-lWwaGOIgkX3Ne27-GnlI3_woqXceVCzCfcp5HImzJ830xN_hkzVIesTIzDBiMVODxRxZPH6BFw1Ne8M29Q_D9-bLCrblXd3780ZlBTWr3UUV6QlZS-rgPDzh5rX8GN_asgtT5lFqb8aYOvpVC9ReCdfc285wv8gKgZfORTBkm7ZT2lM25_BpIoP0wokem3MW-gQV0ZZ7pEx-jg5KzIUshh2rAiv7-aSfy_7AJ8'
FOLDER_PATH = "/Cennos/Bloomingdale's/FOAE250100138/Swatch Image"

# === KẾT NỐI DROPBOX ===
dbx = dropbox.Dropbox(ACCESS_TOKEN)

# === LẤY DANH SÁCH FILE TRONG FOLDER ===
entries = []
result = dbx.files_list_folder(FOLDER_PATH)

entries.extend(result.entries)
while result.has_more:
    result = dbx.files_list_folder_continue(result.cursor)
    entries.extend(result.entries)

# === TẠO LINK dl=1 CHO MỖI FILE ===
ten_anh = []
link_raw = []

for entry in tqdm(entries, desc="Lấy link ảnh"):
    if isinstance(entry, dropbox.files.FileMetadata):
        ten_anh.append(entry.name)
        try:
            shared_link_metadata = dbx.sharing_create_shared_link_with_settings(entry.path_lower)
            raw_link = shared_link_metadata.url.replace("dl=0", "dl=1")
        except dropbox.exceptions.ApiError as e:
            # Nếu link đã tồn tại, vẫn tạo link mới
            links = dbx.sharing_list_shared_links(path=entry.path_lower).links
            if links:
                raw_link = links[0].url.replace("dl=0", "dl=1")
            else:
                raw_link = "Không tạo được link"
        link_raw.append(raw_link)

# === TẠO DATAFRAME VÀ XUẤT EXCEL ===
df = pd.DataFrame({
    "Tên ảnh": ten_anh,
    "Link dl=1": link_raw
})

df.to_excel("dropbox_links.xlsx", index=False)
print(f"Đã lưu {len(df)} ảnh vào dropbox_links.xlsx")
