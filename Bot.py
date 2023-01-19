print('Copyright (C) 2022 @TEXCODER \n')
print('</ Upgrade /> To+ V:1.2.0  or @TEXSBOT \n\n')
import asyncio
import base64
import concurrent.futures
import datetime
import glob
import json
import math
import os
import pathlib
import random
from random import choice,randint
import sys
import time
from json import dumps, loads
from random import randint
import re
from re import findall
from rubika_lib import _date_time
import requests
import urllib3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from requests import post
from googletrans import Translator
import io
from PIL import Image , ImageFont, ImageDraw 
import arabic_reshaper
from bidi.algorithm import get_display
from mutagen.mp3 import MP3
from gtts import gTTS
from threading import Thread
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from difflib import SequenceMatcher

from api_rubika import Bot,encryption

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def hasInsult(msg):
	swData = [False,None]
	for i in open("dontReadMe.txt").read().split("\n"):
		if i in msg:
			swData = [True, i]
			break
		else: continue
	return swData

def hasAds(msg):
	links = list(map(lambda ID: ID.strip()[1:],findall("@[\w|_|\d]+", msg))) + list(map(lambda link:link.split("/")[-1],findall("rubika\.ir/\w+",msg)))
	joincORjoing = "joing" in msg or "joinc" in msg

	if joincORjoing: return joincORjoing
	else:
		for link in links:
			try:
				Type = bot.getInfoByUsername(link)["data"]["chat"]["abs_object"]["type"]
				if Type == "Channel":
					return True
			except KeyError: return False

def search_i(text,chat,bot):
    try:
        search = text[11:-1]
        if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':
            bot.sendMessage(chat['object_guid'], '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])                           
            jd = json.loads(requests.get('https://zarebin.ir/api/image/?q=' + search + '&chips=&page=1').text)
            jd = jd['results']
            a = 0
            for j in jd:
                if a <= 8:
                    try:
                        res = requests.get(j['image_link'])
                        if res.status_code == 200 and res.content != b'' and j['cdn_thumbnail'] != '':
                            thumb = str(j['cdn_thumbnail'])
                            thumb = thumb.split('data:image/')[1]
                            thumb = thumb.split(';')[0]
                            if thumb == 'png':
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.png', len(b2), 'png')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['last_message']['author_object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, j['title'] + '.png', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'])
                                print('sended file')
                            elif thumb == 'webp':
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.webp', len(b2), 'webp')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['last_message']['author_object_guid'] ,tx['id'] , 'webp', tx['dc_id'] , access, j['title'] + '.webp', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'])
                                print('sended file')
                            else:
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.jpg', len(b2), 'jpg')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['last_message']['author_object_guid'] ,tx['id'] , 'jpg', tx['dc_id'] , access, j['title'] + '.jpg', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'])
                                print('sended file')
                        a += 1
                    except:
                        print('image error')
                else:
                    break                                    
        elif chat['abs_object']['type'] == 'User':
            bot.sendMessage(chat['object_guid'], 'در حال یافتن کمی صبور باشید...', chat['last_message']['message_id'])
            print('search image')
            jd = json.loads(requests.get('https://zarebin.ir/api/image/?q=' + search + '&chips=&page=1').text)
            jd = jd['results']
            a = 0
            for j in jd:
                if a < 10:
                    try:                        
                        res = requests.get(j['image_link'])
                        if res.status_code == 200 and res.content != b'' and j['cdn_thumbnail'] != '' and j['cdn_thumbnail'].startswith('data:image'):
                            thumb = str(j['cdn_thumbnail'])
                            thumb = thumb.split('data:image/')[1]
                            thumb = thumb.split(';')[0]
                            if thumb == 'png':
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.png', len(b2), 'png')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, j['title'] + '.png', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'], chat['last_message']['message_id'])
                                print('sended file')
                            elif thumb == 'webp':
                                b2 = res.content
                                width, height = bot.getImageSize(b2)
                                tx = bot.requestFile(j['title'] + '.webp', len(b2), 'webp')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                bot.sendImage(chat['object_guid'] ,tx['id'] , 'webp', tx['dc_id'] , access, j['title'] + '.webp', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'], chat['last_message']['message_id'])
                                print('sended file')
                            else:
                                b2 = res.content
                                tx = bot.requestFile(j['title'] + '.jpg', len(b2), 'jpg')
                                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                                width, height = bot.getImageSize(b2)
                                bot.sendImage(chat['object_guid'] ,tx['id'] , 'jpg', tx['dc_id'] , access, j['title'] + '.jpg', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, j['title'], chat['last_message']['message_id'])
                                print('sended file')
                        a += 1  
                    except:
                        print('image erorr')
        return True
    except:
        print('image search err')
        return False

def write_image(text,chat,bot):
    try:
        c_id = chat['last_message']['message_id']
        msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
        msg_data = msg_data[0]
        if 'reply_to_message_id' in msg_data.keys():
            msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
            if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                txt_xt = msg_data['text']
                paramiters = text[8:-1]
                paramiters = paramiters.split(':')
                if len(paramiters) == 5:
                    b2 = bot.write_text_image(txt_xt,paramiters[0],int(paramiters[1]),str(paramiters[2]),int(paramiters[3]),int(paramiters[4]))
                    tx = bot.requestFile('code_image.png', len(b2), 'png')
                    access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                    width, height = bot.getImageSize(b2)
                    bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, 'code_image.png', len(b2) , str(bot.getThumbInline(b2))[2:-1] , width, height ,message_id= c_id)
                    print('sended file') 
                    return True
        return False	              
    except:
        print('server ban bug')
        return False

def uesr_remove(text,chat,bot):
    try:
        admins = [i["member_guid"] for i in bot.getGroupAdmins(chat['object_guid'])["data"]["in_chat_members"]]
        if chat['last_message']['author_object_guid'] in admins:
            c_id = chat['last_message']['message_id']
            msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
            msg_data = msg_data[0]
            if 'reply_to_message_id' in msg_data.keys():
                msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
                if not msg_data['author_object_guid'] in admins:
                    bot.banGroupMember(chat['object_guid'], msg_data['author_object_guid'])
                    bot.sendMessage(chat['object_guid'], 'کاربر حذف شد✅' , chat['last_message']['message_id'])
                    return True
        return False
    except:
        print('server ban bug')
        return False

def speak_after(text,chat,bot):
    try:
        c_id = chat['last_message']['message_id']
        msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
        msg_data = msg_data[0]
        if 'reply_to_message_id' in msg_data.keys():
            msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
            if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                txt_xt = msg_data['text']
                speech = gTTS(txt_xt)
                changed_voice = io.BytesIO()
                speech.write_to_fp(changed_voice)
                b2 = changed_voice.getvalue()
                tx = bot.requestFile('sound.ogg', len(b2), 'sound.ogg')
                access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                f = io.BytesIO()
                f.write(b2)
                f.seek(0)
                audio = MP3(f)
                dur = audio.info.length
                bot.sendVoice(chat['object_guid'],tx['id'] , 'ogg', tx['dc_id'] , access, 'sound.ogg', len(b2), dur * 1000 ,message_id= c_id)
                print('sended voice')
                return True
        return False
    except:
        print('server gtts bug')
        return False

