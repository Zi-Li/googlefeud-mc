from random import choice
from tkinter import *
from functools import partial
from datafile_reader import read_datafile
from os import listdir
from os.path import isfile, join, dirname

QUESTION_PATH = join(dirname(__file__),"questions")

XMARGIN = 5
YMARGIN = 5
CELL_WIDTH = 14
QUESTION_FILES = [join(QUESTION_PATH, f) for f in listdir(QUESTION_PATH) if isfile(join(QUESTION_PATH, f))]

# COLOUR_DESAT = {
#     "#4285f4": "#6F90C7",
#     "#db4437": "#AC6C66",
#     "#f4b400": "#ab9149",
#     "#0f9d58": "#3a7257"
# }

# FUNCTIONS FOR TILE FRAME
class TILE_FRAME_TOOL:
    def __init__(self, team1, team2, alt_team=False):
        self.active_team = team1
        self.other_team = team2
        if alt_team:
            self.active_team = team2
            self.other_team = team1
        self.colour_teams()
        self.buttons_left = 0
        self.correct_left = 0
        
    def populate_tile_frame(self, correct, wrong, point_dict, tile_frame: Frame, button_width, correct_res, wrong_frame):
        tile_row_num = 5
        tile_col_num = 3
        tiles = [None] * tile_row_num
        choices_left = correct + wrong
        for i in range(tile_row_num):
            tiles[i] = [None] * tile_col_num
            for j in range(tile_col_num):
                self.buttons_left += 1
                tile_text = choice(choices_left)
                tiles[i][j] = Button(tile_frame, bg=pick_colour(i,j), fg="white", font=('ariel',20,'bold')) 
                tiles[i][j].configure(text=tile_text, width=button_width, wraplength=180, height=3, 
                                      command=partial(self.button_action,tile_text,wrong_frame,point_dict,correct_res, tiles[i][j], i, j))
                tiles[i][j].grid(column=j,row=i,columnspan=1,rowspan=1)
                choices_left.remove(tile_text)
        self.correct_left = len(correct)

    def clean_tile_frame(self, tile_frame: Frame):
        for elem in list(tile_frame.children.values()).copy():
            elem.destroy()

    def button_action(self, word, wrong_label: LabelFrame, point_dict, correct_res, button: Button, i, j):
        self.buttons_left -= 1
        if is_correct(correct_res, word):
            self.correct_left -= 1
            reveal_correct_label(correct_res, word, point_dict[word])
            edit_team_score(get_team_score(self.active_team) + point_dict[word], self.active_team)
        else:
            add_wrong_label(wrong_label, word)
        button.configure(bg="#666666", disabledforeground="#aaaaaa")
        button['state'] = DISABLED
        if self.correct_left == 0:
            self.decolour_teams()
            # depress all buttons
            frame = button.master
            for bu in list(frame.children.values()):
                bu.configure(bg="#666666", disabledforeground="#aaaaaa")
                bu['state'] = DISABLED
        else:
            self.active_team, self.other_team = self.other_team, self.active_team
            self.colour_teams()
        
    def colour_teams(self):
        self.active_team.configure(font=("ariel",24,'bold'), fg="#4285f4")
        self.other_team.configure(font=("ariel",24), fg="black")
        set_current_team(self.active_team.master.nametowidget("current_team"),self.active_team.cget("text").split(":")[0])
        
    def decolour_teams(self):
        self.active_team.configure(font=("ariel",24), fg="black")
        self.other_team.configure(font=("ariel",24), fg="black")
        clear_current_team(self.active_team.master.nametowidget("current_team"))

def pick_colour(row,col):
    colours = ["#4285f4","#db4437","#f4b400","#0f9d58"]
    index = (col + row) % len(colours)
    return colours[index]

# FUNCTIONS FOR PROMPT FRAME
def setup_prompt(prompt_text, prompt_frame):
    prompt = Text(prompt_frame, font=("ariel",22,'bold'), bg="#ffffff", height=1, width=40)
    prompt.insert(1.0, " " + prompt_text)
    prompt.configure(state=DISABLED, inactiveselectbackground="#ffffff")
    prompt.pack(anchor="center")
    return prompt

