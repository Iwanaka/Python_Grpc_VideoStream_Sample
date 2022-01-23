# カメラ映像を接続されたクライアントに送信する

#============================================================
# import packages
#============================================================
from concurrent import futures
import grpc
import Datas_pb2
import Datas_pb2_grpc
import time
import cv2
import base64
import sys

#============================================================
# property
#============================================================
# カメラを設定
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

captureBuffer = None


#============================================================
# class
#============================================================
# サーバークラス
class Greeter(Datas_pb2_grpc.MainServerServicer):

	#==========
	def __init__(self):
		pass

	#==========
	def getStream(self, request_iterator, context):

		for req in request_iterator:

			# リクエストメッセージを表示
			print("request message = ", req.msg)

			while True:

				# グレースケールに変換
				gray = cv2.cvtColor(captureBuffer, cv2.COLOR_BGR2GRAY)

				# jpgとしてデータをエンコード
				ret, buf = cv2.imencode('.jpg', gray)
				if ret != 1:
					return
				
				# 画像を文字列などで扱いたい場合はbase64でエンコード
				# b64e = base64.b64encode(buf)
				#print("base64 encode size : ", sys.getsizeof(b64e))

				# データを送信
				yield Datas_pb2.Reply(datas = buf.tobytes())

				# 60FPSに設定
				time.sleep(1/ 60)



#============================================================
# functions
#============================================================
def serve():

	# サーバーを生成
	server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))
	Datas_pb2_grpc.add_MainServerServicer_to_server(Greeter(), server)

	# ポートを設定
	server.add_insecure_port('[::]:50051')

	# 動作開始
	server.start()

	print('server start')

	while True:
		try:
			# カメラ映像から読み込み
			ret, frame = cap.read()
			if ret != 1:
				continue

			global captureBuffer
			captureBuffer = frame

			# 確認用ウィンドウ表示
			cv2.imshow('Capture Image', captureBuffer)

			# ESCキーで抜ける
			k = cv2.waitKey(1)
			if k == 27:
				server.stop(0)
				break

			time.sleep(0)

		except KeyboardInterrupt:
			server.stop(0)



#============================================================
# main
#============================================================
if __name__ == '__main__':
	serve()

#============================================================
# after the App exit
#============================================================
cap.release()
cv2.destroyAllWindows()