from logging import *
pack = Packet("Ayush")
log = Log()
pack.add(log)
pack_str = pack.to_string()
print(pack_str)
pack2 = Packet.from_string(pack_str)
print(pack2)
print(pack2.__dict__)
for log in pack2.logs:
    print(log.header, log.message)