def change_prompt(new_text, prompt_elem: Text):
    prompt_elem.configure(state=NORMAL)
    prompt_elem.delete(1.0, END)
    prompt_elem.insert(1.0, " " + new_text)
    prompt_elem.configure(state=DISABLED)


# FUNCTIONS FOR TEAM FRAME      
def setup_team_frame(points_frame: Frame, team_name1="Team 1", team_name2="Team 2"):
    title_lbl = googlefeud_logo(points_frame, font=("ariel",32,'bold'))
    title_lbl.grid(column=1,row=0, columnspan=1,rowspan=1, sticky='N', pady=4)

    line = Canvas(points_frame, height=1, width=points_frame.winfo_width(), bg="#7d7d7d")
    line.grid(column=0,row=1, columnspan=3, rowspan=1, sticky='NSEW', pady=4)
    
    team1_lbl = Label(points_frame, text=f"{team_name1}: 0", font=("ariel",20))
    team1_lbl.grid(column=0,row=2, columnspan=1, rowspan=1, sticky='W')

    team2_lbl = Label(points_frame, text=f"{team_name2}: 0", font=("ariel",20))
    team2_lbl.grid(column=2,row=2, columnspan=1, rowspan=1, sticky='E')
    
    current_team = Label(points_frame, text="", font=("ariel",22,'bold','underline'), fg="red", name="current_team")
    current_team.grid(column=1,row=2, columnspan=1, rowspan=1, sticky='N')
    
    return team1_lbl, team2_lbl

def set_current_team(elem, team_name):
    elem.configure(text=f"{team_name}'s turn")
def clear_current_team(elem):
    elem.configure(text=f"")
    
def edit_team_score(new_score, team_label: Label):
    team_text = team_label.cget("text")
    splitted_text = team_text.split(":")
    team_label.config(text=f"{splitted_text[0]}: {new_score}")

def get_team_score(team_label: Label):
    return int(team_label.cget("text").split(":")[1])

