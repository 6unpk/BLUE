#-*- coding: utf-8 -*-
import pygame
import UI
import Setting_Value
import time
import node
import map
import math
import effect
import random

# Made By Junu Park

pygame.display.init()
pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()

size = Setting_Value.Display_Set.display_size
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
pygame.display.set_caption("BLUE!")

import MapList

INTRO_STATE = True
SETTING_STATE = False
MAIN_STATE = False
GAME_STATE = False
MAIN_FADE_OUT_STATE = False
EFFECT_ON = False
GAME_READY_STATE = False
PAUSE = False
COMPLETE_STATE = False

tmp = pygame.Surface(Setting_Value.Display_Set.display_size)
tmp.fill(UI.BLACK)

start_button = UI.button_main(screen, "START", Setting_Value.Display_Set.main_btn_x,
                              Setting_Value.Display_Set.main_btn_start_y, 60)
setting_button = UI.button_main(screen, "SETTING", Setting_Value.Display_Set.main_btn_x,
                                Setting_Value.Display_Set.main_btn_set_y, 60)
exit_button = UI.button_main(screen, "EXIT", Setting_Value.Display_Set.main_btn_x,
                             Setting_Value.Display_Set.main_btn_exitt_y, 60)

button_group = pygame.sprite.RenderPlain([start_button, setting_button, exit_button])

Easy_Hard = UI.button_SongList(screen, "EASY", Setting_Value.Display_Set.easy_x, Setting_Value.Display_Set.easy_y,
                               "HARD", Setting_Value.Display_Set.hard_x, Setting_Value.Display_Set.hard_y)


# Font and Image
main_font = pygame.font.Font("Resource\Font\MASQUE__.ttf", 35)
main_font2 = pygame.font.Font("Resource\Font\MASQUE__.ttf",20)
main_font3 = pygame.font.Font("Resource\Font\MASQUE__.ttf",60)
number_font = pygame.font.Font("Resource\Font\Infinite.ttf", 35)
background = pygame.image.load("image2.jpg").convert()
main_bck = pygame.image.load("Resource\main_background.jpg").convert()
main_bck.set_alpha(80)
drawer = pygame.image.load("Resource\Drawer.png").convert()
drawer.set_colorkey(UI.BLACK)

# Back Button
Back_Btn = UI.button_back(screen, 25,25)

# Song List
List = UI.SongList(screen)
for Map in MapList.MapList:
    List.append(Map.get_title(), pygame.image.load("image"+str(random.randrange(2, 5)) + ".jpg").convert(), Map.get_artist(), Map.get_level())

# About Setting
Setting = UI.SettingList(screen)

# Background Music

Selected = 1
alpha = 0
comp = 0

# About Game

node1 = node.node(Setting_Value.Display_Set.node_x, Setting_Value.Display_Set.node1_y, 47, 128, 1, screen)
node2 = node.node(Setting_Value.Display_Set.node_x, Setting_Value.Display_Set.node2_y, 47, 128, 2, screen)
node3 = node.node(Setting_Value.Display_Set.node_x, Setting_Value.Display_Set.node3_y, 47, 128, 3, screen)

node_group = pygame.sprite.RenderPlain([node1, node2, node3])

time_bar = UI.TimeBar(screen)

NoteList = []
NoteList_Drawer = []

Note_Count = 0
MODE_NOTE_FALL = False


# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while not done:

    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            pygame.mixer.music.stop()
            done = True

        if event.type == pygame.KEYDOWN and MAIN_FADE_OUT_STATE:
            if event.key == pygame.K_KP_ENTER:
                GAME_READY_STATE = True
                pygame.mixer.music.fadeout(1500)
                List.isGameReadyMode(True)
                start_time = time.time()
        if event.type == pygame.KEYDOWN and (MAIN_STATE == True) and (MAIN_FADE_OUT_STATE == False):
            if event.key == pygame.K_UP:
                List.update(True,False)
            if event.key == pygame.K_DOWN:
               List.update(False,True)
            if event.key == pygame.K_KP_ENTER :
                List.update(False,False,False,False,True)
                MAIN_FADE_OUT_STATE =True
            if event.key == pygame.K_ESCAPE:
                MAIN_STATE = False
                INTRO_STATE = True
                pygame.mixer.music.stop()
                pygame.time.delay(300)
        if event.type == pygame.MOUSEBUTTONDOWN and MAIN_STATE and MAIN_FADE_OUT_STATE == False:
            if event.button == 5:
                List.update(False, True)
        if event.type == pygame.MOUSEBUTTONUP and MAIN_STATE and MAIN_FADE_OUT_STATE == False:
            if event.button == 4:
                List.update(True, False)
        if event.type == pygame.MOUSEBUTTONUP and MAIN_FADE_OUT_STATE:
            if event.button == 4:
                List.update()
        if event.type == pygame.MOUSEBUTTONDOWN and MAIN_FADE_OUT_STATE:
            if event.button == 5:
                List.update()

    if GAME_STATE:

        while COMPLETE_STATE:
            tmp.set_alpha(100)
            screen.blit(tmp, [0, 0])
            result_txt = main_font3.render("Result", True, UI.WHITE)
            score_txt = main_font.render("Score", True, UI.WHITE)
            rank_txt = main_font.render("Rank", True, UI.WHITE)

            screen.blit(result_txt, Setting_Value.Display_Set.result)

            if Back_Btn.update():
                GAME_STATE = False
                MAIN_STATE = True
                COMPLETE_STATE = False

                pass

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.time.delay(200)
                        COMPLETE_STATE = False
                        GAME_READY_STATE = False

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
            # --- Limit to 60 frames per second
            clock.tick(60)

        tmp.set_alpha(75)
        screen.blit(tmp, [0, 0])

        while PAUSE:
            if Back_Btn.update():
                pygame.mixer.unpause()
                MapList.MapList[List.get_selected_Song()].sound.stop()
                GAME_STATE = False
                GAME_READY_STATE = False
                MAIN_STATE = True
                List.isGameReadyMode(False)
                # Clear the NoteList When Game Finished
                for i in range(0, MapList.MapList[List.get_selected_Song()].get_note_count()):
                    NoteList.pop()
                    NoteList_Drawer.pop()
                break

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.time.delay(200)
                        pygame.mixer.unpause()
                        PAUSE = False
                        GAME_READY_STATE = False
            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
            # --- Limit to 60 frames per second
            clock.tick(60)

        while GAME_READY_STATE:
            end_time = MapList.MapList[List.get_selected_Song()].playtime

            # background
            screen.blit(background, [0, 0])
            pygame.draw.line(screen, (0, 0, 0), (0, 128),
                             (Setting_Value.Display_Set.note_init_pos, 128), 2)
            pygame.draw.line(screen, (0, 0, 0), (0, 256),
                             (Setting_Value.Display_Set.note_init_pos, 256), 2)
            pygame.draw.line(screen, (0, 0, 0), (0, 383),
                             (Setting_Value.Display_Set.note_init_pos, 383), 2)
            pygame.draw.line(screen, (0, 0, 0), (0, 513),
                             (Setting_Value.Display_Set.note_init_pos, 513), 2)
            time_bar.update()

            screen.blit(drawer, Setting_Value.Display_Set.drawer)
            screen.blit(main_font.render("combo", True, UI.WHITE), Setting_Value.Display_Set.combo_txt)
            screen.blit(main_font.render("score", True, UI.WHITE), Setting_Value.Display_Set.score_txt)
            screen.blit(number_font.render(str(map.combo(0)), True, UI.WHITE), Setting_Value.Display_Set.combo)
            screen.blit(number_font.render(str(map.score(0)), True, UI.WHITE), Setting_Value.Display_Set.score)

            node_group.draw(screen)
            tmp.set_alpha(alpha)
            screen.blit(tmp, [0,0])
            gap = time.time() - start_time
            if gap < 2:
                title = main_font3.render("Ready", True, UI.WHITE)
                title = pygame.transform.rotate(title, math.sin(gap * 30))
            elif 2 <= gap < 4:
                title = main_font3.render("Start", True, UI.WHITE)
            else:
                # Get Selected Mode of Song(Easy or Hard)
                MapList.MapList[List.get_selected_Song()].set_mode(Easy_Hard.get_mode())
                print Easy_Hard.get_mode()
                # Right before Game Begin
                for i in range(0, MapList.MapList[List.get_selected_Song()].get_note_count()):
                    # 노트 초기화의 과정(Note Initializing)
                    if MapList.MapList[List.get_selected_Song()].get_long_note_length():
                        # case Long Note
                        NoteList.append(
                            map.note(screen, MapList.MapList[List.get_selected_Song()].get_long_note_length(), 128, MapList.MapList[0].get_note(), MapList.MapList[List.get_selected_Song()].speed,
                                     isLongNote=True))
                        MapList.MapList[List.get_selected_Song()].move_index()
                        NoteList_Drawer.append(pygame.sprite.RenderPlain(NoteList[i]))
                    else:
                        # case Normal Note
                        NoteList.append(map.note(screen, 27, 128, MapList.MapList[0].get_note(), MapList.MapList[List.get_selected_Song()].speed))
                        MapList.MapList[List.get_selected_Song()].move_index()
                        NoteList_Drawer.append(pygame.sprite.RenderPlain(NoteList[i]))

                for i in range(0, MapList.MapList[List.get_selected_Song()].get_note_count()):
                    # 노트 재 할당(노트 위치 초기화)
                    NoteList[i].re_init()

                MapList.MapList[List.get_selected_Song()].sound.play()
                Note_Count = 0
                # revising value of the sync_time  = comp
                comp = Setting_Value.Display_Set.note_init_pos / (MapList.MapList[List.get_selected_Song()].speed * 60)
                start_time = time.time()
                break
            screen.blit(title, Setting_Value.Display_Set.center)

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
            # --- Limit to 60 frames per second
            clock.tick(60)

        # When Game is Playing
        while pygame.mixer.get_busy() and not PAUSE:
            end_time = MapList.MapList[List.get_selected_Song()].playtime

            if time.time() - start_time > end_time:
                pygame.mixer.quit()
                COMPLETE_STATE = True
                break
            screen.fill(UI.BLACK)

            # background
            screen.blit(background, [0, 0])
            pygame.draw.line(screen, (0, 0, 0), (0, 128),
                             (Setting_Value.Display_Set.note_init_pos, 128), 2)
            pygame.draw.line(screen, (0, 0, 0), (0, 256),
                             (Setting_Value.Display_Set.note_init_pos, 256), 2)
            pygame.draw.line(screen, (0, 0, 0), (0, 383),
                             (Setting_Value.Display_Set.note_init_pos, 383), 2)
            pygame.draw.line(screen, (0, 0, 0), (0, 513),
                             (Setting_Value.Display_Set.note_init_pos, 513), 2)

            screen.blit(tmp, [0,0])
            time_bar.update()
            node_group.draw(screen)

            pygame.draw.rect(screen,(106,141,246),[0,500,1500,300])
            screen.blit(drawer, Setting_Value.Display_Set.drawer)
            screen.blit(main_font.render("combo", True, UI.WHITE), Setting_Value.Display_Set.combo_txt)
            screen.blit(main_font.render("score", True, UI.WHITE), Setting_Value.Display_Set.score_txt)
            screen.blit(number_font.render(str(map.combo(0)), True, UI.WHITE), Setting_Value.Display_Set.combo)
            screen.blit(number_font.render(str(map.score(0)), True, UI.WHITE), Setting_Value.Display_Set.score)

            node_group.update(False, False)
            effect.note_anim1.blit(screen,(Setting_Value.Display_Set.node_x + 27, Setting_Value.Display_Set.node1_y -64))
            effect.note_anim2.blit(screen,(Setting_Value.Display_Set.node_x + 27, Setting_Value.Display_Set.node2_y -64))
            effect.note_anim3.blit(screen,(Setting_Value.Display_Set.node_x + 27, Setting_Value.Display_Set.node3_y -64))

            if time.time() - start_time >= MapList.MapList[List.get_selected_Song()].get_sync() - comp:
                if MapList.MapList[List.get_selected_Song()].move_sync_index():
                    MODE_NOTE_FALL = True
                    Note_Count += 1
                    MapList.MapList[List.get_selected_Song()].move_index()

            if MODE_NOTE_FALL:
                for i in range(map.killed_note(0), Note_Count):
                    NoteList_Drawer[i].draw(screen)
                    NoteList_Drawer[i].update(0)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.stop()
                    GAME_STATE = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        effect.note_anim1.play()
                        for i in range(map.killed_note(0), Note_Count):
                            NoteList_Drawer[i].update(1, True)
                        node1.update(True, False, 1)

                    if event.key == pygame.K_s:
                        effect.note_anim2.play()
                        for i in range(map.killed_note(0), Note_Count):
                            NoteList_Drawer[i].update(2, True)
                        node2.update(True, False, 2)
                    if event.key == pygame.K_d:
                        effect.note_anim3.play()
                        for i in range(map.killed_note(0), Note_Count):
                            NoteList_Drawer[i].update(3, True)
                        node3.update(True, False, 3)
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.pause()
                        PAUSE = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        effect.note_anim1.stop()
                        for i in range(map.killed_note(0), Note_Count):
                            NoteList_Drawer[i].update(1, True, True)
                        node1.update(False, True, 1)
                    if event.key == pygame.K_s:
                        effect.note_anim2.stop()
                        for i in range(map.killed_note(0), Note_Count):
                            NoteList_Drawer[i].update(2, True, True)
                        node2.update(False, True, 2)
                    if event.key == pygame.K_d:
                        effect.note_anim3.stop()
                        for i in range(map.killed_note(0), Note_Count):
                            NoteList_Drawer[i].update(3, True, True)
                        node3.update(False, True, 3)
            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
            # --- Limit to 60 frames per second
            clock.tick(60)

    # --- INTRO SCENE LOOP ---
    elif INTRO_STATE:
        # Intro Scene

        screen.fill(UI.BLACK)
        screen.blit(main_bck, [0,0])

        button_group.draw(screen)

        if 2 == start_button.update(1):
            INTRO_STATE = False
            MAIN_STATE = True
        if 3 == setting_button.update(2):
            SETTING_STATE = True
            INTRO_STATE = False
        if 4 == exit_button.update(3):
            pygame.mixer.music.fadeout(2700)
            pygame.time.delay(3000)
            pygame.mixer.music.pause()
            pygame.mixer.music.stop()
            pygame.time.delay(500)
            exit()
        pygame.display.flip()
        clock.tick(60)

    # --- SONG_LIST SCENE LOOP ---
    elif MAIN_STATE:
        # Songs List

        screen.fill(UI.BLACK)

        now_item = List.get_selected_Song()

        List.update()
        if Back_Btn.update() and MAIN_FADE_OUT_STATE == False:
            MAIN_STATE = False
            INTRO_STATE = True
            pygame.time.delay(100)
        if Back_Btn.update() and MAIN_FADE_OUT_STATE:
            MAIN_FADE_OUT_STATE = False
            pygame.time.delay(100)

        Easy_Hard.update(Selected)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Easy and Hard Btn
        if Setting_Value.Display_Set.easy_x + 85 > mouse[0] > Setting_Value.Display_Set.easy_x and Setting_Value.Display_Set.easy_y < mouse[1] < Setting_Value.Display_Set.easy_y + 30:
            if click[0] == 1:
                pygame.mixer.Sound("Sound\sound3.ogg").play()
                Selected = 1
                Easy_Hard.update(Selected)
                pygame.time.delay(100)
        elif Setting_Value.Display_Set.hard_x + 85 > mouse[0] > Setting_Value.Display_Set.hard_x and Setting_Value.Display_Set.hard_y < mouse[1] < Setting_Value.Display_Set.hard_y + 30:
            if click[0] == 1:
                pygame.mixer.Sound("Sound\sound3.ogg").play()
                Selected = 2
                Easy_Hard.update(Selected)
                pygame.time.delay(100)
        if GAME_READY_STATE:
            gap = (time.time() - start_time)
            if gap < 2.5:
                tmp.set_alpha(gap * 155)
                screen.blit(tmp, [0, 0])
            elif 2 <= gap < 4.8 :
                alpha = 255 - (gap - 2) * 45
                tmp.set_alpha(alpha)
                end_time = MapList.MapList[List.get_selected_Song()].playtime

                # background
                screen.blit(background, [0, 0])
                pygame.draw.line(screen, (0, 0, 0), (0, 128), (Setting_Value.Display_Set.note_init_pos, 128), 2)
                pygame.draw.line(screen, (0, 0, 0), (0, 256), (Setting_Value.Display_Set.note_init_pos, 256), 2)
                pygame.draw.line(screen, (0, 0, 0), (0, 383), (Setting_Value.Display_Set.note_init_pos, 383), 2)
                pygame.draw.line(screen, (0, 0, 0), (0, 513), (Setting_Value.Display_Set.note_init_pos, 513), 2)


                screen.blit(drawer, Setting_Value.Display_Set.drawer)
                screen.blit(main_font.render("combo", True, UI.WHITE), Setting_Value.Display_Set.combo_txt)
                screen.blit(main_font.render("score", True, UI.WHITE), Setting_Value.Display_Set.score_txt)
                screen.blit(number_font.render(str(map.combo(0)), True, UI.WHITE), Setting_Value.Display_Set.combo)
                screen.blit(number_font.render(str(map.score(0)), True, UI.WHITE), Setting_Value.Display_Set.score)

                time_bar.set_endTime(end_time)
                time_bar.update()
                node_group.draw(screen)
                screen.blit(tmp, [0, 0])
                if gap >= 4.6 :
                    GAME_STATE = True
                    MAIN_STATE = False
                    PAUSE = False
                    MapList.MapList[List.get_selected_Song()].init_index()
                    MapList.MapList[List.get_selected_Song()].set_speed(List.SongSpeed-1)
                    map.killed_note(0, True)
                    map.combo(0, True)
                    map.score(-1, MapList.MapList[List.get_selected_Song()])
                    start_time = time.time()

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # --- SETTING BAR LOOP ---
    elif SETTING_STATE:


        """
        Setting_Value.Display_Set.change_display_size(2)
        screen = pygame.display.set_mode(Setting_Value.Display_Set.display_size, pygame.FULLSCREEN)
        """


        if Back_Btn.update():
            SETTING_STATE = False
            INTRO_STATE = True

        Setting.update()
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)


