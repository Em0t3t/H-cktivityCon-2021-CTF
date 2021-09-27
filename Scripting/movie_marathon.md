# Movie Marathon - Hard

## Summary 

The problem is to give you the name of a movie with the year of production, your task is to find 5 actors playing in that movie!

## Solve


+ To solve this problem, I went online to search for APIs that might be related to movies and luckily I found a youtube page that shows how to get data through the API. That is [movidb](https://www.youtube.com/watch?v=Gf45f5cW6c4)


+ And after a while of searching, I found 2 important APIs to solve this problem: The first is the API to find the movie's ID through the movie name and the second is to find the actor list through the movie ID.

+ And when you find the necessary APIs, your only job is to call the API, process the data, and interact with the server to get the flag.

+ Here is the source code to get the flag that I have coded

```py
#API key: 1a065e36b05557397b931ef5027b85fb
import urllib.request,json 
from pwn import *
r = remote("challenge.ctf.games",31260)
 
def get_actor_from_movie_id(movie_id):
#https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=1a065e36b05557397b931ef5027b85fb&language=en-US    
    url = "https://api.themoviedb.org/3/movie/" + str(movie_id)  + "/credits?api_key=1a065e36b05557397b931ef5027b85fb&language=en-US"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    _list = data["cast"]
    answer=[]
    for _dict in _list:
        answer.append(_dict["name"])
    # return data
    return answer
def get_movie_id_from_movie_name(ten_phim,ngay_thang,ten_phim_full):
# https://api.themoviedb.org/3/search/movie?api_key=1a065e36b05557397b931ef5027b85fb&query=Mind+Blown
    url = "https://api.themoviedb.org/3/search/movie?api_key=1a065e36b05557397b931ef5027b85fb&query="
    url += ten_phim
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    _list = data["results"]
    for _dict in _list:
        if(_dict["title"]==ten_phim_full and _dict["release_date"]==ngay_thang):
            return _dict["id"]
    # return data
def solve(source):
    t = source.split("(") 
    ### SOLVE DAY
    day = t[1]
    res_day=""
    for _ in day:
        if(_!=')'):
            res_day+=_
    print(res_day)
    
    ### SOLVE NAME
    name = t[0].split(" ")
    name_arr=[]
    res_full=""
    for _ in name:
        if _!="":
            name_arr.append(_)
    # print(name_arr)
    # print(len(name_arr))
    res=""
    for i in range(0,len(name_arr)):
        
        if(i<len(name_arr)-1):
            # print("test",i)
            res=res+name_arr[i] + "+" 
            res_full= res_full + name_arr[i] + " "
        else:
            res=res+name_arr[i]
            res_full = res_full + name_arr[i]
    print(res)
    # print(t)
    return res,res_day,res_full
def xuly(source):
    ans = ""
    for i in range(0,5):
        if(i!=4):
            ans = ans + source[i] + "; "
        else:
            ans = ans + source[i]
    return ans
def sol(source):
    # ok1 = get_actor_from_movie_id()
    #print(ok1)
    ten_phim,ngaythang,ten_phim_full = solve(source)
    # print("{0}--{1}--{2}".format(ten_phim,ngaythang,ten_phim_full))
    movie_id = get_movie_id_from_movie_name(ten_phim,ngaythang,ten_phim_full)
    res = get_actor_from_movie_id(movie_id)
    last_answer = xuly(res)
    return last_answer
def start(source):
    #source = "Mind Blown (2016-01-01)"
    return sol(source)
def _interactive():
	r.recvline()
	r.recvline()
	r.recvline()
	r.recvline()
	r.recvline()
	r.recvline()
	r.recvline()
	r.recvline()
	r.recvline()
	r.recvline()
	r.recvline()
	dem=0
	for i in range(0,30):
		print("----",dem+1)
		dem+=1
		u = r.recvline()
		a = u.decode('utf-8')
		source=""
		for i in range(2,len(a)-1):
			source+=a[i]
		print("{0}--{1}".format(source,len(source)))
		gui_len = start(source)
		print(gui_len)
		r.sendline(gui_len)
		u = r.recvline()
		print(u)
	u = r.recvline()
	print(u)
	u = r.recvline()
	print(u)
	u = r.recvline()
	print(u)
_interactive()
r.interactive()

# test_source = "The Avengers (2012-04-25)"
#solve(test_source)
# sol(test_source)
```

## Flag

~~~
flag{f404a3c065a0bff9da8aedebd40d415b}
~~~

