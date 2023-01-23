import pygame
import os
os.environ["PYTHONIOENCODING"] = "utf-8"
import locale
myLocale = locale.setlocale(category = locale.LC_ALL, locale = "en_GB.UTF-8")
import time
import math
import urllib.request
import json
import socket
from pygame.draw import polygon
import requests
import zipfile

# path = os.path.dirname(os.path.realpath(__file__))
path = '.'
server = 'https://maohupi.riarock.com/web/game/run_on_tempo/user_login/login.php'
shop = 'https://maohupi.riarock.com/web/game/run_on_tempo/resource_shop/shop.php'
version = '2.0.0'
langF = open(path+'/system/user/lang.json', 'r', encoding='utf-8')
lang = langF.read()
lang = json.loads(lang)
langF.close()
textFont = './system/font/'+lang[lang['now']]['__font-family__']

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

isWifi = False
with urllib.request.urlopen(server) as response:
    try:
        isWifi = response.read().decode("utf-8") == 'null'
    except: pass
def web_open(url):
    if isWifi:
        with urllib.request.urlopen(url) as response:
            return(response.read().decode("utf-8"))
    else:
        return('no wifi')
def file_open(url):
    if isWifi:
        with urllib.request.urlopen(url) as response:
            return(response.read())
    else:
        return('no wifi')

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = [s.getsockname()[0], requests.get('https://api.ipify.org').text]
s.close()

userF = open(path+'/system/user/user.json', 'a+')
userF.seek(0)
r = userF.read()
if r != '':
    user = json.loads(r) 
else:
    user = {}
userF.close()

pygame.init()
pygame.mixer.init()
nTime = time.time()
def gameQuit():
    global cvs
    f = open(path+'/system/user/settings.json', 'w')
    f.write(json.dumps({'bgm_volume':cvs.bgm_volume, 'se_volume':cvs.se_volume, 'key_left':cvs.left_key, 'key_right':cvs.right_key, 'character':cvs.player_data['character'], 'modeling':cvs.player_data['modeling'], 'levels':cvs.page['levels']}))
    f.close()
    global se
    se['point'].play()
    time.sleep(0.15)
    cvs.running = False
    pygame.quit()
    for tsfn in os.listdir(path+'/system/temporaryStorage/'):
                os.remove('%s/system/temporaryStorage/%s' %(path, tsfn))
    try:
        exit()
    except:
        exitError = True
def re(a):
    return a
def deg(deg):
    return(math.pi/180*deg)
song_fgi = ''
def set_fg():
    global song_fgi
    i = where(cvs.page[cvs.page[cvs.page['self']]], cvs.own[cvs.page[cvs.page['self']]])
    cvs.pageBackgroundMusic['start'] = cvs.own[cvs.page['start']][i]+'/fgm.wav'
    fn = cvs.own[cvs.page['start']][i]+'/fgi.png'
    song_fgi = pygame.image.load(fn) if os.path.exists(fn) else ''
class levels:
    def __init__(self):
        self.Radius = 10
        self.Radius2 = 8
        self.Top = 82
        self.Left = 65
        self.Margin = 2
levels = levels()
class getContext2d:
    def __init__(self, canvas, lineWidth = 10, fillStyle = (255, 255, 255), strokeStyle = (0, 0, 0), font = '10px '+textFont):
        self.canvas = canvas
        self.lineWidth = lineWidth
        self.fillStyle = fillStyle
        self.strokeStyle = strokeStyle
        self.nowXY = [0, 0]
        self.font = font
        self.polygon_data = []
    def fillRect(self, x, y, w, h):
        pygame.draw.rect(self.canvas, self.fillStyle, [x, y, w, h], 0)
    def strokeRect(self, x, y, w, h):
        pygame.draw.rect(self.canvas, self.strokeStyle, [x, y, w, h], int(self.lineWidth))
    def fillText(self, t, x, y, againstX = 'left', againstY = 'top', fontType = 'sys'):
        font = self.font.split()
        flag = len(font) == 3
        b = font[0] == 'bg' if flag else False
        s = int(font[1].replace('px', '')) if flag else int(font[0].replace('px', ''))
        f = font[2] if flag else font[1]
        font = pygame.font.SysFont(f, s) if fontType != 'file' else pygame.font.Font(f, s)
        size = {'w':0, 'h':0}
        size['w'], size['h'] = font.size(t)
        addX = size['w'] if againstX == 'right' else size['w']/2 if againstX == 'center' else 0
        addY = size['h'] if againstY == 'bottom' else size['h']/2 if againstY == 'center' else 0
        if b:
            self.canvas.blit(font.render(t, True, self.fillStyle, self.strokeStyle), (int(x-addX), int(y-addY)))
        else:
            self.canvas.blit(font.render(t, True, self.fillStyle), (int(x-addX), int(y-addY)))
    def drawImage(self, i, xy, wh = False, a = False):
        if wh:
            i = pygame.transform.scale(i, (int(wh[0]), int(wh[1])))
        if a:
            i.set_alpha(a)
        self.canvas.blit(i, (int(xy[0]), int(xy[1])))
    def fillBox(self, x, y, w, h, r):
        pygame.draw.rect(self.canvas, self.fillStyle, [re(x+r), re(y), re(w-2*r), re(h)], 0)
        pygame.draw.rect(self.canvas, self.fillStyle, [re(x), re(y+r), re(w), re(h-2*r)], 0)
        pygame.draw.circle(self.canvas, self.fillStyle, (re(x+r), re(y+r)), re(r), 0)
        pygame.draw.circle(self.canvas, self.fillStyle, (re(x+r), re(y+h-r)), re(r), 0)
        pygame.draw.circle(self.canvas, self.fillStyle, (re(x+w-r), re(y+r)), re(r), 0)
        pygame.draw.circle(self.canvas, self.fillStyle, (re(x+w-r), re(y+h-r)), re(r), 0)
    def strokeBox(self, x, y, w, h, r):
        lw = self.lineWidth
        pygame.draw.line(self.canvas, self.strokeStyle, (re(x+r+lw), re(y)), (re(x+w-2*r+lw), re(y)), int(self.lineWidth))
        pygame.draw.line(self.canvas, self.strokeStyle, (re(x+w), re(y+r+lw)), (re(x+w), re(y+h-2*r+lw)), int(self.lineWidth))
        pygame.draw.line(self.canvas, self.strokeStyle, (re(x+w-2*r+lw), re(y+h)), (re(x+r+lw), re(y+h)), int(self.lineWidth))
        pygame.draw.line(self.canvas, self.strokeStyle, (re(x), re(y+h-2*r+lw)), (re(x), re(y+r+lw)), int(self.lineWidth))
    def moveTo(self, x = 'old', y = 'old'):
        x = x if x != 'old' else self.nowXY[0]
        y = y if y != 'old' else self.nowXY[1]
        self.nowXY = [x, y]
        self.polygon_data.append({'x':x, 'y':y, 'draw':False})
    def lineTo(self, x, y, drawLine = False):
        x = x if x != 'old' else self.nowXY[0]
        y = y if y != 'old' else self.nowXY[1]
        if drawLine:
            pygame.draw.line(self.canvas, self.strokeStyle, (re(self.nowXY[0]), re(self.nowXY[1])), (re(x), re(y)), int(self.lineWidth))
        self.nowXY = [x, y]
        self.polygon_data.append({'x':x, 'y':y, 'draw':True})
    def stroke(self):
        if len(self.polygon_data) > 1:
            for i in range(0, len(self.polygon_data)-1):
                if self.polygon_data[i+1]['draw']:
                    pygame.draw.line(self.canvas, self.strokeStyle, (re(self.polygon_data[i]['x']), re(self.polygon_data[i]['y'])), (re(self.polygon_data[i+1]['x']), re(self.polygon_data[i+1]['y'])), int(self.lineWidth))
    def fill(self):
        if len(self.polygon_data) > 1:
            polygons = []
            for i in range(0, len(self.polygon_data)):
                polygons.append([self.polygon_data[i]['x'], self.polygon_data[i]['y']])
            pygame.draw.polygon(cvs.this, self.fillStyle, polygons)
    def beginPath(self):
        self.polygon_data = []
    def closePath(self):
        self.polygon_data.append({'x':self.polygon_data[0]['x'], 'y':self.polygon_data[0]['y'], 'draw':True})

