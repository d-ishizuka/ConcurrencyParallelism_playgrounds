import time
import threading
from threading import Thread
import random

def cpu_task_with_different_patterns(i: int, pattern: str) -> int:
    """異なるパターンのCPU処理（GILのタイムスライスにより並行実行される）"""
    name = threading.current_thread().name
    print(f"{name} starting {pattern} task {i}")
    start_time = time.time()
    
    if pattern == "simple":
        # シンプルな計算
        result = 0
        for j in range(10**7):
            result += j
    
    elif pattern == "complex":
        # 複雑な計算
        result = 0
        for j in range(10**7):
            result += j * j + j // 2 + j % 3
            if result > 10**20:
                result = result % 10**10
    
    elif pattern == "memory_intensive":
        # メモリ集中処理
        data = []
        for j in range(10**6):
            data.append(j * j)
        result = sum(data)
    
    elif pattern == "random":
        # ランダムアクセス
        result = 0
        for j in range(10**7):
            result += random.randint(1, 100)
    
    end_time = time.time()
    print(f"{name} finished {pattern} task {i} in {end_time - start_time:.2f} seconds")
    return result

def test_single_threaded():
    """シングルスレッドでの実行"""
    print("=" * 70)
    print("シングルスレッド実行")
    print("=" * 70)
    
    patterns = ["simple", "complex", "memory_intensive", "random"]
    results = {}
    
    for pattern in patterns:
        start_time = time.time()
        result1 = cpu_task_with_different_patterns(0, pattern)
        result2 = cpu_task_with_different_patterns(1, pattern)
        end_time = time.time()
        
        results[pattern] = {
            'time': end_time - start_time,
            'result1': result1,
            'result2': result2
        }
        print(f"{pattern}: {end_time - start_time:.2f} seconds")
    
    return results

def test_multi_threaded():
    """マルチスレッドでの実行"""
    print("\n" + "=" * 70)
    print("マルチスレッド実行")
    print("=" * 70)
    
    patterns = ["simple", "complex", "memory_intensive", "random"]
    results = {}
    
    for pattern in patterns:
        start_time = time.time()
        threads = []
        
        for i in range(2):
            thread = Thread(target=cpu_task_with_different_patterns, args=(i, pattern), name=f"Multi-{pattern}-{i}")
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        results[pattern] = {
            'time': end_time - start_time
        }
        print(f"{pattern}: {end_time - start_time:.2f} seconds")
    
    return results

def compare_performance():
    """性能比較"""
    print("\n" + "=" * 70)
    print("性能比較")
    print("=" * 70)
    
    single_results = test_single_threaded()
    multi_results = test_multi_threaded()
    
    print("\n" + "=" * 70)
    print("詳細比較")
    print("=" * 70)
    print(f"{'Pattern':<20} {'Single':<10} {'Multi':<10} {'Speedup':<10}")
    print("-" * 50)
    
    for pattern in single_results.keys():
        single_time = single_results[pattern]['time']
        multi_time = multi_results[pattern]['time']
        speedup = single_time / multi_time
        
        print(f"{pattern:<20} {single_time:<10.2f} {multi_time:<10.2f} {speedup:<10.2f}x")

def test_cache_effects():
    """キャッシュ効果のテスト"""
    print("\n" + "=" * 70)
    print("キャッシュ効果のテスト")
    print("=" * 70)
    
    def cache_friendly_task():
        """キャッシュフレンドリーな処理"""
        name = threading.current_thread().name
        print(f"{name} starting cache-friendly task")
        start_time = time.time()
        
        # 連続したメモリアクセス
        data = [0] * 10**6
        for i in range(10**6):
            data[i] = i * i
        
        end_time = time.time()
        print(f"{name} finished cache-friendly task in {end_time - start_time:.2f} seconds")
    
    def cache_unfriendly_task():
        """キャッシュアンフレンドリーな処理"""
        name = threading.current_thread().name
        print(f"{name} starting cache-unfriendly task")
        start_time = time.time()
        
        # ランダムアクセス
        data = [0] * 10**6
        indices = list(range(10**6))
        random.shuffle(indices)
        
        for i in indices:
            data[i] = i * i
        
        end_time = time.time()
        print(f"{name} finished cache-unfriendly task in {end_time - start_time:.2f} seconds")
    
    # シングルスレッド
    print("Single-threaded cache-friendly:")
    start_time = time.time()
    cache_friendly_task()
    cache_friendly_task()
    single_cache_time = time.time() - start_time
    print(f"Total time: {single_cache_time:.2f} seconds")
    
    # マルチスレッド
    print("\nMulti-threaded cache-friendly:")
    start_time = time.time()
    threads = []
    for i in range(2):
        thread = Thread(target=cache_friendly_task, name=f"Cache-{i}")
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    multi_cache_time = time.time() - start_time
    print(f"Total time: {multi_cache_time:.2f} seconds")
    print(f"Speedup: {single_cache_time / multi_cache_time:.2f}x")

if __name__ == "__main__":
    compare_performance()
    test_cache_effects() 