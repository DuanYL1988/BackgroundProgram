import requests

headers = {
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
}
hostUrl = "https://www.pearvideo.com/"
inputUrl = "video_1797546"
realUrl = "videoStatus.jsp?contId=[param1]&mrd=0.5893905789610572"

def getDataWhenRefer(hostUrl, inputUrl ,realUrl):
  url = hostUrl + inputUrl
  videoId = inputUrl.split("_")[1]
  realUrl = hostUrl + realUrl.replace("[param1]",videoId)
  headers["Referer"] = url
  resp = requests.get(realUrl, headers = headers)
  data = resp.json()
  videoSrc = data["videoInfo"]["videos"]["srcUrl"]
  # https://video.pearvideo.com/mp4/short/20241209/1734105548646-16041964-hd.mp4
  # https://video.pearvideo.com/mp4/short/20241209/cont-1797546-16041964-hd.mp4
  videoSrc = videoSrc.replace(data["systemTime"],f"cont-{videoId}")
  print(videoSrc)

getDataWhenRefer(hostUrl, inputUrl ,realUrl)