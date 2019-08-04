import re
import os
import praw
import youtube_dl
import pdfkit
import glob
from UserInfo import *
from urllib import request
from urllib.parse import urlparse
from imgurpython import ImgurClient

ydl_opts = {
	'format': 'bestvideo+bestaudio/best',
	}

path_wkhtmltopdf = r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe' #make sure this is set correctly
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

def filename(string):
    nameFriendlyString=(re.sub(r'[/:]','',string)).split('?')[0]
    return[nameFriendlyString]

def download(url,path):
    try:
        if not os.path.isfile(path):
            r=request.urlopen(url)
            if not (bool(re.search('removed',r.geturl()))):
                request.urlretrieve(url,path)
            elif (bool(re.search('removed',r.geturl()))):
                Unable.write('Image removed!'+' '+toDownload[i].url+' '+' http://www.reddit.com/'+toDownload[i].id+'\n')
                print('Image removed!')
    except Exception as e:
        Unable.write(str(e)+' '+toDownload[i].url+' '+' http://www.reddit.com/'+toDownload[i].id+'\n')
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

if postFirstRun == 1:
    limit=50

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
    print(i,toDownload[i].id,'\t',end='')
    if isinstance(toDownload[i], praw.models.Comment):
        print('Saved comment! Ignoring...')
        continue
    if toDownload[i].hidden==True and ignoreHidden==True:
        print('Post hidden! Ignoring...')
        continue
    if not (bool(glob.glob(mypath+'/'+toDownload[i].id+".*")) or os.path.isdir(mypath+'/' + toDownload[i].id + '/')):
        imgCheck=(bool(re.search('\.png|\.jpg|\.jpeg|\.gif|\.tiff|\.bmp|\.tif|\.jif|\.jfif',toDownload[i].url,re.IGNORECASE)))
        try:
            if(bool(re.search('imgur',toDownload[i].url,re.IGNORECASE))):
                if(bool(re.search('/a/|gallery',toDownload[i].url,re.IGNORECASE))):
                    if ignoreImgurAlbums==False:
                        albumID=(toDownload[i].url.split('/')[4]).split('#')[0]
                        if not (os.path.isdir(mypath+'/' + toDownload[i].id + '/') or (bool(glob.glob(mypath+'/'+toDownload[i].id+".*")))):
                            items=client.get_album_images(albumID)
                            if len(items) > 1:
                                album_path=mypath+'/' + toDownload[i].id + '/'
                                if not os.path.isdir(album_path):
                                    os.makedirs(album_path)
                                    order=0
                                    for item in items:
                                        downLink=(item.mp4 if hasattr(item,"mp4") else item.link)
                                        download(downLink,album_path+str(order)+' '+''.join(filename(downLink)))
                                        order+=1 
                                print('imgur album: ' + toDownload[i].id)
                            else:
                                album_path=mypath+'/'
                                for item in items:
                                    downLink=(item.mp4 if hasattr(item,"mp4") else item.link)
                                    download(downLink,album_path+toDownload[i].id+'.'+(urlparse(downLink).path).split('.')[-1])
                                print('1 image imgur album')
                    else:
                        print('Ignoring imgur albums')
                elif(bool(re.search('\.gifv',toDownload[i].url,re.IGNORECASE))):
                    base=os.getcwd()
                    os.chdir(mypath)
                    if not os.path.isfile(toDownload[i].id+'.mp4'):
                        try:
                            ydl_opts['outtmpl']=toDownload[i].id+'.mp4'
                            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                                ydl.download([toDownload[i].url])
                        except Exception as e:
                            Unable.write(str(e)+' '+toDownload[i].url+' http://www.reddit.com/'+toDownload[i].id+'\n')
                    os.chdir(base)
                    print('imgur gifv: ' + toDownload[i].id)
                else:
                    imgurCode=(urlparse(toDownload[i].url).path).split('/')[-1].split('.')[0]
                    image=client.get_image(imgurCode)
                    if not(imgCheck):
                        ext=(".mp4" if hasattr(image,"mp4") else "."+(urlparse(image.link).path).split('.')[-1])
                        toDownload[i].url="https://i.imgur.com/" + imgurCode + ext
                        imgur_path=mypath+'/'+toDownload[i].id+'.'+(urlparse(toDownload[i].url).path).split('.')[-1]
                        download(toDownload[i].url,imgur_path)
                        print('Basic imgur file, missing extension: ' + toDownload[i].id)
                    if (imgCheck):
                        imgur_path=mypath+'/'+''.join(filename(toDownload[i].id))+'.'+(urlparse(image.link).path).split('.')[-1]
                        download(toDownload[i].url,imgur_path)
                        print('Basic imgur file ' + toDownload[i].id)
            elif(bool(re.search('tumblr',toDownload[i].url,re.IGNORECASE))):
                if (imgCheck):
                    tumblr_path=mypath+'/'+toDownload[i].id+'.'+(urlparse(toDownload[i].url).path).split('.')[-1]
                    download(toDownload[i].url,tumblr_path)
                else: 
                    Unable.write('Working on it... '+toDownload[i].url+' http://www.reddit.com/'+toDownload[i].id+'\n')
                print('Basic tumblr file: ' + toDownload[i].id)  
            elif(bool(re.search('i\.redd\.it|i\.reddituploads\.com',toDownload[i].url,re.IGNORECASE))):
                if not(imgCheck):
                    toDownload[i].url+='.gif'
                reddit_path=mypath+'/'+toDownload[i].id+'.'+(urlparse(toDownload[i].url).path).split('.')[-1]
                download(toDownload[i].url,reddit_path)
                print('Reddit hosted, possibly defaulted to .gif ' + toDownload[i].id)
            else:
                if(bool(re.search('gfycat\.com',toDownload[i].url,re.IGNORECASE))):
                    base=os.getcwd()
                    os.chdir(mypath)
                    if not os.path.isfile(toDownload[i].id+'.mp4'):
                        try:
                            ydl_opts['outtmpl']=toDownload[i].id+'.mp4'
                            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                                ydl.download([toDownload[i].url])
                            print('youtube-dl supported!' + toDownload[i].id)
                        except Exception as e:
                            Unable.write(str(e)+' '+toDownload[i].url+' http://www.reddit.com/'+toDownload[i].id+'\n')
                    else:
                        print('YTDL supported: ' + toDownload[i].id)
                    os.chdir(base)
                elif (imgCheck):
                    unknown_path=mypath+'/'+toDownload[i].id+'.'+(urlparse(toDownload[i].url).path).split('.')[-1]
                    download(toDownload[i].url,unknown_path)
                    print('Unknown image host!',end='')
                elif(bool(re.search('|'.join(lines),toDownload[i].url,re.IGNORECASE))):
                    base=os.getcwd()
                    os.chdir(mypath)
                    if not os.path.isfile(toDownload[i].id+'.mp4'):
                        try:
                            ydl_opts['outtmpl']=toDownload[i].id+'.mp4'
                            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                                ydl.download([toDownload[i].url])
                            print('youtube-dl supported!' + toDownload[i].id)
                        except Exception as e:
                            Unable.write(str(e)+' '+toDownload[i].url+' http://www.reddit.com/'+toDownload[i].id+'\n')
                    else:
                        print('ytdl exists! ' + toDownload[i].id)
                    os.chdir(base)
                elif bool(toDownload[i].is_self):
                    if not os.path.isfile(mypath+'/'+toDownload[i].id+'.pdf'):
                        if not bool(toDownload[i].over_18):
                            pdfkit.from_url(toDownload[i].url, mypath+'/'+toDownload[i].id+'.pdf',configuration=config)
                else:
                    Unable.write('Not Supported! '+toDownload[i].url+' http://www.reddit.com/'+toDownload[i].id+'\n')
                    print('Unsupported host: ' + toDownload[i].url + toDownload[i].id)
        except Exception as e:
            print('Error retrieving link @' + toDownload[i].url)
            Unable.write(str(e)+' '+toDownload[i].url+' http://www.reddit.com/'+toDownload[i].id+'\n')
    else:
        print('Exists',end='')
    print('\n',end='')
Unable.close()
input('\nPress enter to exit...')
