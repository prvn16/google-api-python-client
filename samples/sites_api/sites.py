#!/usr/bin/python
#
# Copyright 2009 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


__author__ = 'e.bidelman (Eric Bidelman)'

import mimetypes
import os.path
import pprint

import gdata.sample_util
import gdata.sites.client
import gdata.sites.data
import html
from bs4 import BeautifulSoup

from string import Template


import sys
import os.path
sys.path.insert(0, "./samples")

from samples.sites_api.googleTemplates import *
from samples.sites_api.googleTemplates import param0
import googleTemplates

import re



SOURCE_APP_NAME = 'googleInc-GoogleSitesAPIPythonLibSample-v1.1'
MAIN_MENU = ['1)  List site content',
             '2)  List recent activity',
             '3)  List revision history',
             '4)  Create webpage',
             '5)  Create web attachment',
             '6)  Upload attachment',
             '7)  Download attachment',
             '8)  Delete item',
             '9)  List sites',
             '10)  Create a new site',
             "11) List site's sharing permissions",
             '12) Change settings',
             '13) Exit']
SETTINGS_MENU = ['1) Change current site.',
                 '2) Change domain.']

def publishWeb (site= "sumpurn-en",domain= "sumpurn.com",debug = True) :
    f = open('googleTemplates.py', 'r')  # Past stored templates

    sample = SitesManipulator(site, domain, debug=debug)

    # Create the following to start the web page on google sites
    _webpage = '''
    <div>
    <table cellspacing="0" class="sites-layout-name-one-column sites-layout-hbox">
     <tbody>
       <tr><td class="sites-layout-tile sites-tile-name-content-1">
           </td>
       </tr>
     </tbody>
    </table>
    </div>
    '''

    webpage = BeautifulSoup(_webpage)
    tdwebpage = webpage.div.table.tbody.tr.td

    for count in range(10) :
        _myTemplate = eval("Template" + str(count))
        _myparam = eval("param"+str(count))
        _newhtml = BeautifulSoup(_myTemplate)
        ___template = Template(_newhtml.prettify()).safe_substitute(_myparam)

        newheading = webpage.new_tag("h3")
        newheading.append("Substituted Template:")
        tdwebpage.append(newheading)
        newtag = webpage.new_tag("div")
        newtag.append(BeautifulSoup(___template))


        #tdwebpage.append(newtag)
        if count not in [2, 10]:
            tdwebpage.append(newtag)


    path = '/templates'

    print 'Fetching page by its path: ' + path
    uri = '%s?path=%s' % (sample.client.MakeContentFeedUri(), path)
    feed = sample.client.GetContentFeed(uri=uri)
    old_entry = feed.entry[0]
    # Update the listpage's title, html content, and first column's name.
    old_entry.title.text = 'Updated Title'
    # old_entry.content.html = str(mypage)+webpage.prettify().encode("utf-8")
    old_entry.content.html = webpage.encode("utf8")
    # old_entry.data.column[0].name = 'Owner'

    # You can also change the page's webspace page name on an update.
    # old_entry.page_name = 'new-page-path'

    updated_entry = sample.client.Update(old_entry)
    print 'List page updated!'


