# サーバーから送信されるカメラ映像を表示する

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
# class
#============================================================
# ***

#============================================================
# property
#============================================================
# ***

#============================================================
# functions
#============================================================
def run():

	# サーバーの宛先
	channel = grpc.insecure_channel('127.0.0.1:50051')
	stub = Datas_pb2_grpc.MainServerStub(channel)
	
	try:

		# リクエストデータを作成
		message = []
		message.append(Datas_pb2.Request(msg = 'give me the stream!!'))
		responses = stub.getStream(iter(message))

		for res in responses:
			# print(res.datas)

			# 画像を文字列などで扱いたい場合
			# b64d = base64.b64decode(res.datas)

			# バッファを作成
			dBuf = np.frombuffer(res.datas, dtype = np.uint8)

			# 作成したバッファにデータを入れる
			dst = cv2.imdecode(dBuf, cv2.IMREAD_COLOR)

			# 確認用Window
			cv2.imshow('Capture Image', dst)
			
			# ESCキーで抜ける
			k = cv2.waitKey(1)
			if k == 27:
				break

	except grpc.RpcError as e:
		print(e.details())
		#break


#============================================================
# Awake
#============================================================
# ***

#============================================================
# main
#============================================================
if __name__ == '__main__':
	run()

#============================================================
# after the App exit
#============================================================
cv2.destroyAllWindows()
