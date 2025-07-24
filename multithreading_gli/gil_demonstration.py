import time
import threading
from threading import Thread
import math

def cpu_intensive_without_gil_release(i: int) -> None:
    """GILを解放しないCPU集中処理（実際にはGILのタイムスライスにより並行実行される）"""
    name = threading.current_thread().name
    print(f"{name} starting CPU intensive task {i}")
    start_time = time.time()
    
    # 非常に長い計算処理（GILを解放しない）
    result = 0
    for j in range(10**8):  # 1億回の計算
        result += math.sqrt(j)
        # 注意: この処理はGILを解放しない
    
    end_time = time.time()
    print(f"{name} finished CPU intensive task {i} in {end_time - start_time:.2f} seconds")

def cpu_intensive_with_gil_release(i: int) -> None:
    """GILを定期的に解放するCPU集中処理（明示的に並行実行を促進）"""
    name = threading.current_thread().name
    print(f"{name} starting CPU intensive task with GIL release {i}")
    start_time = time.time()
    
    # 計算処理を小さなブロックに分けて、定期的にGILを解放
    result = 0
    for block in range(100):  # 100ブロックに分割
        for j in range(10**6):  # 各ブロックで100万回の計算
            result += math.sqrt(block * 10**6 + j)
        
        # 定期的にGILを解放（他のスレッドに実行機会を与える）
        time.sleep(0.001)  # 1ミリ秒のスリープ
    
    end_time = time.time()
    print(f"{name} finished CPU intensive task with GIL release {i} in {end_time - start_time:.2f} seconds")

def test_without_gil_release():
    """GILを解放しない場合のテスト"""
    print("=" * 60)
    print("GILを解放しないCPUバウンド処理のテスト")
    print("（実際にはGILのタイムスライスにより並行実行される）")
    print("=" * 60)
    
    start_time = time.time()
    threads = []
    
    for i in range(2):
        thread = Thread(target=cpu_intensive_without_gil_release, args=(i,), name=f"CPU-NoRelease-{i}")
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    print(f"GILを解放しない場合の総実行時間: {end_time - start_time:.2f}秒")
    print("（各スレッドが順次実行されるため、時間は積算される）")

def test_with_gil_release():
    """GILを定期的に解放する場合のテスト"""
    print("\n" + "=" * 60)
    print("GILを定期的に解放するCPUバウンド処理のテスト")
    print("（明示的に並行実行を促進）")
    print("=" * 60)
    
    start_time = time.time()
    threads = []
    
    for i in range(2):
        thread = Thread(target=cpu_intensive_with_gil_release, args=(i,), name=f"CPU-WithRelease-{i}")
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    print(f"GILを定期的に解放する場合の総実行時間: {end_time - start_time:.2f}秒")
    print("（各スレッドが並行実行されるため、時間は短縮される）")

def simple_io_bound():
    """シンプルなI/Oバウンド処理（完全に並行実行される）"""
    name = threading.current_thread().name
    print(f"{name} starting I/O bound task")
    time.sleep(2)
    print(f"{name} finished I/O bound task")

def test_io_bound():
    """I/Oバウンド処理のテスト"""
    print("\n" + "=" * 60)
    print("I/Oバウンド処理のテスト（完全に並行実行される）")
    print("=" * 60)
    
    start_time = time.time()
    threads = []
    
    for i in range(3):
        thread = Thread(target=simple_io_bound, name=f"IO-Thread-{i}")
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    print(f"I/Oバウンド処理の総実行時間: {end_time - start_time:.2f}秒")
    print("（各スレッドが並行実行されるため、時間は短縮される）")

if __name__ == "__main__":
    test_without_gil_release()
    test_with_gil_release()
    test_io_bound() 