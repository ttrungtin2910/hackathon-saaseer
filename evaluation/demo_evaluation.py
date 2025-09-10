"""
Demo script để test đánh giá hiệu suất với một số files mẫu
Chạy trước khi xử lý toàn bộ dataset
"""

import os
import sys
from pathlib import Path

# Thêm thư mục gốc vào Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from evaluation.evaluation_script import ContractExtractionEvaluator


def run_demo(num_files: int = 5):
    """Chạy demo với số files giới hạn"""
    print(f"🧪 Chạy demo đánh giá với {num_files} files đầu tiên...")
    print("-" * 60)
    
    try:
        # Khởi tạo evaluator
        evaluator = ContractExtractionEvaluator("data")
        
        # Lấy danh sách files và giới hạn số lượng
        all_files = evaluator.get_file_list()
        demo_files = all_files[:num_files]
        
        print(f"📁 Sẽ xử lý {len(demo_files)} files:")
        for i, file_path in enumerate(demo_files, 1):
            print(f"   {i}. {file_path.name}")
        
        print("\n🚀 Bắt đầu xử lý...")
        
        # Xử lý từng file
        for i, file_path in enumerate(demo_files, 1):
            print(f"\n📄 Đang xử lý file {i}/{len(demo_files)}: {file_path.name}")
            
            result = evaluator.extract_from_single_file(file_path)
            evaluator.results.append(result)
            
            # Cập nhật metrics
            if result['success']:
                evaluator.performance_metrics['successful_extractions'] += 1
                print(f"   ✅ Thành công - Điểm chất lượng: {result['data_quality_score']}/100")
                print(f"   📊 Dữ liệu trích xuất:")
                print(f"      • Provider: {result.get('provider', 'N/A')}")
                print(f"      • Service: {result.get('service', 'N/A')}")
                print(f"      • Start Date: {result.get('start_date', 'N/A')}")
                print(f"      • End Date: {result.get('end_date', 'N/A')}")
                price = result.get('price', 'N/A')
                currency = result.get('currency', '')
                price_display = f"{price} {currency}".strip() if price != 'N/A' and price else 'N/A'
                print(f"      • Price: {price_display}")
            else:
                evaluator.performance_metrics['failed_extractions'] += 1
                print(f"   ❌ Thất bại - Lỗi: {result.get('error_message', 'Unknown error')}")
            
            print(f"   ⏱️  Thời gian xử lý: {result['processing_time_seconds']}s")
            
            evaluator.performance_metrics['total_processing_time'] += result['processing_time_seconds']
        
        # Cập nhật metrics cuối cùng
        evaluator.performance_metrics['total_files'] = len(demo_files)
        evaluator._calculate_final_metrics()
        
        # Xuất kết quả demo
        evaluator.export_to_excel("demo_evaluation_results.xlsx")
        
        # In tóm tắt
        print("\n" + "="*60)
        print("           KẾT QUẢ DEMO ĐÁNH GIÁ")
        print("="*60)
        evaluator.print_summary()
        
        print("📊 Files kết quả demo:")
        print("   • demo_evaluation_results.xlsx")
        print("\n✅ Demo hoàn thành! Bây giờ có thể chạy full evaluation với:")
        print("   python run_evaluation.py")
        
    except Exception as e:
        print(f"\n❌ Lỗi khi chạy demo: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Demo đánh giá hiệu suất AI")
    parser.add_argument("--files", "-f", type=int, default=5, 
                       help="Số lượng files để test (mặc định: 5)")
    
    args = parser.parse_args()
    run_demo(args.files)
