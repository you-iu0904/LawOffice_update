import  tkinter as tk

var_stageID=''
var_stageName=''
var_stageStartDate_y=''
var_stageStartDate_m=''
var_stage_endDate_y=''
var_stage_endDate_m=''
var_stageNumber=''

def stage_ui(stage_page):
    global var_stageID
    global var_stageName
    global var_stageStartDate_y
    global var_stageStartDate_m
    global var_stage_endDate_y
    global var_stage_endDate_m
    global var_stageNumber

    var_stageID = tk.StringVar()
    var_stageName = tk.StringVar()
    var_stageStartDate_y = tk.StringVar()
    var_stageStartDate_m = tk.StringVar()
    var_stage_endDate_y = tk.StringVar()
    var_stage_endDate_m = tk.StringVar()
    var_stageNumber = tk.StringVar()

    stageNumber_en = tk.Entry(stage_page, textvariable=var_stageNumber)

    stageID_La = tk.Label(stage_page, text='Stage ID:')
    stageID_La.place(x=50, y=40)
    stageID_en = tk.Entry(stage_page, textvariable=var_stageID, width=11)
    stageID_en.place(x=140 , y=40)

    stageName_La = tk.Label(stage_page, text='Stage Name:')
    stageName_La.place(x=50, y=70)
    stageName_en = tk.Entry(stage_page, textvariable=var_stageName, width=35)
    stageName_en.place(x=140, y=70)

    stageDateLa = tk.Label(stage_page, text='Date:')
    stageDateLa.place(x=50, y=100)

    stageDateLa_y = tk.Label(stage_page, text='Y:')
    stageDateLa_y.place(x=130, y=100)

    stage_startDate_y = tk.Entry(stage_page, textvariable=var_stageStartDate_y, width=5)
    stage_startDate_y.place(x=150, y=100)

    stageDateLa_m = tk.Label(stage_page, text='M:')
    stageDateLa_m.place(x=190, y=100)

    stage_startDate_m = tk.Entry(stage_page, textvariable=var_stageStartDate_m, width=5)
    stage_startDate_m.place(x=215, y=100)

    to = tk.Label(stage_page, text='—')
    to.place(x=260, y=100)

    stageDateLa_toy = tk.Label(stage_page, text='Y:')
    stageDateLa_toy.place(x=280, y=100)

    stage_endDate_y = tk.Entry(stage_page, textvariable=var_stage_endDate_y, width=5)
    stage_endDate_y.place(x=300, y=100)

    stageDateLa_tom = tk.Label(stage_page, text='M:')
    stageDateLa_tom.place(x=340, y=100)

    stage_endDate_m = tk.Entry(stage_page, textvariable=var_stage_endDate_m, width=5)
    stage_endDate_m.place(x=365, y=100)