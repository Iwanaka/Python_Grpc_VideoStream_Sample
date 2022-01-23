# クライアントから送信される映像データを表示する

#============================================================
# import packages
#============================================================
from concurrent import futures
import time
import cv2
import grpc
import base64
import numpy as np
import Datas_pb2
import Datas_pb2_grpc
import sys

#============================================================
# classes
#============================================================
# クライアントから飛ばされる映像を表示する
class ShowVideoStream:
	
	img = None
	thread = futures.ThreadPoolExecutor(max_workers=1)

	#==========
	def start(self):
		self.thread.submit(self.ShowWindow)

	#==========
	def set(self, img):
		self.img = img

	#==========
	def ShowWindow(self):
		while True:
			if self.img is not None:

				# 表示
				cv2.imshow('dst Image', self.img)

				# ESCキーで抜ける
				k = cv2.waitKey(1)
				if k == 27:
					break

#====================
# サーバークラス
class Greeter(Datas_pb2_grpc.MainServerServicer):

	#==========
	def __init__(self):
		pass

	#==========
	def getStream(self, request_iterator, context):

		timer = 0

		# リクエストデータを表示クラスに渡す
		for req in request_iterator:
		
			# 所要時間を表示
			print('process time = ' + str(time.clock() - timer))
			timer = time.clock()
			
			# base64などで受信した場合はデコード
			# b64d = base64.b64decode(req.datas)
			#　print("base64 decode size : ", sys.getsizeof(b64d))
			
			# バッファを取得
			dBuf = np.frombuffer(req.datas, dtype = np.uint8)
			#print("buffer size : ", sys.getsizeof(dBuf))
			
			# デコード
			dst = cv2.imdecode(dBuf, cv2.IMREAD_COLOR)
			#print("dst size : ", sys.getsizeof(dst))
			
			# 表示クラスに渡す
			show.set(dst)

			# リプライ
			yield Datas_pb2.Reply(reply = 1)

#============================================================
# property
#============================================================
# 表示クラスを作成
show = ShowVideoStream()

#============================================================
# functions
#============================================================
def serve():

	# サーバーを生成
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	Datas_pb2_grpc.add_MainServerServicer_to_server(Greeter(), server)

	# ポートを設定
	server.add_insecure_port('[::]:50051')

	# 動作開始
	server.start()

	print('server start')

	# プロセスが止まらないようにメインプロセスを常に動作させておく
	try:
		while True:
			time.sleep(1/60)

	except KeyboardInterrupt:
		server.stop(0)



#============================================================
# main
#============================================================
if __name__ == '__main__':
	show.start()
	serve()

#============================================================
# after the App exit
#============================================================
cv2.destroyAllWindows()