class canvas:
    def __init__(self, width = 0, height = 0, bgc = (0, 0, 0), title = '', icon = '', bgm_volume = 80, se_volume = 80, left_key = 115, right_key = 108):
        global levels
        self.this = False
        self.width = width
        self.height = height
        self.bgc = bgc
        self.running = False
        self.page = {'slef':'home', 'home':'', 'player':'player_character', 'shop':'shop_character', 'start':'start_official', 'setting':'', 'player_character':'', 'player_modeling':'', 'shop_character':'', 'shop_modeling':'', 'shop_character':'', 'shop_song':'', 'start_official':'', 'start_mine':'', 'levels':'levels_easy', 'score':'', 'play':''}
        self.own = {'player_character':os.listdir(path+'/player/'), 'player_modeling':[], 'shop_character':[], 'shop_modeling':[], 'shop_character':[], 'shop_song':[], 'start_official':os.listdir(path+'/song/'), 'start_mine':[], 'shop_character':json.loads(web_open(shop+'?type=character')), 'shop_song':json.loads(web_open(shop+'?type=song'))}
        for i in range(0, len(self.own['player_character'])):
            self.own['player_character'][i] = path + '/player/' + self.own['player_character'][i]
        if len(self.own['player_character']) < 1:
            self.own['player_character'].append('')
        self.page['player_character'] = self.own['player_character'][0]
        for i in range(0, len(self.own['start_official'])):
            self.own['start_official'][i] = path + '/song/' + self.own['start_official'][i]
        if len(self.own['start_official']) < 1:
            self.own['start_official'].append('')
        self.page['start_official'] = self.own['start_official'][0]
        self.page['shop_character'] = self.own['shop_character'][0]
        self.page['shop_song'] = self.own['shop_song'][0]
        self.title = title
        self.getContex2d = False
        self.alpha = pygame.Surface((width, height), pygame.SRCALPHA)
        self.alpha_getContex2 = False
        self.icon = pygame.image.load(icon)
        self.login_page = 'login_old'
        self.bgm_volume = bgm_volume
        self.se_volume = se_volume
        self.home_marquee = ['', '']
        self.home_marquee_information = {'now_item':0, 'last_time':time.time()}
        self.pageButtons = {'home':[], 'player':[], 'shop':[], 'start':[], 'setting':[], 'login':[], 'playing':[], 'play':[], 'score':[]}
        self.pageBackgroundImage = {'xy':-40, 'home':False, 'player':False, 'shop':False, 'start':False, 'setting':False, 'login':False, 'playing':False}
        self.pageBackgroundMusic = {'home':False, 'player':False, 'shop':False, 'start':False, 'setting':False, 'login':False, 'playing':False}
        self.song_bgi = False
        self.song_data = {'title':'', 'left_color':color.dot_color['blue'], 'right_color':color.dot_color['red'], 'items':[]}
        self.player_data = {'character':'', 'modeling':'', 'item':{'left':'', 'right':''}, 'modeling_fgi':'', 'character_fgi':''}
        self.shop_data = {'character':'', 'song':'', 'item':{'left':'', 'right':''}, 'song_fgi':'', 'character_fgi':''}
        # self.player_data['character'] = cvs.page['player_character']
        self.score_data = {'point':0, 'point_p':0, 'combo':0, 'kill':0, 'perfect':0, 'good':0, 'bad':0, 'miss':0}
        self.left_key = left_key
        self.right_key = right_key
        self.init()
    def init(self):
        self.this = pygame.display.set_mode((int(self.width), int(self.height)), pygame.RESIZABLE)
        pygame.display.set_caption(self.title)
        pygame.display.set_icon(self.icon)
        self.getContex2d = getContext2d(canvas = self.this)
        self.alpha_getContex2d = getContext2d(canvas = self.alpha)
    def draw_pageButtons(self):
        ctx.font = str(int(3*vw))+'px '+textFont
        for btn in self.pageButtons[self.page['self']]:
            self.getContex2d.fillStyle = (255, 214, 128)
            self.getContex2d.fillRect(btn[0], btn[1], btn[2], btn[3])
            flag1 = MX > btn[0] and MX < btn[0]+btn[2] and MY > btn[1] and MY < btn[1]+btn[3]
            flag2 = self.page[self.page['self']] == btn[4] or (self.page['self'] == 'start' and self.page['levels'] == btn[4])
            ctx.strokeStyle = (113, 71, 0) if flag1 or flag2 else (255, 255, 255)
            ctx.lineWidth = 0.5*vw if flag1 or flag2 else 0.1*vw
            self.getContex2d.strokeRect(btn[0], btn[1], btn[2], btn[3])
            self.getContex2d.fillStyle = color.darkBrown
            self.getContex2d.fillText(lang[lang['now']][btn[4]], btn[0]+btn[2]/2, btn[1]+btn[3]/2, fontType = 'file', againstX = 'center', againstY = 'center')
    def click_pageButtons(self):
        for btn in self.pageButtons[self.page['self']]:
            homeButtonClick(btn[0], btn[1], btn[2], btn[3], btn[4])
    def draw_pageTitle(self):
        self.getContex2d.font = str(int(5*vw))+'px '+textFont
        self.getContex2d.fillStyle = color.darkBrown
        self.getContex2d.fillText(lang[lang['now']][self.page['self']], (50-5)*vw, 1*vh, fontType = 'file')
        self.getContex2d.fillRect(1*vw, 12*vh, 98*vw, 1*vh)
    def draw_pageBackground(self):
        self.this.fill((255, 255, 155))
        for i in range(0, 10):
            for j in range(0, 6):
                self.getContex2d.drawImage(self.pageBackgroundImage[self.page['self']], ((i*20-j*10+self.pageBackgroundImage['xy'])*vw, (j*20+self.pageBackgroundImage['xy'])*vw), (10*vw, 10*vw))
                if self.pageBackgroundImage['xy'] > 0:
                    self.pageBackgroundImage['xy'] = -40
                self.pageBackgroundImage['xy'] += 0.1/fps
        self.alpha.fill((255, 255, 255, 100))
        self.this.blit(self.alpha, (0, 0))
    def pageIs(self, type):
        re = False
        if type == 'homeS':
            re = cvs.page['self'] == 'home'
        elif type == 'homeC':
            re = cvs.page['self'] == 'player' or cvs.page['self'] == 'shop' or cvs.page['self'] == 'start' or cvs.page['self'] == 'setting'
        elif type == 'homeN':
            cvs.page['self'] == 'login' or cvs.page['self'] == 'home'
        return re
    def draw_switcherBg(self):
        self.getContex2d.fillStyle = color.white
        self.getContex2d.fillRect(1*vw, 14*vh, 98*vw, 84*vh)
    def draw_switcherFg(self):
        self.alpha.fill((0, 0, 0, 0))
        self.alpha_getContex2d.fillStyle = (0, 0, 0, 80)
        self.alpha_getContex2d.strokeStyle = (0, 0, 0, 0)
        self.alpha_getContex2d.lineWidth = 0.8*vw
        if loginInputHover(2*vw, 16*vh, 13*vw, 80*vh):
            self.alpha_getContex2d.fillRect(2*vw, 16*vh, 13*vw, 80*vh)
            self.alpha_getContex2d.moveTo((8+1)*vw, (56-3)*vh)
            self.alpha_getContex2d.lineTo((8-1)*vw, 56*vh, drawLine = True)
            self.alpha_getContex2d.lineTo((8+1)*vw, (56+3)*vh, drawLine = True)
        if loginInputHover(85*vw, 16*vh, 13*vw, 80*vh):
            self.alpha_getContex2d.fillRect(85*vw, 16*vh, 13*vw, 80*vh)
            self.alpha_getContex2d.moveTo((91.5-1)*vw, (56-3)*vh)
            self.alpha_getContex2d.lineTo((91.5+1)*vw, 56*vh, drawLine = True)
            self.alpha_getContex2d.lineTo((91.5-1)*vw, (56+3)*vh, drawLine = True)
        self.this.blit(self.alpha, (0, 0))
    def click_switcher(self):
        i = where(self.page[self.page[self.page['self']]], self.own[self.page[self.page['self']]])
        if loginInputHover(85*vw, 16*vh, 13*vw, 80*vh):
            if len(self.own[self.page[self.page['self']]]) > 0 and i < len(self.own[self.page[self.page['self']]])-1:
                self.page[self.page[self.page['self']]] = self.own[self.page[self.page['self']]][i+1]
                if self.page['self'] == 'start':
                    pygame.mixer.music.stop()
            else:
                alertBox.append([lang[lang['now']]['no_next'], alertTime])
        elif loginInputHover(2*vw, 16*vh, 13*vw, 80*vh):
            if len(self.own[self.page[self.page['self']]]) > 0 and i > 0:
                self.page[self.page[self.page['self']]] = self.own[self.page[self.page['self']]][i-1]
                if self.page['self'] == 'start':
                    pygame.mixer.music.stop()
            else:
                alertBox.append([lang[lang['now']]['no_last'], alertTime])
        if cvs.page['self'] == 'player':
            if cvs.page['player'] == 'player_character':
                i = where(cvs.page['player_character'], cvs.own['player_character'])
                fn = cvs.own['player_character'][i]+'/fgi.png'
                cvs.player_data['character_fgi'] = pygame.image.load(fn) if os.path.exists(fn) else ''
            elif cvs.page['player'] == 'player_modeling':
                i = where(cvs.page['player_modeling'], cvs.own['player_modeling'])
                fn = cvs.player_data['character']+'/skin/'+cvs.own['player_modeling'][i]+'/fgi.png'
                cvs.player_data['modeling_fgi'] = pygame.image.load(fn) if os.path.exists(fn) else ''
        elif cvs.page['self'] == 'shop':
            if cvs.page['shop'] == 'shop_character':
                i = where(cvs.page['shop_character'], cvs.own['shop_character'])
                fn = cvs.own['shop_character'][i]+'/fgi.png'
                fn2 = path+'/system/temporaryStorage/'+'.'.join(fn.replace('https://', '').replace('http://', '').split('/'))
                if not os.path.exists(fn2):
                    f = open(fn2, 'wb')
                    f.write(file_open(fn))
                    f.close()
                cvs.shop_data['character_fgi'] = pygame.image.load(fn2) if os.path.exists(fn2) else ''
            elif cvs.page['shop'] == 'shop_song':
                i = where(cvs.page['shop_song'], cvs.own['shop_song'])
                fn = cvs.own['shop_song'][i]+'/fgi.png'
                fn2 = path+'/system/temporaryStorage/'+'.'.join(fn.replace('https://', '').replace('http://', '').split('/'))
                if not os.path.exists(fn2):
                    f = open(fn2, 'wb')
                    f.write(file_open(fn))
                    f.close()
                cvs.shop_data['song_fgi'] = pygame.image.load(fn2) if os.path.exists(fn2) else ''
        elif cvs.page['self'] == 'start':
            set_fg()
class color:
    def __init__(self):
        self.darkBrown = (113, 71, 0)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.orange = (255, 214, 128)
        self.dot_color = {}
        self.dot_color['red'] = (224, 102, 102)
        self.dot_color['orange'] = (246, 178, 107)
        self.dot_color['yellow'] = (255, 217, 102)
        self.dot_color['green'] = (147, 196, 125)
        self.dot_color['darkslategray'] = (118, 165, 175)
        self.dot_color['skyblue'] = (109, 158, 235)
        self.dot_color['blue'] = (111, 168, 220)
        self.dot_color['purple'] = (142, 124, 195)
        self.dot_color['deepwine'] = (194, 123, 160)
        self.dot_color['brown'] = (204, 65, 37)

color = color()
point_cooldown = 0
full_point_cooldown = 5
volume = {'bgm':{'+':False, '-':False}, 'se':{'+':False, '-':False}}
key = {8:['\b', False, 50], 61:['=', False, 50, '+'], 1073742053:['', False, 50], 1073742049:['', False, 50], 1073741881:['', False, 50]}
t = ',-./0123456789'
T = '<_>?)!@#$%^&*('
for i in range(0, len(t)):
    key[i+44] = [t[i], False, 50, T[i]]
t = '[\]'
T = '{|}'
for i in range(0, len(t)):
    key[i+91] = [t[i], False, 50, T[i]]
t = 'abcdefghijklmnopqrstuvwxyz'
T = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
for i in range(0, len(t)):
    key[i+97] = [t[i], False, 50, T[i]]
vw = 1000/100
vh = 500/100
vf = open(path+'/system/user/settings.json', 'r', encoding='utf-8')
vfi = vf.read()
vfi = json.loads(vfi) if vfi != '' else {'bgm_volume':0.8, 'se_volume':0.8}
vf.close()
pygame.mixer.music.set_volume(vfi['bgm_volume'])
cvs = canvas(width = 100*vw, height = 100*vh, title = '在拍點上奔逃 | Run On Tempo', icon = path+'/system/image/bgi-eighthNote.png', bgm_volume = vfi['bgm_volume'], se_volume = vfi['se_volume'], left_key = vfi['key_left'], right_key = vfi['key_right'])
ctx = cvs.getContex2d
cvs.page['self'] = 'home' if user != {} else 'login'
cvs.bgc = 255, 255, 155
cvs.running = True
cvs.player_data['character'] = vfi['character']
cvs.player_data['modeling'] = vfi['modeling']
cvs.page['levels'] = vfi['levels'] if vfi['levels'] == 'levels_easy' or vfi['levels'] == 'levels_normal' or vfi['levels'] == 'levels_hard' else 'levels_easy'
allBtnH = 15
allIptH = 22
fpsUDt = 100 # fps更新倒數(讓設定頁面的fps不會跳不停)
fpsO = lang[lang['now']]['calculating'] + '...' # 上次的fps(顯示於設定頁)
loginInput = {'login_old':[[30*vw, allIptH*vh, 45*vw, 6*vh, '', 1, False, 'login_mail'], [30*vw, (allIptH+8.5)*vh, 38*vw, 6*vh, '', 2, False, 'login_pwd']], 'forgot_pwd':[[30*vw, allIptH*vh, 45*vw, 6*vh, '', 1, False, 'login_mail']], 'login_new':[[30*vw, allIptH*vh, 45*vw, 6*vh, '', 1, False, 'login_mail'], [30*vw, (allIptH+8.5)*vh, 38*vw, 6*vh, '', 2, False, 'login_pwd']], 'checkMail_was_sanded_pwd':[], 'checkMail_was_sanded_mail':[], 'send_pwd_width_mail':[]}
loginButton = {'login_old':[[69.25*vw, (allIptH+8.5)*vh, 5.75*vw, 6*vh, 'view', 2, False], [25*vw, (allIptH+17)*vh, 50*vw, 6*vh, 'forgot_pwd', 2], [25*vw, (allIptH+25.5)*vh, 25*vw-2.5*vh/2, 6*vh, 'login_new', 3], [(50)*vw+2.5*vh/2, (allIptH+25.5)*vh, 25*vw-2.5*vh/2, 6*vh, 'login_old', 4]], 'forgot_pwd':[[25*vw, (allIptH+8.5)*vh, 50*vw, 6*vh, 'send_pwd_width_mail', 1], [25*vw, (allIptH+17)*vh, 25*vw-2.5*vh/2, 6*vh, 'login_new', 2], [(50)*vw+2.5*vh/2, (allIptH+17)*vh, 25*vw-2.5*vh/2, 6*vh, 'login_old', 3]], 'login_new':[[69.25*vw, (allIptH+8.5)*vh, 5.75*vw, 6*vh, 'view', 2, False], [25*vw, (allIptH+17)*vh, 25*vw-2.5*vh/2, 6*vh, 'login_old', 3], [(50)*vw+2.5*vh/2, (allIptH+17)*vh, 25*vw-2.5*vh/2, 6*vh, 'login_new', 4]], 'checkMail_was_sanded_pwd':[[25*vw, (allIptH+8.5)*vh, 50*vw, 6*vh, 'back_to_login', 2]], 'checkMail_was_sanded_mail':[[25*vw, (allIptH+8.5)*vh, 50*vw, 6*vh, 'back_to_login', 2]], 'send_pwd_width_mail':[]}
menu = {'__hover__':[False, False], 'lang':[1*vw+(10/2+5.5)*vw, 23*vh, 10*vw, 3*vw, [], False]}
for ln in lang:
    if ln != 'now':
        menu['lang'][4].append(ln)
