import pygame
import node
import Setting_Value
import time
import map

size = Setting_Value.Display_Set.display_size
screen = pygame.display.set_mode(size)

import MapList

main_font = pygame.font.Font("Resource\Font\MASQUE__.ttf", 35)
number_font = pygame.font.Font("Resource\Font\Infinite.ttf", 35)

node1 = node.node(213,64,47,128,type= 1)
node2 = node.node(213,192,47,128,type= 2)
node3 = node.node(213,320,47,128,type= 3)

node_group = pygame.sprite.RenderPlain([node1, node2, node3])

NoteList = []
NoteList_Drawer = []

# Initializing the Notes
for i in range(0, MapList.MapList[0].get_note_count()):
    if MapList.Click.get_long_note_length():
        NoteList.append(map.note(MapList.Click.get_long_note_length(), 128, MapList.MapList[0].get_note(), speed=5, isLongNote=True))
        MapList.MapList[0].move_index()
        NoteList_Drawer.append(pygame.sprite.RenderPlain(NoteList[i]))

    else:
        NoteList.append(map.note(27, 128, MapList.MapList[0].get_note(), speed=5))
        MapList.MapList[0].move_index()
        NoteList_Drawer.append(pygame.sprite.RenderPlain(NoteList[i]))

length = 0
Note_Count = 0
MODE_NOTE_FALL = False

image1 = pygame.image.load("Resource\DarkGrey\DarkGrey_Rect64x128.png")
background = pygame.image.load("Resource\Background.jpg").convert()

clock = pygame.time.Clock()

start_time = time.time()
done = False

#pygame.mixer.music.load("Songs\_3R2 - Beyond the Horizon.mp3")
#pygame.mixer.music.play(0)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                for i in range(map.killed_note(0), Note_Count):
                    NoteList_Drawer[i].update(1, True)
            if event.key == pygame.K_s:
                for i in range(map.killed_note(0), Note_Count):
                    NoteList_Drawer[i].update(2, True)
            if event.key == pygame.K_d:
                for i in range(map.killed_note(0), Note_Count):
                    NoteList_Drawer[i].update(3, True)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                for i in range(map.killed_note(0), Note_Count):
                    NoteList_Drawer[i].update(1, True, True)
            if event.key == pygame.K_s:
                for i in range(map.killed_note(0), Note_Count):
                    NoteList_Drawer[i].update(2, True, True)
            if event.key == pygame.K_d:
                for i in range(map.killed_note(0), Note_Count):
                    NoteList_Drawer[i].update(3, True, True)

    TimeBar = pygame.Surface([length, 15])
    TimeBar.fill((255,255,255))

    #backround
    image1.set_alpha(120)
    screen.blit(background, [0, 0])
    pygame.draw.line(screen, (0,0,0),(213,128),(1600,128),2)
    pygame.draw.line(screen, (0,0,0),(213,256),(1600, 256),2)
    pygame.draw.line(screen, (0,0,0),(213,383),(1600, 383),2)
    screen.blit(TimeBar, [213, 384])
    length += 0.1

    screen.blit(main_font.render("Score",True,(0,0,0)), Setting_Value.Display_Set.score_txt )
    screen.blit(main_font.render("Combo", True, (0, 0, 0)), Setting_Value.Display_Set.combo_txt)
    screen.blit(number_font.render(str(map.combo(0)), True, (0, 0, 0)), Setting_Value.Display_Set.combo)

    #=========

    node_group.draw(screen)

    node_group.update()

    end_time= MapList.Click.playtime
    if True:

        if (time.time() - start_time >= MapList.MapList[0].get_sync()):
           if MapList.MapList[0].move_sync_index():
               MODE_NOTE_FALL = True
               Note_Count +=1
               MapList.MapList[0].move_index()

        if MODE_NOTE_FALL:
            for i in range(map.killed_note(0), Note_Count):
                NoteList_Drawer[i].draw(screen)
                NoteList_Drawer[i].update(0,False)



    pygame.display.flip()

    clock.tick(60)