def runSample () :
  site = "sumpurn-en"
  domain = "sumpurn.com"
  debug = True

  sample = SitesManipulator(site, domain, debug=debug)
  sample.Run() # On return it has read a page and built the templates from the page

  #parser.saveSite("siteTemplates.json")
  mytemplates = sample.mytemplates
  sub_mytemplates = sample.sub_mytemplates

  f = open('googleTemplates.py', 'r')  # Past stored templates
  _f = open('_googleTemplates.py', 'w') # Newly generated templates

  #Create the following to start the web page on google sites
  _webpage = '''
  <div>
  <table cellspacing="0" class="sites-layout-name-one-column sites-layout-hbox">
   <tbody>
     <tr><td class="sites-layout-tile sites-tile-name-content-1">
         </td>
     </tr>
   </tbody>
  </table>
  </div>
  '''

  webpage = BeautifulSoup(_webpage)
  tdwebpage = webpage.div.table.tbody.tr.td

  _img = webpage.new_tag("img",src="https://www.google.co.jp/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png")

  tdwebpage.append(_img)

  count = 0
  for ii in sorted(mytemplates.keys()):
    print(mytemplates[ii])
    if count <= 15:
        print("count=",count)

        myhtml = str(mytemplates[ii]).replace("html:", "")  # for  BeautifulSoup
        myparams = sample.mytemplatesParams[ii]
        soup = BeautifulSoup(myhtml, 'html.parser')

        _prettyHTML = soup.prettify()
        prettyHTML = _prettyHTML.encode('utf8')

        sub_myhtml = str(sub_mytemplates[ii]).replace("html:", "")  # for  BeautifulSoup
        sub_soup = BeautifulSoup(sub_myhtml, 'html.parser')

        _sub_prettyHTML = sub_soup.prettify()
        sub_prettyHTML = _sub_prettyHTML.encode("utf-8")

        _fmyparams=pprint.PrettyPrinter(indent=4,width=20).pformat(myparams)
        _fmyhtml = pprint.PrettyPrinter(indent=4, width=20).pformat(myhtml)

        _f.write("# This Python file uses the following encoding: utf-8\n")
        _f.write("param"+str(count) + " = " + _fmyparams +"\n\n")
        _f.write("_template" + str(count) + "= '''\n" + _fmyhtml + "\n'''\n\n")
        _f.write("template"+str(count) + "= '''\n"+prettyHTML+"\n'''\n\n")
        _f.write("Template" + str(count) + "= '''\n" + sub_prettyHTML + "\n'''\n\n")

        if 2 > 1 :
            _mytemplate = eval("template"+str(count))
            _newtag = BeautifulSoup(_mytemplate)

            _myTemplate = eval("Template" + str(count))
            _newhtml = BeautifulSoup(_myTemplate)

            newheading = webpage.new_tag("h3")
            newheading.append("Params:")
            tdwebpage.append(newheading)
            newpre = webpage.new_tag("pre")
            newpre.append(_fmyparams)
            tdwebpage.append(newpre)

            newheading = webpage.new_tag("h3")
            newheading.append("Template:")
            tdwebpage.append(newheading)
            newpre = webpage.new_tag("pre")
            newpre.append(prettyHTML)
            tdwebpage.append(newpre)

            newheading = webpage.new_tag("h3")
            newheading.append("Substituted Template:")
            tdwebpage.append(newheading)
            newpre = webpage.new_tag("pre")
            newpre.append(sub_prettyHTML)
            tdwebpage.append(newpre)


            tdwebpage.append(_newtag) # Add the html code for the template

            newheading = webpage.new_tag("h3")
            newheading.append("Substituted Template-2:")
            tdwebpage.append(newheading)
            newpre = webpage.new_tag("pre")
            ___template = Template(_newhtml.prettify()).safe_substitute(myparams)
            newpre.append(___template)
            tdwebpage.append(newpre)

            #tdwebpage.append(BeautifulSoup(___template))

            newheading = webpage.new_tag("h3")
            newheading.append("Substituted Template-2 for html:")
            tdwebpage.append(newheading)
            newpre = webpage.new_tag("div")
            newpre.append(BeautifulSoup(___template))
        if count not in [2,10]:
            tdwebpage.append(newpre)

            #tdwebpage.append(___template)
        else :
            _newtag = webpage.new_tag("h3")
            _newtag.append("SKIPPED " + str(count))
            tdwebpage.append(_newtag)
    else :
        print("Skipped Count",count)

    count += 1

  f.close()
  _f.close()

  path = '/mytemplates2'



  print 'Fetching page by its path: ' + path
  uri = '%s?path=%s' % (sample.client.MakeContentFeedUri(), path)
  feed = sample.client.GetContentFeed(uri=uri)
  old_entry = feed.entry[0]
  # Update the listpage's title, html content, and first column's name.
  old_entry.title.text = 'Updated Title'
  #old_entry.content.html = str(mypage)+webpage.prettify().encode("utf-8")
  old_entry.content.html = str(webpage)
  #old_entry.data.column[0].name = 'Owner'

  # You can also change the page's webspace page name on an update.
  # old_entry.page_name = 'new-page-path'

  updated_entry = sample.client.Update(old_entry)
  print 'List page updated!'



