"""
Script thiết lập môi trường để chạy đánh giá hiệu suất
"""

import os
import sys
from pathlib import Path
import subprocess

def check_python_version():
    """Kiểm tra phiên bản Python"""
    if sys.version_info < (3, 8):
        print("❌ Cần Python 3.8 trở lên")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def check_data_folder():
    """Kiểm tra thư mục data"""
    data_folder = Path("data")
    if not data_folder.exists():
        print("❌ Thư mục 'data' không tồn tại")
        return False
    
    files = list(data_folder.glob("*"))
    print(f"✅ Thư mục 'data' có {len(files)} files")
    return True

def check_env_file():
    """Kiểm tra file .env"""
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  File .env không tồn tại")
        print("   Tạo file .env từ config/.env.example và cấu hình các API keys")
        return False
    print("✅ File .env tồn tại")
    return True

def install_dependencies():
    """Cài đặt dependencies"""
    print("📦 Đang cài đặt dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True, text=True)
        print("✅ Đã cài đặt dependencies")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi cài đặt dependencies: {e}")
        return False

def main():
    """Chạy setup môi trường"""
    print("🛠️  THIẾT LẬP MÔI TRƯỜNG ĐÁNH GIÁ AI")
    print("=" * 50)
    
    checks = [
        ("Kiểm tra Python version", check_python_version),
        ("Kiểm tra thư mục data", check_data_folder),
        ("Kiểm tra file .env", check_env_file),
        ("Cài đặt dependencies", install_dependencies),
    ]
    
    all_passed = True
    for description, check_func in checks:
        print(f"\n{description}...")
        if not check_func():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✅ Thiết lập hoàn thành! Sẵn sàng chạy đánh giá:")
        print("   • Demo test: python evaluation/demo_evaluation.py")
        print("   • Full evaluation: python evaluation/run_evaluation.py")
    else:
        print("❌ Có lỗi trong quá trình thiết lập. Vui lòng khắc phục và chạy lại.")
        
if __name__ == "__main__":
    main()
