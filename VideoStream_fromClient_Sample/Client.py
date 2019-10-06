#============================================================
# import packages
#============================================================
from concurrent import futures
import grpc
import cv2
import Datas_pb2
import Datas_pb2_grpc
import base64
import sys


#============================================================
# class
#============================================================



#============================================================
# property
#============================================================
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)




#============================================================
# functions
#============================================================
def Request(frame):

	#print("origin size : ", sys.getsizeof(gray))
	ret, buf = cv2.imencode('.jpg', frame)

	if ret != 1:
			return

	# encode to base64
	b64e = base64.b64encode(buf)
	#print("base64 encode size : ", sys.getsizeof(b64e))

	yield Datas_pb2.Request(datas = b64e)


#====================
def run():

	channel = grpc.insecure_channel('localhost:50051')
	stub = Datas_pb2_grpc.MainServerStub(channel)
	
	while True:

		try:
		
			ret, frame = cap.read()
			if ret != 1:
				continue

			cv2.imshow('Capture Image', frame)
			k = cv2.waitKey(1)
			if k == 27:
				break

			responses = stub.getStream( Request(frame) )
			for res in responses:
				print(res)
		
		except grpc.RpcError as e:
			print(e.details())
			#break



#============================================================
# Awake
#============================================================



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