import pygame
import math
import eyed3
import Setting_Value
import time
import effect

pygame.init()

# Arguments that decide type of notes
Type1 = 1
Type2 = 2
Type3 = 3

temp_score = 0
increase = 0
rest = 0

Killed_Note = 0
Combo = 0
Perfect_count = 0
Great_count = 0
Miss_count = 0
isFirstPressed = False
MODE_FADE_OUT = False


class Map(pygame.sprite.Sprite):

    Speed_tuple = (6, 7, 8, 9, 10, 11, 12, 13, 14, 15)

    def __init__(self, file, title, artist, level, highlight=0, album_art=None, screen=None):
        # Read the Play time of MP3 File
        pygame.sprite.Sprite.__init__(self)
        self.sound = pygame.mixer.Sound(file)
        self.file = file
        self.tag = eyed3.load(file)

        self.song_title = title
        self.artist = artist
        self.playtime = pygame.mixer.Sound.get_length(self.sound) # Second
        self.mode = 1 # Easy 1/ Hard 2
        self.speed = 0

        self.level = level
        # highlight is the time when you want to set
        self.highlight = highlight

        self.note1 = pygame.Surface([15, 65])
        self.note2 = pygame.Surface([15, 65])
        self.note3 = pygame.Surface([15, 65])
        if(album_art != None):
            self.album_art = album_art
        if(screen != None):
            self.screen = screen

        # Easy Mode Map
        self.Group_Note_Map = []
        self.Group_Note_Map_SyncTime = []
        self.Group_LongNote_Map_Length = []
        self.index_map = 0
        self.index_SyncTime = 0
        self.index_LongNote = 0

        # Hard Mode Map
        self.Group_Note_Map_Hard = []
        self.Group_Note_Map_SyncTime_Hard = []
        self.Group_LongNote_Map_Length_Hard = []
        self.index_map_Hard = 0
        self.index_SyncTime_Hard = 0
        self.index_LongNote_Hard = 0

    def add_note(self, type, sync_time, length = None):
        self.Group_Note_Map.append(type)
        self.Group_Note_Map_SyncTime.append(sync_time)
        if length != None:
            self.Group_LongNote_Map_Length.append(length)
        else:
            self.Group_LongNote_Map_Length.append(0)

    def add_note_hard(self, type, sync_time, length=None):
        self.Group_Note_Map_Hard.append(type)
        self.Group_Note_Map_SyncTime_Hard.append(sync_time)
        if length != None:
            self.Group_LongNote_Map_Length_Hard.append(length)
        else:
            self.Group_LongNote_Map_Length_Hard.append(0)

    def set_speed(self, i):
        self.speed = self.Speed_tuple[i]

    def set_mode(self, mode):
        self.mode = mode

    def get_title(self):
        return self.song_title

    def get_artist(self):
        return self.artist

    def get_level(self):
        return self.level

    def get_album_artist(self):
        return self.album_art

    def get_note(self):
        if self.mode == 1:
            return self.Group_Note_Map[self.index_map]
        else:
            return self.Group_Note_Map_Hard[self.index_map_Hard]

    def get_long_note_length(self):
        if self.mode == 1:
            return self.Group_LongNote_Map_Length[self.index_map]
        else:
            return self.Group_LongNote_Map_Length_Hard[self.index_map_Hard]

    def get_sync(self):
        if self.mode == 1:
            return self.Group_Note_Map_SyncTime[self.index_SyncTime]
        else:
            return self.Group_Note_Map_SyncTime_Hard[self.index_SyncTime_Hard]

    def move_sync_index(self):
        if self.mode == 1:
            if self.index_SyncTime < len(self.Group_Note_Map_SyncTime) - 1:
                self.index_SyncTime += 1
                return True
            return False
        else:
            if self.index_SyncTime_Hard < len(self.Group_Note_Map_SyncTime_Hard) - 1:
                self.index_SyncTime_Hard += 1
                return True
            return False

    def move_index(self):
        if self.mode == 1:
            if self.index_map < len(self.Group_Note_Map) - 1:
                self.index_map += 1
        else:
            if self.index_map_Hard < len(self.Group_Note_Map_Hard) - 1:
                self.index_map_Hard += 1

    def get_note_count(self):
        # Last Note is Dummy Note
        if self.mode == 1:
             return self.Group_Note_Map.__len__() - 1
        else:
            return  self.Group_Note_Map_Hard.__len__() - 1

    def init_index(self):
        self.index_SyncTime = 0
        self.index_map = 0
        self.index_LongNote = 0

        self.index_SyncTime_Hard = 0
        self.index_map_Hard = 0
        self.index_LongNote_Hard = 0


