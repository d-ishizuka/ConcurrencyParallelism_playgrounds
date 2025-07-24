import time
import threading
from threading import Thread

def strict_cpu_intensive(i: int) -> None:
    """I/O操作を完全に排除したCPU集中処理（GILのタイムスライスにより並行実行される）"""
    name = threading.current_thread().name
    print(f"{name} starting strict CPU intensive task {i}")
    start_time = time.time()
    
    # 純粋なCPU計算のみ（I/O操作なし）
    result = 0
    for j in range(10**7):  # 1000万回のループ
        # 純粋なPythonの計算（GILのタイムスライスにより並行実行される）
        result += j * j + j // 2 + j % 3
        # 注意: print文やI/O操作は一切なし
    
    end_time = time.time()
    print(f"{name} finished strict CPU intensive task {i} in {end_time - start_time:.2f} seconds")
    print(f"{name} final result: {result}")  # 結果を表示（最適化を防ぐため）

def strict_cpu_with_gil_release(i: int) -> None:
    """定期的にGILを解放するCPU集中処理"""
    name = threading.current_thread().name
    print(f"{name} starting strict CPU task with GIL release {i}")
    start_time = time.time()
    
    result = 0
    for j in range(10**7):
        result += j * j + j // 2 + j % 3
        if j % 1000000 == 0:  # 100万回ごとにGILを解放
            time.sleep(0.001)  # 1ミリ秒のスリープ
    
    end_time = time.time()
    print(f"{name} finished strict CPU task with GIL release {i} in {end_time - start_time:.2f} seconds")
    print(f"{name} final result: {result}")

def test_strict_cpu_without_gil_release():
    """I/O操作なしのCPU集中処理テスト"""
    print("=" * 70)
    print("I/O操作なしのCPU集中処理テスト")
    print("（実際にはGILのタイムスライスにより並行実行される）")
    print("=" * 70)
    
    start_time = time.time()
    threads = []
    
    for i in range(2):
        thread = Thread(target=strict_cpu_intensive, args=(i,), name=f"StrictCPU-{i}")
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    print(f"I/O操作なしの場合の総実行時間: {end_time - start_time:.2f}秒")
    print("（各スレッドが順次実行されるため、時間は積算される）")

def test_strict_cpu_with_gil_release():
    """定期的にGILを解放するCPU集中処理テスト"""
    print("\n" + "=" * 70)
    print("定期的にGILを解放するCPU集中処理テスト")
    print("（明示的に並行実行を促進）")
    print("=" * 70)
    
    start_time = time.time()
    threads = []
    
    for i in range(2):
        thread = Thread(target=strict_cpu_with_gil_release, args=(i,), name=f"StrictCPU-WithRelease-{i}")
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    print(f"定期的にGILを解放する場合の総実行時間: {end_time - start_time:.2f}秒")
    print("（各スレッドが並行実行されるため、時間は短縮される）")

def io_bound_comparison():
    """I/Oバウンド処理との比較"""
    print("\n" + "=" * 70)
    print("I/Oバウンド処理との比較（完全に並行実行される）")
    print("=" * 70)
    
    def simple_io_task():
        name = threading.current_thread().name
        print(f"{name} starting I/O task")
        time.sleep(2)
        print(f"{name} finished I/O task")
    
    start_time = time.time()
    threads = []
    
    for i in range(2):
        thread = Thread(target=simple_io_task, name=f"IO-Thread-{i}")
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    print(f"I/Oバウンド処理の総実行時間: {end_time - start_time:.2f}秒")

if __name__ == "__main__":
    test_strict_cpu_without_gil_release()
    test_strict_cpu_with_gil_release()
    io_bound_comparison() 