#==========================================================================

class SitesManipulator(object):
  """Wrapper around the Sites API functionality."""

  def __init__(self, site_name=None, site_domain=None, debug=False):
    self.mytemplates = {}
    self.sub_mytemplates =  {}
    self.mytemplatesParams = {}

    if site_domain is None:
      site_domain = self.PromptDomain()

    if site_name is None:
      site_name = self.PromptSiteName()

    mimetypes.init()
    SCOPE = 'https://sites.google.com/feeds/'

    # Get authenticated token to access sites API
    auth2token = getAuth2Token(SCOPE)

    # Create a gdata client
    client = gdata.sites.client.SitesClient(source='sites-test',
                                        site='test1',
                                        domain='sumpurn.com',
                                        auth_token=auth2token)



    self.client = client
    self.client.http_client.debug = debug

    try:
        # Authorize it

        auth2token.authorize(client)
    except gdata.client.BadAuthentication:
      exit('Invalid user credentials given.')
    except gdata.client.Error:
      exit('Login Error')

  def PrintMainMenu(self):
    """Displays a menu of options for the user to choose from."""
    print '\nSites API Sample'
    print '================================'
    print '\n'.join(MAIN_MENU)
    print '================================\n'

  def PrintSettingsMenu(self):
    """Displays a menu of settings for the user change."""
    print '\nSites API Sample > Settings'
    print '================================'
    print '\n'.join(SETTINGS_MENU)
    print '================================\n'

  def GetMenuChoice(self, menu):
    """Retrieves the menu selection from the user.

    Args:
      menu: list The menu to get a selection from.

    Returns:
      The integer of the menu item chosen by the user.
    """
    max_choice = len(menu)
    while True:
      user_input = raw_input(': ')

      try:
        num = int(user_input)
      except ValueError:
        continue

      if num <= max_choice and num > 0:
        return num

  def PromptSiteName(self):
    site_name = ''
    while not site_name:
      site_name = raw_input('site name: ')
      if not site_name:
        print 'Please enter the name of your Google Site.'
    return site_name

  def PromptDomain(self):
    return raw_input(('If your Site is hosted on a Google Apps domain, '
                      'enter it (e.g. example.com): ')) or 'site'

  def GetChoiceSelection(self, feed, message):
    for i, entry in enumerate(feed.entry):
      print '%d.) %s' % (i + 1, entry.title.text)
    choice = 0
    while not choice or not 0 <= choice <= len(feed.entry):
      choice = int(raw_input(message))
    print
    return choice

  def extractParameters(self,html,htmlname,params):
      # type: (object, object, object) -> object
    _myattributes ={}
    _params = {}
    if (len(html)>0):
        for _html in html :
          if _html.name :
            _htmlname = str(_html.name.replace("html:",""))
            __htmlname = (htmlname+"_"+_htmlname).replace("-","_")
            _myattributes = _html.attrs

            for attr in _myattributes :
                _varname = str("$"+__htmlname+"_"+str(attr)).replace("-","_")
                _params[_varname[1:]] = ''.join(_myattributes[attr]) #Remove $ start for dictioanary
                _html[attr] = _varname

            if _html.children :
                _params.update(self.extractParameters(_html.contents,__htmlname,{} ))
            else :
                _html.string
        params.update(_params)
    return params



  def PrintEntry(self, entry):
    print '%s [%s]' % (entry.title.text, entry.Kind())
    if entry.page_name:
      print ' page name:\t%s' % entry.page_name.text
    if entry.content:
      mysoup = BeautifulSoup(str(entry.content.html), 'html.parser')

      if entry.page_name.text == "home" :
        for heading in mysoup.find_all("html:h2") :
          myname = re.sub(r'.*::T::-|.*TOC-',"",heading.contents[0].attrs["name"])

          mytemplates = ""
          mytemplates = heading.nextSibling
          self.mytemplates[myname] = mytemplates
          sub_mytemplates=mytemplates.__copy__()  #Make a copy of the template
          self.sub_mytemplates[myname] = sub_mytemplates
          self.mytemplatesParams[myname] = self.extractParameters(sub_mytemplates,myname,{})



  def PrintListItem(self, entry):
    print '%s [%s]' % (entry.title.text, entry.Kind())
    for col in entry.field:
      print ' %s %s\t%s' % (col.index, col.name, col.text)

  def PrintListPage(self, entry):
    print '%s [%s]' % (entry.title.text, entry.Kind())
    for col in entry.data.column:
      print ' %s %s' % (col.index, col.name)

  def PrintFileCabinetPage(self, entry):
    print '%s [%s]' % (entry.title.text, entry.Kind())
    print ' page name:\t%s' % entry.page_name.text
    print ' content\t%s...' % str(entry.content.html)[0:100]

  def PrintAttachment(self, entry):
    print '%s [%s]' % (entry.title.text, entry.Kind())
    if entry.summary is not None:
      print ' description:\t%s' % entry.summary.text
    print ' content\t%s, %s' % (entry.content.type, entry.content.src)

  def PrintWebAttachment(self, entry):
    print '%s [%s]' % (entry.title.text, entry.Kind())
    if entry.summary.text is not None:
      print ' description:\t%s' % entry.summary.text
    print ' content src\t%s' % entry.content.src

  def Run(self):
    """Executes the demo application."""

    try:
      while True:
        self.PrintMainMenu()
        choice = self.GetMenuChoice(MAIN_MENU)

        if choice == 1:
          kind_choice = raw_input('What kind (all|%s)?: ' % '|'.join(
              gdata.sites.data.SUPPORT_KINDS))
          if kind_choice in gdata.sites.data.SUPPORT_KINDS:
            uri = '%s?kind=%s' % (self.client.make_content_feed_uri(),
                                  kind_choice)
            feed = self.client.GetContentFeed(uri=uri)
          else:
            feed = self.client.GetContentFeed()

          print "\nFetching content feed of '%s'...\n" % self.client.site

          for entry in feed.entry:
            kind = entry.Kind()

            if kind == 'attachment':
              self.PrintAttachment(entry)
            elif kind == 'webattachment':
              self.PrintWebAttachment(entry)
            elif kind == 'filecabinet':
              self.PrintFileCabinetPage(entry)
            elif kind == 'listitem':
              self.PrintListItem(entry)
            elif kind == 'listpage':
              self.PrintListPage(entry)
            else:
              self.PrintEntry(entry)

            print ' revision:\t%s' % entry.revision.text
            print ' updated:\t%s' % entry.updated.text

            parent_link = entry.FindParentLink()
            if parent_link:
              print ' parent link:\t%s' % parent_link

            if entry.GetAlternateLink():
              print ' view in Sites:\t%s' % entry.GetAlternateLink().href

            if entry.feed_link:
              print ' feed of items:\t%s' % entry.feed_link.href

            if entry.IsDeleted():
              print ' deleted:\t%s' % entry.IsDeleted()

            if entry.in_reply_to:
              print ' in reply to:\t%s' % entry.in_reply_to.href

            print

        elif choice == 2:
          print "\nFetching activity feed of '%s'..." % self.client.site
          feed = self.client.GetActivityFeed()
          for entry in feed.entry:
            print '  %s [%s on %s]' % (entry.title.text, entry.Kind(),
                                       entry.updated.text)

        elif choice == 3:
          print "\nFetching content feed of '%s'...\n" % self.client.site

          feed = self.client.GetContentFeed()
          try:
            selection = self.GetChoiceSelection(
                feed, 'Select a page to fetch revisions for: ')
          except TypeError:
            continue
          except ValueError:
            continue

          feed = self.client.GetRevisionFeed(
              feed.entry[selection - 1].GetNodeId())
          for entry in feed.entry:
            print entry.title.text
            print '  new version on:\t%s' % entry.updated.text
            print '  view changes:\t%s' % entry.GetAlternateLink().href
            print '  current version:\t%s...' % str(entry.content.html)[0:100]
            print

        elif choice == 4:
          print "\nFetching content feed of '%s'...\n" % self.client.site

          feed = self.client.GetContentFeed()
          try:
            selection = self.GetChoiceSelection(
                feed, 'Select a parent to upload to (or hit ENTER for none): ')
          except ValueError:
            selection = None

          page_title = raw_input('Enter a page title: ')

          parent = None
          if selection is not None:
            parent = feed.entry[selection - 1]

          new_entry = self.client.CreatePage(
              'webpage', page_title, '<b>Your html content</b>',
              parent=parent)
          if new_entry.GetAlternateLink():
            print 'Created. View it at: %s' % new_entry.GetAlternateLink().href

        elif choice == 5:
          print "\nFetching filecabinets on '%s'...\n" % self.client.site

          uri = '%s?kind=%s' % (self.client.make_content_feed_uri(),
                                'filecabinet')
          feed = self.client.GetContentFeed(uri=uri)

          selection = self.GetChoiceSelection(
              feed, 'Select a filecabinet to create the web attachment on: ')

          url = raw_input('Enter the URL of the attachment: ')
          content_type = raw_input("Enter the attachment's mime type: ")
          title = raw_input('Enter a title for the web attachment: ')
          description = raw_input('Enter a description: ')

          parent_entry = None
          if selection is not None:
            parent_entry = feed.entry[selection - 1]

          self.client.CreateWebAttachment(url, content_type, title,
                                          parent_entry, description=description)
          print 'Created!'

        elif choice == 6:
          print "\nFetching filecainets on '%s'...\n" % self.client.site

          uri = '%s?kind=%s' % (self.client.make_content_feed_uri(),
                                'filecabinet')
          feed = self.client.GetContentFeed(uri=uri)

          selection = self.GetChoiceSelection(
              feed, 'Select a filecabinet to upload to: ')

          filepath = raw_input('Enter a filename: ')
          page_title = raw_input('Enter a title for the file: ')
          description = raw_input('Enter a description: ')

          filename = os.path.basename(filepath)
          file_ex = filename[filename.rfind('.'):]
          if not file_ex in mimetypes.types_map:
            content_type = raw_input(
                'Unrecognized file extension. Please enter the mime type: ')
          else:
            content_type = mimetypes.types_map[file_ex]

          entry = None
          if selection is not None:
            entry = feed.entry[selection - 1]

          new_entry = self.client.UploadAttachment(
              filepath, entry, content_type=content_type, title=page_title,
              description=description)
          print 'Uploaded. View it at: %s' % new_entry.GetAlternateLink().href

        elif choice == 7:
          print "\nFetching all attachments on '%s'...\n" % self.client.site

          uri = '%s?kind=%s' % (self.client.make_content_feed_uri(),
                                'attachment')
          feed = self.client.GetContentFeed(uri=uri)

          selection = self.GetChoiceSelection(
              feed, 'Select an attachment to download: ')

          filepath = raw_input('Save as: ')

          entry = None
          if selection is not None:
            entry = feed.entry[selection - 1]

          self.client.DownloadAttachment(entry, filepath)
          print 'Downloaded.'

        elif choice == 8:
          print "\nFetching content feed of '%s'...\n" % self.client.site

          feed = self.client.GetContentFeed()
          selection = self.GetChoiceSelection(feed, 'Select a page to delete: ')

          entry = None
          if selection is not None:
            entry = feed.entry[selection - 1]

          self.client.Delete(entry)
          print 'Removed!'

        elif choice == 9:
          print ('\nFetching your list of sites for domain: %s...\n'
                 % self.client.domain)

          feed = self.client.GetSiteFeed()
          for entry in feed.entry:
            print entry.title.text
            print '  site name: ' + entry.site_name.text
            if entry.summary.text:
              print '  summary: ' + entry.summary.text
            if entry.FindSourceLink():
              print '  copied from site: ' + entry.FindSourceLink()
            print '  acl feed: %s\n' % entry.FindAclLink()

        elif choice == 10:
          title = raw_input('Enter a title: ')
          summary = raw_input('Enter a description: ')
          theme = raw_input('Theme name (ex. "default"): ')

          new_entry = self.client.CreateSite(
              title, description=summary, theme=theme)
          print 'Site created! View it at: ' + new_entry.GetAlternateLink().href

        elif choice == 11:
          print "\nFetching acl permissions of '%s'...\n" % self.client.site

          feed = self.client.GetAclFeed()
          for entry in feed.entry:
            print '%s (%s) - %s' % (entry.scope.value, entry.scope.type,
                                    entry.role.value)

        elif choice == 12:
          self.PrintSettingsMenu()
          settings_choice = self.GetMenuChoice(SETTINGS_MENU)

          if settings_choice == 1:
            self.client.site = self.PromptSiteName()
          elif settings_choice == 2:
            self.client.domain = self.PromptDomain()

        elif choice == 13:
          print 'Later!\n'
          return

    except gdata.client.RequestError, error:
      print error
    except KeyboardInterrupt:
      return



