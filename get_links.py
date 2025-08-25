# Copyright by Hann-10843 CN 08/24/2025

import dropbox
import pandas as pd
from tqdm import tqdm

# === CẤU HÌNH ===
ACCESS_TOKEN = 'sl.u.AF9c9nnGO8pCds1nShNA0O6IGU0mjLFr8WsXfaJ6T7qK9osmZVC3NZn78SWcnwxEZMMl0QRvH6l1mnjC-GQdFDUwgFGDotncaOfSNKEPVgqYEb3KlVrmGTrSf0Rjtblg6DeavWQ6vBMRjkWhzEFt9YWlJeQAledsfil2rWs6iqBFhG4WDuxzMeLZwwD_tdnlDjA06m4Bp95anh46qJSCB2-T1GdIb-EuntrUNvPTgM2SvGcu0QfVmB4Z8fYnX9AIU9N6YTjF3FxNyP9hps60dz0MI9AFbvnoo6qgavGgVGuLCguYhAeOTg-A2BW3GgdTX7EFQ4MInjnqHsn1k2pkEp-7-sLP20xAOzNvasry56EF5q0lzbL6MlcfuYXx7UOzgOo7FzFmlbSas0WidmXhZWBkhldbRrcwhso3NEYMvgMzOyc0l0_l4E-IkTBsQfuKcKYf-Q0PJ-t7gjfbD-0bKviskpPW1-eJFRM2ABGPLESQjCI1S7jbvKLJHHU2jbvtsQDiNCrmlSW7pcHC17CncTVq2SQ7lBqIjwhDJrEIbtXhsd_sEUNEZkVaN3CAJl3ax0eUFJtQRKmgE4XtZReso0YOxLn26u1gnu759GGRJGujRhsxwkifqiaOGFjL0lXH_sxGqeo-PrAWV7poRJceBAtbZJXwMgEHtfjUm9gcFYAlz0CdDCR0RREgZ_-ouJyiDunBe4AkTiYwkEC27c8TSJgLK3ft0RdWauXtWwgxcX5rXrOLxZKc7IoqXnexcIuGI-qPULUyNsXNGUpxgUhTwZf4GfZjS5yfdv2R05RS8UWJSMApht_HRwc6m17i0dIoDw6v1a0Ju2BUfsDk1L8JnzMnaPTgUHWbUyAuDyKiAjs4Wf1C3JTr7vx3RlWZ5zf4D_NvPqrENBqM4kB15mPsENys5Pv06pQ8nYIBOP1MVrLFX59j66TUqv3LF-PEPjw2UH1qBEdmk6-RAvuzBd-UUrEBFe3RAMnpC-dJWVjOLgMgdbdp4ihyTs1M5EEV_I3aYvG_4GjUFIsH7xfiWNY8021nt4UYMlN5LGEo2vEm4RDYb70rJH3rNKpuqzFNSV3JvqkmDPLXpkuGla-Z3jDbxcOAPITYTiI6RXiZpKEKrsTO5dIh8Ah8uSQmJfQuXGixwUpqJOeN3HD2gojIrDpzKEVefGp3cF8vmVgreFZylk3W1U0ge_wSbE10jDZ4mjskQImXUF_mMw8v5PElCdgpd_wGWoNgIp04m64t6l-Z6NbFT_JZUWROxEnjX7aBytm9JS5Ik1r6AD0TBvqfqh0kmi81'
FOLDER_PATH = "/Cennos/Bloomingdale's/08.25.25"

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
