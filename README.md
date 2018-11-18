# UpvoteDownloader
UpvoteDownloader allows you to download all of your upvoted or saved links from reddit.

Supported websites:
<ul>
<li>imgur</li>
<li>reddit-hosted images</li>
<li>direct tumblr links</li>
<li>Everything supported by youtube-dl (see <a href="#youtube-dl">youtube-dl</a> for more)</li>
</ul>

<table>
<tr><td><ul>
<b><p align="center">Contents</p></b>
<li><a href="#Tech">Technology used</a></li>
<li><a href="#Preq">Prerequisites</a></li>
  <ul>
    <li><a href="#reddit">reddit</a></li>
    <li><a href="#imgur">imgur</a></li>
    <li><a href="#PDFwkhtmltopdf">PDFkit & wkhtmltopdf</a></li>
  </ul>
<li><a href="#run">Running</a></li>
<li><a href="#youtube-dl">youtube-dl</a></li>
<li><a href="#goals">Goals</a></li>
</ul></td></tr>
</table>

## <a name="Tech">Technology used</a>

<table>
  <tr>
    <td><a href="https://praw.readthedocs.io/en/stable/">PRAW</a> (6.0.0) </td>
      <td>Python Reddit Api Wrapper</td>
  </tr>
  <tr>
    <td><a href="https://rg3.github.io/youtube-dl/">youtube-dl</a> (2018.08.04) </td>
      <td>YouTube (and so much more) video downloader</td>
  </tr>
  <tr>
    <td><a href="https://github.com/Imgur/imgurpython">imgurpython</a> (1.1.7) </td>
      <td>Python client for the imgur API</td>
  </tr>
  <tr>
    <td><a href="http://pdfkit.org/">PDFkit</a> (0.6.1) </td>
      <td>PDF generation library</td>
  </tr>
  <tr>
    <td><a href="https://wkhtmltopdf.org/">wkhtmltopdf</a> (0.12.5.0) </td>
      <td> Webpage PDF capture tool</td>
  </tr>
</table>

## <a name="Preq">Prerequisites</a>

Only a few steps are needed to get up and running. First open `UserInfo.py` for editing. You can modify the following settings:

<table>
  <tr>
    <td>ignoreImgurAlbums</td>
    <td>Should UpvoteDownloader skip imgur albums?</td>
    <td>    
      <ul>
        <li>Avoids having to create imgur account</li>
        <li>Helps prevent reaching the imgur API request limit (easy to hit if you have a lot of upvoted/saved posts)</li>
      </ul>
     </td>
  </tr>
  <tr>
    <td>mypath</td>
    <td>Specify the download location</td>
    <td>
      <ul>
        <li>Default location is a folder named "DownloadedUpvotes" in the same directory as UpvoteDownloader.py</li>
        <li>imgur albums will be automatically downloaded to their own folder with images in the original order</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>whatToDownload</td>
    <td>Should UpvoteDownloader download upvoted posts, saved posts, or both?</td>
    <td>
      <ul>
        <li>0 = only upvoted</li>
        <li>1 = only saved</li>
        <li>2 = both</li>
      </ul>
      </td>
  </tr>
  <tr>
    <td>ignoreHidden</td>
    <td>Should UpvoteDownloader skip upvoted links that are also hidden?</td>
    <td><ul><li>Useful to avoid downloading links that were upvoted over 6 months ago (archived posts)</li></ul></td>
  </tr>
</table>
    
### <a name="reddit">reddit</a>
In order to get your reddit client ID and secret,
<ol>
  <li>Go to https://www.reddit.com/prefs/apps</li>
  <li>Scroll down and select "are you a developer? create an app..."</li>
    <ol>
      <li>Enter any name you want</li>
      <li>Select "script"</li>
      <li>Set "redirect uri" to something like "http://localhost:8080". Doesn't really matter what you choose as long as it's valid</li>
      <li>Click "create app"
    </ol>
  <li>The code under "personal use script" is your client ID and the secret is your client secret. Enter it into UserInfo.py</li>
</ol>

### <a name="imgur">imgur</a>
In order to get your imgur client ID and secret (necessary to download albums, but not single images),
<ol>
  <li>Create an imgur account if you don't already have one</li>
  <li>Go to https://api.imgur.com/oauth2/addclient</li>
  <ol>
    <li>Enter any name you want</li>
    <li>Select "Anonymous usage without user authorization"</li>
    <li>Set "Authorization callback URL" to something like "http://localhost:8080". Doesn't really matter what you choose as long as it's valid</li>
    <li>Enter a valid email</li>
  </ol>
  <li>Your client ID and secret will be emailed to you. Enter it into UserInfo.py</li>
</ol>

### <a name="PDFwkhtmltopdf">PDFkit & wkhtmltopdf</a>
In order to download text posts as .PDFs, we need to install PDFkit and wkhtmltopdf. Further usage info can be found <a href="https://github.com/JazzCore/python-pdfkit">here</a>.
<ol>
  <li>Install PDFkit <pre>pip install PDFkit</pre> </li>
  <li>Install wkhtmltopdf
    <li>Windows: download binary from https://wkhtmltopdf.org/</li>
    <li>Debian/Ubuntu: <pre>sudo apt-get install wkhtmltopdf</pre></li>
    <li>Mac: <pre>brew install caskroom/cask/wkhtmltopdf</pre></li>
  </li>
  <li>Edit path in UpvoteDownloader.py to match install location of wkhtmltopdf</li>
</ol> 

## <a name="run">Running</a>

After `UserInfo.py` is set, make sure you have a stable internet connection and a reasonable amount of storage space (requirement will vary widely by user). Run `UpvoteDownloader.py` and your files should download. As long as you do not rename anything, UpvoteDownloader will not overwrite already downloaded files, saving bandwidth and time. Links that are unreachable, or unable to be downloaded will be written to `UndownloadableLinks.txt` in the same directory as `UpvoteDownloader.py`.

## <a name="youtube-dl">youtube-dl</a>

<a href="https://rg3.github.io/youtube-dl/">youtube-dl</a> does most of the heavy lifting in this script, and supports a lot more than what's currently in the `ytdlsupport.txt` file. In the interest of removing clutter, I limited the file to only include websites that I personally tested and found to work well. A full list of the sites youtube-dl should support can be found <a href="https://rg3.github.io/youtube-dl/supportedsites.html">here</a>. You can added the domains to `ytdlsupport.txt` to include them in your downloads. Remeber to escape the periods (\\.) and backslashes (\\/) in longer urls.

## <a name="goals">Goals</a>
<ul>
<li>Figure out how to download images from tumblr that don't end in an image file extension</li>
<li>Change UserInfo.py to a cfg or text file</li>
<li>Install youtube-dl and imgurpython for the user instead of them having to do it manully</li>
</ul>