#===========================================================================

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
#from oauth2client.tools import run

import gdata.sites.client
import gdata.sites.data

from oauth2client import tools

def getAuth2Token(scope) :
    #Authenticate client
        # How to use the OAuth 2.0 client is described here:
    # https://developers.google.com/api-client-library/python/guide/aaa_oauth

    SCOPE = scope

    # client_secrets.json is downloaded from the API console:
    # https://code.google.com/apis/console/#project:<PROJECT_ID>:access
    # where <PROJECT_ID> is the ID of your project
    flow = flow_from_clientsecrets('client_secrets.json',
                               scope=SCOPE,
                               redirect_uri='http://localhost')

    storage = Storage('plus.dat')
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = tools.run_flow(flow, storage)

    # Munge the data in the credentials into a gdata OAuth2Token
    # This is based on information in this blog post:
    # https://groups.google.com/forum/m/#!msg/google-apps-developer-blog/1pGRCivuSUI/3EAIioKp0-wJ

    auth2token = gdata.gauth.OAuth2Token(client_id=credentials.client_id,
                        client_secret=credentials.client_secret,
                        scope=SCOPE,
                        access_token=credentials.access_token,
                        refresh_token=credentials.refresh_token,
                        user_agent='sites-test/1.0')
    return(auth2token)


