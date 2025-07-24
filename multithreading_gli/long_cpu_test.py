import time
import threading
from threading import Thread

def very_long_cpu_intensive(i: int) -> None:
    """非常に長いCPU集中処理（GILのタイムスライスにより並行実行される）"""
    name = threading.current_thread().name
    print(f"{name} starting very long CPU intensive task {i}")
    start_time = time.time()
    
    # 非常に長い計算処理
    result = 0
    for j in range(10**8):  # 1億回のループ
        result += j * j + j // 2 + j % 3
        # 最適化を防ぐため、結果を使用
        if result > 10**20:  # オーバーフロー防止
            result = result % 10**10
    
    end_time = time.time()
    print(f"{name} finished very long CPU intensive task {i} in {end_time - start_time:.2f} seconds")
    print(f"{name} final result: {result}")

def test_very_long_cpu():
    """非常に長いCPU処理のテスト"""
    print("=" * 70)
    print("非常に長いCPU処理のテスト")
    print("（GILのタイムスライスにより並行実行される）")
    print("=" * 70)
    
    start_time = time.time()
    threads = []
    
    for i in range(2):
        thread = Thread(target=very_long_cpu_intensive, args=(i,), name=f"LongCPU-{i}")
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    print(f"非常に長いCPU処理の総実行時間: {end_time - start_time:.2f}秒")

def compare_single_vs_multi():
    """シングルスレッド vs マルチスレッドの比較"""
    print("\n" + "=" * 70)
    print("シングルスレッド vs マルチスレッドの比較")
    print("=" * 70)
    
    def single_cpu_task():
        """シングルスレッドでのCPU処理"""
        print("Starting single-threaded CPU task...")
        start_time = time.time()
        
        result = 0
        for j in range(10**8):
            result += j * j + j // 2 + j % 3
            if result > 10**20:
                result = result % 10**10
        
        end_time = time.time()
        print(f"Single-threaded task finished in {end_time - start_time:.2f} seconds")
        return result
    
    # シングルスレッド実行
    single_start = time.time()
    result1 = single_cpu_task()
    result2 = single_cpu_task()
    single_end = time.time()
    
    print(f"Single-threaded total time: {single_end - single_start:.2f} seconds")
    
    # マルチスレッド実行
    multi_start = time.time()
    threads = []
    
    for i in range(2):
        thread = Thread(target=very_long_cpu_intensive, args=(i,), name=f"MultiCPU-{i}")
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    multi_end = time.time()
    print(f"Multi-threaded total time: {multi_end - multi_start:.2f} seconds")
    
    # 比較
    speedup = (single_end - single_start) / (multi_end - multi_start)
    print(f"Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    test_very_long_cpu()
    compare_single_vs_multi() 