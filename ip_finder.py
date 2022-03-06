import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

for i in range(1,256):
	ip = '192.168.1.{}'.format(i)
	try:
		s.connect((ip, 22))
		print('Raspi is probably on {}'.format(ip))
	except socket.error as e:
		print('Nothing on {}.'.format(ip))
		pass
		
	s.close()