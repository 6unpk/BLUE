
class Display_size:

    def __init__(self, type=1):
        if type == 1:
            # 1366 x 768

            # About Main Position
            self.display_size = (1366, 768)
            self.center = (573, 324)
            self.main_btn_x =  940
            self.main_btn_start_y = 100
            self.main_btn_set_y = 350
            self.main_btn_exitt_y = 600

            # About SongList Position
            self.easy_x = 130
            self.easy_y = 670
            self.hard_x = self.easy_x + 125
            self.hard_y = self.easy_y
            self.bg_margin = 768
            self.scroll_speed = 128
            self.SongList  = (150, 130)
            self.SongCount = (195, 80)
            self.album_art = (160, 220)
            self.title = (160, 440)
            self.artist = (160, 490)
            self.difficulty = (160, 540)

            # About Game_Ready_State Position
            self.SetTheSpeed = (595, 300)
            self.SongSpeed = (665, 350)
            self.plus_x = 745
            self.plus_y = 350
            self.plus = (self.plus_x, self.plus_y)
            self.minus_x = 600
            self.minus_y = 350
            self.minus = (self.minus_x, self.minus_y)

            # About Game Position
            self.node_x = 110
            self.node1_y = 192
            self.node2_y = 320
            self.node3_y = 448
            self.drawer = (600, 513)
            self.combo_txt = (730, 540)
            self.score_txt = (950, 540)
            self.combo = (780, 580)
            self.score = (950, 580)

            self.note_judge_margin = 135
            self.note_init_pos = 1377

            # About Game Result
            self.result = (450, 200)

            # About Setting Bar Position
            self.Setting = (1000, 100)
            self.menuBar = (450,768)
            self.menuBar_pos = 916

        elif type == 2:
            # 1600 x 1200
            self.display_size = (1600, 1200)
            self.main_btn_x = 1200
            self.main_btn_start_y = 300
            self.main_btn_set_y = 600
            self.main_btn_exitt_y = 900
            self.bg_margin = 1200
            self.scroll_speed = 200



    def change_display_size(self, type):
        if type == 1:
            # 1366 x 768
            self.display_size = (1366, 768)
            self.main_btn_x =  940
            self.main_btn_start_y = 100
            self.main_btn_set_y = 350
            self.main_btn_exitt_y = 600
            self.bg_margin = 768
            self.scroll_speed = 128

            self.easy_x = 130
            self.easy_y = 670
            self.hard_x = self.easy_x + 125
            self.hard_y = self.easy_y
            self.bg_margin = 768
            self.scroll_speed = 128
            self.album_art = (160, 220)
            self.title = (160, 440)
            self.artist = (160, 490)

Display_Set = Display_size()

