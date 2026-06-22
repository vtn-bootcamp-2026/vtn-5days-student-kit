import os
import re

# Dinh nghia cac duong dan
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHECKPOINTS_DIR = os.path.join(BASE_DIR, "templates", "checkpoints")

# Ban do thay the tu ban cu sang ban v2
REPLACEMENTS = {
    # 1. Google Sheets OAuth2 API Credentials ID
    "W1oAfYZUJJmp2Lr6": "sumC7KMChnbc4kCV",
    
    # 2. Google Gemini API Credentials ID
    "pSl0vGbiOEn4nWO4": "tkVThA6aB48phz8O",
    
    # 3. Google Sheet Document ID
    "1mU6Nn3wqLcDw8o_hZV9aqhLO-681CM4bLoMnXkAB3VU": "1DBS2rYiRQ3NzcHjg0zA_hURZDllfICnar9YDqSGzWwY",
    
    # 4. Cache Name
    "smart_ticket_triage": "smart-tickage-triage",
    
    # 5. Gemini Model ID
    "models/gemini-3-flash-preview": "models/gemini-3.5-flash",
    "models/gemini-3-flash": "models/gemini-3.5-flash",
    
    # 6. Sheet IDs (Bao gom ca so trong JSON va chuoi trong cac URL)
    "851355465": "1733173600",    # Sheet 'input'
    "644031224": "1987908757",    # Sheet 'review_queue'
    "367600539": "114938839"      # Sheet 'execution_log'
}

def update_checkpoints():
    if not os.path.exists(CHECKPOINTS_DIR):
        print(f"Error: Khong tim thay thu muc checkpoints tai: {CHECKPOINTS_DIR}")
        return

    print("=== BAT DAU CAP NHAT CAC CHECKPOINT THEO CAU HINH V2 ===")
    
    # Lay danh sach cac file JSON trong checkpoints
    files = [f for f in os.listdir(CHECKPOINTS_DIR) if f.endswith(".json")]
    
    if not files:
        print("Khong tim thay file JSON nao can cap nhat.")
        return

    for file_name in files:
        file_path = os.path.join(CHECKPOINTS_DIR, file_name)
        print(f"\nDang xu ly file: {file_name}...")
        
        # Doc noi dung file
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        original_content = content
        changes_count = 0
        
        # Thuc hien thay the theo ban do REPLACEMENTS
        for old_val, new_val in REPLACEMENTS.items():
            # Dem so lan xuat hien cua chuoi can thay the
            occurrences = content.count(old_val)
            if occurrences > 0:
                content = content.replace(old_val, new_val)
                print(f"  * Da thay the '{old_val}' -> '{new_val}' ({occurrences} lan)")
                changes_count += occurrences

        # Ghi lai neu co su thay doi
        if changes_count > 0:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"=> Hoan thanh cap nhat file {file_name}. Tong so thay doi: {changes_count}")
        else:
            print(f"=> Khong co thay doi nao can cap nhat trong file {file_name}.")

    print("\n=== HOAN THANH CAP NHAT TOAN BO CAC CHECKPOINTS ===")

if __name__ == "__main__":
    update_checkpoints()
