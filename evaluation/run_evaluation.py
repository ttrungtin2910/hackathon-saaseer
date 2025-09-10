"""
Script runner để chạy đánh giá hiệu suất trích xuất thông tin
Sử dụng: python run_evaluation.py
"""

import os
import sys
from pathlib import Path

# Thêm thư mục gốc vào Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import và chạy evaluation
from evaluation.evaluation_script import main

if __name__ == "__main__":
    print("🚀 Bắt đầu đánh giá hiệu suất trích xuất thông tin hóa đơn/hợp đồng...")
    print("📁 Đang xử lý các files trong thư mục 'data'...")
    print("⏱️  Quá trình này có thể mất vài phút tùy thuộc vào số lượng files...")
    print("-" * 80)
    
    try:
        main()
        print("\n✅ Đánh giá hoàn thành thành công!")
        print("📊 Kiểm tra các file kết quả đã được tạo:")
        print("   • contract_extraction_evaluation_results.xlsx")
        print("   • evaluation_results.json") 
        print("   • evaluation_log.txt")
        
    except Exception as e:
        print(f"\n❌ Lỗi khi chạy đánh giá: {e}")
        sys.exit(1)
