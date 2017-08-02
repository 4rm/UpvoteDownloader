import re
import os
import praw
import youtube_dl
from UserInfo import *
from urllib import request
from imgurpython import ImgurClient

def filename(string):
    nameFriendlyString=(re.sub(r'[/:]','',string)).split('?')[0]
    return[nameFriendlyString]

def download(url,path):
    try:
        if not os.path.isfile(path):
            request.urlretrieve(url,path)
    except Exception as e:
        Unable.write(str(e)+' '+toDownload[i].url+' '+'\n')
        print('Error! from ',end='')
    return[]

with open('ytdlsupport.txt') as f:
    lines = [line.rstrip('\n') for line in f]

if not os.path.isdir(mypath):
    print('Creating folder...')
    os.makedirs(mypath)

print('Signing into reddit...')
reddit = praw.Reddit(client_id=reddit_client_id,
                     client_secret=reddit_client_secret,
                     user_agent='Download upvoted and saved posts',
                     username=username,
                     password=password)

if ignoreImgurAlbums==False:
    print('Signing into imgur...')
    client = ImgurClient(client_id=imgur_client_id,
                         client_secret=imgur_client_secret)

print('Creating error log...')
Unable=open('UndownloadableLinks.txt','w+')

if whatToDownload==0:
    print('Getting list of upvoted links...')
    toDownload=list(reddit.redditor(username).upvoted(limit=limit))

elif whatToDownload==1:
    print('Getting list of saved links...')
    toDownload=list(reddit.redditor(username).saved(limit=limit))

elif whatToDownload==2:
    print('Getting upvoted and saved links...')
    toDownload=list(reddit.redditor(username).upvoted(limit=limit))+list(reddit.redditor(username).saved(limit=limit))

for i in range(0,len(toDownload)):
    print(i,' ',end='')
    imgCheck=(bool(re.search('\.png|\.jpg|\.jpeg|\.gif',toDownload[i].url,re.IGNORECASE)))
    if toDownload[i].hidden==True and ignoreHidden==True:
        print('Post hidden! Ignoring...')
        continue
    if(bool(re.search('imgur',toDownload[i].url,re.IGNORECASE))):
        if(bool(re.search('/a/',toDownload[i].url,re.IGNORECASE))):
            if ignoreImgurAlbums==False:
                albumID=(toDownload[i].url.split('/')[4]).split('#')[0]
                album_path=mypath+'/' + albumID + '/'
                items=client.get_album_images(albumID)
                if not os.path.isdir(album_path):
                    os.makedirs(album_path)
                    order=0
                    for item in items:            
                        download(item.link,album_path+str(order)+' '+''.join(filename(item.link)))
                        order+=1 
                print('imgur album!')
            else:
                print('Ignoring imgur albums!')
            
        elif(bool(re.search('\.gifv',toDownload[i].url,re.IGNORECASE))):
            base=os.getcwd()
            os.chdir(mypath)
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([toDownload[i].url])
            except Exception as e:
                Unable.write(str(e)+' '+toDownload[i].url+' '+'\n')
            os.chdir(base)
            print('imgur gifv!')
        else:
            if not(imgCheck):
                toDownload[i].url+='.gif'
            imgur_path=mypath+'/'+''.join(filename(toDownload[i].url))
            download(toDownload[i].url,imgur_path)
            print('imgur PNG, GIF, or JPG!')
        
    elif(bool(re.search('tumblr',toDownload[i].url,re.IGNORECASE))):
        if (imgCheck):
            tumblr_path=mypath+'/'+''.join(filename(toDownload[i].url))
            download(toDownload[i].url,tumblr_path)
        else: 
            Unable.write('Working on it... '+toDownload[i].url+'\n')
        print('tumblr!')
        
    elif(bool(re.search('i\.redd\.it|i\.reddituploads\.com',toDownload[i].url,re.IGNORECASE))):
        if not(imgCheck):
            toDownload[i].url+='.gif'
        reddit_path=mypath+'/'+''.join(filename((re.sub(r'[?]','',toDownload[i].url))))
        download(toDownload[i].url,reddit_path)
        print('reddit hosted!')

    elif(bool(re.search('|'.join(lines),toDownload[i].url,re.IGNORECASE))):
        base=os.getcwd()
        os.chdir(mypath)
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([toDownload[i].url])
        except Exception as e:
            Unable.write(str(e)+' '+toDownload[i].url+' '+'\n')
        os.chdir(base)
        print('youtube-dl supported!')
        
    else:
        if (imgCheck):
            unknown_path=mypath+'/'+''.join(filename(toDownload[i].url))
            download(toDownload[i].url,unknown_path)
            print('unknown image host!')
        else:
            Unable.write('Not Supported! '+toDownload[i].url+'\n')
            print('unknown',toDownload[i].url)

Unable.close()
input('\nPress enter to exit...')
