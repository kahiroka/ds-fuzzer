import struct

class ProtoBufs:
    def decode(msg):
        dic = {}
        lis = []
        if len(msg) > 0:
            idx = 0
            while len(msg) > idx:
                var, width = ProtoBufs.devar(msg[idx:])
                key = var >> 3
                wire_type = var & 7
                idx = idx + width
                if wire_type == 0: # var/uint32
                    var, width = ProtoBufs.devar(msg[idx:])
                    dic[str(key) + f":var"] = var
                    idx = idx + width
                elif wire_type == 1: # i64/double
                    val = round(struct.unpack("<d", msg[idx:idx+8])[0], 3)
                    dic[str(key) + f":f64"] = val
                    idx = idx + 8
                elif wire_type == 2: # string/embedded
                    size, width = ProtoBufs.devar(msg[idx:])
                    tmp = msg[idx + width:idx + width + size]
                    if size > 2: # fixme: determination of bytes and embedded
                        printable = True
                        try:
                            if tmp.decode('utf-8').isprintable():
                                dic[str(key)] = tmp
                            else:
                                printable = False
                        except UnicodeDecodeError:
                            printable = False

                        if not printable:
                            if str(key) in dic:
                                if type(dic[str(key)]) == dict:
                                    tmp2 = dic[str(key)]
                                    lis.append(tmp2)
                                    dic[str(key)] = lis
                                dic[str(key)].append(ProtoBufs.decode(tmp))
                            else:
                                dic[str(key)] = ProtoBufs.decode(tmp)
                    else:
                        dic[str(key)] = tmp
                    idx = idx + width + size
                elif wire_type == 5: # i32/float
                    val = round(struct.unpack("<f", msg[idx:idx+4])[0], 3)
                    dic[str(key) + f":f32"] = val
                    idx = idx + 4
                else:
                    print(f"key:{key} wire_type:{wire_type} something wrong")
                    print(msg[idx:])
                    break
            return dic

    def encode(dic):
        if dic == None:
            return b''
        msg = b''
        for key in dic.keys():
            if type(dic[key]) == dict: # embedded
                emb = ProtoBufs.encode(dic[key])
                blen = ProtoBufs.envar(len(emb))
                msg = msg + ProtoBufs.envar((int(key)<<3 | 0x02)) + blen + emb
            elif type(dic[key]) == list: # embedded
                for item in dic[key]:
                    emb = ProtoBufs.encode(item)
                    blen = ProtoBufs.envar(len(emb))
                    msg = msg + ProtoBufs.envar((int(key)<<3 | 0x02)) + blen + emb
            elif "var" in key: # uint32
                msg = msg + ProtoBufs.envar((int(key.split(':')[0])<<3 | 0x00)) + ProtoBufs.envar(dic[key])
            elif "f32" in key: # i32
                msg = msg + ProtoBufs.envar((int(key.split(':')[0])<<3 | 0x05)) + struct.pack('<f', dic[key])
            elif "f64" in key: # i64
                msg = msg + ProtoBufs.envar((int(key.split(':')[0])<<3 | 0x01)) + struct.pack('<d', dic[key])
            else: # string/bytes
                blen = ProtoBufs.envar(len(dic[key]))
                msg = msg + ProtoBufs.envar((int(key)<<3 | 0x02)) + blen + dic[key]
        return msg
    
    def devar(msg): # uint32
        var = 0
        idx = 0
        while True:
            var = ((msg[idx]&0x7f) << (idx*7)) | var
            idx = idx + 1
            if not (msg[idx-1] & 0x80):
                break
        return var, idx

    def envar(var): # uint32
        msg = b''
        for i in range(5):
            if var >> 7:
                msg = msg + (var & 0x7f | 0x80).to_bytes()
                var = var >> 7
            else:
                msg = msg + (var & 0x7f | 0x00).to_bytes()
                break
        return msg

def main():
    dic1 = {"1:var": 256, "256:var": 1, "2": {"1": [{"1": b"john", "2:f32": 0.1}, {"1": b"jane", "2:f32": 0.2}]}}
    print(dic1)
    msg1 = ProtoBufs.encode(dic1)
    print(msg1)
    dic2 = ProtoBufs.decode(msg1)
    print(dic2)

if __name__ == "__main__":
    main()