def reset_variable():
    global homeButton, cvs, loginInput, loginButton, menu, line_start, line_stop, line_height, arc_r, item_leave, item_r, middle_line, middle_line_getContex2d
    homeButton = [(50*vw, allBtnH*vh, 46*vw, 15*vh, 'player', 1), (50*vw, (allBtnH+15)*vh+2*vw, 46*vw, 15*vh, 'shop', 3), (50*vw, (allBtnH+15*2)*vh+(2*2)*vw, 46*vw, 15*vh, 'start', 5), (50*vw, (allBtnH+15*3)*vh+(2*3)*vw, 46*vw, 15*vh, 'setting', 6)]
    cvs.pageButtons['player'] = [[1*vw, 1*vh, 10*vw, 10*vh, 'home'], [12*vw, 1*vh, 10*vw, 10*vh, 'player_use'], [78*vw, 1*vh, 10*vw, 10*vh, 'player_character'], [89*vw, 1*vh, 10*vw, 10*vh, 'player_modeling']]
    # cvs.pageButtons['shop'] = [[1*vw, 1*vh, 10*vw, 10*vh, 'home'], [12*vw, 1*vh, 10*vw, 10*vh, 'shop_buy'], [67*vw, 1*vh, 10*vw, 10*vh, 'player_character'], [78*vw, 1*vh, 10*vw, 10*vh, 'player_modeling'], [89*vw, 1*vh, 10*vw, 10*vh, 'shop_song']]
    cvs.pageButtons['shop'] = [[1*vw, 1*vh, 10*vw, 10*vh, 'home'], [12*vw, 1*vh, 10*vw, 10*vh, 'shop_buy'], [78*vw, 1*vh, 10*vw, 10*vh, 'shop_character'], [89*vw, 1*vh, 10*vw, 10*vh, 'shop_song']]
    cvs.pageButtons['start'] = [[1*vw, 1*vh, 10*vw, 10*vh, 'home'], [12*vw, 1*vh, 10*vw, 10*vh, 'start_play'], [67*vw, 1*vh, 10*vw, 10*vh, 'levels_easy'], [78*vw, 1*vh, 10*vw, 10*vh, 'levels_normal'], [89*vw, 1*vh, 10*vw, 10*vh, 'levels_hard']]
    cvs.pageButtons['setting'] = [[1*vw, 1*vh, 10*vw, 10*vh, 'home'], [89*vw, 1*vh, 10*vw, 10*vh, 'logout']]
    cvs.pageButtons['score'] = [[1*vw, 1*vh, 10*vw, 10*vh, 'start'], [89*vw, 1*vh, 10*vw, 10*vh, 'save_score']]
    loginInput = {'login_old':[[30*vw, allIptH*vh, 45*vw, 6*vh, loginInput['login_old'][0][4], 1, loginInput['login_old'][0][6], 'login_mail'], [30*vw, (allIptH+8.5)*vh, 38*vw, 6*vh, loginInput['login_old'][1][4], 2, loginInput['login_old'][1][6], 'login_pwd']], 'forgot_pwd':[[30*vw, allIptH*vh, 45*vw, 6*vh, loginInput['forgot_pwd'][0][4], 1, loginInput['forgot_pwd'][0][6], 'login_mail']], 'login_new':[[30*vw, allIptH*vh, 45*vw, 6*vh, loginInput['login_new'][0][4], 1, loginInput['login_new'][0][6], 'login_mail'], [30*vw, (allIptH+8.5)*vh, 38*vw, 6*vh, loginInput['login_new'][1][4], 2, loginInput['login_new'][1][6], 'login_pwd']], 'checkMail_was_sanded_pwd':[], 'checkMail_was_sanded_mail':[], 'send_pwd_width_mail':[]}
    loginButton = {'login_old':[[69.25*vw, (allIptH+8.5)*vh, 5.75*vw, 6*vh, 'view', 2, loginButton['login_old'][0][6]], [25*vw, (allIptH+17)*vh, 50*vw, 6*vh, 'forgot_pwd', 2], [25*vw, (allIptH+25.5)*vh, 25*vw-2.5*vh/2, 6*vh, 'login_new', 3], [(50)*vw+2.5*vh/2, (allIptH+25.5)*vh, 25*vw-2.5*vh/2, 6*vh, 'login_old', 4]], 'forgot_pwd':[[25*vw, (allIptH+8.5)*vh, 50*vw, 6*vh, 'send_pwd_width_mail', 1], [25*vw, (allIptH+17)*vh, 25*vw-2.5*vh/2, 6*vh, 'login_new', 2], [(50)*vw+2.5*vh/2, (allIptH+17)*vh, 25*vw-2.5*vh/2, 6*vh, 'login_old', 3]], 'login_new':[[69.25*vw, (allIptH+8.5)*vh, 5.75*vw, 6*vh, 'view', 2, loginButton['login_new'][0][6]], [25*vw, (allIptH+17)*vh, 25*vw-2.5*vh/2, 6*vh, 'login_old', 3], [(50)*vw+2.5*vh/2, (allIptH+17)*vh, 25*vw-2.5*vh/2, 6*vh, 'login_new', 4]], 'checkMail_was_sanded_pwd':[[25*vw, (allIptH+8.5)*vh, 50*vw, 6*vh, 'back_to_login', 2]], 'checkMail_was_sanded_mail':[[25*vw, (allIptH+8.5)*vh, 50*vw, 6*vh, 'back_to_login', 2]], 'send_pwd_width_mail':[]}
    menu = {'__hover__':[False, False], 'lang':[1*vw+(10/2+5.5)*vw, 23*vh, 10*vw, 3*vw, menu['lang'][4], False]}
    line_start = 15*vh
    line_stop = 95*vh
    line_height = 6*vh
    arc_r = 5*vw
    item_leave = 60*vw
    item_r = 3*vw
    cvs.alpha = pygame.Surface((cvs.width, cvs.height), pygame.SRCALPHA)
    cvs.alpha_getContex2d = getContext2d(canvas = cvs.alpha)
    middle_line = pygame.Surface((cvs.width, cvs.height), pygame.SRCALPHA)
    middle_line_getContex2d = getContext2d(canvas = middle_line)
    if cvs.page['self'] == 'play':
        set_bg()
reset_variable()
alertBox = []
alertTime = 100
cvs.home_marquee[0] = pygame.image.load(path+'/system/image/run-on-tempo.png') if os.path.exists(path+'/system/image/run-on-tempo.png') else ''
cvs.home_marquee[1] = pygame.image.load(path+'/system/image/bgi-eighthNote.png') if os.path.exists(path+'/system/image/run-on-tempo.png') else ''
cvs.pageBackgroundImage['login'] = pygame.image.load(path+'/system/image/bgi-eighthNote.png')
cvs.pageBackgroundImage['home'] = pygame.image.load(path+'/system/image/bgi-eighthNote.png')
cvs.pageBackgroundImage['player'] = pygame.image.load(path+'/system/image/bgi-dichotomousRest.png')
cvs.pageBackgroundImage['shop'] = pygame.image.load(path+'/system/image/bgi-eighthRest.png')
cvs.pageBackgroundImage['start'] = pygame.image.load(path+'/system/image/bgi-wholeNote.png')
cvs.pageBackgroundImage['setting'] = pygame.image.load(path+'/system/image/bgi-uarterRest.png')
cvs.pageBackgroundMusic['home'] = path+'/system/music/jump.wav'
cvs.pageBackgroundMusic['player'] = path+'/system/music/childhood.wav'
cvs.pageBackgroundMusic['shop'] = path+'/system/music/morningExercises.wav'
cvs.pageBackgroundMusic['start'] = path+'/system/music/nothing.wav'
cvs.pageBackgroundMusic['start_'] = path+'/system/music/nothing.wav'
cvs.pageBackgroundMusic['setting'] = path+'/system/music/water.wav'
se = {'point':False, 'alert':False, 'keyDown':False, 'keyBreak':False, 'prtscn':False}
se['point'] = pygame.mixer.Sound(path+'/system/music/glas_low.wav')
se['alert'] = pygame.mixer.Sound(path+'/system/music/glas_high.wav')
se['keyDown'] = pygame.mixer.Sound(path+'/system/music/touch_high.wav')
se['keyBreak'] = pygame.mixer.Sound(path+'/system/music/touch_low.wav')
se['prtscn'] = pygame.mixer.Sound(path+'/system/music/prtscn.wav')
pi = {'pause_unpause':False, 'pause_retry':False, 'pause_exit':False}
lrkey_input = [False, False]
for pin in pi:
    pi[pin] = pygame.image.load(path+'/system/image/%s.svg'%(pin))
prtscn_white = 0
prtscn_full = 50
prtscns = []
for m in se:
    se[m].set_volume(vfi['se_volume'])
pygame.mixer.music.set_endevent(pygame.USEREVENT+1)
pygame.mixer.music.load(cvs.pageBackgroundMusic['home'])
pygame.mixer.music.play()
pygame.mixer.music.stop()
def where(someThing, someWhere):
    i = -1
    for t in someWhere:
        i += 1
        if t == someThing:
            return i
    return -1
def reset_player():
    cs = ['red', 'orange', 'yellow', 'green', 'darkslategray', 'skyblue', 'blue', 'purple', 'deepwine', 'brown']
    for c in cs:
        fn = cvs.player_data['character']+'/skin/'+cvs.player_data['modeling']+'/item/%s.png'%(c)
        cvs.player_data['item'][c] = pygame.image.load(fn) if os.path.exists(fn) else pygame.image.load(path+'/system/image/bgi-eighthNote.png')
    fn = cvs.player_data['character']+'/skin/'+cvs.player_data['modeling']+'/pause.png'
    cvs.player_data['pause'] = pygame.image.load(fn) if os.path.exists(fn) else pygame.image.load(path+'/system/image/bgi-eighthNote.png')
    fn = cvs.player_data['character']+'/skin/'+cvs.player_data['modeling']+'/score.png'
    cvs.player_data['score'] = pygame.image.load(fn) if os.path.exists(fn) else pygame.image.load(path+'/system/image/bgi-eighthNote.png')
    fn = cvs.player_data['character']+'/skin/'+cvs.player_data['modeling']+'/home.png'
    cvs.home_marquee[1] = pygame.image.load(fn) if os.path.exists(fn) else pygame.image.load(path+'/system/image/bgi-eighthNote.png')
reset_player()
def countDirInner(dir):
    return(len([name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))]))
def homeButtonHover(x, y, w, h):
    flag = MX > x and MX < x+w and MY > y and MY < y+h
    ctx.strokeStyle = (113, 71, 0) if flag else (255, 255, 255)
    ctx.lineWidth = 0.5*vw if flag else 0.1*vw
