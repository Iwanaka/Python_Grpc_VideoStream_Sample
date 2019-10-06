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



#============================================================
# property
#============================================================



#============================================================
# functions
#============================================================
def run():

	channel = grpc.insecure_channel('127.0.0.1:50051')
	stub = Datas_pb2_grpc.MainServerStub(channel)
	
	while True:
		try:
			
			
			message = []
			message.append(Datas_pb2.Request(msg = 'give me the stream!!'))
			responses = stub.getStream(iter(message))


			for res in responses:
				#print(res)

				b64d = base64.b64decode(res.datas)
				dBuf = np.frombuffer(b64d, dtype = np.uint8)
				dst = cv2.imdecode(dBuf, cv2.IMREAD_COLOR)
				#print("dst size : ", sys.getsizeof(dst))

				cv2.imshow('Capture Image', dst)
				
				k = cv2.waitKey(1)
				if k == 27:
					break


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
cv2.destroyAllWindows()
