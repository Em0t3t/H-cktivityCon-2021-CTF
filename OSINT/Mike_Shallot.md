## Mike Shallot 411 points - 90 solves
----------
### Description
"Mike Shallot is one shady fella. We are aware of him trying to share some specific intel, but hide it amongst the corners and crevices of internet. Can you find his secret? "

This problem, we need to find the person with these data and hint.

* Note it: <strong>shady fella, corners and crevices of internet</strong>

### First Search 

"Mike Shallot" looks like a full name of someone, after searching on Google,.. you can't find any information. So, try to use it as an username "mikeshallot".

Try to check the social media for information. 

* Use <strong>sherlock</strong> tool: 
```
python3 sherlock mikeshallot
```
Result: <br>

![image](https://media.discordapp.net/attachments/621710864004677632/888832165993914408/unknown.png?width=720&height=134)

### Check in turn

Check each item, then I found something suspicious in <em>https://pastebin.com/u/mikeshallot</em>:<br>

![image](https://media.discordapp.net/attachments/621710864004677632/889346030489960468/unknown.png?width=720&height=159)


Choose Shallot's Summons -> It shows: <br>

![image](https://media.discordapp.net/attachments/621710864004677632/889346694301507604/unknown.png?width=720&height=232)

We got: 
```
strongerw2ise74v3duebgsvug4mehyhlpa7f6kfwnas7zofs3kov7yd

pduplowzp/nndw79
```
It looks like more information and the path of something. 

* Note: <strong>in the shadow</strong>, and <strong>shady, corners of internet</strong> at first decription => Find it on darkweb.

### Access Dark Web

Use <strong>Tor browser</strong> to access Dark web, search for "stronger...", we have this url: 
```
http://strongerw2ise74v3duebgsvug4mehyhlpa7f6kfwnas7zofs3kov7yd.onion
```


Paste "pduplowzp/nndw79" to the rest of path in <strong>pastebin</strong> description: 
```
http://strongerw2ise74v3duebgsvug4mehyhlpa7f6kfwnas7zofs3kov7yd.onion/pduplowzp/nndw79
```

Here we got the flag: <br>

![image](https://media.discordapp.net/attachments/621710864004677632/888832468092850186/unknown.png?width=720&height=140)