def get_jok(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/jok/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
        return True
    except:
        print('code bz server err')
        
        
        return False

def get_hagh(text,chat,bot):
    try:                        
        jd = requests.get('http://haji-api.ir/angizeshi/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
        return True
    except:
        print('code bz server err')
        
        
        return False

def info_AmoBot(text,chat,bot):
    try:
        user_info = bot.getInfoByUsername(text[7:])	
        if user_info['data']['exist'] == True:
            if user_info['data']['type'] == 'User':
                bot.sendMessage(chat['object_guid'], '- 𝒏𝒂𝒎𝑬 𝒀𝒐𝒖 •🗿📒• | :\n  ' + user_info['data']['user']['first_name'] + ' ' + user_info['data']['user']['last_name'] + '\n\n- 𝒃𝒊𝒐 𝒚𝒐𝒖 •🥺💛• |:\n   ' + user_info['data']['user']['bio'] + '\n\n𝒈𝒖𝒊𝒅 𝒚𝒐𝒖 •🌚💙• |:\n  ' + user_info['data']['user']['user_guid'] , chat['last_message']['message_id'])
                print('sended response')
            else:
                bot.sendMessage(chat['object_guid'], 'کانال است' , chat['last_message']['message_id'])
                print('sended response')
        else:
            bot.sendMessage(chat['object_guid'], 'وجود ندارد' , chat['last_message']['message_id'])
            print('sended response')
        return True
    except:
        print('server bug6')
        return False

def search(text,chat,bot):
    try:
        search = text[9:-1]    
        if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':                               
            jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
            results = jd['results']['webs']
            text = ''
            for result in results:
                text += result['title'] + '\n\n'
            bot.sendMessage(chat['object_guid'], '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])
            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + search + ') : \n\n'+text)
        elif chat['abs_object']['type'] == 'User':
            jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
            results = jd['results']['webs']
            text = ''
            for result in results:
                text += result['title'] + '\n\n'
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
        return True
    except:
        print('search zarebin err')
        bot.sendMessage(chat['object_guid'], 'در حال حاضر این دستور محدود یا در حال تعمیر است' , chat['last_message']['message_id'])
        return False

def p_danesh(text,chat,bot):
    try:
        res = requests.get('http://api.codebazan.ir/danestani/pic/')
        if res.status_code == 200 and res.content != b'':
            b2 = res.content
            width, height = bot.getImageSize(b2)
            tx = bot.requestFile('jok_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), 'png')
            access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
            bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, 'jok_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, message_id=chat['last_message']['message_id'])
            print('sended file')                       
        return True
    except:
        print('code bz danesh api bug')
        return False

def photo_random(text,chat,bot):
    try:
        res = requests.get('http://haji-api.ir/photography/')
        if res.status_code == 200 and res.content != b'':
            b2 = res.content
            width, height = bot.getImageSize(b2)
            tx = bot.requestFile('random_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), 'png')
            access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
            bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, 'random_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, message_id=chat['last_message']['message_id'])
            print('sended file')                       
        return True
    except:
        print('code bz random api bug')
        return False
        
def photo_time(text,chat,bot):
    try:
        res = requests.get('https://www.far30club.ir/wp-content/uploads/2020/04/2-2-1.jpg')
        if res.status_code == 200 and res.content != b'':
            b2 = res.content
            width, height = bot.getImageSize(b2)
            tx = bot.requestFile('random_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), 'png')
            access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
            bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, 'random_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, message_id=chat['last_message']['message_id'])
            print('sended photo_time')                       
        return True
    except:
        print('code bz random api bug')
        return False

def koshamad(text,chat,bot):
    try:
        res = requests.get('http://viper-robot.ir/wp-content/uploads/2021/01/sdf123.jpg')
        if res.status_code == 200 and res.content != b'':
            b2 = res.content
            width, height = bot.getImageSize(b2)
            tx = bot.requestFile('random_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), 'png')
            access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
            bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, 'random_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, message_id=chat['last_message']['message_id'])
            print('sended photo_time')                       
        return True
    except:
        print('code bz random api bug')
        return False

def logo(text,chat,bot):
    try:
        res = requests.get('http://api2.haji-api.ir/ephoto360?type=text&id=23&text=')
        if res.status_code == 200 and res.content != b'':
            b2 = res.content
            width, height = bot.getImageSize(b2)
            tx = bot.requestFile('random_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), 'png')
            access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
            bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, 'random_'+ str(random.randint(1000000, 9999999)) + '.png', len(b2), str(bot.getThumbInline(b2))[2:-1] , width, height, message_id=chat['last_message']['message_id'])
            print('sended photo_time')                       
        return True
    except:
        print('code bz random api bug')
        return False

def anti_insult(text,chat,bot):
    try:
        admins = [i["member_guid"] for i in bot.getGroupAdmins(chat['object_guid'])["data"]["in_chat_members"]]
        if not chat['last_message']['author_object_guid'] in admins:
            print('yek ahmagh fohsh dad: ' + chat['last_message']['author_object_guid'])
            bot.deleteMessages(chat['object_guid'], [chat['last_message']['message_id']])
            return True
        return False
    except:
        print('delete the fohsh err')

def anti_tabligh(text,chat,bot):
    try:
        admins = [i["member_guid"] for i in bot.getGroupAdmins(chat['object_guid'])["data"]["in_chat_members"]]
        if not chat['last_message']['author_object_guid'] in admins:
            print('yek ahmagh tabligh kard: ' + chat['last_message']['author_object_guid'])
            bot.deleteMessages(chat['object_guid'], [chat['last_message']['message_id']])
            return True
        return False
    except:
        print('tabligh delete err')

def get_curruncy(text,chat,bot):
    try:
        t = json.loads(requests.get('https://api.codebazan.ir/arz/?type=arz').text)
        text = ''
        for i in t:
            price = i['price'].replace(',','')[:-1] + ' تومان'
            text += i['name'] + ' : ' + price + '\n'
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    except:
        print('code bz arz err')
    return True

def shot_image(text,chat,bot):
    try:
        c_id = chat['last_message']['message_id']
        msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
        msg_data = msg_data[0]
        if 'reply_to_message_id' in msg_data.keys():
            msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
            if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                txt_xt = msg_data['text']
                res = requests.get('https://api.otherapi.tk/carbon?type=create&code=' + txt_xt + '&theme=vscode')
                if res.status_code == 200 and res.content != b'':
                    b2 = res.content
                    tx = bot.requestFile('code_image.png', len(b2), 'png')
                    access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                    width, height = bot.getImageSize(b2)
                    bot.sendImage(chat['object_guid'] ,tx['id'] , 'png', tx['dc_id'] , access, 'code_image.png', len(b2) , str(bot.getThumbInline(b2))[2:-1] , width, height ,message_id= c_id)
                    print('sended file')    
    except:
        print('code bz shot err')
    return True

def get_ip(text,chat,bot):
    try:
        ip = text[5:-1]
        if hasInsult(ip)[0] == False:
            jd = json.loads(requests.get('https://api.codebazan.ir/ipinfo/?ip=' + ip).text)
            text = 'نام شرکت:\n' + jd['company'] + '\n\nکشور : \n' + jd['country_name'] + '\n\nارائه دهنده : ' + jd['isp']
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz ip err')  
    return True

def get_weather(text,chat,bot):
    try:
        city = text[10:-1]
        if hasInsult(city)[0] == False:
            jd = json.loads(requests.get('https://api.codebazan.ir/weather/?city=' + city).text)
            text = 'دما : \n'+jd['result']['دما'] + '\n سرعت باد:\n' + jd['result']['سرعت باد'] + '\n وضعیت هوا: \n' + jd['result']['وضعیت هوا'] + '\n\n بروز رسانی اطلاعات امروز: ' + jd['result']['به روز رسانی'] + '\n\nپیش بینی هوا فردا: \n  دما: ' + jd['فردا']['دما'] + '\n  وضعیت هوا : ' + jd['فردا']['وضعیت هوا']
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz weather err')
    return True

def get_whois(text,chat,bot):
    try:
        site = text[8:-1]
        jd = json.loads(requests.get('https://api.codebazan.ir/whois/index.php?type=json&domain=' + site).text)
        text = 'مالک : \n'+jd['owner'] + '\n\n آیپی:\n' + jd['ip'] + '\n\nآدرس مالک : \n' + jd['address'] + '\n\ndns1 : \n' + jd['dns']['1'] + '\ndns2 : \n' + jd['dns']['2'] 
        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz whois err')
    return True

def get_font(text,chat,bot):
    try:
        name_user = text[7:-1]
        jd = json.loads(requests.get('https://api.codebazan.ir/font/?text=' + name_user).text)
        jd = jd['result']
        text = ''
        for i in range(1,100):
            text += jd[str(i)] + '\n'
        if hasInsult(name_user)[0] == False and chat['abs_object']['type'] == 'Group':
            bot.sendMessage(chat['object_guid'], '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])
            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + name_user + ') : \n\n'+text)                                        
        elif chat['abs_object']['type'] == 'User':
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz font err')
    return True

def get_ping(text,chat,bot):
    try:
        site = text[7:-1]
        jd = requests.get('https://api.codebazan.ir/ping/?url=' + site).text
        text = str(jd)
        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz ping err')
    return True

def get_gold(text,chat,bot):
    try:
        r = json.loads(requests.get('https://www.wirexteam.ga/gold').text)
        change = str(r['data']['last_update'])
        r = r['gold']
        text = ''
        for o in r:
            text += o['name'] + ' : ' + o['nerkh_feli'] + '\n'
        text += '\n\nآخرین تغییر : ' + change
        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('gold server err')
    return True

def get_wiki(text,chat,bot):
    try:
        t = text[7:-1]
        t = t.split(':')
        mozoa = ''
        t2 = ''
        page = int(t[0])
        for i in range(1,len(t)):
            t2 += t[i]
        mozoa = t2
        if hasInsult(mozoa)[0] == False and chat['abs_object']['type'] == 'Group' and page > 0:
            text_t = requests.get('https://api.codebazan.ir/wiki/?search=' + mozoa).text
            if not 'codebazan.ir' in text_t:
                CLEANR = re.compile('<.*?>') 
                def cleanhtml(raw_html):
                    cleantext = re.sub(CLEANR, '', raw_html)
                    return cleantext
                text_t = cleanhtml(text_t)
                n = 4200
                text_t = text_t.strip()
                max_t = page * n
                min_t = max_t - n                                            
                text = text_t[min_t:max_t]
                bot.sendMessage(chat['object_guid'], 'مقاله "'+ mozoa + '" صفحه : ' + str(page) + '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])
                bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + mozoa + ') : \n\n'+text)
        elif chat['abs_object']['type'] == 'User' and page > 0:
            text_t = requests.get('https://api.codebazan.ir/wiki/?search=' + mozoa).text
            if not 'codebazan.ir' in text_t:
                CLEANR = re.compile('<.*?>') 
                def cleanhtml(raw_html):
                    cleantext = re.sub(CLEANR, '', raw_html)
                    return cleantext
                text_t = cleanhtml(text_t)
                n = 4200
                text_t = text_t.strip()
                max_t = page * n                                            
                min_t = max_t - n
                text = text_t[min_t:max_t]
                bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    except:
        print('code bz wiki err')
    return True

def get_deghat(text,chat,bot):
    try:                        
        jd = requests.get('https://haji-api.ir/deghat').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz deghat err')
    return True

def get_dastan(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/dastan/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz dastan err')
    return True   

def get_music(text,chat,bot):
    try:                        
        r = requests.get('http://api.codebazan.ir/arz/?type=arz')
        jd = r.json()['Result'][0]['name']
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('err')
    return True   

def get_arz(text,chat,bot):
    try:                        
        r = requests.get('http://api.codebazan.ir/music/?type=search&query=mamad&page=1')
        jd = jd['Result'][0]['Title']
        bot.sendMessage(chat['object_guid'], '😁♥️' + renn + '',chat['last_message']['message_id'])
        #bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('err')
    return True   

def get_search_k(text,chat,bot):
    try:
        search = text[11:-1]
        if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':                                
            jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
            results = jd['results']['webs']
            text = ''
            for result in results:
                text += result['title'] + ':\n\n  ' + str(result['description']).replace('</em>', '').replace('<em>', '').replace('(Meta Search Engine)', '').replace('&quot;', '').replace(' — ', '').replace(' AP', '') + '\n\n'
            bot.sendMessage(chat['object_guid'], '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])
            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + search + ') : \n\n'+text)
        elif chat['abs_object']['type'] == 'User':
            jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
            results = jd['results']['webs']
            text = ''
            for result in results:
                text += result['title'] + ':\n\n  ' + str(result['description']).replace('</em>', '').replace('<em>', '').replace('(Meta Search Engine)', '').replace('&quot;', '').replace(' — ', '').replace(' AP', '') + '\n\n'
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('zarebin search err')
    return True

def get_bio(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/bio/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz bio err')
    return True

def get_khabar(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/khabar/?kind=iran').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz khabar err')
    return True

def get_trans(text,chat,bot):
    try:
        t = text[8:-1]
        t = t.split(':')
        lang = t[0]
        t2 = ''
        for i in range(1,len(t)):
            t2 += t[i]
        text_trans = t2
        if hasInsult(text_trans)[0] == False:
            t = Translator()
            text = 'متن ترجمه شده به ('+lang + ') :\n\n' + t.translate(text_trans,lang).text
            jj = hasInsult(text)
            if jj[0] != True:
                bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
        elif chat['abs_object']['type'] == 'User':
            t = Translator()
            text = 'متن ترجمه شده به ('+lang + ') :\n\n' + t.translate(text_trans,lang).text
            jj = hasInsult(text)
            if jj[0] != True:
                bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    except:
        print('google trans err')
    return True

def get_khatere(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/jok/khatere/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz khatere err')
    return True

def get_danesh(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/danestani/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz danesh err')
    return True

def get_sebt(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/monasebat/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz sebt err')
    return True

def get_alaki_masala(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/jok/alaki-masalan/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz alaki masala err')
    return True

def get_hadis(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/hadis/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz hadis err')
    return True

def get_gang(text,chat,bot):
    try:                        
        jd = requests.get('https://haji-api.ir/gang').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz gang err')
    return True

def get_zeikr(text,chat,bot):
    try:                        
        jd = requests.get('https://haji-api.ir/zekr').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz zekr err')
    return True

def name_shakh(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/name/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz name err')

def get_qzal(text,chat,bot):
    try:                        
        jd = requests.get('https://api.codebazan.ir/ghazalsaadi/').text
        bot.sendMessage(chat['object_guid'], jd, chat['last_message']['message_id'])
    except:
        print('code bz qazal err')
    return True

def get_vaj(text,chat,bot):
    try:
        vaj = text[6:-1]
        if hasInsult(vaj)[0] == False:
            jd = json.loads(requests.get('https://api.codebazan.ir/vajehyab/?text=' + vaj).text)
            jd = jd['result']
            text = 'معنی : \n'+jd['mani'] + '\n\n لغتنامه معین:\n' + jd['Fmoein'] + '\n\nلغتنامه دهخدا : \n' + jd['Fdehkhoda'] + '\n\nمترادف و متضاد : ' + jd['motaradefmotezad']
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz vaj err')

def get_font_fa(text,chat,bot):
    try:
        site = text[10:-1]
        jd = json.loads(requests.get('https://api.codebazan.ir/font/?type=fa&text=' + site).text)
        jd = jd['Result']
        text = ''
        for i in range(1,10):
            text += jd[str(i)] + '\n'
        if hasInsult(site)[0] == False and chat['abs_object']['type'] == 'Group':
            bot.sendMessage(chat['object_guid'], '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])
            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + site + ') : \n\n'+text)                                        
        elif chat['abs_object']['type'] == 'User':
            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
    except:
        print('code bz font fa err')

def get_leaved(text,chat,bot):
    try:
        group = chat['abs_object']['title']
        date = _date_time.historyIran()
        time = _date_time.hourIran()
        send_text = '❌یک کاربر در تاریخ:\n' + date + '\n' + time + '\n از گروه  ' + group + ' لفت داد ❌\n @TEXSBOT | کانال رسمی عموبات'   
        bot.sendMessage(chat['object_guid'],  send_text, chat['last_message']['message_id'])
    except:
        print('rub server err')

def get_added(text,chat,bot):    
    try:
        group = chat['abs_object']['title']
        date = _date_time.historyIran()
        time = _date_time.hourIran()
        send_text = '✅یک کاربر در تاریخ:\n' + date + '\n' + time + '\n به گروه  ' + group + ' پیوست ✅\n @TEXSBOT | کانال رسمی عموبات'
        bot.sendMessage(chat['object_guid'],  send_text, chat['last_message']['message_id'])
    except:
        print('rub server err')

def get_help(text,chat,bot):                                
    text = open('help.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        #bot.sendMessage(chat['object_guid'], '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('help guid sended')
    
def get_grat(text,chat,bot):                                
    text = open('byb.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        #bot.sendMessage(chat['object_guid'], '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('help guid sended')
    
def get_listone(text,chat,bot):                                
    text = open('grat1.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        #bot.sendMessage(chat['object_guid'], '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('help guid sended')
    
def get_listtwo(text,chat,bot):                                
    text = open('grat2.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        #bot.sendMessage(chat['object_guid'], '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('help guid sended')

def get_car(text,chat,bot):                                
    text = open('Sargarmi.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        bot.sendMessage(chat['object_guid'], '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('sar guid sended')
def get_sargarmi(text,chat,bot):                                
    text = open('car.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        #bot.sendMessage(chat['object_guid'], '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('sar guid sended')
def get_srch(text,chat,bot):                                
    text = open('srch.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        #bot.sendMessage(chat['object_guid'], '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('srch guid sended')
    
def get_srch(text,chat,bot):                                
    text = open('srch.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        #bot.sendMessage(chat['object_guid'], '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('srch guid sended')
    
    #کاربردی
def gets_karborde(text,chat,bot):                                
    text = open('karborde.txt','r').read()
    if chat['abs_object']['type'] == 'Group':
        bot.sendMessage(chat['object_guid'], '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])
        bot.sendMessage(chat['last_message']['author_object_guid'], text)                                        
    elif chat['abs_object']['type'] == 'User':
        bot.sendMessage(chat['object_guid'], text, chat['last_message']['message_id'])
    print('karborde guid sended')
    
    #کاربردی

def usvl_save_data(text,chat,bot):
    jj = False
    while jj == False:
        try:
            c_id = chat['last_message']['message_id']
            msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
            msg_data = msg_data[0]
            if 'reply_to_message_id' in msg_data.keys():
                msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
                if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                    txt_xt = msg_data['text']
                    f3 = len(open('farsi-dic.json','rb').read())
                    if f3 < 83886080:
                        f2 = json.loads(open('farsi-dic.json','r').read())
                        if not txt_xt in f2.keys():
                            f2[txt_xt] = [text]
                        else:
                            if not text in f2[txt_xt]:
                                f2[txt_xt].append(text)
                        c1 = open('farsi-dic.json','w')
                        c1.write(json.dumps(f2))
                        c1.close
                    else:
                        bot.sendMessage(chat['object_guid'], '/usvl_stop') 
                        b2 = open('farsi-dic.json','rb').read()
                        tx = bot.requestFile('farsi-dic.json', len(b2), 'json')
                        access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
                        bot.sendFile(chat['object_guid'] ,tx['id'] , 'json', tx['dc_id'] , access, 'farsi-dic.json', len(b2), message_id=c_id)
                    jj = True
                    return True
            jj = True
        except:
            print('server rubika err')

def usvl_test_data(text,chat,bot):
    t = False
    while t == False:
        try:
            f2 = json.loads(open('farsi-dic.json','r').read())
            shebahat = 0.0
            a = 0
            shabih_tarin = None
            shabih_tarin2 = None
            for text2 in f2.keys():
                sh2 = similar(text, text2)
                if sh2 > shebahat:
                    shebahat = sh2
                    shabih_tarin = a
                    shabih_tarin2 = text2
                a += 1
            print('shabih tarin: ' + str(shabih_tarin) , '|| darsad shebaht :' + str(shebahat))
            if shabih_tarin2 != None and shebahat > .45:
                bot.sendMessage(chat['object_guid'], str(random.choice(f2[shabih_tarin2])), chat['last_message']['message_id'])
            t = True
        except:
            print('server rubika err')

def get_backup(text,chat,bot):
    try:
        b2 = open('farsi-dic.json','rb').read()
        tx = bot.requestFile('farsi-dic.json', len(b2), 'json')
        access = bot.fileUpload(b2, tx['access_hash_send'], tx['id'], tx['upload_url'])
        bot.sendFile(chat['object_guid'] ,tx['id'] , 'json', tx['dc_id'] , access, 'farsi-dic.json', len(b2), message_id=chat['last_message']['message_id'])
    except:
        print('back err')

def code_run(text,chat,bot,lang_id):
    try:
        c_id = chat['last_message']['message_id']
        msg_data = bot.getMessagesInfo(chat['object_guid'], [c_id])
        msg_data = msg_data[0]
        if 'reply_to_message_id' in msg_data.keys():
            msg_data = bot.getMessagesInfo(chat['object_guid'], [msg_data['reply_to_message_id']])[0]
            if 'text' in msg_data.keys() and msg_data['text'].strip() != '':
                txt_xt = msg_data['text']
                h = {
                    "Origin":"https://sourcesara.com",
                    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
                }
                p = requests.post('https://sourcesara.com/tryit_codes/runner.php',{'LanguageChoiceWrapper':lang_id,'Program':txt_xt},headers=h)
                p = p.json()
                jj = hasInsult(p['Result'])
                jj2 = hasInsult(p['Errors'])
                time_run = p['Stats'].split(',')[0].split(':')[1].strip()
                if jj[0] != True and jj2[0] != True:
                    if p['Errors'] != None:
                        if len(p['Result']) < 4200:
                            bot.sendMessage(chat['object_guid'], 'Code runned at '+ time_run +'\nErrors:\n' + p['Errors'] + '\n\nResponse:\n'+ p['Result'], chat['last_message']['message_id'])
                        else:
                            bot.sendMessage(chat['object_guid'], 'Code runned at '+ time_run +'\nErrors:\n' + p['Errors'] + '\n\nResponse:\nپاسخ بیش از حد تصور بزرگ است' , chat['last_message']['message_id'])
                    else:
                        if len(p['Result']) < 4200:
                            bot.sendMessage(chat['object_guid'], 'Code runned at '+ time_run +'\nResponse:\n'+ p['Result'], chat['last_message']['message_id'])
                        else:
                            bot.sendMessage(chat['object_guid'], 'Code runned at '+ time_run +'\nResponse:\nپاسخ بیش از حد تصور بزرگ است', chat['last_message']['message_id'])
    except:
        print('server code runer err')

g_usvl = ''
test_usvl = ''
auth = "eyzcgfelfohmjajctvmwjfhosdizfnhg"
#توکن
#Token
bot = Bot(auth)
list_message_seened = []
time_reset = random._floor(datetime.datetime.today().timestamp()) + 350
while(2 > 1):
    try:
        chats_list:list = bot.get_updates_all_chats()
        AmoBotAdmins = open('AmoBotAdmins.txt','r').read().split('\n')
        if chats_list != []:
            for chat in chats_list:
                access = chat['access']
                if chat['abs_object']['type'] == 'User' or chat['abs_object']['type'] == 'Group':
                    text:str = chat['last_message']['text']
                    if 'SendMessages' in access and chat['last_message']['type'] == 'Text' and text.strip() != '':
                        text = text.strip()
                        m_id = chat['object_guid'] + chat['last_message']['message_id']
                        if not m_id in list_message_seened:
                            print('new message')
                            if text == '!start' or text == '!Start' or text == 'start' or text == 'Start' or text == '!استارت' or text == 'استارت' or text == '/on' or text == '!on' or text == '!On' or text == '!ON' or text == 'روشن' or text == '/start' or text == '/Start':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'سلام به عموبات خوش اومدی 👋🏼\n' + '\n' + 'برای دریافت فهرست دستورات ربات\n' + '\n' ' /help ‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍ \n' + 'را بفرستید.\n' + '\n' + '🔹- user ad Bot @TEXSBOT 👹',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
#شروع متون
                            if text == 'گروه' or text == '/Group' or text == '/group':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '🔹لینکهایی که تاکنون ثبت شده‌اند🔹\n\n==========1==========\nhttps://rubika.ir/joing/CHGEDEHB0AONEJASLTHSCNMUKPUPPFZX\n=====================\nجهت ثبت ربات در گروه شما کلمه خرید رو به بات یا یکی از ایدی های زیر پیام بدهید🔹- user ad Bot @TEXCODER 👹',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'اصل' or text == 'اصل بده' or text == 'اشنا بشیم' or text == 'اصل پلیز' or text == 'معرفی کن' or text == 'کی هستی' or text == 'اصل پلیز':
                                print('message geted and sinned')
                                try:
                                    emoji = ["وای‍‌س‍‌ا ب‍‌ب‍‌ی‍‌ن‍‌م ت‍‌و ج‍‌ی‍‌ب‍‌م‍‌ه اع‍ پ‍‌ش‍‌ه پ‍‌ر ن‍‌م‍‌ی‍‌زن‍‌ه ت‍‌و ج‍‌ی‍ب‍‌م ک‍‌ه🗿💙","ربات هستم🥰","خیلی پرویی🤪😉","اسرار کن تا بگم😍😇"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'دا' or text == 'داداش' or text == 'داوش' or text == 'داپش' or text == 'داش':
                                print('message geted and sinned')
                                try:
                                    emoji = ["دخترم🙃","گلم من پسر نیستم😊","اگه با منی من پسر نیستم😉"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'هکرم' or text == 'تایپرم' or text == 'هکت میکنم' or text == 'فیلترت میکنم' or text == 'فیلت میکنم' or text == 'تویپرم':
                                print('message geted and sinned')
                                try:
                                    emoji = ["چرااا اخه؟🙃","میشه منم یاد بدی🥰","وای گرتمند😍"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'دختری؟' or text == 'سلام دختری؟' or text == 'دختر':
                                print('message geted and sinned')
                                try:
                                    emoji = ["بله عزیزم من دخترم😇😉","اره کاری داری؟😉🙃","با منی عشقم؟🤨"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'چخبر؟' or text == 'چخبرا؟' or text == 'چخبرا' or text == 'چخبر' or text == 'چه خبر' or text == 'چه خبر؟':
                                print('message geted and sinned')
                                try:
                                    emoji = ["سلامتی شما😉","سلامتی خودم🤪","س‍‌ل‍‌ام‍‌ت‍‌ی رُول‍‌م | ت‍‌و چ‍‌خ‍‌ب‍‌ر .🗿🗞️.","بی خبرم عزیز🤒","پر خبر میخوای برات تعریف کنم🤗","هیچی تو بگو گلم😉"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'شوخوش' or text == 'شوبخیر' or text == 'شب بخیر' or text == 'شب خوش' :
                                print('message geted and sinned')
                                try:
                                    emoji = ["شبت بخیر عزیزم خوابای خوب ببینی😉😘","جق نزنی ها!😂🙃","نری سوپر ببینی😇😜","نماز شب یادت نره😂😅","شبت شیک","میری بخوابی؟"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'چطوری؟' or text == 'چطوری' or text == 'چطوری تو؟' or text == 'حالت چطوره' :
                                print('message geted and sinned')
                                try:
                                    emoji = ["خوبم عزیزم😘","من عالیم😘","مرسی که به فکرمی🥰","خداروشکر خوبم 🖤"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'عه' or text == 'عه؟' or text == 'عه😐'  or text == 'عه؟😐😂' or text == 'عه😂' or text == 'عه😂😐':
                                print('message geted and sinned')
                                try:
                                    emoji = ["ب‍‌خ‍‌ور و ب‍‌ده 🗿","قلبمو شکستی😶","ن‍‌ه ب‍‌ه 🗿"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            if text == 'آها' or text == 'اها' or text == 'عاها' :
                                print('message geted and sinned')
                                try:
                                    emoji = ["چقدر بی احساسی تو💔","اله🤪","اهوم😝"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '/help' or text == 'دستورات' or text == 'help' :
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '🔴 ިߊ‌ܣـܝ̇ߺـܩߊ‌ܨ𝒯𝐸𝒳𝒮𝐵𝒪𝒯 - 𝓋𝑒𝓇 𝟣.𝟤\n\n📜 ܠࡅ࡙ܢܚࡅ߳ߺߺܙ ߊ‌ܢ̣ܝ̇‌ߊ‌ܝ‌ܣߊ‌ܨ ܝ‌ܢ̣ߊ‌ࡅ߳:\n/Commands \n\n💬 ܢܚܝ‌ویܚܓܩوࡅ߳وܝ‌ ܥܼܢܚࡅ߳ܥܼو:\n/search ‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍\n\n⚠ ܦ̈وߊ‌ܝ̇ߺیܔ ܝ‌ܢ̣ߊ‌ࡅ߳:\n/Rules \n\n⚙ ܭَܝ‌وܘ ܣߊ‌ܨ ܦ̇ܫߊ‌ܠܙ :\n/Group \n\n🔸 ܦ̇ܫߊ‌ܠܙ ܭܝ‌ܥ‌‌ܔ ܢܚܝ‌ویܚܓܢ̣ߊ‌ܝ̇‌ܨ :\n/Sargarmi ‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍‌‍‌‍‍‌‍‌‌‍‌‍‌‌‍‌‌‍‌‍‌‌‍‌‌‍‍‍‌‍‌‍‍‌‌‍‍‌‌‍‌‌‍‌‍‌‌‍‍‍‍‍‌‍‍‌‌‍‌‍‍‍‌‌‍‍‌‌‍‌‌‍‍‌‌‍‍‌‍‍‌‍\n\n🔹- 𝚞𝚜𝚎𝚛 𝚜𝚞𝚙𝚙𝚘𝚛𝚝 @TEXSBOT 👺', chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '😕' or text == '😕😕':
                                print('message geted and sinned')
                                try:
                                    emoji = ["اوخی چی شدی؟😕","نالاحتی؟☹️"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '🗿' or text == '🗿🗿' or text == '🗿🗿🗿' or text == '🗿🗿🗿🗿' or text == '🗿🗿🗿🗿🗿' or text == '🗿🗿🗿🗿🗿🗿':
                                print('message geted and sinned')
                                try:
                                    emoji = ["سید فاز کاک سنگی؟🤪","منم میتونم بفرستم🤨"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'رلپی' or text == 'رل پی' or text == 'رل میخام' or text == 'برلیم؟' or text == 'برلیم' or text == 'عاشقتم' or text == 'عشقم' or text == 'عشقمی' or text == 'دوست دارم':
                                print('message geted and sinned')
                                try:
                                    emoji = ["با من رل میزنی؟😉","ن‍‌ن‍‌ت ک‍‌ی‍‌س م‍‌ون‍‌اس‍‌ب‍‌ی ب‍‌رای #ک‍‌ردن اس‍‌ت | 🫂💛","خ‍‌ون‍‌ه ت‍‌ی‍‌م‍‌ی ک‍‌س‍‌ای م‍‌ف‍‌ت‍‌ی ه‍‌س ک‍‌ه •🗿💛•"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '😐😂' or text == '😂😐' or text == '😐🤣' or text == '🤣😐' or text == '😐😹' or text == '😹😐' or text == '😐😂🤣' or text == '🙂' or text == '🙃' or text == '😸':
                                print('message geted and sinned')
                                try:    
                                    emoji = ["تو فقط بخند من نگات کنم🙃🙂","منم میتونم باهات بخندم؟🤪🤪","عاشق خنده هاتم😘😇"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'وایجر' or text == 'وای جر' or text == 'جر' or text == 'وایجر😂' or text == 'وایجر😐😂' or text == 'جر😐😂' or text == 'جر😂😐' or text == 'جرر' or text == 'جر😂' or text == 'جر😐' or text == 'جر🤣':
                                print('message geted and sinned')
                                try:
                                    emoji = ["اخه چرا؟😂😅"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'ایجان' or text == 'ای جان' or text == 'عیجان' or text == 'عی جان':
                                print('message geted and sinned')
                                try:
                                    emoji = ["اوم بیبی🥰","ساچ واو😉"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'هن' or text == 'ها؟' or text == 'چی میگی' or text == 'چیمیگی' or text == 'چ میگی' or text == 'چمیگی' or text == 'چی؟' or text == 'چی':
                                print('message geted and sinned')
                                try:
                                    emoji = ["برو بابا😒","احمقی گلم؟😒😂","نفهم☹️","نادان😑"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'مشخصات' or text == 'اطلاعات':
                                print('message geted and sinned')
                                try:
                                    emoji = ["این چه شتی بود گفتی😂 😉","اطلاعت چی؟😂😂","فکر کردی من ربات؟ ناراحت شدم از دستت😒"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'آفرین' or text == 'افرین' or text == 'آفری' or text == 'افری' or text == 'ن خشم اومد' or text == 'خوشم میاد ازش' or text == 'ن خوشم اومد':
                                print('message geted and sinned')
                                try:
                                    emoji = ["مقسی🥰","ممنونم😉😍","عشق منی تو😘😇"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'خب' :
                                print('message geted and sinned')
                                try:
                                    emoji = ["قهمیدم شاخی😒☹️","خب به جمالت😒☹️"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'فقر' or text == 'فقیرم':
                                print('message geted and sinned')
                                try:
                                    emoji = ["انشاالله توهم پولدار میشی☹️💜","واقعا کمکی ازم بر نمیاد😞🥺"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'جستجو' or text == '/search':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'سرچ کامل متنے פּ سراسری:\n/srch  [AmoBot]\nبـہ جاے کلمـہ AmoBot موضوعتونو بنویسیـב.\n\nسرچ متن בر گوگل عنوانها:\n/srch-k  [AmoBot]\nܢ̣ܘ ܥܼߊ‌ܨ ܭܠܩܘ AmoBot ܩوضوܫࡅ߳وܝ̇ߺو ܢ̣ܝ̇ߺویܢܚیܥ‌‌.\n\nسرچ عکس בر گوگل :\n/srch-i  [AmoBot]\nبـہ جاے کلمـہ AmoBot موضوعتونو بنویسیـב.\n\nجستجو בر مقالـہ هاے ویکے پـבیا :\n/wiki-s  [AmoBot]\nبـہ جاے AmoBot موضوعتون رو بنویسیـב تمام مقالـہ هاے مرتبط براتون لیست میشـہ\n\nآورـבن متن مقالـہ از ویکے پـבیا :\nویکی [page:name]\npage صـ؋ـحـہ چنـבم مقالـہ رو بزاریـב مثلا 1 یعنے صـ؋ـحـہ اول פּ بـہ جاے name موضوع مقالتون פּ بعـב بـ؋ـرستیـב اگر اسم בقیق موضوع مقالتون رو نمیـבونیـב از בستور بعـבے جستجو اش کنیـב\n\n🔹- 𝚞𝚜𝚎𝚛 𝚜𝚞𝚙𝚙𝚘𝚛𝚝 @TEXSBOT👺', chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '🏳️‍🌈' or text == '💜💜':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'ریستارت' or text == 'ری استارت' or text == '/restart':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'واقعا که چی فکر کردی فکر کردی من باتم؟😒' + renn + '',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'LodinG...' or text == 'لودینگ':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'واقعا که چی فکر کردی فکر کردی من باتم؟😒' + renn + '',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'نه' or text == 'ن' or text == 'No' or text == 'no' or text == 'نع' or text == 'نح':
                                print('message geted and sinned')
                                try:
                                    emoji = ["دقیقاً چرا نه؟😶🤕","قلبمو شکستی دیگه دوست ندارم🖤💔"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '‌' or text == '‌‌' or text == '‌‌‌':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'عشقم این روش خوبی برای خودنمایی نیست❤️😶' + renn + '',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '♥️' or text == '💜' or text == '❤️' or text == '❣️' or text == '💘':
                                print('message geted and sinned')
                                try:
                                    emoji = ["امم بیقولمت😘🥰","بیا بگلم🤪😜","گ‍‌وزم‍‌ ب‍‌ا ق‍‌ل‍‌ب ت‍‌ق‍‌دی‍‌م ب‍‌ه ت‍‌و  🗿💨❤️"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'اره' or text == 'آره' or text == 'آرع' or text == 'ارع'or text == 'آرح' or text == 'ارح' or text == 'رح' or text == 'رع':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'آجر پاره😐🤣' + renn + '',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'کی' or text == 'کی؟':
                                print('message geted and sinned')
                                try:
                                    emoji = ["شوهرم😐","عمم😐","پدرم😑","ننه فرانکی😂"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '/Tools' or text == 'tool' or text == 'Tools' or text == '!Tools':  
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '🎮ܢܚــܝ‌ܭَـܝ‌ܩܨ ܣـߊ‌💸\n\n😂📣 ܥوܭ:\n/jok \n\n👻ܟܿߊ‌طܝ‌ܣ:\n/khatere \n\n🤓 جملات معروـ؋ـ\n/dialog \n\n😑 جوک الکے مثلا:\n/alaki \n\n📿 בانستنے بـہ صورت متن :\n/danesh  \n\n✏ّ️ّ جّمّلّاّتّ سّنّگّیّنّ :ّ\n/gang \n\n📿 ܥ̇‌‌ܭܝ‌ ܝ‌وܝ̇‌ߊ‌ܝ̇ߺܘ :\n/zekr \n\n🤔 בقت کرـבین؟ :\n/deghat \n\n🤠 בاستان:\n/dastan \n\n✏️ ܢ̣یوܭَܝ‌ߊ‌ܦ̇ܨ :\n/bio \n\n🖼 בانستنے بـہ صورت عکس :\n\n/danpic \n\n📊 مناسبت هاے ماه:\n/mont \n\n🔹- تمام בستورات این بخش بصورت ؋ـارسے هم کار میکننـב ماننـב (/jok=جوک)\n\n🔹-@TEXSBOT | کانال رسمے تکسبات' + renn + '',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '!listone' or text == '/listone':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '1. از چه چیزی بیشترین ترس را داری؟\n\n2. حال به هم زن ترین کاری که انجام دادی را بگو.\n\n3. اگر به گذشته برگردی چه چیزی را تغییر میدی؟\n\n4. آیا تا به حال مخفیانه از جیب سایر اعضای خانواده پول برداشتی؟\n\n5.  بزرگ ترین دروغی که تو زندگیت گفتی چی بوده؟\n6. از بیان چه اتفاقی تو زندگی شخصیت خجالت میکشی؟\n\n7. آخرین باری که دست داخل بینی ات کردی کی بود؟\n\n8.  احمقانه ترین کاری که در حمل و نقل عمومی انجام داده ای، چیست؟\n\n9. اگر به مدت یک ماه جنس مخالف خود بودی چه کارهایی می کردی؟\n\n10. از چه شخصی در زندگی بیشترین نفرت را داری؟\n\n11. اگر می خواستی یک نفر از این جمع را به عنوان عشقت انتخاب کنی چه کسی را انتخاب می کردی؟\n\n12. احمقانه ترین اعتیاد یا وابستگی که داری چیست؟\n\n13. نظرت در رابطه با ازدواج چیست؟\n\n14. شرم آورترین شی موجود در اتاقت چیست؟\n\n15. آیا تا به حال شکست عشقی خورده ای؟ چه زمانی و چرا؟\n\n16. احمقانه ترین کاری که تا به حال کرده ای چه بوده است؟\n\n17. آیا رازی داری که تا به حال به هیچ کس نگفته باشی؟\n\n18. نفرت انگیزترین عادت تو چیست؟\n\n19. آخرین باری که عذرخواهی کردی چه موقع بوده است؟ \n\n20. به من چیزی بگو که نمی خواهی بدانم.\n\n21. شرم آورترین لحظه زندگی ات کدام لحظه بوده است؟\n\n22. آیا تا به حال از شدت خنده خودت را خیس کردی؟\n\n24. کدام کار است که اگر همه پول های دنیا را هم به تو بدهند انجام نمی دهی؟\n\n25. یکی از رفتارهایت که دوست داری تغییر بدهی چیست؟\n\n26. بدترین شوخی که با کسی داشته ای چه بوده است؟\n\n27. اگر نامرئی شوی اولین کاری که انجام می دهی چیست؟\n\n28. اگر مجبور باشی در یک جزیره به تنهایی با یک نفر زندگی کنی چه کسی را انتخاب می کنی؟\n\n29. احمقانه ترین حرفی که در لحظات عاشقانه به همسرت زده ای چه بوده است؟\n\n30. اسم کسی را بگو که وانمود می کنی دوستش داری اما در واقع چشم دیدنش را نداری؟\n\n31. دردناک ترین تجربه جسمی ات چه بوده است؟\n\n32. اگر غول چراغ جادو داشته باشی سه آرزویت چیست؟\n\n33. احمقانه ترین کاری که مقابل آینه انجام داده ای چه کاری بوده است؟\n\n34. بیشتر از همه به چه کسی حسادت می کنی؟\n\n35. اگر مطمئن باشی هیچ وقت زندانی نمی شوی دوست داری چه کسی را بکشی؟\n\n36. آیا تا به حال درباره سن خود دروغ گفته ای؟\n\n37. اگر می توانستی یک قانون را حذف کنی یا یک قانون جدید وضع کنی، این قانون چیست و چرا؟\n\n38. به کدام عضو بدن خودت علاقه داری و از کدام متنفر هستی؟\n\n40. آخرین باری که گریه کردی چه زمانی بود؟\n\n41. تا حالا مواد مخدر مصرف کردی؟\n\n42. بهترین روز زندگی ات چه روزی بوده است؟\n\n43. ترسناک ترین اتفاقی که برایت افتاده چیست؟\n\n44. آخرین چیزی که در گوگل سرچ کرده ای چه بوده است؟\n\n45. اگر یک حیوان بودی چه حیوانی بودی؟\n\n46. بدترین کاری که در مقابل چشم مردم انجام داده ای چه بوده است؟\n\n47. اولین باری که به کسی گفتی دوستت دارم چه زمانی و چه کسی بوده است؟\n\n48. آیا شب ها با لباس زیر می خوابی؟\n\n51. آخرین کاری که برای اولین بار انجام دادی چیست؟\n\n52. چه کاری را دوست داری حتما قبل از مرگ انجام دهی؟\n\n54. آیا تاکنون قانونی را نقض کرده اید؟\n\n55. از چه چیز یا چه کسی فوبیا داری؟\n\n56. دو موردی که می خواهی در مورد شخصی که دوستش داری بدانی چیست؟\n\n57. کدام لحظه را خنده دار ترین لحظه زندگی ات می دانی؟', chat['last_message']['message_id'])
                                    bot.sendMessage(chat['object_guid'], 'تعداد 57 تا سوال فرستاده شد اگه دوست دارید بازی شروع شود ابتدا 4 نفر با انتخاب اعداد 1 تا 4 وارد بازی شوند و سپس کلمه [بپرس] را ارسال کنید.', chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'ریدم' or text == 'ریدوم':
                                print('message geted and sinned')
                                try:
                                    emoji = ["واقعا که حالمو بد کردی😒😖","بی ادب😂🤨"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1') 
                            if text == 'بپرس' or text == 'بپ':
                                print('message geted and sinned')
                                try:
                                    emoji = ["۱۰🔓وقتی عصبانی هستی چجوری میشی؟","۱۱🔓دوس داری کیو بزنی یا بکشی؟","۱۲🔓دوس داری کیو بوس کنی؟😉💋","۱۳🔓از تو گالریت عکس بده","۱۴🔓از مخاطبینت عکس بده","۱۵🔓از صفحه چت روبیکات عکس بده","۱۶🔓لباس زیرت چه رنگیه؟🙊","۲۰🔓تالا بهت تجاوز شده؟😥","۲۲🔓تاحالا یه دخترو بردی خونتون؟","۲۳🔓تاحالا یه پسرو بردی خونتون؟","۲۴🔓با کی ل....ب گرفتی؟😜","۲۵🔓خود ار.ض..ای..ی کردی؟😬💦","۵۱🔓تاحالا کسی ل..خ....ت تورو دیده؟🤭","1. از چه چیزی بیشترین ترس را داری؟","2. حال به هم زن ترین کاری که انجام دادی را بگو.","3. اگر به گذشته برگردی چه چیزی را تغییر میدی؟","4. آیا تا به حال مخفیانه از جیب سایر اعضای خانواده پول برداشتی؟","5.  بزرگ ترین دروغی که تو زندگیت گفتی چی بوده؟","6. از بیان چه اتفاقی تو زندگی شخصیت خجالت میکشی؟","7. آخرین باری که دست داخل بینی ات کردی کی بود؟","8.  احمقانه ترین کاری که در حمل و نقل عمومی انجام داده ای، چیست؟","9. اگر به مدت یک ماه جنس مخالف خود بودی چه کارهایی می کردی؟","10. از چه شخصی در زندگی بیشترین نفرت را داری؟","11. اگر می خواستی یک نفر از این جمع را به عنوان عشقت انتخاب کنی چه کسی را انتخاب می کردی؟","12. احمقانه ترین اعتیاد یا وابستگی که داری چیست؟","13. نظرت در رابطه با ازدواج چیست؟\n\n14. شرم آورترین شی موجود در اتاقت چیست؟","15. آیا تا به حال شکست عشقی خورده ای؟ چه زمانی و چرا؟","16. احمقانه ترین کاری که تا به حال کرده ای چه بوده است؟","17. آیا رازی داری که تا به حال به هیچ کس نگفته باشی؟","18. نفرت انگیزترین عادت تو چیست؟","19. آخرین باری که عذرخواهی کردی چه موقع بوده است؟ ","20. به من چیزی بگو که نمی خواهی بدانم.","21. شرم آورترین لحظه زندگی ات کدام لحظه بوده است؟","22. آیا تا به حال از شدت خنده خودت را خیس کردی؟","24. کدام کار است که اگر همه پول های دنیا را هم به تو بدهند انجام نمی دهی؟","65. خجالت آورترین خاطره کودکی ات چیست؟","67. بدترین رازت را بگو؟","70. بدترین قرارت با یک دختر / پسر چطوری بود؟","74. به نظر شما کدام بهتر است داشتن پول یا دوست و خانواده؟","76. می توانی یک هفته را بدون تلفن همراه بگذرانی؟"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1') 
                            if text == 'سلام دا' or text == 'سلام داش' or text == 'سلام داداش':
                                print('message geted and sinned')
                                try:
                                    emoji = ["عشقم مگه نمیدونی من دخترم🙃😉","اه پسر نیستم دخترم😒😤","دخترم😇"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1') 
                            if text == 'جالب' or text == 'عالی' or text == 'گانگ' or text == 'گنگ' or text == 'جذاب':
                                print('message geted and sinned')
                                try:
                                    emoji = ["بسیارم عالی😶","مگه غیر اینم هست؟🤒"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'کص میگی' or text == 'کصمیگی' or text == 'کسمیگی' or text == 'کس میگی':
                                print('message geted and sinned')
                                try:
                                    emoji = ["احمق توی گروه چرا این حرف رو میزنی؟😶","بی تر ادب😂"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')   
                            if text == 'رباتی؟' or text == 'رباتی' or text == 'ربات هستی؟' or text == 'رباط هستی؟':
                                print('message geted and sinned')
                                try:
                                    emoji = ["واقعا که به من میگی ربات😒😤","احمق نمیبینی انسانم😒","اوسکل به من میگه بات اسم من هلنا هست☹️"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'هلن' or text == 'هلنا' or text == 'هلنننن' or text == 'هلناا':
                                print('message geted and sinned')
                                try:
                                    emoji = ["جان عشقم؟🥰😍","منو صدا کردی گلم؟🥰😇","ای جان اقاییم صدام کرد🤪😜"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'خوبه' or text == 'عالیه':
                                print('message geted and sinned')
                                try:
                                    emoji = ["خوب چیه اسن عالی","فقد همین؟😒"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '😐🚶' or text == '😐🚶‍♀️' or text == '😐🚶🏿‍♀' or text == '😐🚶🏿‍♂' or text == '🚶' or text == '🚶‍♀️':
                                print('message geted and sinned')
                                try:
                                    emoji = ["خب که چی؟","منطورت از این ایموجی چی هست؟"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '؟' or text == '؟؟' or text == '?' or text == '??' or text == '?!' or text == '؟!':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'فاز پرسشی برداشته😏😂' + renn + '',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '!' or text == '!!' or text == '!!!':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'عجب🗿' + renn + '',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'عجب' or text == 'اجب' or text == 'عجب😐😂' or text == 'عجب😂😐' or text == 'عجب😐' or text == 'عجب😂':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'ب‍‌ک‍‌ی‍‌ر ن‍‌داش‍‌ت‍‌ه م‍‌ش رج‍‌ب🗿💛' + renn + '',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'رباته؟😐' or text == 'رباته؟' or text == 'رباته؟😐😂' or text == 'رباته😂😐' or text == 'ربات نی' or text == 'ربات نیست':
                                print('message geted and sinned')
                                try:
                                    emoji = ["برو گشمو بابا🙄","نه پدرتم","نه احمق برای باز هزارم من ربات نیستم هلنا هستم🤕","چرا همه فک میکنن من رباتم؟😂😐"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '/listtwo' or text == '!listtwo':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '۱🔓عاشق شدی؟اسمش❤️\n\n۲🔓رل زدی تاحالا؟اسمش\n\n۳🔓کراش داری؟اسمش\n\n۴🔓چند بار تا الان رابطه جنسی داشتی؟با کی😐💦\n\n۵🔓از کی خوشت میاد؟\n\n۶🔓از کی بدت میاد؟\n\n۷🔓منو دوس داری؟بهم ثابت کن\n\n۸🔓کی دلتو شکونده؟\n\n۹🔓دل کیو شکوندی؟\n\n۱۰🔓وقتی عصبانی هستی چجوری میشی؟\n\n۱۱🔓دوس داری کیو بزنی یا بکشی؟\n\n۱۲🔓دوس داری کیو بوس کنی؟😉💋\n\n۱۳🔓از تو گالریت عکس بده\n\n۱۴🔓از مخاطبینت عکس بده\n\n۱۵🔓از صفحه چت روبیکات عکس بده\n\n۱۶🔓لباس زیرت چه رنگیه؟🙊\n\n۱۷🔓از وسایل آرایشت عکس بده\n\n۱۸🔓از لباسای کمدت عکس بده\n\n۱۹🔓از کفشات عکس بده\n\n۲۰🔓تالا بهت تجاوز شده؟😥\n\n۲۱🔓تاحالا مجبور شدی به زور به کسی بگی دوست دارم؟\n\n۲۲🔓تاحالا یه دخترو بردی خونتون؟\n\n۲۳🔓تاحالا یه پسرو بردی خونتون؟\n\n۲۴🔓با کی ل....ب گرفتی؟😜\n\n۲۵🔓خود ار.ض..ای..ی کردی؟😬💦\n\n۲۶🔓خانوادت یا رفیقت یا عشقت؟\n\n۲۷🔓سلامتی یا علم یا پول؟\n\n۲۸🔓شهوتی شدی تاحالا؟😂\n\n۲۹🔓خونتون کجاس؟\n\n۳۰🔓خاستگار داری؟عکسش یا اسمش\n\n۳۱🔓به کی اعتماد داری؟\n\n۳۲🔓تاحالا با کسی رفتی تو خونه خالی؟\n\n۳۳🔓چاقی یا لاغر؟\n\n۳۴🔓قد بلندی یا کوتاه؟\n\n۳۵🔓رنگ چشمت؟\n\n۳۶🔓رنگ موهات؟\n\n۳۷🔓موهات فرفریه یا صاف و تا کجاته؟\n\n۳۸🔓تاریخ تولدت؟\n\n۳۹🔓تاریخ تولد عشقت؟\n\n۴۰🔓عشقت چجوری باهات رفتار میکنه؟\n\n۴۱🔓با دوس پسرت عشق بازی کردی؟🤤\n\n۴۲🔓پیش عشقت خوابیدی؟\n\n۴۳🔓عشقتو بغل کردی؟\n\n۴۴🔓حاضری ۱۰ سال از عمرتو بدی به عشقت؟\n\n۴۵🔓مامان و بابات چقد دوست دارن؟\n\n۴۶🔓دعوا کردی؟\n\n۴۸🔓چند بار کتک زدی؟\n\n۴۹🔓چند بار کتک خوردی؟\n\n۵۰🔓تاحالا تورو دزدیدن؟\n\n۵۱🔓تاحالا کسی ل..خ....ت تورو دیده؟🤭\n\n۵۲🔓تاحالا ل...خ...ت کسیا دیدی؟\n\n۵۳🔓دست نام....حرم بهت خورده؟\n\n\n۵۴🔓دلت برا کی تنگ شده؟\n\n۵۵🔓دوس داشتی کجا بودی؟\n\n۵۶🔓به خودکشی فکر کردی؟\n\n۵۷🔓عکستو بده\n\n۵۸🔓ممه هات بزرگ شدن؟🙈\n\n۵۹🔓با دیدن بدن خودت ح...ش....ری میشی؟\n\n۶۰🔓پیش کسی ضایع شدی؟\n\n۶۱🔓از مدرسه فرار کردی؟' + renn + '',chat['last_message']['message_id'])
                                    bot.sendMessage(chat['object_guid'], 'تعداد 61 تا سوال فرستاده شد اگه دوست دارید بازی شروع شود ابتدا 4 نفر با انتخاب اعداد 1 تا 4 وارد بازی شوند و سپس کلمه [بپرس] را ارل کنید.' + renn + '',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'چنل' or text == 'پشتیبانی':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '🔹- user support @TEXBOT 👺\n' + '🔹- user ad Bot @TEXSBOT 👹' + renn + '',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'کسمادرت' or text == 'کس مادرت' or text == 'کصمادرت' or text == 'کص مادرت' or text == 'مادر جنده':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'فحاشی ممنوع😐🤐' + renn + '',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'جون' or text == 'جان':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'بخورمت😐😂' + renn + '',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '/Rules' or text == 'قوانین' or text.startswith('[قوانین]'):
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], '📁• قوانین گروه •\n📁• فحش و لینک ممنوع \n📁• تبلیغات ممنوع \n📁• توهین به کاربران و ادمین ها ممنوع\n📁• دستورات مستهجن به ربات ممنوع\n🗑• در صورت مشاهده و زیر پا گذاشتن قوانین فورا شما از گروه حذف میشوید!\nمشکلی داشتی پیوی ادمین:@TEXSBOT',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'عجیبه' or text == 'اجیبه' or text == 'اجیب است' or text == 'عجیب'  or text == 'عجیب است':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'بسیار عجیب🗿🔥' + renn + '',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'کسی نی؟' or text == 'کسی نی' or text == 'کسی نیست' or text == 'نی کسی'  or text == 'نیست کسی؟' or text == 'نیست کسی':
                                print('message geted and sinned')
                                try:
                                    emoji = ["چرا من هستم😶","منو تو تنهاییم😉","واقعا که منو نمیبینی؟😇🙃"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'رباتم میشی' or text == 'ربات میخام' or text == 'بات میخام' or text == 'خرید ربات' or text == 'ربات گپم میشی':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'عزیزم ربات نیستم اما اگه خواستی با اندکی پول میتونی منو بیاری به گپت😂😐\nپیوی سازندم:@TEXCODER',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'کیه شاهرخ' or text == 'کیه شاهرخ؟' or text == 'سازنده' or text == 'سازندت کیه' or text == 'سازندت کیه؟':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'اگا شاهرخ:@TEXCODER' + renn + '',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'س' or text == 'ص' or text == 'صلام'  or text == 'سلام' or text == 'سلم' or text == 'صلم' or text == 'سل' or text == 'صل':
                                print('message geted and sinned')
                                try:
                                    emoji = ["ه‍‌وم🧸🗞️","ب‍‌ن‍‌ال‍","ب‍‌ل🥺💛","ج‍‌ون🌚💛  ","زی‍‌بام🥺","ع‍‌س‍‌ل‍‌م🧸📒","چس‍‌ک‍‌م🪣 ","🙁💛بگوز",]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'خبی؟' or text == 'خبی' or text == 'خوبی؟' or text == 'خوبی':
                                print('message geted and sinned')
                                try:
                                    emoji = ["خ‍‌اس‍‌ت‍‌م ک‍‌ص‍‌ل‍‌ی‍‌س‍‌ام‍‌و ب‍‌ی‍‌نم‍ ک‍‌ه دی‍‌دم اخ‍‌ه ب‍ ت‍‌ چ‍ ک‍ص‍‌و؟🗿📒️️","بله🥰","شما خوب باشی ماهم بد نیستم🙃🙂","به خوبی تو😘","ج‍‌ی‍‌ن‍‌دا ع‍‌اول‍‌ی‍‌م ت‍‌و چی‍‌دوری‍ •🌚💛•"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '.' or text == '..':
                                print('message geted and sinned')
                                try:
                                    emoji = ["نت نداری؟😐😂","ایا شماهم از باگ روبیکا رنج میبرید؟"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'شکر' or text == 'شک':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'سلامت باشی😁♥️🔥' + renn + '',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '😞' or text == '🙁' or text == '😔' or text == '☹' or text == '️😣' or text == '😖' or text == '😫' or text == '😩' or text == '😭' or text == '🤕' or text == '💔' or text == '😓' or text == '😟' or text == '😰' or text == '🤒' or text == '😥' or text == '😢':
                                print('message geted and sinned')
                                try:    
                                    emoji = ["اوخی چی شدی؟","نبینم ناراحت باشی","ناراحت شدم","چیزی  شده؟"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'نمال' or text == 'بمال' or text == 'کصکش' or text == 'کسکش':
                                print('message geted and sinned')
                                try:
                                    emoji = ["منو با پیدرت اشتباه گرفتی😒","خودتی🤪"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'کسنگو' or text == 'کس نگو' or text == 'کصنگو' or text == 'کص نگو':
                                print('message geted and sinned')
                                try:
                                    emoji = ["اهمیت نمیدم فشار بخور😶","صدبار گفتم کس اگه گفتنی بود تو الان اینجا نبودی😤"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], '🗿♥️' + renn + '',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '😐😐😐😐' or text == '😐😐😐' or text == '😐😐' or text == '😐':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'ها چه مرگته؟😐' + renn + '',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'بای' or text == 'بحی' or text == 'خداحافظ' or text == 'فعلن' or text == 'فعلا' or text == 'فعلاً':
                                print('message geted and sinned')
                                try:
                                    emoji = ["کجا میری دلم واست تنگ میشه","میشه نری؟","تو چرا میری؟","اگه بری دیگه باهات حرف نمیزنم"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'اخی' or text == 'آخی' or text == 'اوخی' or text == 'اوخ':
                                print('message geted and sinned')
                                try:
                                    emoji = ["بچگانه حرف نزن","لوس","بچه مامانی"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '😂' or text == '😂😂' or text == '😂😂😂' or text == '😂😂😂😂' or text == '😂😂😂😂😂':
                                print('message geted and sinned')
                                try:
                                    emoji = ["جون توفقط بخند","عاشق خندهاتم","جون خندهاشو"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '🤣' or text == '🤣🤣' or text == '🤣🤣🤣' or text == '🤣🤣🤣🤣' or text == '🤣🤣🤣🤣🤣':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'جر نخوری یک وقت😐🤣' + renn + '',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'ربات' or text == 'بات' or text == 'روبات' or text == 'رب' or text == 'ربا'  or text == '!bot' or text == 'ربات جون' or text == 'بات جون' or text == 'ربات جان' or text == 'بات جان' or text == 'بات😐😂' or text == 'ربات😐😂' or text == 'بات😐' or text == 'ربات😐' or text == 'ربات جونم' or text == 'بات جونم':
                                print('message geted and sinned')
                                try:
                                    emoji = ["برو گشمو بابا🙄","نه پدرتم","نه احمق برای باز هزارم من ربات نیستم هلنا هستم🤕","چرا همه فک میکنن من رباتم؟😂😐"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'هعب' or text == 'هعی' or text == 'هیب' or text == 'هعپ' or text == 'هب' or text == 'هی روزگار' or text == 'هب':
                                print('message geted and sinned')
                                try:
                                    bot.sendMessage(chat['object_guid'], 'روزگ‍‌ار ن‍‌ازن‍‌ی‍‌ن #ت‍‌ف💦 ب‍‌زن‍‌م ی‍‌ا #وازل‍‌ی‍‌ن🗿🫂' + renn + '',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'من خودام' or text == 'من خدام' or text == 'خودام' or text == 'خدام':
                                print('message geted and sinned')
                                try:
                                    emoji = ["بچه بیا پایین کسشر نگو سرمون درد گرفت","خیلی تاثیر گذار بود","بچه سال"]
                                    renn= choice(emoji)
                                    bot.sendMessage(chat['object_guid'], renn ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
#اتمام متون
                            if text == '!zaman' or text == '/zaman' or text == 'زمان' :
                                print('message geted and sinned')
                                try:
                                    date = _date_time.historyIran()
                                    time = _date_time.hourIran()

                                    bot.sendMessage(chat['object_guid'], 'تاریخ: \n' + date + '\nساعت:\n'+ time,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '!date' or text == 'تاریخ' or text == '/date' :
                                print('message geted and sinned')
                                try:
                                    date = _date_time.historyIran()

                                    bot.sendMessage(chat['object_guid'], 'تاریخ \n' + date ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == '/time' or text == '/Time' or text == 'ساعت' or text == 'تایم' :
                                print('message geted and sinned')
                                try:
                                    time = _date_time.hourIran()

                                    bot.sendMessage(chat['object_guid'], 'ساعت  \n' + time ,chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'منم خبم' or text == 'منم خوبم' or text == 'منم خبمح' or text == 'خوبم' or text == 'خبم' or text == 'خبمح':
                                print('message geted and sinned')
                                try:

                                    bot.sendMessage(chat['object_guid'], 'شٌکر خوب بمونی' + renn + '',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                            if text == 'تست' or text == 'test' or text == '!test' or text == '/test' or text == '/Test' or text == '!Test':
                                print('message geted and sinned')
                                try:

                                    bot.sendMessage(chat['object_guid'], '@TEXSBOT on' + renn + '',chat['last_message']['message_id'])
                                    print('sended response')    
                                except:
                                    print('server bug1')
                                    
                            elif text.startswith('/nim http://') == True or text.startswith('/nim https://') == True:
                                try:
                                    bot.sendMessage(chat['object_guid'], "در حال آماده سازی لینک ...",chat['last_message']['message_id'])
                                    print('sended response')
                                    link = text[4:]
                                    nim_baha_link=requests.post("https://www.digitalbam.ir/DirectLinkDownloader/Download",params={'downloadUri':link})
                                    pg:str = nim_baha_link.text
                                    pg = pg.split('{"fileUrl":"')
                                    pg = pg[1]
                                    pg = pg.split('","message":""}')
                                    pg = pg[0]
                                    nim_baha = pg    
                                    try:
                                        bot.sendMessage(chat['object_guid'], 'لینک نیم بها شما با موفقیت آماده شد ✅ \n لینک : \n' + nim_baha ,chat['last_message']['message_id'])
                                        print('sended response')    
                                    except:
                                        print('server bug2')
                                except:
                                    print('server bug3')
                            elif text.startswith('/info @'):
                                tawd10 = Thread(target=info_AmoBot, args=(text, chat, bot,))
                                tawd10.start()
                            elif text.startswith('/srch ['):
                                tawd11 = Thread(target=search, args=(text, chat, bot,))
                                tawd11.start()
                            elif text.startswith('/wiki-s ['):
                                try:
                                    search = text[9:-1]    
                                    search = search + 'ویکی پدیا'
                                    if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':                               
                                        jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
                                        results = jd['results']['webs'][0:4]
                                        text = ''
                                        for result in results:
                                            if ' - ویکی‌پدیا، دانشنامهٔ آزاد' in result['title']:
                                                title = result['title'].replace(' - ویکی‌پدیا، دانشنامهٔ آزاد','')
                                                text += title + ' :\n\n' + str(result['description']).replace('</em>', '').replace('<em>', '').replace('(Meta Search Engine)', '').replace('&quot;', '').replace(' — ', '').replace(' AP', '') + '\n\nمقاله کامل صفحه 1 : \n' + '/wiki [1:' + title + ']\n\n' 
                                        bot.sendMessage(chat['object_guid'], 'نتایج کامل به پیوی شما ارسال شد', chat['last_message']['message_id'])
                                        bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + search + ') : \n\n'+text)
                                    elif chat['abs_object']['type'] == 'User':
                                        jd = json.loads(requests.get('https://zarebin.ir/api/?q=' + search + '&page=1&limit=10').text)
                                        results = jd['results']['webs'][0:4]
                                        text = ''
                                        for result in results:
                                            if ' - ویکی‌پدیا، دانشنامهٔ آزاد' in result['title']:
                                                title = result['title'].replace(' - ویکی‌پدیا، دانشنامهٔ آزاد','')
                                                text += title + ' :\n\n' + str(result['description']).replace('</em>', '').replace('<em>', '').replace('(Meta Search Engine)', '').replace('&quot;', '').replace(' — ', '').replace(' AP', '') + '\n\nمقاله کامل صفحه 1 : \n' + '!wiki [1:' + title + ']\n\n'
                                        bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
                                except:
                                    print('wiki s err')              
                            elif text.startswith('/zekr') or text.startswith('ذکر'):
                                tawd219 = Thread(target=get_zeikr, args=(text, chat, bot,))
                                tawd219.start()
                            elif text.startswith('حدیث') or text.startswith('!hadis'):
                                tawd275 = Thread(target=get_hadis, args=(text, chat, bot,))
                                tawd275.start()
                            elif text.startswith('/name_shakh')  or text.startswith('نام شاخ'):
                                tawd32 = Thread(target=name_shakh, args=(text, chat, bot,))
                                tawd32.start()
                                
                            elif text.startswith('/jok') or text.startswith('جوک'):
                                tawd21 = Thread(target=get_jok, args=(text, chat, bot,))
                                tawd21.start()
                            elif text.startswith('/hagh') or text.startswith('حرف حق'):
                                tawd21 = Thread(target=get_hagh, args=(text, chat, bot,))
                                tawd21.start()
                                
                            elif text.startswith('/khatere')  or text.startswith('خاطره'):
                                tawd29 = Thread(target=get_khatere, args=(text, chat, bot,))
                                tawd29.start()
                            elif text.startswith('/danesh')  or text.startswith('دانستنی'):
                                tawd30 = Thread(target=get_danesh, args=(text, chat, bot,))
                                tawd30.start()
                            elif text.startswith('/deghat')  or text.startswith('دقت کردین'):
                                tawd20 = Thread(target=get_deghat, args=(text, chat, bot,))
                                tawd20.start()
                            elif text.startswith('جملات سنگین') or text.startswith('/gang'):
                                tawd215 = Thread(target=get_gang, args=(text, chat, bot,))
                                tawd215.start()
                            elif text.startswith('/alaki_masala')  or text.startswith('الکلی مثلا'):
                                tawd31 = Thread(target=get_alaki_masala, args=(text, chat, bot,))
                                tawd31.start()
                            elif text.startswith('/dastan')  or text.startswith('داستان'):
                                tawd25 = Thread(target=get_dastan, args=(text, chat, bot,))
                                tawd25.start()
                            elif text.startswith('/bio')  or text.startswith('بیو'):
                                tawd27 = Thread(target=get_bio, args=(text, chat, bot,))
                                tawd27.start()
                            elif text.startswith('!mont') or text.startswith('/mont') or text.startswith('مناسبت'):
                                tawd27 = Thread(target=get_sebt, args=(text, chat, bot,))
                                tawd27.start()
                            elif text.startswith('/srch-k ['):
                                tawd26 = Thread(target=get_search_k, args=(text, chat, bot,))
                                tawd26.start()
                            elif text.startswith('/ban [') and chat['abs_object']['type'] == 'Group' and 'BanMember' in access:
                                try:
                                    user = text[6:-1].replace('@', '')
                                    guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]
                                    admins = [i["member_guid"] for i in bot.getGroupAdmins(chat['object_guid'])["data"]["in_chat_members"]]
                                    if not guid in admins and chat['last_message']['author_object_guid'] in admins:
                                        bot.banGroupMember(chat['object_guid'], guid)
                                        bot.sendMessage(chat['object_guid'], 'کاربر به همراه ایدی حذف شد @TEXSBOT 👺' , chat['last_message']['message_id'])
                                except:
                                    print('ban bug')
                            elif text.startswith('/srch-p ['):
                                print('mpa started')
                                tawd = Thread(target=search_i, args=(text, chat, bot,))
                                tawd.start()
                            elif text.startswith('بن') and chat['abs_object']['type'] == 'Group' and 'BanMember' in access:
                                print('mpa started')
                                tawd2 = Thread(target=uesr_remove, args=(text, chat, bot,))
                                tawd2.start()
                            elif text.startswith('/trans ['):
                                tawd28 = Thread(target=get_trans, args=(text, chat, bot,))
                                tawd28.start()
                            elif text.startswith('/myket ['):
                                try:
                                    search = text[10:-1]
                                    if hasInsult(search)[0] == False and chat['abs_object']['type'] == 'Group':
                                        bot.sendMessage(chat['object_guid'], '🔷 نتایج کامل به پیوی شما ارسال گردید 🔷', chat['last_message']['message_id'])                           
                                        jd = json.loads(requests.get('https://www.wirexteam.ga/myket?type=search&query=' + search).text)
                                        jd = jd['search']
                                        a = 0
                                        text = ''
                                        for j in jd:
                                            if a <= 7:
                                                text += '🔸 عنوان : ' + j['title_fa'] + '\nℹ️ توضیحات : '+ j['tagline'] + '\n🆔 نام یکتا برنامه : ' + j['package_name'] + '\n⭐️امتیاز: ' + str(j['rate']) + '\n✳ نام نسخه : ' + j['version'] + '\nقیمت : ' + j['price'] + '\nحجم : ' + j['size'] + '\nبرنامه نویس : ' + j['developer'] + '\n\n' 
                                                a += 1
                                            else:
                                                break     
                                        if text != '':
                                            bot.sendMessage(chat['last_message']['author_object_guid'], 'نتایج یافت شده برای (' + search + ') : \n\n'+text)                               
                                    elif chat['abs_object']['type'] == 'User':
                                        jd = json.loads(requests.get('https://www.wirexteam.ga/myket?type=search&query=' + search).text)
                                        jd = jd['search']
                                        a = 0
                                        text = ''
                                        for j in jd:
                                            if a <= 7:
                                                text += '🔸 عنوان : ' + j['title_fa'] + '\nℹ️ توضیحات : '+ j['tagline'] + '\n🆔 نام یکتا برنامه : ' + j['package_name'] + '\n⭐️امتیاز: ' + str(j['rate']) + '\n✳ نام نسخه : ' + j['version'] + '\nقیمت : ' + j['price'] + '\nحجم : ' + j['size'] + '\nبرنامه نویس : ' + j['developer'] + '\n\n' 
                                                a += 1
                                            else:
                                                break     
                                        if text != '':
                                            bot.sendMessage(chat['object_guid'], text , chat['last_message']['message_id'])
                                except:
                                    print('myket server err')
                            elif text.startswith('/viki ['):
                                tawd23 = Thread(target=get_wiki, args=(text, chat, bot,))
                                tawd23.start()
                            elif text.startswith('/arz'):
                                print('mpa started')
                                tawd15 = Thread(target=get_curruncy, args=(text, chat, bot,))
                                tawd15.start()
                            elif text.startswith('/gold'):
                                tawd22 = Thread(target=get_gold, args=(text, chat, bot,))
                                tawd22.start()
                            elif text.startswith('/ping ['):
                                tawd21 = Thread(target=get_ping, args=(text, chat, bot,))
                                tawd21.start()
                            elif text.startswith('/font-en ['):
                                tawd20 = Thread(target=get_font, args=(text, chat, bot,))
                                tawd20.start()
                            elif text.startswith('/font-fa ['):
                                tawd34 = Thread(target=get_font_fa, args=(text, chat, bot,))
                                tawd34.start()
                            elif text.startswith('/whois ['):
                                tawd19 = Thread(target=get_whois, args=(text, chat, bot,))
                                tawd19.start()
                            elif text.startswith('/vaj ['):
                                tawd33 = Thread(target=get_vaj, args=(text, chat, bot,))
                                tawd33.start()
                            elif text.startswith('/mus'):
                                tawd33 = Thread(target=get_music, args=(text, chat, bot,))
                                tawd33.start()
                            elif text.startswith('/mus'):
                                tawd33 = Thread(target=get_arz, args=(text, chat, bot,))
                                tawd33.start()
                            elif text.startswith('/hvs ['):
                                tawd18 = Thread(target=get_weather, args=(text, chat, bot,))
                                tawd18.start()
                            elif text.startswith('/ip ['):
                                tawd17 = Thread(target=get_ip, args=(text, chat, bot,))
                                tawd17.start()
                            elif text.startswith("/add [") and chat['abs_object']['type'] == 'Group' and 'AddMember' in access:
                                try:
                                    user = text[6:-1]
                                    bot.invite(chat['object_guid'], [bot.getInfoByUsername(user.replace('@', ''))["data"]["chat"]["object_guid"]])
                                    bot.sendMessage(chat['object_guid'], 'کاربر اضافه شد @TEXSBOT 👺' , chat['last_message']['message_id'])                         
                                except:
                                    print('add not successd')  
                            elif text.startswith('/math ['):
                                try:
                                    amal_and_value = text[7:-1]
                                    natije = ''
                                    if amal_and_value.count('*') == 1:
                                        value1 = float(amal_and_value.split('*')[0].strip())
                                        value2 = float(amal_and_value.split('*')[1].strip())
                                        natije = value1 * value2
                                    elif amal_and_value.count('/') > 0:
                                        value1 = float(amal_and_value.split('/')[0].strip())
                                        value2 = float(amal_and_value.split('/')[1].strip())
                                        natije = value1 / value2
                                    elif amal_and_value.count('+') > 0:
                                        value1 = float(amal_and_value.split('+')[0].strip())
                                        value2 = float(amal_and_value.split('+')[1].strip())
                                        natije = value1 + value2
                                    elif amal_and_value.count('-') > 0:
                                        value1 = float(amal_and_value.split('-')[0].strip())
                                        value2 = float(amal_and_value.split('-')[1].strip())
                                        natije = value1 - value2
                                    elif amal_and_value.count('**') > 0:
                                        value1 = float(amal_and_value.split('**')[0].strip())
                                        value2 = float(amal_and_value.split('**')[1].strip())
                                        natije = value1 ** value2
                                    
                                    if natije != '':
                                        bot.sendMessage(chat['object_guid'], natije , chat['last_message']['message_id'])
                                except:
                                    print('math err')  
                                    #شات
                            elif text.startswith('/shot') or text.startswith('شات'):
                                tawd516 = Thread(target=shot_image, args=(text, chat, bot,))
                                tawd516.start()
                                #شات
                            elif text.startswith('/bgo') or text.startswith('بگو') or text.startswith('بنال') or text.startswith('ویس') or text.startswith('/speak'):
                                print('mpa started')
                                tawd6 = Thread(target=speak_after, args=(text, chat, bot,))
                                tawd6.start()
                            elif text.startswith('/danpic') or text.startswith('عکس دانستنی') or text.startswith('دانش') or text.startswith('!danpic'):
                                tawd12 = Thread(target=p_danesh, args=(text, chat, bot,))
                                tawd12.start()
                            elif text.startswith('منتقیه') or text.startswith('منطق') or text.startswith('منطقیه') or text.startswith('منتطقیه'):
                                tawd15 = Thread(target=photo_random, args=(text, chat, bot,))
                                tawd15.start()
                            elif text.startswith('فوتوتایم') or text.startswith('فوتو تایم') or text.startswith('تایم در عکس') or text.startswith('/photo_time'):
                                tawd16 = Thread(target=photo_time, args=(text, chat, bot,))
                                tawd16.start()
                            elif text.startswith('1 عضو جدید به گروه افزوده شد.') or text.startswith('یک عضو از طریق لینک به گروه افزوده شد.'):
                                tawd16 = Thread(target=koshamad, args=(text, chat, bot,))
                                tawd16.start()
                            elif text.startswith('/write ['):
                                print('mpa started')
                                tawd5 = Thread(target=write_image, args=(text, chat, bot,))
                                tawd5.start()
                            elif text.startswith('/logo ['):
                                tawd5 = Thread(target=logo, args=(text, chat, bot,))
                                tawd5.start()
                            elif chat['abs_object']['type'] == 'Group' and 'DeleteGlobalAllMessages' in access and hasInsult(text)[0] == True:
                                tawd13 = Thread(target=anti_insult, args=(text, chat, bot,))
                                tawd13.start()
                            elif chat['abs_object']['type'] == 'Group' and 'DeleteGlobalAllMessages' in access and hasAds(text) == True:
                                tawd14 = Thread(target=anti_tabligh, args=(text, chat, bot,))
                                tawd14.start()
                            elif text.startswith('!help') or text.startswith('/help') or text.startswith('دستورات') or text.startswith('پنل') or text.startswith('Help'):
                                tawd112 = Thread(target=get_help, args=(text, chat, bot,))
                                tawd112.start()
                            elif text.startswith('ج ح') or text.startswith('جرعت حقیقت') or text.startswith('جرعت') or text.startswith('جرات') or text.startswith('!GH') or text.startswith('/gh') or text.startswith('/jrat') or text.startswith('حقیقت'):
                                tawd412 = Thread(target=get_grat, args=(text, chat, bot,))
                                bot.sendMessage(chat['object_guid'], 'بـہ منوے بازے (جرعت פּ حقیقت خوش آمـבیـב)\n\nܠیܢܚࡅ߳ߺߺܙ ܢܚوߊ‌ܠߊ‌ࡅ߳ߺߺܙ ߊ‌وܠܙ -\n/listone \n\nܠیܢܚࡅ߳ߺߺܙ ܢܚوߊ‌ܠߊ‌ࡅ߳ߺߺܙ ܥ‌‌وܩܢ -\n/listtwo \n\n🔹- 𝚞𝚜𝚎𝚛 𝚜𝚞𝚙𝚙𝚘𝚛𝚝 @TEXSBOT👺', chat['last_message']['message_id'])
                                tawd412.start()
                            elif text.startswith('!listone') or text.startswith('!listone') or text.startswith('/listone'):
                                tawd912 = Thread(target=get_listone, args=(text, chat, bot,))
                                #bot.sendMessage(chat['object_guid'], '1. از چه چیزی بیشترین ترس را داری؟\n\n2. حال به هم زن ترین کاری که انجام دادی را بگو.\n\n3. اگر به گذشته برگردی چه چیزی را تغییر میدی؟\n\n4. آیا تا به حال مخفیانه از جیب سایر اعضای خانواده پول برداشتی؟\n\n5.  بزرگ ترین دروغی که تو زندگیت گفتی چی بوده؟\n6. از بیان چه اتفاقی تو زندگی شخصیت خجالت میکشی؟\n\n7. آخرین باری که دست داخل بینی ات کردی کی بود؟\n\n8.  احمقانه ترین کاری که در حمل و نقل عمومی انجام داده ای، چیست؟\n\n9. اگر به مدت یک ماه جنس مخالف خود بودی چه کارهایی می کردی؟\n\n10. از چه شخصی در زندگی بیشترین نفرت را داری؟\n\n11. اگر می خواستی یک نفر از این جمع را به عنوان عشقت انتخاب کنی چه کسی را انتخاب می کردی؟\n\n12. احمقانه ترین اعتیاد یا وابستگی که داری چیست؟\n\n13. نظرت در رابطه با ازدواج چیست؟\n\n14. شرم آورترین شی موجود در اتاقت چیست؟\n\n15. آیا تا به حال شکست عشقی خورده ای؟ چه زمانی و چرا؟\n\n16. احمقانه ترین کاری که تا به حال کرده ای چه بوده است؟\n\n17. آیا رازی داری که تا به حال به هیچ کس نگفته باشی؟\n\n18. نفرت انگیزترین عادت تو چیست؟\n\n19. آخرین باری که عذرخواهی کردی چه موقع بوده است؟ \n\n20. به من چیزی بگو که نمی خواهی بدانم.\n\n21. شرم آورترین لحظه زندگی ات کدام لحظه بوده است؟\n\n22. آیا تا به حال از شدت خنده خودت را خیس کردی؟\n\n24. کدام کار است که اگر همه پول های دنیا را هم به تو بدهند انجام نمی دهی؟\n\n25. یکی از رفتارهایت که دوست داری تغییر بدهی چیست؟\n\n26. بدترین شوخی که با کسی داشته ای چه بوده است؟\n\n27. اگر نامرئی شوی اولین کاری که انجام می دهی چیست؟\n\n28. اگر مجبور باشی در یک جزیره به تنهایی با یک نفر زندگی کنی چه کسی را انتخاب می کنی؟\n\n29. احمقانه ترین حرفی که در لحظات عاشقانه به همسرت زده ای چه بوده است؟\n\n30. اسم کسی را بگو که وانمود می کنی دوستش داری اما در واقع چشم دیدنش را نداری؟\n\n31. دردناک ترین تجربه جسمی ات چه بوده است؟\n\n32. اگر غول چراغ جادو داشته باشی سه آرزویت چیست؟\n\n33. احمقانه ترین کاری که مقابل آینه انجام داده ای چه کاری بوده است؟\n\n34. بیشتر از همه به چه کسی حسادت می کنی؟\n\n35. اگر مطمئن باشی هیچ وقت زندانی نمی شوی دوست داری چه کسی را بکشی؟\n\n36. آیا تا به حال درباره سن خود دروغ گفته ای؟\n\n37. اگر می توانستی یک قانون را حذف کنی یا یک قانون جدید وضع کنی، این قانون چیست و چرا؟\n\n38. به کدام عضو بدن خودت علاقه داری و از کدام متنفر هستی؟\n\n40. آخرین باری که گریه کردی چه زمانی بود؟\n\n41. تا حالا مواد مخدر مصرف کردی؟\n\n42. بهترین روز زندگی ات چه روزی بوده است؟\n\n43. ترسناک ترین اتفاقی که برایت افتاده چیست؟\n\n44. آخرین چیزی که در گوگل سرچ کرده ای چه بوده است؟\n\n45. اگر یک حیوان بودی چه حیوانی بودی؟\n\n46. بدترین کاری که در مقابل چشم مردم انجام داده ای چه بوده است؟\n\n47. اولین باری که به کسی گفتی دوستت دارم چه زمانی و چه کسی بوده است؟\n\n48. آیا شب ها با لباس زیر می خوابی؟\n\n51. آخرین کاری که برای اولین بار انجام دادی چیست؟\n\n52. چه کاری را دوست داری حتما قبل از مرگ انجام دهی؟\n\n54. آیا تاکنون قانونی را نقض کرده اید؟\n\n55. از چه چیز یا چه کسی فوبیا داری؟\n\n56. دو موردی که می خواهی در مورد شخصی که دوستش داری بدانی چیست؟\n\n57. کدام لحظه را خنده دار ترین لحظه زندگی ات می دانی؟\n\n\n\n\n\n\n\n\n', chat['last_message']['message_id'])
                                #bot.sendMessage(chat['object_guid'], 'تعداد 60 تا سوال فرستاده شد اگه دوست دارید بازی شروع شود ابتدا 4 نفر با انتخاب اعداد 1 تا 4 وارد بازی شوند و سپس کلمه [بپرس] را ارسال کنید.', chat['last_message']['message_id'])
                                tawd912.start()
                            elif text.startswith('/listtwo') or text.startswith('!listtwo'):
                                tawd512 = Thread(target=get_listtwo, args=(text, chat, bot,))
                                tawd512.start()
                            elif text.startswith('سرگرمی ها') or text.startswith('/Sargarmi') or text.startswith('!sargarmi') or text.startswith('سرگرمی') or text.startswith('[سرگرمی]') or text.startswith('[سرگرمی ها]'):
                                tawd3668 = Thread(target=get_car, args=(text, chat, bot,))
                                tawd3668.start()        
                            elif text.startswith('tool') or text.startswith('/Tools') or text.startswith('Tools') or text.startswith('!Tools') or text.startswith('!tool') or text.startswith('/tools'):
                                tawd3606 = Thread(target=get_sargarmi, args=(text, chat, bot,))
                                tawd3606.start()                         
                            elif text.startswith('جستجو') or text.startswith('/Search') or text.startswith('/search'):
                                tawd358 = Thread(target=get_srch, args=(text, chat, bot,))
                                tawd358.start()
 #کاربردی
                            elif text.startswith('کاربردی') or text.startswith('ابزار کاربردی') or text.startswith('/Commands') or text.startswith('Commands') or text.startswith('commands') or text.startswith('!commands'):
                                tawd238 = Thread(target=gets_karborde, args=(text, chat, bot,))
                                tawd238.start()
#کاربردی                         
                            elif text.startswith('66') or text.startswith('666'):
                                tawd348 = Thread(target=get_sar, args=(text, chat, bot,))
                            elif text.startswith('شروع') and chat['abs_object']['type'] == 'Group' and chat['last_message']['author_object_guid'] in AmoBotAdmins and g_usvl == '':
                                g_usvl = chat['object_guid']
                                bot.sendMessage(chat['object_guid'], 'یادگیری فعال شد', chat['last_message']['message_id'])
                            elif text.startswith('پایان') and chat['abs_object']['type'] == 'Group' and chat['last_message']['author_object_guid'] in AmoBotAdmins and g_usvl != '':
                                g_usvl = ''
                                bot.sendMessage(chat['object_guid'], 'یادگیری غیرفعال شد.', chat['last_message']['message_id'])  
                            elif text.startswith('فعال') and chat['abs_object']['type'] == 'Group' and chat['last_message']['author_object_guid'] in AmoBotAdmins and g_usvl == '' and test_usvl == '':
                                test_usvl = chat['object_guid']
                                bot.sendMessage(chat['object_guid'], 'پاسخگویی فعال شد.', chat['last_message']['message_id'])
                            elif text.startswith('غیرفعال') and chat['abs_object']['type'] == 'Group' and chat['last_message']['author_object_guid'] in AmoBotAdmins and test_usvl == chat['object_guid']:
                                test_usvl = ''
                                bot.sendMessage(chat['object_guid'], 'پاسخگویی غیرفعال شد.', chat['last_message']['message_id'])   
                            elif text.startswith('!backup') and chat['object_guid'] in AmoBotAdmins:
                                tawd44 = Thread(target=get_backup, args=(text, chat, bot,))
                                tawd44.start()
                            elif chat['object_guid'] == g_usvl and chat['last_message']['author_object_guid'] != 'u0Eea8W0bbfab55937316fcd06c0f9bc' and chat['abs_object']['type'] == 'Group':
                                tawd42 = Thread(target=usvl_save_data, args=(text, chat, bot,))
                                tawd42.start()
                            elif test_usvl == chat['object_guid'] and chat['last_message']['author_object_guid'] != 'u0Eea8W0bbfab55937316fcd06c0f9bc' and chat['abs_object']['type'] == 'Group':
                                print('usvl tested')
                                tawd43 = Thread(target=usvl_test_data, args=(text, chat, bot,))
                                tawd43.start()
                            list_message_seened.append(m_id)
                    elif 'SendMessages' in access and chat['last_message']['type'] == 'Other' and text.strip() != '' and chat['abs_object']['type'] == 'Group' and chat['abs_object']['type'] == 'Group':
                        text = text.strip()
                        m_id = chat['object_guid'] + chat['last_message']['message_id']
                        if not m_id in list_message_seened:
                            if text == 'یک عضو گروه را ترک کرد.':
                                tawd35 = Thread(target=get_leaved, args=(text, chat, bot,))
                                tawd35.start()
                            elif text == '1 عضو جدید به گروه افزوده شد.' or text == 'یک عضو از طریق لینک به گروه افزوده شد.':
                                tawd36 = Thread(target=get_added, args=(text, chat, bot,))
                                tawd36.start()
                            list_message_seened.append(m_id)
                    elif 'SendMessages' in access and text.strip() != '' and chat['abs_object']['type'] == 'Group':
                        text = text.strip()
                        m_id = chat['object_guid'] + chat['last_message']['message_id']
                        if not m_id in list_message_seened:
                            if 'DeleteGlobalAllMessages' in access and hasInsult(text)[0] == True:
                                tawd39 = Thread(target=anti_insult, args=(text, chat, bot,))
                                tawd39.start()
                                list_message_seened.append(m_id)
                            elif 'DeleteGlobalAllMessages' in access and hasAds(text) == True:
                                tawd40 = Thread(target=anti_tabligh, args=(text, chat, bot,))
                                tawd40.start()
                                list_message_seened.append(m_id)
        else:
            print('چت ها را آپدیت کنید ')
    except:
        print('ارور کلی')
    time_reset2 = random._floor(datetime.datetime.today().timestamp())
    if list_message_seened != [] and time_reset2 > time_reset:
        list_message_seened = []
        time_reset = random._floor(datetime.datetime.today().timestamp()) + 350
