import time
import threading
from threading import Thread

def pure_python_cpu_intensive(i: int) -> None:
    """純粋なPythonコードによるCPU集中処理（GILのタイムスライスにより並行実行される）"""
    name = threading.current_thread().name
    print(f"{name} starting pure Python CPU intensive task {i}")
    start_time = time.time()
    
    # 純粋なPythonコードによる計算処理
    result = 0
    for j in range(10**7):  # 1000万回のループ
        # 純粋なPythonの計算（GILのタイムスライスにより並行実行される）
        result += j * j + j // 2 + j % 3
        if j % 1000000 == 0:  # 100万回ごとに進捗表示
            print(f"{name} progress: {j//1000000}/10")
    
    end_time = time.time()
    print(f"{name} finished pure Python CPU intensive task {i} in {end_time - start_time:.2f} seconds")

def pure_python_with_gil_release(i: int) -> None:
    """定期的にGILを解放する純粋なPython処理"""
    name = threading.current_thread().name
    print(f"{name} starting pure Python task with GIL release {i}")
    start_time = time.time()
    
    result = 0
    for j in range(10**7):
        result += j * j + j // 2 + j % 3
        if j % 1000000 == 0:
            print(f"{name} progress: {j//1000000}/10")
            # 定期的にGILを解放
            time.sleep(0.001)  # 1ミリ秒のスリープ
    
    end_time = time.time()
    print(f"{name} finished pure Python task with GIL release {i} in {end_time - start_time:.2f} seconds")

def test_pure_python_without_gil_release():
    """GILを解放しない純粋なPython処理のテスト"""
    print("=" * 70)
    print("GILを解放しない純粋なPython処理のテスト")
    print("（実際にはGILのタイムスライスにより並行実行される）")
    print("=" * 70)
    
    start_time = time.time()
    threads = []
    
    for i in range(2):
        thread = Thread(target=pure_python_cpu_intensive, args=(i,), name=f"PurePython-{i}")
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    print(f"GILを解放しない場合の総実行時間: {end_time - start_time:.2f}秒")
    print("（各スレッドが順次実行されるため、時間は積算される）")

def test_pure_python_with_gil_release():
    """GILを定期的に解放する純粋なPython処理のテスト"""
    print("\n" + "=" * 70)
    print("GILを定期的に解放する純粋なPython処理のテスト")
    print("（明示的に並行実行を促進）")
    print("=" * 70)
    
    start_time = time.time()
    threads = []
    
    for i in range(2):
        thread = Thread(target=pure_python_with_gil_release, args=(i,), name=f"PurePython-WithRelease-{i}")
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    print(f"GILを定期的に解放する場合の総実行時間: {end_time - start_time:.2f}秒")
    print("（各スレッドが並行実行されるため、時間は短縮される）")

def simple_io_bound():
    """シンプルなI/Oバウンド処理"""
    name = threading.current_thread().name
    print(f"{name} starting I/O bound task")
    time.sleep(3)
    print(f"{name} finished I/O bound task")

def test_io_bound():
    """I/Oバウンド処理のテスト"""
    print("\n" + "=" * 70)
    print("I/Oバウンド処理のテスト（完全に並行実行される）")
    print("=" * 70)
    
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
    test_pure_python_without_gil_release()
    test_pure_python_with_gil_release()
    test_io_bound() 