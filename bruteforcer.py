import os
import asyncio
import aiohttp
import time

writelog = True
stopatfound = True

def get_urls(urls):
  count = 0
  total = len(urls)

  async def fetch(session, url):
    async with session.get(url) as resp:
      found = False
      us = url.split("/")

      if (resp.content_type.startswith("image")):
        found = True
        result = f"Image found at {url}\n"
        print(f"\n\n{result}")

        if (writelog):
          with open("Log.txt", 'a') as log:
            log.write(f"{result}\n")
        
        with open(us[9], 'wb') as file:
          while True:
            chunk = await resp.content.read(10)
            if not chunk:
              break
            file.write(chunk)
        
      nonlocal count
      count += 1

      orig = us[2].split(".",1)[0]
      currenthex = us[3]
      folder1 = us[7]
      folder2 = us[8]
      ext = us[9].rsplit(".",1)[1]

      print(f"Got {count} of {total} : {orig} {currenthex} {folder1} {folder2} {ext}", end="\r")
      if (found):
        return url
      else:
        return

  async def start(urls):
    async with aiohttp.ClientSession() as session:
      futures = [asyncio.create_task(fetch(session, url)) for url in urls]
      htmls = await asyncio.gather(*futures)
      return htmls

  
  responses = asyncio.run(start(urls))
  print()
  if (stopatfound):
    for r in responses:
      if r:
        return r
  
  return
  
def display_time(t):
  if (t < 60):
    return f"{t:.2f} seconds"
  t = t/60
  if (t < 60):
    return f"{t:.2f} minutes"
  t = t/60
  if (t < 24):
    return f"{t:.2f} hours"
  t = t/24
  return f"{t:.2f} days"

def main():
  #The amount urls the program will try to get at one time.
  #I was able to go up to 60000 just fine
  block = 2000

  #check options
  #change and shorten them accoring to pre00 url and preferences

  #orig00 list. Can go up to orig15. Recommended check orig00 first.
  #full list: [f"{n:02d}" for n in range(0,16)]
  origns = ["00"]
  #list of all 4 digit hex numnbers 0000 - ffff. Recommended check all as it is random.
  #full list: [f"{n:04x}" for n in range(0,65536)]
  hexes = [f"{n:04x}" for n in range(28000,35000)]
  #first folder options. Can be any hex number. Recommended check the folder in the pre00 url first.
  #full list: "0123456789abdef"
  folder1 = "c"
  #second folder options. Can be any hex number. Recommended check the folder in the pre00 url first.
  #full list: "0123456789abdef"
  folder2 = "3"
  #file extension options. Usually jpg or png. Recommended check what the artist usually posts as.
  exts = ["png", "jpg"]

  #order of url checking. Last in list will change first.
  order = [origns, folder1, folder2, hexes, exts]

  #Example
  #https://pre00.deviantart.net/e49c/th/pre/f/2013/192/c/3/2600db_by_pascalcampion-d6czloj.jpg

  #Change the url according to your pre00 url.
  #change the numbers according to the order in the list above starting from 0.
  url = "https://orig{0}.deviantart.net/{3}/f/2013/192/{1}/{2}/2600db_by_pascalcampion-d6czloj.{4}"

  print("Building urls")
  urlsall = [url.format(i, j, k, l, m) for i in order[0] for j in order[1] for k in order[2] for l in order[3] for m in order[4]]
  
  urlssplit = [urlsall[i:i+block] for i in range(0,len(urlsall),block)]
  totalblocks = len(urlssplit)

  logtu = f"Total urls: {len(urlsall)}"
  logtb = f"Total blocks: {totalblocks}\n"

  if(writelog):
    with open("Log.txt", 'w') as log:
      log.write(f"{logtu}\n")
      log.write(f"{logtb}\n")

  print(logtu)
  print(logtb)

  start_time = time.time()
  timelist = []
  totaltimelist = [0]
  found = ""
  for i, urls in enumerate(urlssplit, 1):
    while True:
      try:
        print("Staring ClientSession")
        found = get_urls(urls)
        if (found and stopatfound):
          break

        totaltime = time.time() - start_time
        timelist.append(totaltime - totaltimelist[-1])
        totaltimelist.append(totaltime)
        estimate = sum(timelist) / len(timelist) * (totalblocks - i)

        blocklog = f"Finished {i} of {totalblocks} blocks"
        atlog = f"At {urls[-1]}"
        runlog = f"Running for {display_time(totaltime)}: Estimated time remaining {display_time(estimate)}\n"

        if (writelog):
          with open("Log.txt", 'a') as log:
            log.write(blocklog + "\n")
            log.write(atlog + "\n")
            log.write(runlog + "\n")
          
        print(blocklog)
        print(atlog)
        print(runlog)
        break
      except:
        pass

    if (found and stopatfound):
      result = f"An image was found at {found}\nRuntime: {display_time(time.time() - start_time)}"
      print(f"\n{result}")

      if (writelog):
        with open("Log.txt", 'a') as log:
          log.write(f"{result}\n")
      break

main()
input("\nFinished.")