#=============================================================================
def showSiteContents():
    SCOPE = 'https://sites.google.com/feeds/'

    # Get authenticated token to access sites API
    auth2token = getAuth2Token(SCOPE)

    # Create a gdata client
    client = gdata.sites.client.SitesClient(source='sites-test',
                                        #site='sumpurn-en',
                                        domain='sumpurn.com',
                                        auth_token=auth2token)

    # Authorize it

    auth2token.authorize(client)

    # Call an API e.g. to get the site content feed

    #feed = client.GetContentFeed()
    listOfSites = client.GetSiteFeed()

    print(client.site)
    #for entry in feed.entry:
    #    print '%s [%s]' % (entry.title.text, entry.Kind())

    import inspect

    for entry in listOfSites.entry:
        print(inspect.getmembers(entry))
        print (entry.title.text,"=====\n","type=",type(entry),entry.site_name.text)
        #Entry is of type : gdata.sites.data.SiteEntry

        #gdata.sites.client.SitesClient
        #gdata.sites.client.data

        #for k in entry : print(k,"=",entry[k])

        line=entry.link[0].href
        print("line=>",line)
        #matchObj = re.match( r'(.*)/(.*)/', line, re.M|re.I)

        #print(matchObj.group(),"=>",matchObj.group(1),"=>",matchObj.group(2))

        #client.site = matchObj.group(2)
        client.site = entry.site_name.text

        print("=========",client.site)
        listOfContents = client.GetContentFeed()
        for content in listOfContents.entry :
            print  '%s [%s]' % (content.title.text, content.Kind())

