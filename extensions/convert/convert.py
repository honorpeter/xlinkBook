#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
from config import Config
from extensions.bas_extension import BaseExtension
from utils import Utils
from record import Record
from record import Tag
from bs4 import BeautifulSoup
import requests
import os


class Convert(BaseExtension):

    form_dict = None
    convert_data_file = 'web_content/convert_data'
    convert_output_file = ''
    def __init__(self):
        BaseExtension.__init__(self)
        self.utils = Utils()
        self.count = 0
        self.tag = Tag()

        self.convert_url_is_base = False
        self.convert_url_args = '' #'?start=' #'?start=0&tag='
        self.convert_url_args_2 = ''
        self.convert_next_page = ''
        self.convert_page_step = 1
        self.convert_page_start = 1
        self.convert_page_max = 10
        self.convert_page_to_end = False
        self.convert_tag = '' #"div#title"  # tag#class or tag
        self.convert_min_num = 0
        self.convert_max_num = 1000
        self.convert_filter = ""
        self.convert_contain = ""
        self.convert_start = 0
        self.convert_split_column_number = 0
        self.convert_top_item_number = 0
        self.convert_output_data_to_new_tab = False
        self.convert_output_data_to_temp = False
        self.convert_output_data_format = ''
        self.convert_cut_start = ''
        self.convert_cut_start_offset = 0
        self.convert_cut_end = ''
        self.convert_cut_end_offset = 0
        self.convert_remove = []
        self.convert_replace = {}
        self.convert_append = ''
        self.convert_cut_max_len = 1000
        self.convert_script = ''
        self.convert_script_custom_ui = False
        self.convert_smart_engine = ''
        self.convert_div_width_ratio = 0
        self.convert_div_height_ratio = 0
        self.convert_show_url_icon = False
        self.url_prefix = ''
        self.convert_priority = 0
        self.convert_domain_stat_field = []

        self.domainDict = {}


    def initArgs(self, url, resourceType, isEnginUrl=False):
        if url.startswith('http') == False:
            if url.find('[') != -1:
                url = url[url.find('(') + 1 : url.find(')')]
        self.convert_url_is_base = Config.convert_url_is_base
        self.convert_url_args = Config.convert_url_args #'?start=' #'?start=0&tag='
        self.convert_url_args_2 = Config.convert_url_args_2
        self.convert_next_page = Config.convert_next_page
        self.convert_page_step = Config.convert_page_step
        self.convert_page_start = Config.convert_page_start
        self.convert_page_max = Config.convert_page_max
        self.convert_page_to_end = Config.convert_page_to_end
        self.convert_tag = Config.convert_tag #"div#title"  # tag#class or tag
        self.convert_min_num = Config.convert_min_num
        self.convert_max_num = Config.convert_max_num
        self.convert_filter = Config.convert_filter
        self.convert_contain = Config.convert_contain
        self.convert_start = Config.convert_start
        self.convert_split_column_number = Config.convert_split_column_number
        self.convert_top_item_number = Config.convert_top_item_number
        self.convert_output_data_to_new_tab = Config.convert_output_data_to_new_tab
        self.convert_output_data_to_temp = Config.convert_output_data_to_temp
        self.convert_output_data_format = Config.convert_output_data_format  
        self.convert_cut_start = Config.convert_cut_start
        self.convert_cut_start_offset = Config.convert_cut_start_offset
        self.convert_cut_end = Config.convert_cut_end
        self.convert_cut_end_offset = Config.convert_cut_end_offset
        self.convert_remove = Config.convert_remove
        self.convert_replace = Config.convert_replace
        self.convert_append = Config.convert_append
        self.convert_cut_max_len = Config.convert_cut_max_len
        self.convert_script = Config.convert_script
        self.convert_script_custom_ui = Config.convert_script_custom_ui
        self.convert_smart_engine = Config.convert_smart_engine
        self.convert_div_width_ratio = Config.convert_div_width_ratio
        self.convert_div_height_ratio = Config.convert_div_height_ratio
        self.convert_show_url_icon = Config.convert_show_url_icon
        self.convert_priority = Config.convert_priority
        self.convert_domain_stat_field = Config.convert_domain_stat_field


        items = Config.convert_dict.items()
        if isEnginUrl:
            items = Config.convert_engin_dict.items()

        for k, v in items:
            if url.lower().find(k.lower()) != -1 or (resourceType != '' and k.lower() == resourceType.lower()):
                print 'matched:' + k 
                print v
                if v.has_key('url_is_base'):
                    self.convert_url_is_base = v['url_is_base']
                if v.has_key('url_args'):
                    self.convert_url_args = v['url_args']
                if v.has_key('url_args_2'):
                    self.convert_url_args_2 = v['url_args_2']
                if v.has_key('next_page'):
                    self.convert_next_page = v['next_page']
                if v.has_key('page_step'):
                    self.convert_page_step = v['page_step']
                if v.has_key('page_start'):
                    self.convert_page_start = v['page_start']                
                if v.has_key('page_max'):
                    self.convert_page_max = v['page_max']
                if v.has_key('page_to_end'):
                    self.convert_page_to_end = v['page_to_end']
                if v.has_key('tag'):
                    self.convert_tag = v['tag']   
                if v.has_key('min_num'):
                    self.convert_min_num = v['min_num']
                if v.has_key('max_num'):
                    self.convert_max_num = v['max_num']
                if v.has_key('filter'):
                    self.convert_filter = v['filter']   
                if v.has_key('contain'):
                    self.convert_contain = v['contain']
                if v.has_key('start'):
                    self.convert_start = v['start']
                if v.has_key('split_column_number'):
                    self.convert_split_column_number = v['split_column_number']
                if v.has_key('top_item_number'):
                    self.convert_top_item_number = v['top_item_number']
                if v.has_key('output_data_to_new_tab'):
                    self.convert_output_data_to_new_tab = v['output_data_to_new_tab']  
                if v.has_key('output_data_to_temp'):
                    self.convert_output_data_to_temp = v['output_data_to_temp']  
                if v.has_key('output_data_format'):
                    self.convert_output_data_format = v['output_data_format']   
                if v.has_key('cut_start'):
                    self.convert_cut_start = v['cut_start'] 
                if v.has_key('cut_start_offset'):
                    self.convert_cut_start_offset = v['cut_start_offset'] 
                if v.has_key('cut_end'):
                    self.convert_cut_end = v['cut_end'] 
                if v.has_key('cut_end_offset'):
                    self.convert_cut_end_offset = v['cut_end_offset']   
                if v.has_key('remove'):
                    self.convert_remove = v['remove'] 
                if v.has_key('replace'):
                    self.convert_replace = v['replace']
                if v.has_key('append'):
                    self.convert_append = v['append']
                if v.has_key('cut_max_len'):
                    self.convert_cut_max_len = v['cut_max_len'] 
                if v.has_key('script'):
                    self.convert_script = v['script'] 
                if v.has_key('script_custom_ui'):
                    self.convert_script_custom_ui = v['script_custom_ui'] 
                if v.has_key('smart_engine'):
                    self.convert_smart_engine = v['smart_engine'] 
                if v.has_key('div_width_ratio'):
                    self.convert_div_width_ratio = v['div_width_ratio'] 
                if v.has_key('div_height_ratio'):
                    self.convert_div_height_ratio = v['div_height_ratio'] 
                if v.has_key('show_url_icon'):
                    self.convert_show_url_icon = v['show_url_icon']
                if v.has_key('priority'):
                    self.convert_priority = v['priority']
                if v.has_key('domain_stat_field'):
                    self.convert_domain_stat_field = v['domain_stat_field']

 
                #if self.convert_smart_engine == '' and self.utils.search_engin_dict.has_key(k):
                #    self.convert_smart_engine = k
                break

    def processData(self, data, dataToTemp=False, dataStat=Config.convert_domain_stat_enable):
        result = ''
        info = ''

        datas = data.split('\n')
        self.domainDict = {}

        if len(datas) <= self.convert_split_column_number:
            self.convert_cut_max_len = 1000
        elif len(datas) <= (self.convert_split_column_number * 2):
            self.convert_cut_max_len += self.convert_cut_max_len / 2
        for line in datas:
            if line.strip() == '':
                continue
            r = Record(line)
            url = r.get_url().strip()
            desc = r.get_describe().strip()

            if self.convert_contain != '' and line.find(self.convert_contain) == -1:
                continue

            if self.convert_filter != '' and line.find(self.convert_filter) != -1:
                continue

            if url.find('twitter') != -1:
                info += url[url.rfind('/') + 1 :] + ', '

            title = r.get_title().strip()


            if title != '':
                title = self.customFormat(title)
                newUrl = url

                if self.convert_smart_engine != '':
                    if url == '' or (self.convert_smart_engine != 'glucky' and url.find('btnI=') != -1):
                        newUrl = self.utils.toQueryUrl(self.utils.getEnginUrl(self.convert_smart_engine), title)

                line = r.get_id().strip() + ' | ' + title + ' | ' + newUrl + ' | ' + desc

                result += line + '\n'

            if dataStat and url != '' and len(self.convert_domain_stat_field) > 0:
                self.domainStatistics(Record(line))

        if dataStat and len(self.domainDict) > 0:
            result = self.getDomainStatisticsData()

        if dataToTemp and self.convert_output_data_to_new_tab == False:
            flag = 'w'
            if self.form_dict['fileName'].find('exclusive') != -1 and Config.exclusive_append_mode:
                flag = 'a'
            f = open(self.convert_data_file, flag)
            #f.write(self.utils.clearHtmlTag(line) + '\n')
            f.write(result + '\n')
            f.close()

        print info[0 : len(info) - 2]

        return result


    def getDomainStatisticsData(self):
        data = ''
        enginData = ''
        allLinks = ''
        if len(self.domainDict) > 0:
            domainDict = self.domainDict

            print domainDict.keys()
            for item in sorted(domainDict.items(), key=lambda domainDict:int(len(domainDict[1])), reverse=True):
            #for item in self.domainDict.items():
                website = 'website:'
                siteDict = {}
                for site in sorted(item[1], reverse=True):
                    if siteDict.has_key(site):
                        continue
                    else:
                        siteDict[site] = site
                    website += site + ', '
                website = website.strip()
                if website.endswith(','):
                    website = website[0 : len(website) - 1]
                title = item[0][item[0].find('//') + 2 : item[0].rfind('.')]
    
                data += ' | ' +  str(len(item[1])) + ' -- ' + title + ' | ' + item[0] + ' | ' + website + '\n'

                allLinks += title + '(' + item[0] + ')+'

                enginList = [item[0][item[0].find('//') + 2 : item[0].find('.')], item[0][item[0].find('//') + 2 :]]
                for engin in enginList:
                    if self.utils.search_engin_dict.has_key(engin):
                        enginData += engin + ' '

        if enginData != '':
            print ''
            print '---->enginData<----'
            print enginData
            print ''
            print allLinks[0 : len(allLinks) - 1]
            #data += ' | ' + enginData + ' | | \n' 
        return data

    def domainStatistics(self, record):
        for field in self.convert_domain_stat_field:
            urlList = []
            textList = [] 

            if field == 'url':
                urlList.append(record.get_url().strip())
                textList.append(record.get_title().strip())
            else:
                fieldValue = self.utils.reflection_call('record', 'WrapRecord', 'get_tag_content', record.line, {'tag' : field})
                print fieldValue
                if fieldValue != None:
                    fieldValue = fieldValue.strip()
                    fieldValueList = fieldValue.split(',')
    
                    for fv in fieldValueList:
                        fv = fv.strip()
                        if field == 'website':
                            urlList.append(self.utils.getValueOrText(fv, returnType='value'))
                            textList.append(self.utils.getValueOrText(fv, returnType='text'))
    

            for i in range(0, len(urlList)):
                text = textList[i]
                url = urlList[i]

                if url.startswith('http') == False:
                    return
                url = url.replace('https', 'http').replace('www.', '')
                domain = url
                index = url.find('/', url.find('://') + 3)
                if index != -1:
                    domain = url[0 : index].strip()
                if text == '':
                    text = 'link'
                if text.startswith('http'):

                    if text.find(',') != -1:
                        text = text.replace(',', '')
                    linkText = text
                    if linkText.endswith('/'):
                        linkText = linkText[0 : len(linkText) - 1]
                    if linkText.find('/') != -1:

                        linkText = linkText[linkText.rfind('/') + 1 : ]
                        
                    linkText = linkText.replace('"', '').replace("'", '')
                    if len(urlList) == 1 and len(linkText) > 60:
                        linkText = linkText[0 : 60]
                    elif len(urlList) > 1 and len(linkText) > 15:
                        linkText = linkText[0 : 15]

                    text = linkText

                text = text.replace('%20', ' ').replace('%', '').strip()
        
                if url.endswith('/') == False:
                    url += '/'
                if self.domainDict.has_key(domain):
                    self.domainDict[domain].append(text + '(' + url + ')')
                else:
                    self.domainDict[domain] = [text + '(' + url + ')']
    

      
    def excute(self, form_dict):
        print 'excute'
        print form_dict
        self.form_dict = form_dict
        resourceType = ''
        if form_dict.has_key('resourceType'):
            resourceType = form_dict['resourceType'].encode('utf8')
        url = form_dict['url'].encode('utf8')

        urlList = []
        enginUrlList = []
        allUrl = []
        if url.find(',') != -1:
            allUrl = url.split(',')
        else:
            allUrl = [url]
        print allUrl
        for u in allUrl:
            u = u.replace('%20', ' ').strip()
            if u.startswith('http'):
                urlList.append(u)
            elif u.startswith('[') and u.find(']') != -1:
                if u.find('http') != -1:
                    urlList.append(u)
                else:
                    keyword = u[u.find('[') + 1 : u.find(']')]
                    engin = u[u.find('(') + 1 : u.find(')')]
                    for k in keyword.split('*'):
                        enginUrlList.append(self.utils.toQueryUrl(self.utils.getEnginUrl(engin), k))
 
            elif self.utils.search_engin_dict.has_key(u):
                enginUrlList.append(self.utils.toQueryUrl(self.utils.getEnginUrl(u), form_dict['rTitle'].strip()))
 
        print ','.join(urlList)
        print ','.join(enginUrlList)
        html = ''
        if len(urlList) > 0:
            html += self.doConvert(url, form_dict, resourceType, isEnginUrl=False)

        if len(enginUrlList) > 0:
             html += self.doConvert(url, form_dict, resourceType, isEnginUrl=True)

        return html

    def doConvert(self, url, form_dict, resourceType, isEnginUrl=False):
        self.initArgs(url, resourceType, isEnginUrl=isEnginUrl)

        if form_dict.has_key('command'):
            if url.find('[') != -1 and url.find(']') != -1:
                if url.startswith('['):
                    self.initArgs(url[url.find('(') + 1 : url.find(')')], resourceType, isEnginUrl=isEnginUrl)
                else:
                    self.initArgs(url, resourceType, isEnginUrl=isEnginUrl)
            command = form_dict['command']
            if command.startswith('./') == False:
                source = ''
                if form_dict.has_key('fileName') and form_dict['fileName'] != '':
                    source = form_dict['fileName']
                else:
                    source = self.convert_data_file
                    form_dict['fileName'] = source
                form_dict['command'], form_dict['commandDisplay'] = self.buildCmd('list.py', source, args=form_dict['command'])
            else:
                form_dict['fileName'] = '' 
            return self.runCommand(form_dict)
        elif url.find(Config.ip_adress) != -1:
            urlList = [url]
            allData = ''
            if url.find('[') != -1 and url.find(']') != -1:
                value, urlList = self.genUrlList(url)
                self.initArgs(value, resourceType, isEnginUrl=isEnginUrl)     

            for link in urlList:
                print link
                db = link[link.find('db=') + 3 : ]
                if db.find('&') != -1:
                    db = db[0 : db.find('&')]
    
                key = link[link.find('key=') + 4 :]
                if key.find('&') != -1:
                    key = key[0 : key.find('&')]
    
                form_dict['command'], form_dict['commandDisplay'] = self.buildCmd('list.py', 'db/' + db + key)
                form_dict['fileName'] = 'db/' + db + key
    
                print form_dict
                allData += self.runCommand(form_dict)

            return allData


        divID = form_dict['divID'].encode('utf8')
        rID = form_dict['rID'].encode('utf8')
        

        crossrefQuery = ''

        if form_dict.has_key('crossrefQuery'):
            crossrefQuery = form_dict['crossrefQuery'].encode('utf8')


        #print self.convert_remove
        #print 'convert_script:' + self.convert_script
        html = ''
        if self.convert_script != '':
            allData = ''
            data = ''
            urlList = [url]
            if url.find('[') != -1 and url.find(']') != -1:
                value, urlList = self.genUrlList(url)
                self.initArgs(value, resourceType, isEnginUrl=isEnginUrl)

            for u in urlList:

                cmd = './extensions/convert/' + self.convert_script + ' -u "' + u + '" -q "' + crossrefQuery + '" '
                print cmd

                data = subprocess.check_output(cmd, shell=True)

                print 'convert_script_custom_ui:' + str(self.convert_script_custom_ui)
                print 'data:' + data

                allData += data
            if self.convert_script_custom_ui:
                return allData.replace('\n', '<br>')
            else:
                return self.genHtml(self.processData(allData, dataToTemp=self.convert_output_data_to_temp), divID, rID, resourceType)

        else:
            if url.startswith('http') and self.convert_tag == '':
                return self.genCommandBox()

            if url == '':
                url = self.utils.bestMatchEnginUrl(form_dict['rTitle'].encode('utf8'))
            if self.convert_url_args != '':
                url += self.convert_url_args
            print url

            step = self.convert_page_start
            #new_url = url
            new_url = url

            if self.convert_url_args != '':
                new_url = url + str(step)
            if self.convert_url_args_2 != '':
                new_url += self.convert_url_args_2

            page_count = 0
            print self.convert_page_step
            print self.convert_url_args
            all_data = ''
            if self.convert_page_step > 0 and self.convert_url_args != '':
                all_data = self.convertPages2data(url)
                if all_data != '':
                    return self.genHtml(self.processData(all_data, dataToTemp=self.convert_output_data_to_temp), divID, rID, resourceType)
                else:
                    return ''
            elif self.convert_next_page != '':

                if self.convert_next_page.find('#') != -1:
                    args = self.convert_next_page.split('#')
                    base_url = new_url
                    if base_url.endswith('/'):
                        base_url = base_url[0 : len(base_url) - 1]
                    if base_url.find('/', base_url.find('//') + 2) != -1:
                        base_url = base_url[0 : base_url.find('/', base_url.find('//') + 2)]
                    data = self.convert2data(new_url)
                    page_count += 1
                    if data != '':
                        all_data += data + '\n'
  
                        while True:

                            r = requests.get(new_url)
                            sp = BeautifulSoup(r.text)

                            nextLink = sp.find(args[0], class_=args[1])

                            if nextLink == None:
                                break

                            if nextLink.a != None:
                                nextLink = nextLink.a

                            if nextLink != None:
                                if nextLink['href'].startswith('http') == False and self.convert_url_is_base:
                                    if nextLink['href'].startswith('/'):
                                        new_url = base_url + '/' + nextLink['href'][1:]
                                    else:
                                        new_url = base_url + '/' + nextLink['href']
                                else:
                                    new_url = nextLink['href']


                                print new_url
                                data = self.convert2data(new_url)
                                if data != '' and data != None:
                                    all_data += data + '\n'
                                    page_count += 1
                                    if page_count >= self.convert_page_max:
                                        break
                                elif data == '':
                                    if self.convert_page_to_end == False:
                                        break
                            else:
                                break

                    if all_data != '':
                        return self.genHtml(self.processData(all_data, dataToTemp=self.convert_output_data_to_temp), divID, rID, resourceType)
                    else:
                        return''


            else:
                data = ''
                if url.find('[') != -1 and url.find(']') != -1:
                    value, urlList = self.genUrlList(url)
                    self.initArgs(value, resourceType, isEnginUrl=isEnginUrl)

                    for u in urlList:
                        #print u
                        if self.convert_page_step > 0 and self.convert_url_args != '':
                            data += self.convertPages2data(u)
                        else:
                            data += self.convert2data(u)

                elif url.find(',') != -1:
                    for u in url.split(','):
                        u = u.strip()
                        if u.startswith('http'):
                            data += self.convert2data(u)
                else:
                    data = self.convert2data(new_url)
                html = self.genHtml(self.processData(data, dataToTemp=self.convert_output_data_to_temp), divID, rID, resourceType)

        return html


    def genUrlList(self, url):
        urlList = []
        value = ''
        if url.find('[') != -1 and url.find(']') != -1:
            keys = []
            if url.startswith('['):
                keys = url[1 : url.find(']')].split('*')
                value = url[url.find('(') + 1 : url.find(')')]
            else:
                part1 = url[0 : url.find('[')]
                part2 = url[url.find(']') + 1 : ]
                keys = url[url.find('[') + 1 : url.find(']')].split('*')
                value = part1 + '%s' + part2
            for k in keys:
                if value.find('%s') != -1:
                    u = value.replace('%s', k)
                    urlList.append(u)
                else:
                    urlList.append(value + k)
            return value, urlList

        return url, [url]



    def genCommandBox(self, command='', fileName=''):
        if command == '':
            command = "-f '' -e '" + self.convert_smart_engine + "'"
        script = "var text = $('#command_txt'); console.log('', text[0].value);"
        divID = self.form_dict['divID']
        script += "var dataDiv = $('#" + divID + "'); dataDiv.html('');"

        script += "var postArgs = {name : 'convert', command : text[0].value, rTitle : '', 'url' : '" + self.form_dict['url'] + "', check: 'false', fileName : '" + fileName + "', 'divID' : '" + divID + "'};";
        script += "$.post('/runCommand', postArgs, function(data) { \
                        console.log('refresh:' + data);\
                        if (data.indexOf('#') != -1) {\
                            divID = data.substring(0, data.indexOf('#'));\
                            html = data.substring(data.indexOf('#') + 1);\
                            $('#'+ divID).html(html);\
                        };\
                        });"
        box = '<br><div style="text-align:center;width:100%;margin: 0px auto;"><input id="command_txt" style="border-radius:5px;border:1px solid" maxlength="256" tabindex="1" size="46" name="word" autocomplete="off" type="text" value="' + command + '">&nbsp;&nbsp;'\
              '&nbsp;&nbsp;<button alog-action="g-search-anwser" type="submit" id="command_btn" hidefocus="true" tabindex="2" onClick="' + script + '">Run</button></div>'
        return box

    def runCommand(self, form_dict):
        cmd = form_dict['command']
        if form_dict.has_key('commandDisplay') == False:
            form_dict['commandDisplay'] = cmd
        print 'cmd ----> ' + cmd.replace('"', "'")  + ' <----'
        data = subprocess.check_output(cmd, shell=True)

        result = ''
        for line in  data.split('\n'):
            line = line[line.find(' ') + 1 :].strip()

            if line != '' and line.find('ecords, File:') == -1:
                #r = Record(line)
                result += line + '\n'



        result =  self.genHtml(self.processData(result, dataToTemp=False, dataStat=False), '', '', '', command=form_dict['commandDisplay'], fileName=form_dict['fileName'])


        result = form_dict['divID'] + '-data#' + result

        return result


    def buildCmd(self, script, source, args=''):
        cmd = ''
        cmdDisplay = ''
        if script == 'convert.py':

            cmd = './' + script + ' -i "' + source + '" '

            if self.convert_url_is_base != False:
                cmd += '-b ' + str(self.convert_url_is_base) + ' '

            if self.convert_tag != '':
                cmd += '-t "' + self.convert_tag + '" '
            if self.convert_min_num >= 0:
                cmd += '-n ' + str(self.convert_min_num) + ' '
            if self.convert_max_num >= 0:
                cmd += '-m ' + str(self.convert_max_num) + ' '

            if self.convert_filter != '':
                cmd += '-f "' + self.convert_filter + '" '
            if self.convert_contain != '':
                if self.convert_contain.find('"') != -1:
                    cmd += "-c '" + self.convert_contain + "' "
                else:
                    cmd += '-c "' + self.convert_contain + '" '
            if self.convert_start > 0:
                cmd += '-s ' + str(self.convert_start) + ' '
            if Config.delete_from_char != '':
                cmd += '-d "' + Config.delete_from_char + '" '

        elif script == 'list.py':
            cmd = './' + script + " -i '" + source + "' " + args
            cmdDisplay += args
            if cmd.find(' -b ') == -1:
                cmd += " -b 'raw' "
            if cmd.find(' -e ') == -1:
                cmd += " -e '" + self.convert_smart_engine + "' "
                cmdDisplay += " -e '" + self.convert_smart_engine + "' "
            else:
                engin = cmd[cmd.find(' -e') + 3 :].strip().replace('"', '').replace("'", '')
                if engin.find(' -') != -1:
                    engin = engin[0 : engin.find(' -')].strip()
                for e in engin.split(' '):
                    if e.find('d:') == -1:
                        self.convert_smart_engine = engin
                        break
            if cmd.find(' -f ') == -1:
                cmd += " -f '" + self.convert_contain + "' "
                cmdDisplay += " -f '" + self.convert_contain + "' "
            if cmd.find(' -n ') == -1 and self.convert_min_num >= 0:
                cmd += ' -n ' + str(self.convert_min_num) + ' '
            if cmd.find(' -m ') == -1 and self.convert_max_num >= 0:
                cmd += ' -m ' + str(self.convert_max_num) + ' '


            if source == self.convert_data_file:
                if cmd.find(' --merger ') != -1:
                    mergerFile = self.getCmdArg(cmd, '--merger')
                    cmd = self.removeCmdArg(cmd, '--merger')

                    if mergerFile != '':

                        files = []
                        if mergerFile.find(' ') != -1:
                            files = mergerFile.split(' ')
                        else:
                            files = [mergerFile]
                        for f in files:
                            if f.startswith('db/') == False:
                                f = 'db/' + f
                            if os.path.exists(f):
                                print 'mergerFile:' + f
                                mergerCmd = 'cat ' + f + ' >> ' + self.convert_data_file
                                print mergerCmd
                                data = subprocess.check_output(mergerCmd, shell=True)

                        cmdDisplay = self.removeCmdArg(cmdDisplay, '--merger')

                if cmd.find('--output') != -1:
                    self.convert_output_file = self.getCmdArg(cmd, '--output')
                    print self.convert_output_file
                    if self.convert_output_file != '':
                        command = 'cp ' + self.convert_data_file  + ' ' + self.convert_output_file
                        data = subprocess.check_output(command, shell=True)
       
                    cmd = self.removeCmdArg(cmd, '--output')
                    cmdDisplay = self.removeCmdArg(cmdDisplay, '--output')

                if cmd.find('--split') != -1:
                    self.convert_split_column_number = int(self.getCmdArg(cmd, '--split'))
                    cmd = self.removeCmdArg(cmd, '--split')


        print 'cmd ----> ' + cmd.replace('"', "'") + ' <----'
        print 'cmdDisplay ----> ' + cmdDisplay + ' <----'


        return cmd, cmdDisplay


    def getCmdArg(self, cmd, arg):
        value = cmd[cmd.find(arg) + len(arg) :].replace('"', '').replace("'", '').strip()
        if value.find(' -') != -1:
            value = value[0 : value.find(' -')].strip()

        return value
       

    def removeCmdArg(self, cmd, arg):
        cmd1 = cmd[0 : cmd.find(' ' + arg)]
        cmd2 = ''
        index = cmd.find(' -', cmd.find(' ' + arg) + len(arg) + 1)
        if index != -1:
            cmd2 = cmd[index :]
        cmd = cmd1 + cmd2 

        return cmd.strip()


    def convertPages2data(self, url):
        step = self.convert_page_start
        #new_url = url
        new_url = url

        if self.convert_url_args != '':
            new_url = url + str(step)
        if self.convert_url_args_2 != '':
            new_url += self.convert_url_args_2
        all_data = ''
        while True:
            print new_url
            data = self.convert2data(new_url)
            if data != '' and data != None:
                all_data += data + '\n'
            elif data == '':
                if self.convert_page_to_end == False:
                    break
            step += self.convert_page_step
            if step > self.convert_page_max:
                break
            new_url = url + str(step)

        return all_data


    def convert2data(self, url):

        self.url_prefix = url[0 : url.find('/', url.find('//') + 2)]

            
        cmd, cmdShow = self.buildCmd('convert.py', url)
        data = subprocess.check_output(cmd, shell=True)

        return data.strip()


    def genHtml(self, data, divID, rID, resourceType, command='', fileName=''):

        
        html = ''
        start = False
        if self.convert_split_column_number == 0:
            html = '<div class="ref"><ol>'
            start = True
        count = 0
        records = []
        titles = ''
        debugSplitChar = '\n '
        noNumber = False
        desc = ''
        line_count = 0
        show_url_icon = False
        smartIcon = self.utils.getIconHtml('', title=self.convert_smart_engine, width=8, height=6)
        if smartIcon == '':
            smartIcon = self.utils.getIconHtml('url', width=8, height=6)

        datas = data.split('\n')

        if self.convert_top_item_number > 0 and len(datas) > self.convert_top_item_number:
            datas = datas[0 : self.convert_top_item_number]
        for line in datas:
            line = line.encode('utf-8')
            show_url_icon = False
            r = Record(line)
            smartLink = ''
            id = r.get_id().strip()
            title = r.get_title().strip().encode('utf-8')
            #title = self.customFormat(title)
                
            if self.convert_smart_engine != '':
                smartLink = self.utils.toQueryUrl(self.convert_smart_engine, title.lower().replace('"', '').replace("'", ''))
            
            if title.strip() == '':
                continue
            link = r.get_url().strip()
            if link != '' and self.convert_show_url_icon:
                show_url_icon = True

            if link != '' and link.startswith('http') == False:
                link = self.url_prefix + link
            elif link == '' and self.convert_smart_engine != '':
                link = smartLink

            desc = r.get_describe().strip()

            self.count += 1
            count += 1
            titles += title + debugSplitChar
            r = Record('convert-' + str(count) + ' | ' + title + ' | ' + link + ' | ' + desc)
            records.append(r)


            if link != '':
                title = '<a href="' + link + '" target="_blank">' + title + "</a>"
            else:
                title = self.utils.toSmartLink(title, br_number=self.convert_cut_max_len)

            if show_url_icon:
                title += self.utils.getIconHtml('url', width=8, height=6)

            if desc.find('icon:') != -1:
                icon = self.utils.reflection_call('record', 'WrapRecord', 'get_tag_content', r.line, {'tag' : 'icon'})

                title = ' <a href="javascript:void(0);" onclick="' + "openUrl('" + link + "', '" + link[link.rfind('/') + 1 :] + "', true, false, '" + rID + "', '" + resourceType + "', '', 'convert', '');" + '"><img width="48" height="48" src="' + icon + '"' + ' alt="' + r.get_title().strip() + '"  style="border-radius:10px 10px 10px 10px; opacity:0.7;"></a>'


            if self.convert_split_column_number > 0 and (self.count== 1 or self.count > self.convert_split_column_number):
                if start:
                    html += '</ol></div>'
                    self.count = 1
                
                line_count += 1
                if line_count == 3:
                    #html += '<br>'
                    line_count = 0

                heightAndWidthStyle = ''

                if self.convert_div_height_ratio > 0:
                    height = self.convert_split_column_number * self.convert_div_height_ratio
                    heightAndWidthStyle = 'height:' + str(height) + 'px;'
                if self.convert_div_width_ratio > 0 and self.convert_cut_max_len < 100:
                    width = self.convert_div_width_ratio * self.convert_cut_max_len
                    heightAndWidthStyle += ' width:' + str(width) + 'px; '

                html += '<div style="float:left; ' + heightAndWidthStyle + '"><ol>'
                noNumber = True
                start = True


            html += '<li>'
            if noNumber == False:
                html += '<span>' + str(count) + '.</span><p>'


            if link != '' and smartLink != '' and show_url_icon == False:

                title += '<a target="_blank" href="' + smartLink + '">' + smartIcon + '</a>'

            html += title

            ref_divID = divID + '-' + str(count)
            linkID = 'a-' + ref_divID[ref_divID.find('-') + 1 :]
            appendID = str(count)
            newTitle = self.customFormat(r.get_title().strip())

            if newTitle.find('<') != -1 and newTitle.find('>') != -1:
                newTitle = self.utils.clearHtmlTag(newTitle).replace('"', '').replace("'", '').replace('\n', ' ')
            script = self.utils.genMoreEnginScript(linkID, ref_divID, "loop-" + rID.replace(' ', '-') + '-' + str(appendID), newTitle, link, '-', hidenEnginSection=True)

            descHtml = ''
            if desc != '':
                descHtml = self.utils.genDescHtml(desc, Config.course_name_len, self.tag.tag_list, iconKeyword=True, fontScala=1, rid=rID)
            
            html += self.utils.genMoreEnginHtml(linkID, script.replace("'", '"'), '...', ref_divID, '', False, descHtml=descHtml);

            #html += '<br>'
            if noNumber == False:
                html += '</p>'
            html += '</li>'
            if noNumber:
                html += '<div style="height:6px;"></div>'
        if start:
            html += '</ol></div>'
        #html += "</ol></div>"
        #print '\n' + titles + '\n'


        if self.convert_output_data_to_new_tab:
            return self.utils.output2Disk(records, 'convert', self.form_dict['rTitle'], self.convert_output_data_format)
        else:
            if self.convert_output_data_to_temp and self.convert_output_data_to_new_tab == False:
                html = self.genCommandBox(command=command, fileName=fileName) + '<br>' + html

            return html

    def customFormat(self, text, cut=True):
        #text = text.replace('《','').replace('》', '').replace('"', '').replace("'", '')
        #return text[0 : text.find('/')].strip()

        if self.convert_cut_start != '' and text.find(self.convert_cut_start) != -1:
            text = text[text.find(self.convert_cut_start) + len(self.convert_cut_start) + self.convert_cut_start_offset :].strip()
        if self.convert_cut_end != '':
            text = text[0 : text.find(self.convert_cut_end) + self.convert_cut_end_offset].strip()

        if len(self.convert_remove) > 0:
            for remove in self.convert_remove:
                if text.lower().find(remove.lower()) != -1:
                    #print text
                    text = text.replace(remove, '').replace(remove.lower(), '').strip()
                    #print text
        if len(self.convert_replace.items()) > 0:
            for k, v in self.convert_replace.items():
                if text.lower().find(k.lower()) != -1:
                    text = text.replace(k, v).replace(k.lower(), v).strip()


        if self.convert_append != '':
            text = text + ' ' + self.convert_append 



        if len(text) > self.convert_cut_max_len and cut:
            text = text[0 : self.convert_cut_max_len]

        return text

    def check(self, form_dict):
        url = form_dict['url'].encode('utf8')
        return url != '' 
        #return url != '' and url.startswith('http') or (url.find('[') != -1 and url.find(']') != -1)
        #url = form_dict['url'].encode('utf8')
        #return url != "" and url.startswith('http')