def homeButtonClick(x, y, w, h, n:str, o = 0):
    global user, point_cooldown, alertBox
    if MX > x and MX < x+w and MY > y and MY < y+h and point_cooldown == 0:
        se['point'].play()
        if n.find('levels_') > -1:
            cvs.page['levels'] = n
        # elif cvs.page['self'] == 'home' and n == 'shop':
        #     alertBox.append([lang[lang['now']]['shop_closed'], alertTime])
        elif cvs.page['self'] == 'score':
            if n == 'start':
                cvs.page['self'] = 'start'
                pygame.mixer.music.play()
                pygame.mixer.music.stop()
                set_fg()
            if n == 'save_score':
                cvs.page['self'] = 'save_score'
                se['prtscn'].stop()
                se['prtscn'].play()
        elif n == 'start_play':
            i = where(cvs.page[cvs.page['start']], cvs.own[cvs.page['start']])
            fn = cvs.own[cvs.page['start']][i]+'/bgi.png'
            if os.path.exists(fn):
                cvs.song_bgi = pygame.image.load(fn)
                f = open(cvs.own[cvs.page['start']][i]+'/'+cvs.page['levels'].replace('levels_', '')+'.json', 'r', encoding='utf-8')
                fi = f.read()
                f.close()
                fi = json.loads(fi) if fi != '' else ''
                cvs.song_data['title'] = fi['title']
                cvs.song_data['left_color'] = color.dot_color[fi['color'][0]]
                cvs.song_data['right_color'] = color.dot_color[fi['color'][1]]
                cvs.song_data['left_color_text'] = fi['color'][0]
                cvs.song_data['right_color_text'] = fi['color'][1]
                cvs.player_data['item']['left'] = cvs.player_data['item'][fi['color'][0]]
                cvs.player_data['item']['right'] = cvs.player_data['item'][fi['color'][1]]
                cvs.song_data['items'] = fi['items']
                cvs.score_data = {'point':0, 'point_p':0, 'combo':0, 'kill':0, 'perfect':0, 'good':0, 'bad':0, 'miss':0}
                cvs.score_data['point_p'] = 1000000 / len(fi['items'])
                for item in cvs.song_data['items']:
                    item['kill'] = False
                cvs.page['self'] = 'play'
                pygame.mixer.music.load(cvs.own[cvs.page['start']][i]+'/bgm.wav')
                pygame.mixer.music.play()
                set_bg()
            else:
                alertBox.append([lang[lang['now']]['error'], alertTime])
        elif cvs.page['self'] == 'player' and n == 'player_use':
            if cvs.page['player'] == 'player_character':
                if cvs.player_data['character'] != cvs.page['player_character'] or cvs.page['player_modeling'] == '':
                    cvs.player_data['character'] = cvs.page['player_character']
                    cvs.player_data['modeling'] = 'auto'
                    cvs.page['player_modeling'] = 'auto'
            # elif cvs.page['player'] == 'player_modeling':
            cvs.player_data['modeling'] = cvs.page['player_modeling']
            reset_player()
        elif cvs.page['self'] == 'shop' and n == 'shop_buy':
            if cvs.page['shop'] == 'shop_character':
                character_name = cvs.page['shop_character'].split('/')[-1]
                if os.path.isdir(path+'/player/'+character_name):
                    alertBox.append([lang[lang['now']]['buyed'], alertTime])
                else:
                    f = open(path+'/system/temporaryStorage/download.zip', 'wb')
                    f.write(file_open(cvs.page['shop_character']+'/download.zip'))
                    f.close()
                    z = zipfile.ZipFile(path+'/system/temporaryStorage/download.zip')
                    z.extractall(r'%s'%(path+'/player/'))
                    z.close()
                cvs.own['player_character'] = os.listdir(path+'/player/')
                for i in range(0, len(cvs.own['player_character'])):
                    cvs.own['player_character'][i] = path + '/player/' + cvs.own['player_character'][i]
                if len(cvs.own['player_character']) < 1:
                    cvs.own['player_character'].append('')
                cvs.page['player_character'] = cvs.own['player_character'][0]
            elif cvs.page['shop'] == 'shop_song':
                song_name = cvs.page['shop_song'].split('/')[-1]
                if os.path.isdir(path+'/song/'+song_name):
                    alertBox.append([lang[lang['now']]['buyed'], alertTime])
                else:
                    f = open(path+'/system/temporaryStorage/download.zip', 'wb')
                    f.write(file_open(cvs.page['shop_song']+'/download.zip'))
                    f.close()
                    z = zipfile.ZipFile(path+'/system/temporaryStorage/download.zip')
                    z.extractall(r'%s'%(path+'/song/'))
                    z.close()
                cvs.own['start_official'] = os.listdir(path+'/song/')
                for i in range(0, len(cvs.own['start_official'])):
                    cvs.own['start_official'][i] = path + '/song/' + cvs.own['start_official'][i]
                if len(cvs.own['start_official']) < 1:
                    cvs.own['start_official'].append('')
                if not(cvs.page['start_official'] in cvs.own['start_official']):
                    cvs.page['start_official'] = cvs.own['start_official'][0]
        elif n == 'logout':
            os.remove('./system/user/user.json')
            cvs.page['self'] = 'login'
            pygame.mixer.music.set_endevent(pygame.USEREVENT+2)
            pygame.mixer.music.stop()
        elif n == 'view':
            loginButton[cvs.login_page][0][6] = False if loginButton[cvs.login_page][0][6] else True
        elif n == 'player_character' or n == 'player_modeling' or n == 'shop_character' or n == 'shop_song' or n == 'start_official' or n == 'start_mine':
            cvs.page[cvs.page['self']] = n
            if n == 'player_modeling':
                if cvs.player_data['character'] == '':
                    alertBox.append([lang[lang['now']]['role_selected'], alertTime])
                    cvs.page[cvs.page['self']] = 'player_character'
                elif os.path.exists(cvs.player_data['character']) == False:
                    alertBox.append([lang[lang['now']]['error'], alertTime])
                    cvs.page[cvs.page['self']] = 'player_character'
                else:
                    cvs.own['player_modeling'] = os.listdir(cvs.player_data['character'] + '/skin')
                    if len(cvs.own['player_modeling']) < 1:
                        cvs.own['player_modeling'].append('')
                    cvs.page['player_modeling'] = cvs.own['player_modeling'][0]
                    i = where(cvs.page['player_modeling'], cvs.own['player_modeling'])
                    fn = cvs.player_data['character']+'/skin/'+cvs.own['player_modeling'][i]+'/fgi.png'
                    cvs.player_data['modeling_fgi'] = pygame.image.load(fn) if os.path.exists(fn) else ''
            cvs.click_switcher()
        elif n == 'forgot_pwd' or n == 'login_old' or n == 'login_new' or n == 'checkMail_was_sanded_pwd' or n == 'send_pwd_width_mail' or n == 'back_to_login':
            if cvs.login_page != n:
                if n == 'send_pwd_width_mail':
                    r = web_open(server+'?t=pwd&m='+loginInput['forgot_pwd'][0][4])
                    print(server+'?t=pwd&m='+loginInput['forgot_pwd'][0][4])
                    if r == None or r == '[]':
                        alertBox.append([lang[lang['now']]['error'], alertTime])
                    else:
                        r = json.loads(r)[0]
                        if r == 'done':
                            cvs.login_page = 'send_pwd_width_mail'
                        elif r == 'new':
                            alertBox.append([lang[lang['now']]['n_pwd_this_mail_after'], alertTime])
                else:
                    cvs.login_page = n
            else:
                if cvs.login_page == 'login_old':
                    r = web_open(server+'?t=old&m='+loginInput['login_old'][0][4]+'&p='+loginInput['login_old'][1][4])
                    if r == None or r == '[]':
                        alertBox.append([lang[lang['now']]['error'], alertTime])
                    else:
                        r = json.loads(r)[0]
                        if r == 'done':
                            cvs.page['self'] = 'home'
                            cvs.login_page = 'login_old'
                            user = {"m":loginInput['login_old'][0][4], "p":loginInput['login_old'][1][4]}
                            userF = open(path+'/system/user/user.json', 'w+')
                            userF.write(json.dumps(user))
                            userF.close()
                            pygame.mixer.music.play()
                        elif r == 'new':
                            alertBox.append([lang[lang['now']]['mail_n'], alertTime])
                        elif r == 'pwd_e':
                            alertBox.append([lang[lang['now']]['pwd_e'], alertTime])
                        elif r == 'mail_uc':
                            alertBox.append([lang[lang['now']]['mail_uc'], alertTime])
                        pygame.mixer.music.set_endevent(pygame.USEREVENT+1)
                        pygame.mixer.music.load(cvs.pageBackgroundMusic['home'])
                        pygame.mixer.music.play()
                        pygame.mixer.music.stop()
                elif cvs.login_page == 'login_new':
                    r = web_open(server+'?t=new&m='+loginInput['login_new'][0][4]+'&p='+loginInput['login_new'][1][4])
                    if r == None or r == '[]':
                        alertBox.append([lang[lang['now']]['error'], alertTime])
                    else:
                        r = json.loads(r)[0]
                        if r == 'done':
                            cvs.login_page = 'checkMail_was_sanded_mail'
                        elif r == 'old':
                            alertBox.append([lang[lang['now']]['mail_o'], alertTime])
        else:
            alertBox = []
            cvs.page['self'] = n
            pygame.mixer.music.stop()
            if n == 'player':
                i = where(cvs.page['player_character'], cvs.own['player_character'])
                fn = cvs.own['player_character'][i]+'/fgi.png'
                cvs.player_data['character_fgi'] = pygame.image.load(fn) if os.path.exists(fn) else ''
            elif n == 'start':
                set_fg()
        point_cooldown = full_point_cooldown
def rotate_triangle(center, scale, mouse_pos):
    vMouse  = pygame.math.Vector2(mouse_pos)
    vCenter = pygame.math.Vector2(center)
    angle   = pygame.math.Vector2().angle_to(vMouse - vCenter)
    points = [(-0.5, -0.866), (-0.5, 0.866), (2.0, 0.0)]
    rotated_point = [pygame.math.Vector2(p).rotate(angle) for p in points]
    triangle_points = [(vCenter + p*scale) for p in rotated_point]
    return(triangle_points)
def loginInputHover(x, y, w, h):
    return(MX > x and MX < x+w and MY > y and MY < y+h)
def loginInputClick(x, y, w, h, n):
    loginInput[cvs.login_page][n-1][6] = True if (MX > x and MX < x+w and MY > y and MY < y+h) else False
def tsj(t, s, j):
    t = str(t)
    s = str(s)
    j = str(j)
    return(j.join(t.split(s)))
def text_against(texts:list):
    texts = texts.copy()
    for i in range(0, len(texts)):
        texts[i] = len(texts[i])
    return(max(texts))
item_key_now = []
def splice(List:list, num:int):
    List = List[:num] + List[num+1:]
    return(List)
