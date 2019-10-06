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
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

captureBuffer = None


#============================================================
# class
#============================================================
class Greeter(Datas_pb2_grpc.MainServerServicer):

	#==========
	def __init__(self):
		pass

	#==========
	def getStream(self, request_iterator, context):

		for req in request_iterator:

			print("request message = ", req.msg)


			gray = cv2.cvtColor(captureBuffer, cv2.COLOR_BGR2GRAY)


			ret, buf = cv2.imencode('.jpg', gray)
			if ret != 1:
				return
			
			b64e = base64.b64encode(buf)
			#print("base64 encode size : ", sys.getsizeof(b64e))

			yield Datas_pb2.Reply(datas = b64e)



#============================================================
# functions
#============================================================
def serve():

	server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))
	Datas_pb2_grpc.add_MainServerServicer_to_server(Greeter(), server)

	server.add_insecure_port('[::]:50051')
	server.start()

	print('server start')

	while True:
		try:
			ret, frame = cap.read()
			if ret != 1:
				continue

			global captureBuffer
			captureBuffer = frame
			cv2.imshow('Capture Image', captureBuffer)
			k = cv2.waitKey(1)
			if k == 27:
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