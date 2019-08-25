from packet import Packet, Level

pack = Packet(header="HEARTBEAT", message="Hello")
print(type(pack))
print(pack)
temp = pack.to_string()
print(type(temp))
print(temp)
back = Packet.from_string(temp)
print(type(back))
print(back)