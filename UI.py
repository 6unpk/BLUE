#-*- coding: utf-8 -*-
import pygame
import time
import threading
import MapList
import Setting_Value

pygame.init()

# Defined Color
BLACK = (0,0,0)
WHITE = (255,255,255)
NOT_SELECTED = (129,129,129)
SETTING_BAR = (62, 96, 111)
EASY = (12, 232, 118)
HARD = (232, 44, 12)
TIMEBAR = (255, 0, 98)

MODE_GAME_READY = False


class button_main(pygame.sprite.Sprite):
    def __init__(self, screen, msg, x, y, font_size, action=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([30, 30])
        self.image.fill((0,0,0))
        self.image.set_alpha(0)
        self.fadeOut = pygame.Surface(Setting_Value.Display_Set.display_size)
        self.fadeOut.fill(BLACK)
        self.fadeOut.set_alpha(0)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.msg = msg
        self.font_size = font_size
        self.action = action
        self.screen = screen

    def update(self,type = None):
        self.mouse = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()
        if self.x + 150 > self.mouse[0] > self.x and self.y + 90 > self.mouse[1] > self.y:
            font = pygame.font.Font('Resource\Font\MASQUE__.ttf', self.font_size + 30)
            txt = font.render(self.msg, True, WHITE)

            #pygame.mixer.Sound("Sound\sound4.ogg").play()
            if self.click[0] == 1 and type == 1:
                pygame.mixer.Sound("Sound\sound2.ogg").play()
                pygame.time.delay(500)
                return 2
            elif self.click[0] == 1 and type == 2:
                pygame.mixer.Sound("Sound\sound2.ogg").play()
                pygame.time.delay(500)
                return 3
            elif self.click[0] == 1 and type == 3:
                pygame.mixer.Sound("Sound\sound2.ogg").play()
                pygame.mixer.Sound("Sound\sound2.ogg").stop()
                pygame.time.delay(150)
                return 4

        else:
            font = pygame.font.Font('Resource\Font\MASQUE__.ttf', self.font_size)
            txt = font.render(self.msg, True, NOT_SELECTED)

        self.screen.blit(txt,[self.x, self.y])


class button_SongList(pygame.sprite.Sprite):
    selected = 1
    # Easy = 1 / Hard = 2
    def __init__(self, screen, button1_msg,  button1_x, button1_y, button2_msg,  button2_x, button2_y, action =None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([30, 30])
        self.image.fill(BLACK)
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.button1_x = button1_x
        self.button1_y = button1_y
        self.button1_msg = button1_msg
        self.button2_x = button2_x
        self.button2_y = button2_y
        self.button2_msg = button2_msg
        self.screen = screen


    def update(self, selected):
        if selected ==1:
            font = pygame.font.Font('Resource\Font\MASQUE__.ttf', 32)
            self.easy = font.render(self.button1_msg, True, EASY)
            font = pygame.font.Font('Resource\Font\MASQUE__.ttf', 25)
            self.hard = font.render(self.button2_msg, True, NOT_SELECTED)
            self.selected = 1
        if selected == 2:
            font = pygame.font.Font('Resource\Font\MASQUE__.ttf', 32)
            self.hard = font.render(self.button2_msg, True, HARD)
            font = pygame.font.Font('Resource\Font\MASQUE__.ttf', 25)
            self.easy = font.render(self.button1_msg, True, NOT_SELECTED)
            self.selected = 2

        self.screen.blit(self.easy, [self.button1_x, self.button1_y])
        self.screen.blit(self.hard, [self.button2_x, self.button2_y])

    def get_mode(self):
        return self.selected


class button_back(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.screen = screen
    def update(self):
        self.mouse = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()

        font = pygame.font.Font('Resource\Font\MASQUE__.ttf', 20)
        back_txt = font.render("back",True,WHITE)
        self.screen.blit(back_txt, [self.x, self.y])
        if 75 > self.mouse[0] > 25 and  25 < self.mouse[1] <  50:
            if self.click[0] == 1 :
                return True


class MainLogo(pygame.sprite.Sprite):
    Text = "BLUE"
    font = pygame.font.Font('Resource\Font\MASQUE__.ttf',65)
    def __init__(self,x,y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface([250,250])
            self.image.set_alpha(0)
            self.rect =  self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
    def update(self):
        return


class SongList(pygame.sprite.Sprite):
    List= []
    List_map = []
    List_font = []
    List_Background = []
    List_SongInfo = []
    list_focus = 0
    list_count = 0

    start = 200
    margin = 50
    margin_background = 600

    MODE_FADE_OUT = False
    MODE_SCROLL_DOWN = False
    MODE_SCROLL_UP = False
    speed = 0

    first_pos = 0
    pos = 0

    alpha_value = 180
    alpha_value_change_speed = 0

    SongSpeed = 1

    main_font = pygame.font.Font("Resource\Font\MASQUE__.ttf", 35)
    font = pygame.font.Font('Resource\Font\infinite.ttf', 25)
    font2 = pygame.font.Font('Resource\Font\infinite.ttf', 40)
    font3 = pygame.font.Font("Resource\Font\infinite.ttf", 25)
    font4 = pygame.font.Font("Resource\Font\infinite.ttf", 55)
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([500, 1600])
        self.background = pygame.Surface(Setting_Value.Display_Set.display_size)
        self.screen = screen

    def append(self,title, bg_image, artist,difficulty ,map= None):
        self.List.append(title)
        self.List_font.append(self.font.render(title,True,NOT_SELECTED))
        self.List_Background.append(bg_image)
        self.List_map.append(map)
        self.List_SongInfo.append(SongInfo(self.screen,title,artist,None,0,difficulty,None))
        self.list_count +=1

    def update(self, up= False, down= False, Sort_A = False, Sort_B = False, enter= False, SpeedUp = False, SpeedDown = False):
        global list_focus
        self.mouse = pygame.mouse.get_pos()
        self.click = pygame.mouse.get_pressed()
        # gap size between two items
        self.margin = 50
        self.screen.blit(self.background, [0, self.pos])
        selected = pygame.Surface([1600,70])
        selected.fill(NOT_SELECTED)

        if up and self.list_focus > 0:
            if self.MODE_SCROLL_UP:
                return False
            self.list_focus -= 1
            print self.list_focus
            self.start += 60
            sound = pygame.mixer.Sound("Sound\sound1.ogg")
            sound.play()
            self.MODE_SCROLL_UP = True

        if down and self.list_focus < self.list_count-1 :
            if self.MODE_SCROLL_DOWN:
                return False
            self.list_focus += 1
            print self.list_focus
            self.start -= 60
            sound = pygame.mixer.Sound("Sound\sound1.ogg")
            sound.play()
            self.MODE_SCROLL_DOWN = True

        if enter:
            self.MODE_FADE_OUT = True
            self.cover = pygame.Surface(Setting_Value.Display_Set.display_size)
            self.start_time = time.time()
            self.cover.fill(BLACK)
            pygame.mixer.Sound("Sound\sound2.ogg").play()


        if 1600 > self.mouse[0] > 400 and 300 > self.mouse[1] > 230:
            if self.click[0] == 1:
                pygame.time.delay(100)
                self.MODE_FADE_OUT = True
                self.cover = pygame.Surface(Setting_Value.Display_Set.display_size)
                self.start_time = time.time()
                self.cover.fill(BLACK)
                pygame.mixer.Sound("Sound\sound2.ogg").play()

        self.margin_background = 0
        for image in self.List_Background:
            self.screen.blit(image, [0,self.pos + self.margin_background])
            self.margin_background  += Setting_Value.Display_Set.bg_margin

        self.margin_background = 0
        # When Scroll Up
        if self.MODE_SCROLL_UP:
            self.pos += self.speed
            self.speed += Setting_Value.Display_Set.scroll_speed
            self.alpha_value -= self.alpha_value_change_speed
            self.alpha_value_change_speed += 9
            if self.alpha_value > 0:
                self.alpha_value -=1
            for image in self.List_Background:
                self.screen.blit(image, [0, self.pos + self.margin_background])
                self.margin_background += Setting_Value.Display_Set.bg_margin
            if self.pos ==  -Setting_Value.Display_Set.bg_margin * (self.list_focus):
                self.MODE_SCROLL_UP = False
                self.speed = 0
                self.alpha_value = 180
                pygame.mixer.music.fadeout(1200)

        # When Scroll down
        if self.MODE_SCROLL_DOWN:
            self.pos -= self.speed
            self.speed += Setting_Value.Display_Set.scroll_speed
            self.alpha_value -= self.alpha_value_change_speed
            self.alpha_value_change_speed += 9
            for image in self.List_Background:
                self.screen.blit(image, [0, self.pos + self.margin_background])
                self.margin_background += Setting_Value.Display_Set.bg_margin
            if self.pos == -Setting_Value.Display_Set.bg_margin * self.list_focus:
                self.MODE_SCROLL_DOWN = False
                self.speed = 0
                self.alpha_value = 180
                pygame.mixer.music.fadeout(1200)

        # BGM
        if not pygame.mixer.music.get_busy() and not self.isGameReadyMode():
            pygame.time.delay(50)
            pygame.mixer.music.load(MapList.MapList[self.get_selected_Song()].file)
            pygame.mixer.music.play(0, MapList.MapList[self.get_selected_Song()].highlight + 0.01)
            pygame.mixer.music.set_volume(0.5)

        selected.set_alpha(self.alpha_value)
        self.screen.blit(selected, (400, 230))

        i = 0
        for title in self.List:
            self.List_font[i] = (self.font.render(title, True, NOT_SELECTED))
            i +=1
        # only focused item Set Font with WHITE color
        self.List_font[self.list_focus] = self.font2.render(self.List[self.list_focus], True, WHITE)

        # OUTPUT PART
        for i in self.List_font:
            if(i == self.List_font[self.list_focus]):
                self.screen.blit(i, [405, self.start + self.margin])
                self.margin += 60
                continue
            self.screen.blit(i,[450, self.start + self.margin])
            self.margin += 60

        SongsList_txt = self.main_font.render('Song List', True, WHITE)
        self.screen.blit(SongsList_txt, Setting_Value.Display_Set.SongList)

        # COUNT Of Songs
        s = "(%d / %d)" %(self.list_focus+1, self.list_count)
        self.screen.blit(self.font3.render(s,True,WHITE ), Setting_Value.Display_Set.SongCount)

        # Information Of Song
        self.List_SongInfo[self.list_focus].update()

        # Back Button
        if 75 > self.mouse[0] > 25 and 25 < self.mouse[1] < 50:
            if self.click[0] == 1:
                self.MODE_FADE_OUT = False

        # Set The Speed Of Song
        if self.MODE_FADE_OUT:
            self.end_time = time.time()
            gap = (self.end_time - self.start_time)
            if gap < 1:
                self.cover.set_alpha(gap * 215)
                self.screen.blit(self.cover, [0, 0])
            else:
                self.screen.blit(self.cover, [0, 0])
                self.screen.blit(self.font.render("Set The Speed", True, WHITE), Setting_Value.Display_Set.SetTheSpeed)
                self.screen.blit(self.font4.render(str(self.SongSpeed), True, WHITE), Setting_Value.Display_Set.SongSpeed)
                self.screen.blit(self.font2.render("-", True, WHITE), Setting_Value.Display_Set.minus)
                self.screen.blit(self.font2.render("+", True, WHITE), Setting_Value.Display_Set.plus)
                if Setting_Value.Display_Set.plus_x + 65 > self.mouse[0] > Setting_Value.Display_Set.plus_x and Setting_Value.Display_Set.plus_y < self.mouse[1] < Setting_Value.Display_Set.plus_y + 55:
                    if self.click[0]:
                        if self.SongSpeed < 9:
                            self.SongSpeed += 1
                        pygame.time.delay(100)
                if Setting_Value.Display_Set.minus_x + 65 > self.mouse[0] > Setting_Value.Display_Set.minus_x and Setting_Value.Display_Set.minus_y < self.mouse[1] <Setting_Value.Display_Set.minus_y + 55:
                    if self.click[0]:
                        if self.SongSpeed > 1:
                            self.SongSpeed -= 1
                        pygame.time.delay(100)

    def isGameReadyMode(self, bool = None):
        global MODE_GAME_READY
        if bool == None:
            return MODE_GAME_READY
        MODE_GAME_READY = bool
        return MODE_GAME_READY

    def get_selected_Song(self):
        return self.list_focus

    def get_selected_SongSpeed(self):
        return self.SongSpeed


class TimeBar(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Resource\_bar.png")
        self.image.set_colorkey(BLACK)
        self.image = pygame.transform.scale(self.image, (568, 120))
        self.image2 = pygame.image.load("Resource\_bar2.png")
        self.length = 0
        self.screen = screen
        self.speed = 0

    def update(self):
        self.indicator = pygame.Surface([self.length, 45])
        self.indicator.fill(TIMEBAR)

        if self.length > 505:
            self.speed = 0
        self.length += self.speed
        self.screen.blit(self.indicator, (Setting_Value.Display_Set.node_x , Setting_Value.Display_Set.node1_y - 130 ))
        self.screen.blit(self.image, (Setting_Value.Display_Set.node_x - 45, Setting_Value.Display_Set.node1_y - 165))

    def set_endTime(self, _time):
        self.speed = 500/(_time * 60)


class SongInfo(pygame.sprite.Sprite):
    font = pygame.font.Font('Resource\Font\MASQUE__.ttf', 20)
    font2 = pygame.font.Font('Resource\Font\Infinite.ttf', 20)

    def __init__(self, screen, title, artist, album_art, speed, difficulty ,BPM = None):
        pygame.sprite.Sprite.__init__(self)
        self.album_art = pygame.Surface([200, 200])
        self.album_art.set_alpha(0)
        self.screen = screen
        self.artist = artist
        self.title = title
        if len(title) > 16:
            self.title= title[:15]
            self.title += "..."
        self.speed = speed
        self.difficulty = difficulty
        self.BPM = BPM

    def update(self):
        title_txt = self.font2.render(self.title,True,WHITE)
        artist_txt = self.font2.render(self.artist, True, WHITE)
        difficulty_txt = self.font2.render("Level: "+str(self.difficulty) +" lv", True, WHITE)

        self.screen.blit(self.album_art, Setting_Value.Display_Set.album_art)
        self.screen.blit(title_txt, Setting_Value.Display_Set.title)
        self.screen.blit(artist_txt, Setting_Value.Display_Set.artist)
        self.screen.blit(difficulty_txt, Setting_Value.Display_Set.difficulty)
        return


class SettingList(pygame.sprite.Sprite):
    main_font = pygame.font.Font("Resource\Font\MASQUE__.ttf", 35)

    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.menuBar = pygame.Surface(Setting_Value.Display_Set.menuBar)
        self.menuBar.fill(SETTING_BAR)
        self.menuBar.set_alpha(5)
        self.menuBar_pos = 1366
        self.screen = screen

    def update(self):
        # 작아질때 까지 작업을 반복
        if not (self.menuBar_pos < Setting_Value.Display_Set.menuBar_pos):
            self.screen.blit(self.menuBar, [self.menuBar_pos, 0])
            self.menuBar_pos -= 10
        else:
            self.screen.blit(self.menuBar, [self.menuBar_pos, 0])
            self.screen.blit(self.main_font.render("Setting", True, WHITE), Setting_Value.Display_Set.Setting)


class FadeOut(threading.Thread):
    def __init__(self, screen, surface):
        threading.Thread.__init__(self)
        self.screen = screen
        self.surface = surface
        self.start_time = 0

    def set_start_time(self, time):
        self.start_time = time

    def run(self):
        while True:
            end_time = time.time()
            gap = end_time - self.start_time
            if gap < 2:
                self.surface.set_alpha(gap * 55)
                self.screen.blit(self.surface, [0, 0])
            else:
                break


