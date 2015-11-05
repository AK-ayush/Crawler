################################################################################
# Javascript enabled web spider for extracting the the content of hidden links #
#  Ayush Kumar  March 31, 2015                                                 #
################################################################################


# libraries used
import os,sys
import time
import re
import urllib
import urllib2
#from proxy import urllib2
import urlparse
from bs4 import BeautifulSoup
import mechanize
from urlparse import urlsplit,urlparse

#perticuler function for download the files for this program which is platform independent
def downloader(url):
    try:
        #extracting the filename from the path
        file_name = urllib.unquote(url).decode('utf8').split('/')[-1]

        #opening the url to write the content in as it is format in the file
        u = urllib2.urlopen(url)

        #open the file for writing into the file
        f = open(file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])

        #display the download size of the files
        print "Downloading: %s Bytes: %s" % (file_name, file_size)

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)

            #getting the current status of ongoing download
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status,

        f.close()
    except:
        pass


#scrapper function to extract the links from href links of page 
def scraper(baseUrl, data, urlList):

    print 'working.........'
    dwnld = []   #desired links to download the pdfs

    #extracting the prefix for the improper/relative links
    parts = urlsplit(baseUrl)
    base_url =  "{0.scheme}://{0.netloc}".format(parts)
    path = baseUrl[:baseUrl.rfind('/')+1] if '/' in parts.path else baseUrl

    #apply the beautiful soup on the html data provided to extract the links 
    soup = BeautifulSoup(data)
    divs = soup.findAll('div',attrs={'class':'news_content_mid'})
    for div in divs:
        for tag in div.findAll('a'):
            link = tag.attrs["href"] if "href" in tag.attrs else ''
            #print link         #for debuging

            #filter the type of links such as javascripts onclick functions  
            if link and not 'javascript' in link :

                #convert the relative links into absolute links
                if link.startswith('/'):
                    link = base_url + link
                elif not link.startswith('http'):
                    link = path + link

                #parse  the link and modify the content of the links
                #and follow this convention on each and every links
                #so that decrease the possibility of duplication of href
                obj = urlparse(link)
                protocol = obj.scheme
                hostname = obj.netloc
                hostname = hostname.lower()
                protocol = protocol.lower()
                fragment = ''           #no fragment
                params = ''             #no params
                query = ''              #no query
                location = obj.path
                #print location     #for debuging

                #modifying the path part of the link
                location = location.replace('/./','/')
                while  '../' in location:
                    # convert the path having a/b/../c in to  a/c 
                    regex = '/([a-zA-Z0-9_ -]+)?/\.\./'
                    pattern = re.compile(regex)
                    occur = re.search(pattern,location)
                    if occur:
                        occur = format(occur.group(0))
                        location = location.replace(occur,'/')
                location = location.replace('/ /','/')

                #extract hte extension from the link
                ext = os.path.splitext(location)[1]

                #check for encoding 
                if not '%' in location:
                    en_location = urllib2.quote(location.encode('utf8'))

                #combine the parts and forming the absolute the link
                link_new = protocol +'://'+ hostname + en_location

                #putting the required links into the List
                if link_new.startswith('http') and not link_new in urlList :
                    
                    #check if the domain is same as the original url
                    link_d = urlsplit(link_new)
                    url_d =  urlsplit(baseUrl)
                    if link_d.netloc == url_d.netloc:
                        urlList.append(link_new)
                    else:
                        pass
        
    return 