def set_bg():
    global middle_line, middle_line_getContex2d, line_start, line_stop, line_height, arc_r
    middle_line.fill((0, 0, 0, 0))
    middle_line.fill((0, 0, 0, 100))
    middle_line_getContex2d.fillStyle = color.white
    for i in range(int(line_start), int(line_stop), int(line_height)):
        middle_line_getContex2d.fillRect(49.5*vw, i, 1*vw, line_height-1*vw if i+(line_height-1*vw) < line_stop else line_stop - i)
    middle_line_getContex2d.lineWidth = 0.2*vw
    middle_line_getContex2d.strokeStyle = color.white
    middle_line_getContex2d.moveTo(49*vw, line_start)
    middle_line_getContex2d.lineTo(49*vw, line_stop, drawLine = True)
    middle_line_getContex2d.moveTo(51*vw-middle_line_getContex2d.lineWidth/2, line_start)
    middle_line_getContex2d.lineTo(51*vw-middle_line_getContex2d.lineWidth/2, line_stop, drawLine = True)
    middle_line_getContex2d.fillStyle = color.white
    middle_line_getContex2d.font = str(int(1.5*vw))+'px '+textFont
    middle_line_getContex2d.fillText(cvs.song_data['title'], 1*vw, 95*vh, fontType = 'file')

    cvs.alpha.fill((0, 0, 0, 0))
    cvs.alpha_getContex2d.fillStyle = cvs.song_data['left_color']
    cvs.alpha_getContex2d.fillBox(50*vw-arc_r, (line_start+line_stop)/2-arc_r, arc_r*2, arc_r*2, arc_r)
    sub_r = arc_r - 1*vw
    cvs.alpha_getContex2d.fillStyle = (0, 0, 0, 0)
    cvs.alpha_getContex2d.fillBox(50*vw-sub_r, (line_start+line_stop)/2-sub_r, sub_r*2, sub_r*2, sub_r)
    sub_r = sub_r - 1*vw
    cvs.alpha_getContex2d.fillStyle = cvs.song_data['left_color']
    cvs.alpha_getContex2d.fillBox(50*vw-sub_r, (line_start+line_stop)/2-sub_r, sub_r*2, sub_r*2, sub_r)
    sub_r = sub_r - 0.5*vw
    cvs.alpha_getContex2d.fillStyle = (0, 0, 0, 0)
    cvs.alpha_getContex2d.fillBox(50*vw-sub_r, (line_start+line_stop)/2-sub_r, sub_r*2, sub_r*2, sub_r)
    cvs.alpha_getContex2d.fillRect(49*vw, 0, 51*vw, cvs.height)
    sub_r = sub_r + 0.5*vw
    cvs.alpha_getContex2d.fillRect(48*vw, (line_start+line_stop)/2-sub_r, 4*vw, sub_r*2)
    middle_line.blit(cvs.alpha, (0, 0))

    cvs.alpha.fill((0, 0, 0, 0))
    cvs.alpha_getContex2d.fillStyle = cvs.song_data['right_color']
    cvs.alpha_getContex2d.fillBox(50*vw-arc_r, (line_start+line_stop)/2-arc_r, arc_r*2, arc_r*2, arc_r)
    sub_r = arc_r - 1*vw
    cvs.alpha_getContex2d.fillStyle = (0, 0, 0, 0)
    cvs.alpha_getContex2d.fillBox(50*vw-sub_r, (line_start+line_stop)/2-sub_r, sub_r*2, sub_r*2, sub_r)
    sub_r = sub_r - 1*vw
    cvs.alpha_getContex2d.fillStyle = cvs.song_data['right_color']
    cvs.alpha_getContex2d.fillBox(50*vw-sub_r, (line_start+line_stop)/2-sub_r, sub_r*2, sub_r*2, sub_r)
    sub_r = sub_r - 0.5*vw
    cvs.alpha_getContex2d.fillStyle = (0, 0, 0, 0)
    cvs.alpha_getContex2d.fillBox(50*vw-sub_r, (line_start+line_stop)/2-sub_r, sub_r*2, sub_r*2, sub_r)
    cvs.alpha_getContex2d.fillRect(0, 0, 51*vw, cvs.height)
    sub_r = sub_r + 0.5*vw
    cvs.alpha_getContex2d.fillRect(48*vw, (line_start+line_stop)/2-sub_r, 4*vw, sub_r*2)
    middle_line.blit(cvs.alpha, (0, 0))

    middle_line_getContex2d.fillText(key[cvs.left_key][0], 47*vw, 92*vh, fontType = 'file')
    middle_line_getContex2d.fillText(key[cvs.right_key][0], 52*vw, 92*vh, fontType = 'file')

