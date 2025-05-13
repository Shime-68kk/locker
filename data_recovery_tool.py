
import os
import subprocess
import shutil
from datetime import datetime

def list_shadow_copies():
    try:
        output = subprocess.check_output("vssadmin list shadows", shell=True, text=True)
        return output
    except subprocess.CalledProcessError as e:
        return f"Lỗi khi lấy danh sách shadow copy: {e}"

def recover_files_from_shadow_copy(drive_letter='C'):
    shadow_output = list_shadow_copies()
    shadow_paths = []

    for line in shadow_output.splitlines():
        if "Shadow Copy Volume" in line:
            path = line.split(": ")[-1]
            shadow_paths.append(path)

    restore_folder = os.path.join(os.getcwd(), f"recovered_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    os.makedirs(restore_folder, exist_ok=True)

    recovered = []

    for shadow_path in shadow_paths:
        try:
            target_path = f"{shadow_path}\Users"
            if os.path.exists(target_path):
                dst = os.path.join(restore_folder, os.path.basename(shadow_path))
                shutil.copytree(target_path, dst, dirs_exist_ok=True)
                recovered.append(dst)
        except Exception as e:
            print(f"Lỗi khi khôi phục từ {shadow_path}: {e}")

    return recovered

if __name__ == "__main__":
    print("🔍 Đang quét các bản sao lưu hệ thống...")
    paths = recover_files_from_shadow_copy()
    if paths:
        print("✅ Dữ liệu đã được khôi phục tại các thư mục sau:")
        for path in paths:
            print(f" - {path}")
    else:
        print("❌ Không tìm thấy bản sao lưu có thể phục hồi.")
