import time
import threading
from threading import Thread
import math

def cpu_intensive_task(i: int) -> None:
    """CPUを集中的に使用する処理（GILのタイムスライスにより並行実行される）"""
    name = threading.current_thread().name
    print(f"{name} starting CPU intensive task {i}")
    start_time = time.time()
    
    # CPUを集中的に使用する計算処理
    result = 0
    for j in range(10**7):  # 1000万回の計算
        result += math.sqrt(j)
    
    end_time = time.time()
    print(f"{name} finished CPU intensive task {i} in {end_time - start_time:.2f} seconds")

def io_bound_task(i: int) -> None:
    """I/O処理（time.sleep）をシミュレート（完全に並行実行される）"""
    name = threading.current_thread().name
    print(f"{name} starting I/O bound task {i}")
    start_time = time.time()
    
    # I/O処理をシミュレート（実際にはスリープ）
    time.sleep(3)
    
    end_time = time.time()
    print(f"{name} finished I/O bound task {i} in {end_time - start_time:.2f} seconds")

def test_cpu_bound():
    """CPUバウンド処理のテスト"""
    print("=" * 50)
    print("CPUバウンド処理のテスト（GILのタイムスライスにより並行実行される）")
    print("=" * 50)
    
    start_time = time.time()
    threads = []
    
    for i in range(3):
        thread = Thread(target=cpu_intensive_task, args=(i,), name=f"CPU-Thread-{i}")
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    print(f"CPUバウンド処理の総実行時間: {end_time - start_time:.2f}秒")
    print("（GILのタイムスライスにより並行実行されるため、時間は短縮される）")

def test_io_bound():
    """I/Oバウンド処理のテスト"""
    print("\n" + "=" * 50)
    print("I/Oバウンド処理のテスト（並行実行されるはず）")
    print("=" * 50)
    
    start_time = time.time()
    threads = []
    
    for i in range(3):
        thread = Thread(target=io_bound_task, args=(i,), name=f"IO-Thread-{i}")
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    print(f"I/Oバウンド処理の総実行時間: {end_time - start_time:.2f}秒")
    print("（各スレッドが並行実行されるため、時間は短縮される）")

if __name__ == "__main__":
    test_cpu_bound()
    test_io_bound() 