is_left_key = 0
is_right_key = 0
while cvs.running:
    point_cooldown = point_cooldown - 1 if point_cooldown > 0 else 0
    item_key_now = []
    oTime = nTime
    nTime = time.time()
    if fpsUDt <= 0:
        fpsUDt = 100
        fpsO = fps
    else:
        fpsUDt -= 1
    fps = 1 / (nTime-oTime) if (nTime-oTime) > 0 else 0
    MX = pygame.mouse.get_pos()[0]
    MY = pygame.mouse.get_pos()[1]
    if is_left_key > 0:
        is_left_key = is_left_key - 1
    else:
        is_left_key = 0
    if is_right_key > 0:
        is_right_key = is_right_key - 1
    else:
        is_right_key = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameQuit()
        if event.type == pygame.MOUSEBUTTONDOWN and (event.button == 1 or event.button == 3):
            lrkey_input = [False, False]
            if cvs.page['self'] == 'home':
                for btn in homeButton:
                    homeButtonClick(btn[0], btn[1], btn[2], btn[3], btn[4])
            if cvs.page['self'] == 'player' or cvs.page['self'] == 'shop' or cvs.page['self'] == 'setting':
                if cvs.page['self'] == 'setting':
                    if loginInputHover(11.5*vw, 47*vh, (len(key[cvs.left_key][0])*2+2)*vw, 3*vw):
                        lrkey_input[0] = True
                    elif loginInputHover((12.5+len(key[cvs.left_key][0])*2+2)*vw, 47*vh, (len(key[cvs.right_key][0])*2+2)*vw, 3*vw):
                        lrkey_input[1] = True
                    if menu['__hover__'][0] == False:
                        if loginInputHover((17.4+2.1)*vw, 30.9*vh, (4.2-2.1)*vw, 3.2*vw):
                            volume['bgm']['+'] = True
                        elif loginInputHover(17.4*vw, 30.9*vh, (4.2-2.1)*vw, 3.2*vw):
                            volume['bgm']['-'] = True
                        elif loginInputHover((17.4+2.1)*vw, 38.9*vh, (4.2-2.1)*vw, 3.2*vw):
                            volume['se']['+'] = True
                        elif loginInputHover(17.4*vw, 38.9*vh, (4.2-2.1)*vw, 3.2*vw):
                            volume['se']['-'] = True
                    menu['lang'][5] = True if loginInputHover(1*vw+(10/2+5.5)*vw, 23*vh, len(lang['now'])*2*vw, 3*vw) else False
                    if menu['__hover__'][0] == 'lang':
                        lang['now'] = menu['__hover__'][1]
                        textFont = './system/font/'+lang[lang['now']]['__font-family__']
                        f = open('./system/user/lang.json', 'w')
                        f.write(json.dumps(lang))
                        f.close()
                        menu['__hover__'] = [False, False]
                        for m in menu:
                            if m != '__hover__':
                                menu[m][5] = False
            if cvs.page['self'] == 'player' or cvs.page['self'] == 'shop' or cvs.page['self'] == 'start':
                cvs.click_switcher()
            cvs.click_pageButtons()
            if cvs.page['self'] == 'login':
                if loginInputHover(75*vw-1.5*len(lang[lang['now']]['use_visitor'])*vw, 80*vh, 1.5*len(lang[lang['now']]['use_visitor'])*vw, 3*vh):
                    user = {'m':lang[lang['now']]['not_logged_in'], 'p':lang[lang['now']]['not_logged_in']}
                    f = open(path+'/system/user/user.json', 'w')
                    f.write(json.dumps(user))
                    f.close()
                    cvs.page['self'] = 'home'
                    pygame.mixer.music.set_endevent(pygame.USEREVENT+1)
                    pygame.mixer.music.load(cvs.pageBackgroundMusic['home'])
                    pygame.mixer.music.play()
                    pygame.mixer.music.stop()
                for ipt in loginInput[cvs.login_page]:
                    loginInputClick(ipt[0], ipt[1], ipt[2], ipt[3], ipt[5])
                for btn in loginButton[cvs.login_page]:
                    homeButtonClick(btn[0], btn[1], btn[2], btn[3], btn[4])
            if cvs.page['self'] == 'play':
                if cvs.page['play'] == '':
                    if loginInputHover(0.5*vw, 2*vh, 4*vw, 8*vh):
                        cvs.page['play'] = 'pause'
                        pygame.mixer.music.pause()
                        se['point'].play()
                elif cvs.page['play'] == 'pause':
                    if loginInputHover(0.5*vw, 2*vh, 4*vw, 8*vh):
                        cvs.page['play'] = ''
                        pygame.mixer.music.unpause()
                        se['point'].play()
                    bs = ['pause_unpause', 'pause_retry', 'pause_exit']
                    bb = 0.5*vw
                    bw = 20*vw
                    bh = 10*vh
                    for i in range(0, len(bs)):
                        if loginInputHover(50*vw-bw/2-bb, (38+i*14)*vh-bh/2-bb, bw+bb*2, bh+bb*2):
                            se['point'].play()
                            if bs[i] == 'pause_unpause':
                                cvs.page['play'] = ''
                                pygame.mixer.music.unpause()
                            elif bs[i] == 'pause_retry':
                                cvs.page['play'] = ''
                                cvs.score_data = {'point':0, 'point_p':0, 'combo':0, 'kill':0, 'perfect':0, 'good':0, 'bad':0, 'miss':0}
                                cvs.score_data['point_p'] = 1000000 / len(cvs.song_data['items'])
                                for item in cvs.song_data['items']:
                                    item['kill'] = False
                                # pygame.mixer.music.stop()
                                pygame.mixer.music.play()
                            elif bs[i] == 'pause_exit':
                                cvs.page['play'] = ''
                                cvs.page['self'] = 'start'
                                pygame.mixer.music.play()
                                pygame.mixer.music.stop()
        if event.type == pygame.MOUSEBUTTONUP:
            for v1 in volume:
                for v2 in volume[v1]:
                    volume[v1][v2] = False
        if event.type == pygame.USEREVENT+1:
            if cvs.pageIs('homeC') and cvs.page['self'] != 'start' or cvs.pageIs('homeS'):
                pygame.mixer.music.load(cvs.pageBackgroundMusic[cvs.page['self']])
                pygame.mixer.music.play()
            elif cvs.page['self'] == 'start':
                if os.path.exists(cvs.pageBackgroundMusic['start']):
                    pygame.mixer.music.load(cvs.pageBackgroundMusic['start'])
                else:
                    pygame.mixer.music.load(cvs.pageBackgroundMusic['start_'])
                pygame.mixer.music.play()
            elif cvs.page['self'] == 'play':
                cvs.page['self'] = 'score'
        if event.type == pygame.KEYDOWN:
            # print(event.key)
            if event.key == pygame.K_TAB:
                print(pygame.mixer.music.get_pos())
            elif event.key == pygame.K_F8:
                fn = './prtscn/run-on-tempo{num}.jpg'.format(num = countDirInner('./prtscn')+1)
                pygame.image.save(cvs.this, fn)
                prtscns.append([pygame.image.load(fn), time.time()])
                prtscn_white = time.time()
            elif cvs.page['self'] == 'setting':
                if lrkey_input[0] == True:
                    if event.key in key:
                        if cvs.right_key == event.key:
                            alertBox.append([lang[lang['now']]['keybuttonrepeat'], alertTime])
                        else:
                            cvs.left_key = event.key
                    else:
                        alertBox.append([lang[lang['now']]['keybuttonerror'], alertTime])
                elif lrkey_input[1] == True:
                    if event.key in key:
                        if cvs.left_key == event.key:
                            alertBox.append([lang[lang['now']]['keybuttonrepeat'], alertTime])
                        else:
                            cvs.right_key = event.key
                    else:
                        alertBox.append([lang[lang['now']]['keybuttonerror'], alertTime])
            elif cvs.page['self'] == 'play':
                if event.key == cvs.left_key:
                    is_left_key = 20
                    item_key_now.append('left')
                elif event.key == cvs.right_key:
                    is_right_key = 20
                    item_key_now.append('right')
            elif cvs.page['self'] == 'login':
                if event.key in key:
                    if event.key == 1073741881:
                        key[1073741881][1] = False if key[1073741881][1] else True
                    else:
                        key[event.key][1] = True
                        key[event.key][2] = 50
                        if key[event.key][0] == '\b':
                            se['keyBreak'].play()
                        elif event.key != 1073742053 and event.key != 1073742049:
                            se['keyDown'].play()
                        for ipt in loginInput[cvs.login_page]:
                            if ipt[6]:
                                if key[event.key][0] == '\b':
                                    ipt[4] = ipt[4][0:len(ipt[4])-1]
                                else:
                                    ipt[4] = ipt[4] + key[event.key][3] if (key[1073742053][1] == True or key[1073742049][1] == True or key[1073741881][1] == True) and len(key[event.key]) > 3 else ipt[4] + key[event.key][0]
        if event.type == pygame.KEYUP:
            if cvs.page['self'] == 'login':
                if event.key in key and event.key != 1073741881:
                    key[event.key][1] = False
    # 截圖特效
    I = 50
    O = 100
    pwt = I + O - (time.time() - prtscn_white)*510
    if pwt > 0:
        pwt = pwt/O*255 if pwt <= O else 255 - (pwt - O)/I*255
        cvs.alpha.fill((255, 255, 255, pwt))
        cvs.this.blit(cvs.alpha, (0, 0))
    # 截圖預覽
    i = 0
    while i < len(prtscns):
        prtscn = prtscns[i]
        T = prtscn_full - (time.time() - prtscn[1])*50
        if prtscn[0] != '' and T > 0:
            bottomT = 20
            rightT = 15
            X = (79+21-(T/rightT*21 if T < rightT else 21))*vw
            Y = (2+76-((T-(prtscn_full-bottomT))/bottomT*76 if T > (prtscn_full-bottomT) else 0))*vh
            ctx.fillStyle = color.white
            ctx.fillRect(X-0.5*vw, Y-1*vh, 21*vw, 22*vh)
            ctx.drawImage(prtscn[0], [X, Y], [20*vw, 20*vh])
            i += 1
        else:
            prtscns = splice(prtscns, i)
    if not cvs.running:
        break
    pygame.display.update()
    pygame.time.Clock().tick(1000)
    cvs.this.fill(cvs.bgc)
    if cvs.pageIs('homeN') or cvs.pageIs('homeC'):
        cvs.draw_pageBackground()
        cvs.draw_pageTitle()
        cvs.draw_pageButtons()
    if cvs.page['self'] == 'login':
        if cvs.login_page == 'send_pwd_width_mail':
            cvs.login_page = 'checkMail_was_sanded_pwd'
        elif cvs.login_page == 'back_to_login':
            cvs.login_page = 'login_old'
        for k in key:
            if key[k][1] == True:
                for ipt in loginInput[cvs.login_page]:
                        if ipt[6]:
                            if key[k][2] > 0:
                                key[k][2] = key[k][2] - 1
                            if key[k][2] == 0:
                                if key[k][0] == '\b':
                                    ipt[4] = ipt[4][0:len(ipt[4])-1]
                                else:
                                    ipt[4] = ipt[4] + key[k][3] if (key[1073742053][1] == True or key[1073742049][1] == True or key[1073741881][1] == True) and len(key[k]) > 3 else ipt[4] + key[k][0]
                                key[k][2] = 5
        cvs.draw_pageBackground()
        for btn in homeButton:
            ctx.fillStyle = (255, 214, 128)
            ctx.fillRect(btn[0], btn[1], btn[2], btn[3])
            ctx.strokeStyle = (255, 255, 255)
            ctx.strokeRect(btn[0], btn[1], btn[2], btn[3])
            ctx.font = str(int(5*vw))+'px '+textFont
            ctx.fillStyle = color.darkBrown
            ctx.fillText(lang[lang['now']][btn[4]], btn[0]+btn[2]/2-5*vw, btn[1]+3*vh, fontType = 'file')
        cvs.alpha.fill((0, 0, 0, 200))
        cvs.this.blit(cvs.alpha, (0, 0))
        ctx.fillStyle = (255, 214, 128)
        r = 0.5*vw
        ctx.fillBox(20*vw-r, 10*vh-r, 60*vw+2*r, 80*vh+2*r, 1*vw)
        ctx.fillStyle = (255, 255, 255)
        ctx.fillBox(20*vw, 10*vh, 60*vw, 80*vh, 1*vw)
        ctx.font = str(int(3*vw))+'px '+textFont
        ctx.fillStyle = color.darkBrown
        ctx.fillText(lang[lang['now']][cvs.login_page], 50*vw-1.5*len(lang[lang['now']][cvs.login_page])*vw, 12*vh, fontType = 'file')
        ctx.fillRect(21*vw, 20*vh, 58*vw, 0.5*vh)
        ctx.font = str(int(1.5*vw))+'px '+textFont
        if loginInputHover(75*vw-1.5*len(lang[lang['now']]['use_visitor'])*vw, 80*vh, 1.5*len(lang[lang['now']]['use_visitor'])*vw, 3*vh):
            ctx.fillStyle = color.orange
            ctx.fillRect(75*vw-1.5*len(lang[lang['now']]['use_visitor'])*vw, 80*vh, 1.5*len(lang[lang['now']]['use_visitor'])*vw, 3*vh)
        ctx.fillStyle = color.darkBrown
        ctx.fillText(lang[lang['now']]['use_visitor'], 75*vw-1.5*len(lang[lang['now']]['use_visitor'])*vw, 80*vh, fontType = 'file')
        ctx.fillText(version, 25*vw, 80*vh, fontType = 'file')
        for input in loginInput[cvs.login_page]:
            ctx.font = str(int(2*vw))+'px '+textFont
            ctx.fillText(lang[lang['now']][input[7]], 25*vw, input[1]+0.5*vh, fontType = 'file')
            r = 0.3*vw
            ctx.fillStyle = color.darkBrown if input[6] or loginInputHover(input[0], input[1], input[2], input[3]) else color.orange
            ctx.fillBox(input[0]-r, input[1]-r, input[2]+2*r, input[3]+2*r, r)
            ctx.fillStyle = color.white
            ctx.fillBox(input[0], input[1], input[2], input[3], r)
            ctx.font = str(int(2.5*vw))+'px '+textFont
            ctx.fillStyle = color.darkBrown
            input[4] = input[4] if len(input[4]) <= 33 else input[4][0:33]
            if input[5] == 2 and loginButton[cvs.login_page][0][6] != True:
                t = ''
                for i in range(0, len(input[4])):
                    t = t + '*'
            else:
                t = input[4]
            ctx.fillText(t, input[0]+1*vw, input[1]+2.5*vh-1.15*vw, fontType = 'file')
        for button in loginButton[cvs.login_page]:
            r = 0.3*vw
            ctx.fillStyle = color.darkBrown if loginInputHover(button[0], button[1], button[2], button[3]) else color.orange
            ctx.fillBox(button[0]-r, button[1]-r, button[2]+2*r, button[3]+2*r, r)
            ctx.fillStyle = color.white
            ctx.fillBox(button[0], button[1], button[2], button[3], r)
            ctx.font = str(int(2.5*vw))+'px '+textFont
            ctx.fillStyle = color.darkBrown
            if button[4] == 'view':
                if loginButton[cvs.login_page][0][6]:
                    t = lang[lang['now']]['hide']
                else:
                    t = lang[lang['now']]['show']
            else:
                t = lang[lang['now']][button[4]]
            ctx.fillText(t, button[0]+button[2]/2-len(t)*2.5/2*vw, button[1]+2.5*vh-1.15*vw, fontType = 'file')
        if len(cvs.login_page) > 20 and cvs.login_page[0:20] == 'checkMail_was_sanded':
            ctx.font = str(int(2.5*vw))+'px '+textFont
            ctx.fillStyle = color.darkBrown
            t = lang[lang['now']][cvs.login_page+'_infoText']
            ctx.fillText(t, (50-len(t)*2.5/2)*vw, allIptH*vh+2.5*vh-1.15*vw, fontType = 'file')
    else:
        if cvs.page['self'] == 'home':
            cvs.draw_pageBackground()
            for btn in homeButton:
                ctx.fillStyle = (255, 214, 128)
                ctx.fillRect(btn[0], btn[1], btn[2], btn[3])
                homeButtonHover(btn[0], btn[1], btn[2], btn[3])
                ctx.strokeRect(btn[0], btn[1], btn[2], btn[3])
                ctx.font = str(int(5*vw))+'px '+textFont
                ctx.fillStyle = color.darkBrown
                ctx.fillText(lang[lang['now']][btn[4]], btn[0]+btn[2]/2-5*vw, btn[1]+3*vh, fontType = 'file')
            if len(cvs.home_marquee) > 0:
                cvs.alpha.fill((0, 0, 0, 0))
                if len(cvs.home_marquee) == 1:
                    cvs.alpha_getContex2d.drawImage(cvs.home_marquee[0], [5*vw, 10*vh], [40*vw, 80*vh])
                else:
                    T = (time.time()-cvs.home_marquee_information['last_time'])
                    F = True if T >= 10 else False
                    T = 0 if T <= 8 else (T-8)/2*40
                    cvs.alpha_getContex2d.drawImage(cvs.home_marquee[cvs.home_marquee_information['now_item']], [(5-T)*vw, 10*vh], [40*vw, 80*vh])
                    cvs.alpha_getContex2d.drawImage(cvs.home_marquee[cvs.home_marquee_information['now_item']+1 if cvs.home_marquee_information['now_item'] < len(cvs.home_marquee)-1 else 0], ((45-T)*vw, 10*vh), (40*vw, 80*vh))
                    cvs.alpha_getContex2d.fillStyle = (0, 0, 0, 0)
                    cvs.alpha_getContex2d.fillRect(0, 0, 2*vw, 100*vh)
                    cvs.alpha_getContex2d.fillRect(48*vw, 0, 52*vw, 100*vh)
                    if F:
                        cvs.home_marquee_information['last_time'] = time.time()
                        cvs.home_marquee_information['now_item'] = cvs.home_marquee_information['now_item']+1 if cvs.home_marquee_information['now_item'] < len(cvs.home_marquee)-1 else 0
                cvs.this.blit(cvs.alpha, (0, 0))
        elif cvs.page['self'] == 'player':
            cvs.draw_switcherBg()
            if cvs.page['player'] == 'player_character' and cvs.player_data['character_fgi'] != '':
                ctx.drawImage(cvs.player_data['character_fgi'], (1*vw, 14*vh), (98*vw, 84*vh))
            elif cvs.page['player'] == 'player_modeling' and cvs.player_data['modeling_fgi'] != '':
                ctx.drawImage(cvs.player_data['modeling_fgi'], (1*vw, 14*vh), (98*vw, 84*vh))
            cvs.draw_switcherFg()
            ctx.fillStyle = color.white
            ctx.strokeStyle = color.black
            ctx.font = 'bg '+str(int(1.5*vw))+'px '+textFont
            ctx.fillText(' '+lang[lang['now']]['using']+lang[lang['now']][cvs.page['player']]+': '+cvs.player_data[cvs.page['player'].replace('player_', '')].replace(path+'/player/', '')+' | '+lang[lang['now']]['seeing']+lang[lang['now']][cvs.page['player']]+': '+cvs.page[cvs.page['player']].replace(path+'/player/', '')+' ', 0, 100*vh, againstX = 'left', againstY = 'bottom', fontType = 'file')
        elif cvs.page['self'] == 'shop':
            cvs.draw_switcherBg()
            if cvs.page['shop'] == 'shop_character' and cvs.shop_data['character_fgi'] != '':
                ctx.drawImage(cvs.shop_data['character_fgi'], (1*vw, 14*vh), (98*vw, 84*vh))
            elif cvs.page['shop'] == 'shop_song' and cvs.shop_data['song_fgi'] != '':
                ctx.drawImage(cvs.shop_data['song_fgi'], (1*vw, 14*vh), (98*vw, 84*vh))
            cvs.draw_switcherFg()
            ctx.fillStyle = color.white
            ctx.strokeStyle = color.black
            ctx.font = 'bg '+str(int(1.5*vw))+'px '+textFont
            itemName = cvs.shop_data[cvs.page['shop'].replace('shop_', '')]
            if len(itemName) > 0:
                ctx.fillText(' '+itemName+' ', 0, 100*vh, againstX = 'left', againstY = 'bottom', fontType = 'file')
        elif cvs.page['self'] == 'start':
            cvs.draw_switcherBg()
            if song_fgi != '':
                ctx.drawImage(song_fgi, (1*vw, 14*vh), (98*vw, 84*vh))
            cvs.draw_switcherFg()
            ctx.fillStyle = color.white
            ctx.strokeStyle = color.black
            ctx.font = 'bg '+str(int(1.5*vw))+'px '+textFont
            ctx.fillText(' '+lang[lang['now']]['seeing']+lang[lang['now']]['start']+': '+cvs.page[cvs.page['start']].replace(path+'/song/', '')+' ', 0, 100*vh, againstX = 'left', againstY = 'bottom', fontType = 'file')
        elif cvs.page['self'] == 'setting':
            ctx.font = str(int(3*vw))+'px '+textFont
            ctx.fillStyle = color.darkBrown
            ctx.fillText(lang[lang['now']]['user']+' : '+user['m'], 3*vw, 15*vh, fontType = 'file')
            ctx.fillStyle = color.white
            ctx.fillRect(11.5*vw, 23*vh, len(lang['now'])*2*vw, 3*vw)
            ctx.fillRect(11.5*vw, 31*vh, 10*vw, 3*vw)
            ctx.fillRect(11.5*vw, 39*vh, 10*vw, 3*vw)
            ctx.fillRect(11.5*vw, 47*vh, (len(key[cvs.left_key][0])*2+2)*vw, 3*vw)
            ctx.fillRect((12.5+len(key[cvs.left_key][0])*2+2)*vw, 47*vh, (len(key[cvs.right_key][0])*2+2)*vw, 3*vw)
            ctx.fillStyle = color.darkBrown
            ctx.fillText(lang[lang['now']]['lang']+' : ', 3*vw, 23*vh, fontType = 'file')
            ctx.fillText(lang['now'], 11.5*vw+len(lang['now'])*vw, 23*vh, fontType = 'file', againstX = 'center')
            ctx.fillText(lang[lang['now']]['bgm_volume']+' : ', 3*vw, 31*vh, fontType = 'file')
            ctx.fillText(str(math.floor(cvs.bgm_volume*100)), 14.45*vw, 31*vh, fontType = 'file', againstX = 'center')
            ctx.fillText(lang[lang['now']]['se_volume']+' : ', 3*vw, 39*vh, fontType = 'file')
            ctx.fillText(str(math.floor(cvs.se_volume*100)), 14.45*vw, 39*vh, fontType = 'file', againstX = 'center')
            ctx.fillText(lang[lang['now']]['keybutton']+' : ', 3*vw, 47*vh, fontType = 'file')
            ctx.fillText(key[cvs.left_key][0], (12.5+len(key[cvs.left_key][0]))*vw, 47*vh, fontType = 'file', againstX = 'center')
            ctx.fillText(key[cvs.right_key][0], (15.5+len(key[cvs.left_key][0])*2+len(key[cvs.right_key][0]))*vw, 47*vh, fontType = 'file', againstX = 'center')
            ctx.fillText(lang[lang['now']]['version']+' : '+str(version), 3*vw, 55*vh, fontType = 'file')
            ctx.fillText(lang[lang['now']]['fps']+' : '+str(fpsO), 3*vw, 63*vh, fontType = 'file')
            # 71
            # 79
            # 87
            ctx.fillText(lang[lang['now']]['developer']+' : 貓虎皮｜MaoHuPi', 3*vw, 90*vh, fontType = 'file')
            ctx.font = str(int(2*vw))+'px '+textFont
            ctx.fillText('-', 18.45*vw, 32*vh, fontType = 'file', againstX = 'center')
            ctx.fillText('+', 20.55*vw, 32*vh, fontType = 'file', againstX = 'center')
            ctx.fillText('-', 18.45*vw, 40*vh, fontType = 'file', againstX = 'center')
            ctx.fillText('+', 20.55*vw, 40*vh, fontType = 'file', againstX = 'center')
            ctx.strokeStyle = color.darkBrown
            if loginInputHover(11.5*vw, 23*vh, len(lang['now'])*2*vw, 3*vw):
                ctx.strokeRect(11.5*vw, 23*vh, len(lang['now'])*2*vw, 3*vw)
            if menu['__hover__'][0] == False:
                if loginInputHover(1*vw+(16.4)*vw, 30.9*vh, (4.2-2.1)*vw, 3.2*vw):
                    ctx.strokeRect(1*vw+(16.4)*vw, 30.9*vh, (4.2-2.1)*vw, 3.2*vw)
                elif loginInputHover(1*vw+(16.4+2.1)*vw, 30.9*vh, (4.2-2.1)*vw, 3.2*vw):
                    ctx.strokeRect(1*vw+(16.4+2.1)*vw, 30.9*vh, (4.2-2.1)*vw, 3.2*vw)
                elif loginInputHover(1*vw+(16.4)*vw, 38.9*vh, (4.2-2.1)*vw, 3.2*vw):
                    ctx.strokeRect(1*vw+(16.4)*vw, 38.9*vh, (4.2-2.1)*vw, 3.2*vw)
                elif loginInputHover(1*vw+(16.4+2.1)*vw, 38.9*vh, (4.2-2.1)*vw, 3.2*vw):
                    ctx.strokeRect(1*vw+(16.4+2.1)*vw, 38.9*vh, (4.2-2.1)*vw, 3.2*vw)
            if loginInputHover(11.5*vw, 47*vh, (len(key[cvs.left_key][0])*2+2)*vw, 3*vw) or lrkey_input[0]:
                ctx.strokeRect(11.5*vw, 47*vh, (len(key[cvs.left_key][0])*2+2)*vw, 3*vw)
            if loginInputHover((12.5+len(key[cvs.left_key][0])*2+2)*vw, 47*vh, (len(key[cvs.right_key][0])*2+2)*vw, 3*vw) or lrkey_input[1]:
                ctx.strokeRect((12.5+len(key[cvs.left_key][0])*2+2)*vw, 47*vh, (len(key[cvs.right_key][0])*2+2)*vw, 3*vw)
        elif cvs.page['self'] == 'play':
            alertBox = []
            ctx.drawImage(cvs.song_bgi, (0, 0), (100*vw, 100*vh))
            cvs.this.blit(middle_line, (0, 0))
            if is_left_key > 0 and cvs.page['play'] != 'pause':
                cvs.alpha.fill((0, 0, 0, 0))
                c = cvs.song_data['left_color']
                cvs.alpha_getContex2d.fillStyle = (c[0], c[1], c[2], 10+is_left_key*5)
                cvs.alpha_getContex2d.fillRect(1*vw, line_start, 48*vw, line_stop-line_start)
                cvs.this.blit(cvs.alpha, (0, 0))
            if is_right_key > 0 and cvs.page['play'] != 'pause':
                cvs.alpha.fill((0, 0, 0, 0))
                c = cvs.song_data['right_color']
                cvs.alpha_getContex2d.fillStyle = (c[0], c[1], c[2], 10+is_right_key*5)
                cvs.alpha_getContex2d.fillRect(51*vw, line_start, 48*vw, line_stop-line_start)
                cvs.this.blit(cvs.alpha, (0, 0))
            # items
            items = cvs.song_data['items']
            R = item_r
            for item in items:
                if item['kill'] != True:
                    T = item['time']
                    CR = T - pygame.mixer.music.get_pos()
                    if CR > -item_leave:
                        A = 255 + CR*255/item_leave if CR < 0 else 255
                        D = deg(item['angle'])
                        LR = math.floor(D/180)
                        LR = 'right' if LR%2 == 0 else 'left'
                        if CR < item_leave/2 and LR in item_key_now:
                            item['kill'] = True
                            cvs.score_data['combo'] += 1
                            cvs.score_data['kill'] += 1
                            if CR < item_leave/4 and CR > -item_leave/4:
                                cvs.score_data['point'] += math.floor(cvs.score_data['point_p'])
                                item['accuracy'] = 'perfect'
                                cvs.score_data['perfect'] += 1
                            elif CR > -item_leave/2:
                                cvs.score_data['point'] += math.floor(cvs.score_data['point_p']*0.8)
                                item['accuracy'] = 'good'
                                cvs.score_data['good'] += 1
                            else:
                                cvs.score_data['point'] += math.floor(cvs.score_data['point_p']*0.5)
                                item['accuracy'] = 'bad'
                                cvs.score_data['bad'] += 1
                        CR = CR if CR > 0 else 0
                        CR = CR*item['speed']/100*vw # "speed"的單位為"cvw/sec(每秒一萬分之幾視窗寬度)"
                        X = 50*vw + math.sin(D)*CR
                        Y = (line_start+line_stop)/2 - math.cos(D)*CR
                        if X > 1*vw-R and X < 99*vw+R and Y > line_start-R and Y < line_stop+R:
                            ctx.drawImage(cvs.player_data['item'][LR], [X-R, Y-R], [R*2, R*2], A)
                    else:
                        item['kill'] = True
                        cvs.score_data['combo'] = 0
                        item['accuracy'] = 'miss'
                        cvs.score_data['miss'] += 1
            # score
            point = str(cvs.score_data['point']) if cvs.score_data['perfect'] < len(items) else '1000000'
            combo = str(cvs.score_data['combo'])
            ctx.fillStyle = color.white
            ctx.font = str(int(4.5*vw))+'px '+textFont
            ctx.fillText(combo, 50*vw, 1.5*vh, againstX = 'center', fontType = 'file')
            ctx.fillText(point, 99*vw, 1.5*vh, againstX = 'right', fontType = 'file')
            ctx.font = str(int(1.5*vw))+'px '+textFont
            ctx.fillText('combo', 50*vw, 10*vh, againstX = 'center', fontType = 'file')
            ctx.fillText('point', 99*vw, 10*vh, againstX = 'right', fontType = 'file')
            # pause mask
            if cvs.page['play'] == 'pause':
                cvs.alpha.fill((0, 0, 0, 100))
                cvs.this.blit(cvs.alpha, (0, 0))
                ctx.drawImage(cvs.player_data['pause'], (60*vw, 20*vh), (40*vw, 80*vh), a = 100)
                ctx.fillStyle = color.white
                ctx.font = str(int(3*vw))+'px '+textFont
                bs = ['pause_unpause', 'pause_retry', 'pause_exit']
                bb = 0.5*vw
                bw = 20*vw
                bh = 10*vh
                for i in range(0, len(bs)):
                    if loginInputHover(50*vw-bw/2-bb, (38+i*14)*vh-bh/2-bb, bw+bb*2, bh+bb*2):
                        cvs.alpha.fill((0, 0, 0, 0))
                        cvs.alpha_getContex2d.fillStyle = color.white
                        cvs.alpha_getContex2d.fillRect(50*vw-bw/2-bb, (38+i*14)*vh-bh/2-bb, bw+bb*2, bh+bb*2)
                        cvs.alpha_getContex2d.fillStyle = (0, 0, 0, 0)
                        cvs.alpha_getContex2d.fillRect(50*vw-bw/2, (38+i*14)*vh-bh/2, bw, bh)
                        cvs.this.blit(cvs.alpha, (0, 0))
                        ctx.drawImage(pi[bs[i]], (50*vw-bw/2, (38+i*14)*vh-bh/2), (bh, bh))
                    ctx.fillText(lang[lang['now']][bs[i]], 50*vw, (38+i*14)*vh, againstX = 'center', againstY = 'center', fontType = 'file')
            # pause button
            top = 0
            left = 0.7*vw
            ishover = loginInputHover(0.5*vw, 2*vh, 4*vw, 8*vh)
            cvs.alpha.fill((0, 0, 0, 0))
            cvs.alpha_getContex2d.fillStyle = color.white if ishover or cvs.page['play'] == 'pause' else (255, 255, 255, 80)
            cvs.alpha_getContex2d.fillRect(left+0.5*vw, top+2*vh, 4*vw, 8*vh)
            cvs.alpha_getContex2d.fillStyle = (0, 0, 0, 0)
            cvs.alpha_getContex2d.fillRect(left+0.75*vw, top+2.5*vh, 3.5*vw, 7*vh)
            cvs.alpha_getContex2d.fillStyle = color.white if ishover or cvs.page['play'] == 'pause' else (255, 255, 255, 80)
            if cvs.page['play'] == 'pause':
                cvs.alpha_getContex2d.beginPath()
                cvs.alpha_getContex2d.moveTo(left+1.6*vw, top+4*vh)
                cvs.alpha_getContex2d.lineTo(left+1.6*vw, top+8*vh)
                cvs.alpha_getContex2d.lineTo(left+3.3*vw, top+6*vh)
                cvs.alpha_getContex2d.closePath()
                cvs.alpha_getContex2d.fill()
            else:
                cvs.alpha_getContex2d.fillRect(left+1.6*vw, top+4*vh, 0.5*vw, 4*vh)
                cvs.alpha_getContex2d.fillRect(left+2.8*vw, top+4*vh, 0.5*vw, 4*vh)
            cvs.this.blit(cvs.alpha, (0, 0))
            ctx.fillStyle = color.white
            ctx.font = str(int(1.5*vw))+'px '+textFont
            ctx.fillText(('play' if cvs.page['play'] == 'pause' else 'pause'), 1*vw, 10*vh, fontType = 'file')
        elif cvs.page['self'] == 'score':
            ctx.drawImage(cvs.song_bgi, (0, 0), (100*vw, 100*vh))
            cvs.alpha.fill((0, 0, 0, 100))
            cvs.this.blit(cvs.alpha, (0, 0))
            ctx.drawImage(cvs.player_data['score'], (60*vw, 20*vh), (40*vw, 80*vh), a = 100)
            cvs.score_data['point'] = 1000000 if cvs.score_data['point'] > 1000000 else cvs.score_data['point'] if cvs.score_data['perfect'] < len(items) else 1000000
            P = cvs.score_data['point']
            cvs.score_data['rating'] = 'FP' if P == 1000000 else 'A+' if P >= 950000 else 'A' if P >= 900000 else 'B+' if P >= 850000 else 'B' if P >= 800000 else 'C+' if P >= 750000 else 'C' if P >= 700000 else 'D+' if P >= 650000 else 'D' if P >= 600000 else 'F'
            scores = ['point', 'combo', 'perfect', 'good', 'bad', 'miss']
            maxlen = text_against(scores)
            ctx.fillStyle = color.white
            ctx.font = str(int(3.5*vw))+'px '+textFont
            for i in range(0, len(scores)):
                s = scores[i]
                ctx.fillText('%s: %s' %(s, cvs.score_data[s]), 53*vw, 13*vh+i*14*vh, fontType = 'file')
            ctx.fillStyle = color.white
            ctx.font = str(int(16*vw))+'px '+path+'/system/font/Zpix.ttf'
            ctx.fillText(cvs.score_data['rating'], 28*vw, 30*vh, fontType = 'file', againstX = 'center')
            ctx.font = str(int(3*vw))+'px '+path+'/system/font/Zpix.ttf'
            ctx.fillText(cvs.song_data['title'], 28*vw, 70*vh, fontType = 'file', againstX = 'center')
            cvs.draw_pageButtons()
        elif cvs.page['self'] == 'save_score':
            ctx.drawImage(cvs.song_bgi, (0, 0), (100*vw, 100*vh))
            cvs.alpha.fill((0, 0, 0, 0))
            cvs.alpha_getContex2d.fillStyle = color.dot_color['green'] if cvs.page['levels'] == 'levels_easy' else color.dot_color['blue'] if cvs.page['levels'] == 'levels_normal' else color.dot_color['red']
            cvs.alpha_getContex2d.fillBox(0.5*vw, 1*vh, 99*vw, 98*vh, 1*vw)
            cvs.alpha_getContex2d.fillStyle = (0, 0, 0, 100)
            cvs.alpha_getContex2d.fillBox(1*vw, 2*vh, 98*vw, 96*vh, 1*vw)
            cvs.this.blit(cvs.alpha, (0, 0))
            ctx.drawImage(cvs.player_data['score'], (59*vw, 18*vh), (40*vw, 80*vh), a = 100)
            cvs.score_data['point'] = 1000000 if cvs.score_data['point'] > 1000000 else cvs.score_data['point'] if cvs.score_data['perfect'] < len(items) else 1000000
            P = cvs.score_data['point']
            cvs.score_data['rating'] = 'FP' if P == 1000000 else 'A+' if P >= 950000 else 'A' if P >= 900000 else 'B+' if P >= 850000 else 'B' if P >= 800000 else 'C+' if P >= 750000 else 'C' if P >= 700000 else 'D+' if P >= 650000 else 'D' if P >= 600000 else 'F'
            scores = ['point', 'combo', 'perfect', 'good', 'bad', 'miss']
            maxlen = text_against(scores)
            ctx.fillStyle = color.white
            ctx.font = str(int(3.5*vw))+'px '+textFont
            for i in range(0, len(scores)):
                s = scores[i]
                ctx.fillText('%s: %s' %(s, cvs.score_data[s]), 53*vw, 13*vh+i*14*vh, fontType = 'file')
            T = time.localtime()
            def TJ(n:int, s:int):
                return(str(n).rjust(s, '0'))
            ctx.font = str(int(1.5*vw))+'px '+textFont
            ctx.fillText('{yy}/{MM}/{dd}  {hh}:{mm}:{ss}'.format(yy = TJ(T.tm_year, 4), MM = TJ(T.tm_mon, 2), dd = TJ(T.tm_mday, 2), hh = TJ(T.tm_hour, 2), mm = TJ(T.tm_min, 2), ss = TJ(T.tm_sec, 2)), 2*vw, 96*vh, fontType = 'file', againstX = 'left', againstY = 'bottom')
            ctx.fillText(user['m'], 98*vw, 96*vh, fontType = 'file', againstX = 'right', againstY = 'bottom')
            ctx.fillStyle = color.white
            ctx.font = str(int(16*vw))+'px '+path+'/system/font/Zpix.ttf'
            ctx.fillText(cvs.score_data['rating'], 28*vw, 30*vh, fontType = 'file', againstX = 'center')
            ctx.font = str(int(3*vw))+'px '+path+'/system/font/Zpix.ttf'
            ctx.fillText(cvs.song_data['title'], 28*vw, 70*vh, fontType = 'file', againstX = 'center')
            fn = './prtscn/run-on-tempo{num}.jpg'.format(num = countDirInner('./prtscn')+1)
            pygame.image.save(cvs.this, fn)
            prtscns.append([pygame.image.load(fn), time.time()])
            prtscn_white = time.time()
            cvs.page['self'] = 'score'
    for m in menu:
        if m != '__hover__' and menu[m][5] == True:
            h = (-1, -1, 0, 0)
            menu['__hover__'] = [False, False]
            for i in range(0, len(menu[m][4])):
                ctx.fillStyle = color.white
                ctx.fillRect(menu[m][0], menu[m][1]+menu[m][3]*i, menu[m][2], menu[m][3])
                ctx.fillStyle = color.darkBrown
                ctx.font = str(int(3*vw))+'px '+textFont
                ctx.fillText(menu[m][4][i], menu[m][0]+0.3*vw, menu[m][1]+menu[m][3]*i, fontType = 'file')
                if loginInputHover(menu[m][0], menu[m][1]+menu[m][3]*i, menu[m][2], menu[m][3]):
                    h = (menu[m][0], menu[m][1]+menu[m][3]*i, menu[m][2], menu[m][3])
                    menu['__hover__'] = [m, menu[m][4][i]]
            ctx.lineWidth = 0.25*vw
            ctx.strokeStyle = color.darkBrown
            ctx.strokeRect(h[0], h[1], h[2], h[3])
    for alertText in alertBox:
        if alertText[1] > 0:
            ctx.fillStyle = color.black
            ctx.fillRect((49.5-len(alertText[0]))*vw, 47*vh, (1+len(alertText[0])*2)*vw, 6*vh)
            ctx.font = str(int(2*vw))+'px '+textFont
            ctx.fillStyle = color.white
            ctx.fillText(alertText[0], (50-len(alertText[0]))*vw, 48*vh, fontType = 'file')
            alertText[1] = alertText[1] - 1
        else:
            alertBox.remove(alertText)
    if loginInputHover((17.4+2.1)*vw, 30.9*vh, (4.2-2.1)*vw, 3.2*vw) != True:
        volume['bgm']['+'] = False
    if loginInputHover(17.4*vw, 30.9*vh, (4.2-2.1)*vw, 3.2*vw) != True:
        volume['bgm']['-'] = False
    if loginInputHover((17.4+2.1)*vw, 39.9*vh, (4.2-2.1)*vw, 3.2*vw) != True:
        volume['se']['+'] = False
    if loginInputHover(17.4*vw, 39.9*vh, (4.2-2.1)*vw, 3.2*vw) != True:
        volume['se']['-'] = False
    cvs.bgm_volume = round(cvs.bgm_volume, 2)
    cvs.se_volume = round(cvs.se_volume, 2)
    if volume['bgm']['+'] and cvs.bgm_volume < 1:
        cvs.bgm_volume = round(cvs.bgm_volume + 0.01, 2)
        pygame.mixer.music.set_volume(cvs.bgm_volume)
    elif volume['bgm']['-'] and cvs.bgm_volume > 0:
        cvs.bgm_volume = round(cvs.bgm_volume - 0.01, 2)
        pygame.mixer.music.set_volume(cvs.bgm_volume)
    elif (volume['se']['+'] and cvs.se_volume < 1) or (volume['se']['-'] and cvs.se_volume > 0):
        if volume['se']['+'] and cvs.se_volume < 1:
            cvs.se_volume = round(cvs.se_volume + 0.01, 2)
        elif volume['se']['-'] and cvs.se_volume > 0:
            cvs.se_volume = round(cvs.se_volume - 0.01, 2)
        for m in se:
            se[m].set_volume(cvs.se_volume)
    i = tsj(tsj(str(pygame.display.get_surface()), '(', 'x'), ')', 'x').split('x')
    if cvs.width != int(i[1]) or cvs.height != int(i[1])/2:
        cvs.width = int(i[1])
        cvs.height = int(i[1])/2
        lw = ctx.lineWidth/vw
        vw = int(i[1])/100
        vh = int(i[1])/200
        ctx.lineWidth = lw*vw
        pygame.display.set_mode((int(cvs.width), int(cvs.height)), pygame.RESIZABLE)
        reset_variable()
    # print(pygame.font.get_fonts())