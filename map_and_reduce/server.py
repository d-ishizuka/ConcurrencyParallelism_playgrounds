import os
import glob
import asyncio

from scheduler import Scheduler
from protocol import Protocol, HOST, PORT, FileWithId

class Server(Protocol):
    # 入力ファイル群 → Map処理 → 中間結果 → Reduce処理 → 最終結果
    def __init__(self, scheduler:Scheduler) -> None:
        super().__init__()
        self.scheduler = scheduler
    
    def connnection_made(self, transport: asyncio.Transport) -> None:
        # 新しいワーカーが接続すると自動的にタスクを割り当てる
        # 非同期処理により、複数のワーカーを同時に管理する
        peername = transport.get_extra_info("peername")
        print(f"New worker connection from {peername}")
        self.start_new_task()
    
    def start_new_task(self) -> None:
        # スケジューラが次のタスクを割り当てるための処理
        command, data = self.scheduler.get_next_task()
        self.send_command(command=command, data=data)
        
    def process_command(self, command: bytes, data: FileWithId = None) -> None:
        # ワーカーがファイルを処理完了すると、mapdoneコマンドを送ってくる（reducedoneも同様）
        # スケジューラが次のタスクを割り当てる
        if command == b"mapdone":
            self.scheduler.map_done(data)
            self.start_new_task()
        elif command == b"reducedone":
            self.scheduler.reduce_done()
            self.start_new_task()
        else:
            print(f"Unknown commandn recived: {command}")

def main():
    # シングルスレッドで複数の接続を処理
    # I/O待機中は他の処理を実行
    # 効率的なリソース使用
    
    # asyncioはシングルスレッドで動作します：
    #　　1つのイベントループで複数のタスクを管理
    # スレッドは作成されない
    # スレッドを作成してマルチスレッドの場合は、threadingモジュールを使用することになる
    event_loop = asyncio.get_event_loop()
    
    current_path = os.path.abspath(os.getcwd())
    file_locations = list(
        glob.glob(f"{current_path}/input_files/*.txt")
    )
    scheduler = Scheduler(file_locations)
    
    # 非同期サーバーを作成
    # ワーカーからの接続を待機
    server = event_loop.create_server(
        lambda: Server(scheduler), HOST, PORT
    )
    
    # completeの条件:
    # サーバーが正常に起動
    # ソケットがリッスン状態になる
    # 接続を受け付けられる状態になる
    # 内部的にはこんな感じ
    # async def create_server():
    #     # ソケット作成
    #     sock = socket.socket()
    #     sock.bind((HOST, PORT))
    #     sock.listen()
    #     ret`urn server  # ← ここでcomplete
    # run_until_completeは、このcreate_server()が完了するまで待機
    # 1. サーバー作成（完了まで待機）
    server = event_loop.run_until_complete(server)
    
    print(f"Serving on {server.sockets[0].getsockname()}")
    
    try:
        # 2. 永久ループ開始
        event_loop.run_forever()
    finally:
        server.close()
        event_loop.run_until_complete(server.wait_closed())
        event_loop.close()

if __name__ == "__main__":
    main()