reddit_client_id='xxx'
reddit_client_secret='xxx'
username='xxx'
password='xxx'
limit=None

##Needed to download albums
imgur_client_id='xxx'
imgur_client_secret = 'xxx'

##Ignore imgur album requests (imgur API runs out quick)
ignoreImgurAlbums=1

ydl_opts = {
    'restrictfilenames': True,
    'nooverwrites': True,
    'format': 'bestvideo+bestaudio/best',
    'quiet': True
}

##Folder to save downloads to
mypath='DownloadedUpvotes'

##(0 = Only Upvoted Links, 1 = Only Saved Links, 2 = Both)
whatToDownload=2

##(0 = attempt to download hidden links, 1 = ignore hidden links)
ignoreHidden=1