# See:
# https://developers.google.com/google-apps/sites/docs/1.0/developers_guide_python
# for more details of the Sites API

from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

import json

class MyHTMLParser(HTMLParser):

    def __init__ (self) :
        self.reset()  # HTML  Parser calls this
        self.resetVariables()
        self.nlines = None # No. of lines in rawdata.
        # Can be computed only after rawdata is set by feed
        self.linesMap = None # Indices where the rawdata has line breaks
        self.latestName = None
        self.htmlTemplates = {}     #Discovered templates will be stored here

    def saveSite(self,filename):
        output = open(filename, 'wb')

        # Pickle dictionary using protocol 0.
        json.dump(self.htmlTemplates, output)
        output.close()

    def setLineMap(self):
        self.nlines = self.rawdata.count("\n")
        self.linesMap = {}
        self.linesMap[0] = 0    # line 0 Starts from position 0
        for lineno in range(self.nlines):
            startpos = self.linesMap[lineno]
            self.linesMap[lineno+1]=self.linesMap[lineno]+\
                                    self.rawdata.find("\n",startpos+1)



    def resetVariables (self) :
        self.startedH2 = False
        self.endedH2 = False
        self.template = ""
        self.startedTemplate = False
    #    self.endedTemplate = False
        self.templateStart = None
        self.templateEnd = None
        self.templateName = None


    def printVariables(self):
        print ("PRINTING VARIABLES")
        print("startedH2=",self.startedH2,
        "endedH2=",self.endedH2,
              "i=",self.i,
              "j=",self.j,
              "ij_text=",self.rawdata[self.i:self.j+1],
              "lineno=",self.lineno,
              "nlines=",self.nlines,
              "pos=",self.getpos(),
              "template=",self.template,
              "startedTemplate=",self.startedTemplate,
              #"endedTemplate=",self.endedTemplate,
              "templateStart=",self.templateStart,
              "templateEnd=",self.templateEnd,
              "templateName=",self.templateName)
        print("linesMap = ",self.linesMap)
        print("Tag text is = ", self.get_starttag_text())


    def getTemplate(self) :
        html = self.rawdata
        print("Lines map for  =", self.templateName, " is : " , self.linesMap)
        print("Template start = ",self.templateStarti,self.templateStart)
        print("Template end = ", self.templateEndi,self.templateEnd)
        #print("i,j= ",i,j)
        #start = self.linesMap[self.templateStart[0]-1]+self.templateStart[1]
        #end = self.linesMap[self.templateEnd[0]-1]+self.templateEnd[1]
        start = self.templateStarti
        end = self.templateEndi
        self.htmlTemplates[self.templateName] = html[start:end]
        print('Found template  :', self.templateName," ::: ",html[start:end])

    def printTemplate(self):
        html = self.rawdata
        templateStart = self.getpos()
        #start = self.linesMap[templateStart[0] - 1] + templateStart[1]
        #end = self.linesMap[self.templateEnd[0] - 1] + self.templateEnd[1]
        print('Template starting to end :', html[self.templateStarti:])


    def handle_starttag(self, tag, attrs):
        if not self.nlines : self.setLineMap()
        print "Start tag:", tag, self.getpos()
        self.printVariables()


        for attr in attrs:
            print "     attr:", attr
            if attr[0] == 'name' : self.latestName = attr[1]

        if not self.startedTemplate and self.endedH2 and not self.startedTemplate:
            self.templateStart = self.getpos()  # Template has started
            self.templateStarti = self.i  # Template has started
            self.printTemplate()
            self.startedTemplate = True

        if tag == 'html:h2':

            if self.templateStart:
                self.templateEnd = self.getpos()
                self.templateEndi = self.i
                #self.printTemplate()
                self.getTemplate()  # Read the discovered tempalate
                self.resetVariables() # Fresh template block started
            self.startedH2 = True

    def handle_endtag(
            self, tag):
        print "End tag  :", tag
        #self.printTemplate()
        if tag == 'html:h2':
            self.endedH2 = True
            self.templateName = self.latestName # Got the template name




    def handle_data(self, data):
        print "Data     :", data
        #self.latestData = data

    def handle_comment(self, data):
        print "Comment  :", data
    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        print "Named ent:", c
    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        print "Num ent  :", c
    def handle_decl(self, data):
        print "Decl     :", data

parser = MyHTMLParser()

if __name__ == '__main__':
    #runSample()
    publishWeb()
    1
    #showSiteContents()aq