# RESULT FRAME
def setup_result_frame(result_frame, points_dict, correct):
    heading1 = Label(result_frame, text="Correct Answers:", justify='left', font=('ariel',18,'bold','underline'))
    heading1.grid(column=0,row=0,columnspan=2,rowspan=1, sticky='W',pady=5)
    heading2 = Label(result_frame, text="Incorrect Answers:", justify='left', font=('ariel',18,'bold', 'underline'))
    heading2.grid(column=0,row=5,columnspan=2,rowspan=1, sticky='W', pady=5)
    correct_labels = LabelFrame(result_frame, bg="#4285F4")
    correct_labels.grid(column=0,row=1,columnspan=1,rowspan=4,pady=5, sticky="W")
    wrong_labels = LabelFrame(result_frame, labelanchor='w', bg="#db4437")
    wrong_labels.grid(column=0,row=6,columnspan=2,rowspan=2,pady=5, sticky="W")
    correct_res_frame = {}
    for i in range(1,11):
        elem = Label(correct_labels, text=f"{i}) .................... ({points_dict[correct[i-1]]} points)", 
                     width=26, justify='left', anchor='w', wraplength=1600, font=('ariel',16), bg="#4285F4", fg="#FFFFFF")
        correct_res_frame[correct[i-1]] = elem
        elem.grid(column=i//6, row=(i-1)%5, sticky='W', pady=2)
    return correct_res_frame, wrong_labels

def is_correct(correct_res, word):
    if word in correct_res.keys():
        return True
    else:
        return False

def reveal_correct_label(correct_res, word, points):
    cut_at = 20
    assert is_correct(correct_res, word)
    elem: Label = correct_res[word]
    elem_text: str = elem.cget("text")
    num = elem_text.split(")")[0]
    cut_word = word
    if len(word) > cut_at:
        cut_word = word[:18] + "..."
    elem.configure(text=f"{num}) {cut_word} ({points} points)")

def add_wrong_label(wrong_label_frame: LabelFrame, word):
    wrong_label = Label(wrong_label_frame, text=word, justify='left', width=40, anchor='w', pady=2, padx=10,
                        bg="#db4437", fg="#FFFFFF", font=('ariel',16))
    wrong_label.pack(side='top', anchor='w')

def clean_result_frame(result_frame: Frame):
    for elem in list(result_frame.children.values()).copy():
        elem.destroy()
        
# MENU FRAME
class MENU_FRAME_TOOL:
    def __init__(self):
        pass
    
    def setup_frame(self, menu_frame, tile_frame, tileframetool, pointsdict, correctres, wronglabel, promptelem, resframe, menuframe, dataque, t1elem, t2elem, final_flag, points_frame, prompt_frame, prev_altteam):
        next_button = Button(menu_frame)
        nb_text = "Next Prompt"
        if final_flag:
            nb_text = "Finish"
        next_button.configure(text=nb_text, width=20, height=2, bg="#0f9d58", fg="#ffffff", font=("ariel",16,"bold"),
                                command=partial(next_level, promptelem, tile_frame, resframe, menuframe, dataque, t1elem, t2elem, points_frame, prompt_frame, prev_altteam))
        next_button.grid(column=2,row=0,columnspan=1,rowspan=1)
        reveal_button = Button(menu_frame)
        reveal_button.configure(text="Reveal Answers", width=20, height=2, bg="#db4437", fg="#ffffff", font=("ariel",16,"bold"),
                                command=partial(self.reveal_action, tile_frame, tileframetool, pointsdict, correctres, wronglabel, reveal_button))
        reveal_button.grid(column=0,row=0,columnspan=1,rowspan=1,sticky='w')
        
    def reveal_action(self, tile_frame: Frame, tileframe_tool: TILE_FRAME_TOOL, points_dict, correct_res, wronglabel, itself):
        for button in list(tile_frame.children.values()):
            if button['state'] == DISABLED:
                continue
            button.configure(bg="#666666", disabledforeground="#aaaaaa")
            button['state'] = DISABLED
            tileframe_tool.buttons_left -= 1
            if is_correct(correct_res, button.cget("text")):
                tileframe_tool.correct_left -= 1
                reveal_correct_label(correct_res, button.cget("text"), points_dict[button.cget("text")])
            else:
                add_wrong_label(wronglabel, button.cget("text"))
        itself['state'] = DISABLED
        tileframe_tool.decolour_teams()
        
    def clean_menu(self, menuframe: Frame):
        for elem in list(menuframe.children.values()):
            elem.destroy()

def next_level(prompt_elem, tile_frame, result_frame, menu_frame, next_data, team1_elem, team2_elem, points_frame, prompt_frame, prevaltteam):
    if len(next_data) > 0:
        data = next_data[0]
        
        # prompt frame setup
        change_prompt(data['prompt'], prompt_elem)
        mftool = MENU_FRAME_TOOL()

        # result frame
        clean_result_frame(result_frame)
        correct_frame, wrong_frame = setup_result_frame(result_frame, data['points'], data['correct'])

        # tile frame setup
        tftool = TILE_FRAME_TOOL(team1_elem, team2_elem, alt_team=(not prevaltteam))
        tftool.clean_tile_frame(tile_frame)
        tftool.populate_tile_frame(data["correct"], data["wrong"], data['points'], tile_frame, CELL_WIDTH, correct_frame, wrong_frame)

        # menu frame setup
        final_flag = (len(next_data) <= 1)
        mftool.clean_menu(menu_frame)
        mftool.setup_frame(menu_frame,tile_frame,tftool,data["points"],correct_frame,wrong_frame,prompt_elem, result_frame, menu_frame, next_data[1:], team1_elem, team2_elem, final_flag, points_frame, prompt_frame, not prevaltteam)
    else:
        # finish the game
        # get team name and scores
        t1_res = team1_elem.cget("text")
        t1_score = get_team_score(team1_elem)
        t2_res = team2_elem.cget("text")
        t2_score = get_team_score(team2_elem)
        # destroy everything
        gui: Tk = prompt_frame.master
        prompt_frame.destroy()
        points_frame.destroy()
        result_frame.destroy()
        menu_frame.destroy()
        tile_frame.destroy()
        # make finishing display
        title_label = googlefeud_logo(gui)
        titleline = Canvas(title_label, height=1, width=title_label.winfo_width(), bg="#7d7d7d")
        titleline.grid(column=0,row=1, columnspan=13, rowspan=1, sticky='NSEW')
        title_label.pack(side='top',anchor='center')
        
        
        winner = None
        scoredisp = []
        tie = False
        if t1_score > t2_score:
            winner = t1_res.split(":")[0].strip()
            scoredisp = [t1_res, t2_res]
        elif t2_score > t1_score:
            winner = t2_res.split(":")[0].strip()
            scoredisp = [t2_res, t1_res]
        else:
            tie = True
            scoredisp = [t1_res, t2_res]
        winner_text = "None"
        if not tie:
            winner_text = f"{winner} WINS!".upper()
        else:
            winner_text = "DRAW!"
        heading_label = googlify_word(gui, winner_text, ["#4285f4","#db4437","#f4b400","#0f9d58"],font=("ariel",32,'bold'), add_line=True)
        heading_label.pack(side='top',anchor='center', pady=30)
        head2_lbl = Label(gui, text="Scores: ", font=("ariel",24,'underline'))
        head2_lbl.pack(side='top',anchor='center', after=heading_label)
        score_labels = LabelFrame(gui)
        score_labels.pack(after=head2_lbl, side='top', anchor='center')
        for st in scoredisp:
            lbl = Label(score_labels, text=st, font=("ariel",24), padx=2, pady=4)
            lbl.pack(anchor='center',padx=5, side='top')
        with open("last_result.txt",'w') as f:
            f.write("scores:\n")
            f.write(t1_res)
            f.write("\n")
            f.write(t2_res)
            f.write("\n")

def clean_slate(gui: Tk):
    for elem in list(gui.children.values()):
        elem.destroy()  

def initial_setup(gui, teamname1fr, teamname2fr):
    teamname1 = teamname1fr.get().replace(":","")
    teamname2 = teamname2fr.get().replace(":","")
    clean_slate(gui)
    
    points_frame = Frame(gui)
    points_frame.grid(column=0,row=1,columnspan=3,rowspan=2,padx=XMARGIN,pady=YMARGIN)

    prompt_frame = Frame(gui)
    prompt_frame.grid(column=0,row=3,columnspan=3,rowspan=1,padx=XMARGIN,pady=YMARGIN/2)

    tile_frame = Frame(gui)
    tile_frame.grid(column=0,row=4, columnspan=3,rowspan=10,padx=XMARGIN,pady=YMARGIN/2)

    result_frame = Frame(gui)
    result_frame.grid(column=4,row=3,columnspan=2,rowspan=8,padx=XMARGIN,pady=YMARGIN)

    menu_frame = Frame(gui)
    menu_frame.grid(column=4, row=2, columnspan=2, rowspan=1,padx=XMARGIN,pady=YMARGIN)
    mftool = MENU_FRAME_TOOL()
    # get data
    datas = []
    for fn in QUESTION_FILES[1:]:
        datas.append(read_datafile(fn))
    data = read_datafile(QUESTION_FILES[0])
    
    # points frame setup
    team1_elem, team2_elem = setup_team_frame(points_frame, teamname1, teamname2)

    # prompt frame setup
    prompt_elem = setup_prompt(data["prompt"], prompt_frame)

    # result frame
    correct_frame, wrong_frame = setup_result_frame(result_frame, data['points'], data['correct'])

    # tile frame setup
    tftool = TILE_FRAME_TOOL(team1_elem, team2_elem)
    tftool.populate_tile_frame(data["correct"], data["wrong"], data['points'], tile_frame, CELL_WIDTH, correct_frame, wrong_frame)

    # menu frame setup
    final_flag = (len(datas) == 0)
    mftool.setup_frame(menu_frame,tile_frame,tftool,data["points"],correct_frame,wrong_frame,prompt_elem, result_frame, menu_frame, datas, team1_elem, team2_elem, final_flag, points_frame, prompt_frame, False)

def frontpage(gui):
    # bit of top padding
    top_pad = Canvas(gui,height=10)
    top_pad.pack(pady=20,anchor='center')
    # show title
    title_frame = googlefeud_logo(gui)
    title_frame.configure(width=40)
    title_frame.pack(after=top_pad,pady=10, anchor='center')
    
    bot_title_pad = Canvas(gui,height=10)
    bot_title_pad.pack(pady=15,anchor='center', after=title_frame)
    # text fields for team names
    name_entry_frames = Frame(gui, width=60, pady=10)
    name_entry_frames.pack(after=bot_title_pad, anchor='center')
    team1_name = Entry(name_entry_frames, width=20, font=("ariel", 32), justify='left')
    team1_name.insert(0,"Team 1")
    team2_name = Entry(name_entry_frames, width=20, font=("ariel", 32), justify='right')
    team2_name.insert(0,"Team 2")
    team1_name.pack(padx=20, side='left', anchor='w', ipadx=4)
    team2_name.pack(padx=20, side='left', anchor='e', ipadx=4)
    # start button
    sb_pad = Canvas(gui, height=10)
    sb_pad.pack(after=name_entry_frames, anchor='center', pady=6)
    sb = Button(gui, text="Start", width=20, height=1, bg="#4285f4", font=("ariel", 24, 'bold'), fg="white",
                command=partial(initial_setup, gui, team1_name, team2_name))
    sb.pack(after=sb_pad, anchor='center', ipadx=4, ipady=2)

def googlify_word(master, word, colours, font=("ariel",24), add_line=False):
    tbox = Frame(master)
    counter = 0
    for c in word:
        lbl = Label(tbox, text=c, font=font, fg=colours[counter % len(colours)])
        lbl.grid(column=counter, row=0,rowspan=1,columnspan=1)
        counter += 1
    if add_line:
        line = Canvas(tbox, height=1, width=tbox.winfo_width(), bg="#7d7d7d")
        line.grid(column=0,row=1, columnspan=counter, rowspan=1, sticky='NSEW', pady=4)
    return tbox

def googlefeud_logo(master, font=("ariel", 48, "bold"), bg="white"):
    logo = Frame(master, bg=bg)
    bl1 = Label(logo, text=" ", font=font, fg=bg)
    g1 = Label(logo, text="G", fg="#4285f4" , font=font )
    o1 = Label(logo, text="o", fg="#db4437" , font=font )
    o2 = Label(logo, text="o", fg="#f4b400" , font=font )
    g2 = Label(logo, text="g", fg="#4285f4" , font=font )
    l = Label(logo,  text="l", fg="#0f9d58" , font=font )
    e1 = Label(logo,  text="e", fg="#db4437" , font=font )
    bl2 = Label(logo, text=" ", font=font, fg=bg)
    f =  Label(logo, font=font, text="F", fg="#4285f4")
    e2 = Label(logo, font=font, text="e", fg="#db4437")
    u =  Label(logo, font=font, text="u", fg="#f4b400")
    d =  Label(logo, font=font, text="d", fg="#0f9d58")
    bl3 = Label(logo, text=" ", font=font, fg=bg)
    bl1.grid(column=0,row=0,rowspan=1,columnspan=1)
    g1.grid(column=1,row=0,rowspan=1,columnspan=1)
    o1.grid(column=2,row=0,rowspan=1,columnspan=1)
    o2.grid(column=3,row=0,rowspan=1,columnspan=1)
    g2.grid(column=4,row=0,rowspan=1,columnspan=1)
    l.grid(column=5,row=0,rowspan=1,columnspan=1)
    e1.grid(column=6,row=0,rowspan=1,columnspan=1)
    bl2.grid(column=7,row=0,rowspan=1,columnspan=1)
    f.grid(column=8,row=0,rowspan=1,columnspan=1)
    e2.grid(column=9,row=0,rowspan=1,columnspan=1)
    u.grid(column=10,row=0,rowspan=1,columnspan=1)
    d.grid(column=11,row=0,rowspan=1,columnspan=1)
    bl3.grid(column=12,row=0,rowspan=1,columnspan=1)
    return logo

class FS_Handler:
    def __init__(self, gui):
        self.gui = gui
        self.fs = False
        self.gui.bind("<F11>", self.toogle)
        self.gui.bind("<Escape>", self.fs_off)
        # self.fs_set(True)

    def toogle(self, event=None):
        self.fs_set(not self.fs)
    
    def fs_set(self, val):
        self.fs = val
        self.gui.attributes("-fullscreen",val)
        
    def fs_off(self, event=None):
        self.fs = False
        self.fs_set(False)