class note(pygame.sprite.Sprite):
    Killed_Note = 0
    Combo = 0
    onCount = 0
    MODE_FADE_OUT = None

    def __init__(self, screen, width, height, type, speed =10, isLongNote = False):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.screen = screen
        self.width = width
        if type == 1:
            self.image = pygame.image.load("Resource\_note\_note1.jpg").convert()
        elif type == 2:
            self.image = pygame.image.load("Resource\_note\_note2.jpg").convert()
        else:
            self.image = pygame.image.load("Resource\_note\_note3.jpg").convert()
        self.image = pygame.transform.scale(self.image,(width, height))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.x = Setting_Value.Display_Set.note_init_pos
        self.type = type
        self.isLongNote = isLongNote
        self.LongNote_judge = 3
        if type == 1:
            self.rect.y = Setting_Value.Display_Set.node1_y - 64
        elif type == 2:
            self.rect.y = Setting_Value.Display_Set.node2_y - 64
        else:
            self.rect.y = Setting_Value.Display_Set.node3_y - 64

    def update(self, type = 0, KeyPressed = False, KeyUp = False):
        self.rect.x -= self.speed

        if self.note_fade_out():
            if self.onCount == 0:
                # When This Loop Was First Called, init the start_time
                self.start_time = time.time()
            end_time = time.time() - self.start_time
            self.image.set_alpha(255 - (end_time * 555))
            self.onCount += 1
            if end_time> 1.25:
                self.kill()
                killed_note(1)
                self.onCount = 0
                self.note_fade_out(False)
            return
        if self.isLongNote:
            if isFirstPressed:
                if (self.rect.x + self.width)/3 *2 < Setting_Value.Display_Set.note_judge_margin and KeyUp:
                    print 'done'
                    combo(1)
                    self.note_fade_out(True)
                    score(self.LongNote_judge)
                    is_first_pressed(False)
                elif KeyUp:
                    print 'miss1'
                    combo(0, True)
                    self.note_fade_out(True)
                    score(3)
                    is_first_pressed(False)
            elif Setting_Value.Display_Set.note_judge_margin < self.rect.x < Setting_Value.Display_Set.note_judge_margin + 30 and KeyPressed and self.type == type:
                print 'miss'
                combo(0, True)
                self.note_fade_out(True)
                self.LongNote_judge = 3
                miss(1)
            elif Setting_Value.Display_Set.note_judge_margin - 25 <= self.rect.x < Setting_Value.Display_Set.note_judge_margin and KeyPressed and self.type == type:
                print 'great'
                is_first_pressed(True)
                self.LongNote_judge = 2
            elif Setting_Value.Display_Set.note_judge_margin - 57 <= self.rect.x < Setting_Value.Display_Set.note_judge_margin - 25 and KeyPressed and self.type == type:
                print 'perfect1'
                is_first_pressed(True)
                self.LongNote_judge = 1
            elif not KeyPressed and self.rect.x < Setting_Value.Display_Set.note_judge_margin - 57:
                if self.rect.x + self.width < 230:
                    print 'miss2'
                    combo(0, True)
                    self.note_fade_out(True)
                    score(3)
        else:
            if Setting_Value.Display_Set.note_judge_margin < self.rect.x < Setting_Value.Display_Set.note_judge_margin + 30 and KeyPressed and self.type == type:
                print 'miss'
                combo(0, True)
                self.note_fade_out(True)
                score(3)
                miss(1)
            elif Setting_Value.Display_Set.note_judge_margin - 25 <= self.rect.x < Setting_Value.Display_Set.note_judge_margin and KeyPressed and self.type == type:
                print 'great'
                combo(1)
                self.note_fade_out(True)
                score(2)
                great(1)
            elif Setting_Value.Display_Set.note_judge_margin - 57 < self.rect.x < Setting_Value.Display_Set.note_judge_margin - 25 and KeyPressed and self.type == type:
                print 'perfect'
                combo(1)
                self.note_fade_out(True)
                score(1)
                perfect(1)
            elif self.rect.x < Setting_Value.Display_Set.note_judge_margin -57:
                print 'miss3'
                combo(0,True)
                self.note_fade_out(True)
                score(3)
                miss(1)

    def re_init(self):
        self.alive()
        self.rect.x = Setting_Value.Display_Set.note_init_pos

    def note_fade_out(self, bool = None):
        if bool == None:
            return self.MODE_FADE_OUT
        self.MODE_FADE_OUT = bool
        return self.MODE_FADE_OUT


def combo(increase, init = False):
    global Combo
    if init:
        Combo = 0
    Combo += increase
    return Combo


def killed_note(increase, init = False):
    global Killed_Note
    if init:
        Killed_Note = 0
    Killed_Note += increase
    return Killed_Note


def perfect(increase, init = False):
    global Perfect_count
    if init:
        Perfect_count = 0
    Perfect_count += 1
    return Perfect_count


def great(increase, init = False):
    global Great_count
    if init:
        Great_count = 0
    Great_count += 1
    return Great_count


def miss(increase, init = False ):
    global Miss_count
    if init:
        Miss_count = 0
    Miss_count += 1
    return Miss_count


def is_first_pressed(bool):
    global isFirstPressed
    isFirstPressed = bool
    return isFirstPressed


def score(__type, selected_map=None):
    global temp_score
    global rest
    global increase
    if __type == -1:
        # INIT
        temp_score = 0
        rest = 0
        increase = 0

    if not selected_map == None:
        rest = math.fmod(100000, selected_map.get_note_count())
        increase = (100000 - rest) / selected_map.get_note_count()

    if __type == 1:
        # PERFECT
        temp_score += increase
    elif __type == 2:
        # GREAT
        temp_score += (increase / 10) * 8
    elif __type == 3:
        # MISS
        temp_score += 0

    return int(temp_score)