#declaration of the function that find the pdf links of the web page
def extensionFinder(baseUrl, urlList, Extension):

    #since urlList contails unique urls
    print 'working............'
    #print 'url'    #for debuging

    #print urlList     #for debuging
    

    #extracting the prefix for the improper/relative links
    parts = urlsplit(baseUrl)
    base_url =  "{0.scheme}://{0.netloc}".format(parts)
    path = baseUrl[:baseUrl.rfind('/')+1] if '/' in parts.path else baseUrl

    ctr=0       #to print the warning
    for url in urlList:
        #print url         for debuging  
        
        #getting the html content of the urls of the urlList 
        try:
            htmlText = urllib2.urlopen(url).read()
            FromRaw = lambda r: r if isinstance(r, unicode) else r.decode('utf-8', 'ignore')
            htmlText = FromRaw(htmlText)
            soup = BeautifulSoup(htmlText)
        except:
            continue

        #with the help of beautiful soup extract hte links
        
        for tag in soup.findAll('a'):

            link = tag.attrs["href"] if "href" in tag.attrs else ''
            #print link     #for debuging


            #filter the type of links such as javascripts onclick functions
            if link and not 'javascript' in link:

                #convert the relative links into absolute links
                if link.startswith('/'):
                    link = base_url + link
                elif not link.startswith('http'):
                    link = path + link


                #parse  the link and modify the content of the links
                #and follow this convention on each and every links
                #so that decrease the possibility of duplication of href
                obj = urlparse(link)
                protocol = obj.scheme
                hostname = obj.netloc
                hostname = hostname.lower()
                protocol = protocol.lower()
                fragment = ''           #no fragment
                params = ''             #no params
                query = ''              #no query
                location = obj.path

                #no further scrapping of the pages
                if not '.asp' in location:

                    #extract hte extension from the link
                    ext = os.path.splitext(location)[1]

                    #check for encoding 
                    if not '%' in location:
                        en_location = urllib2.quote(location.encode('utf8'))

                     #combine the parts and forming the absolute the link
                    link_new = protocol +'://'+ hostname + en_location

    
                    #time.sleep()
                    if  ext == Extension:
                        if ctr ==0:
                            folder = Extension[1:]
                            folder = folder.upper()+'s'
                            pwd = os.getcwd()
                            path = os.path.join(pwd, folder)
                            if not os.path.exists(path):
                                os.mkdir(path)
                            os.chdir(path)
                        ctr +=1
                        print '*********************'
                        #print link_new           #for debuging
                        #os.system(' wget --tries=2 '+link_new)
                        downloader(link_new)
                        print str(ctr) + '---files have downloaded'
    if ctr==0:
        print 'not found!'


    

#definition of the function which ressolve the paginated links issue
def eventTaget(url, pageNo, urlList, Extension):
    print 'working......'
    br = mechanize.Browser()
    br.set_handle_robots(False)
    content = br.open(url)

    #iterate through the number of pages given
    for i in range(pageNo):

        #selecting the from whose id is 'aspnetForm'
        formcount =0
        for frm in br.forms():
            if str(frm.attrs["id"])=="aspnetForm":
                break
            formcount=formcount+1
        br.select_form(nr = formcount)

        #make the from editable
        br.form.set_all_readonly(False)

        data = content.read()
        #print data     #for debuging
        scraper(url, data, urlList);
        if i == (pageNo-1):
            #print urlList ,'list'      #for debuging
            extensionFinder(url, urlList, Extension);

        #regex to find the __EVENTTARGET value from the function
        regex = 'javascript:__doPostBack((.*?),(.*?))">Next</a>'
        pattern = re.compile(regex)
        mnext = re.search(pattern, data)

        nextValue = mnext.group(2)
        nextValue = nextValue.replace('(','')
        nextValue = nextValue.replace("'",'')
        #print nextValue, 'nextValue'       #for debuging

        #set the value of hidden elements whose ids are known
        br.form.new_control('hidden', '__EVENTTARGET', {'value':''+nextValue+''})
        br.form.new_control('hidden','__EVENTARGUMENT', {'value':''})
        br.form.new_control('hidden', '__LASTFOCUS', {'value':''})
        br.form.fixup()

        #before submiting the from disable all the control
        for control in br.form.controls[:]:
            if control.type in ['submit', 'image', 'checkbox']:
                    br.form.controls.remove(control)

        #Now submit the from 
        res = br.submit()
        time.sleep(1)		#sleep time to load the content
        content = res
#end of the eventTarget function





#main function of the program
def main(url , pageNo, Extension):
    urlList=[]          #list for containing the urls which contains the desired extension links
    print 'working...'

    #calling the function for scrapping the dynamic page
    eventTaget(url, pageNo , urlList, Extension);


if __name__ =="__main__":
    #print sys.argv  #for debuging
    
    main(str(sys.argv[1]), int(sys.argv[2]), str(sys.argv[3]))
