# サーバーに接続して、カメラ映像を都度送信する ※ストリームではない

#============================================================
# import packages
#============================================================
from concurrent import futures
import grpc
import cv2
import Datas_pb2
import Datas_pb2_grpc
import time
import base64
import sys

#============================================================
# class
#============================================================
# ***

#============================================================
# property
#============================================================
# カメラを設定
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#============================================================
# functions
#============================================================
# サーバーにリクエストデータとして映像を送信
def Request(frame):

	#print("origin size : ", sys.getsizeof(gray))

	# jpgとしてエンコード
	ret, buf = cv2.imencode('.jpg', frame)
	if ret != 1:
		return

	# 文字列などで扱いたい場合はbase64などにエンコード
	# b64e = base64.b64encode(buf)
	#print("base64 encode size : ", sys.getsizeof(b64e))

	# データをリクエスト
	yield Datas_pb2.Request(datas = buf.tobytes())


#====================
# メインプロセス
def run():

	# 送信先を指定
	channel = grpc.insecure_channel('localhost:50051')
	stub = Datas_pb2_grpc.MainServerStub(channel)
	
	while True:

		try:

			# カメラ映像を読み込み
			ret, frame = cap.read()
			if ret != 1:
				continue
			
			# 確認用ウィンドウ
			cv2.imshow('Capture Image', frame)

			# ESCキーで抜ける
			k = cv2.waitKey(1)
			if k == 27:
				break

			# データをリクエスト
			responses = stub.getStream( Request(frame) )

			# レスポンスを表示
			for res in responses:
				print(res)

			# 60FPSで動作
			time.sleep(1/60)
		
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
cap.release()
cv2.destroyAllWindows()