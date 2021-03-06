import tkinter.filedialog
import tkinter as tk
import sys
import os
import window.index as index


#欢迎页面
def welcomeUI():
    window = tk.Tk()
    window.title('xxx律师所')
    window.geometry('500x300')
    window.resizable(False, False)

    var_userFile = tk.StringVar()
    var_stageFile = tk.StringVar()

    #页面初始化时将读取记忆文件并赋值控件中
    recordFile = open('Data/record.txt', 'r')
    text = recordFile.readlines()
    for dic in text:
        data = eval(dic)
        for i in data.values():
            var_userFile.set(i[0])
            var_stageFile.set(i[1])

    def chooseuserfile(event):
        userfile = tk.filedialog.askopenfilename()
        var_userFile.set(userfile)

    def choosestagefile(event):
        stagefile = tk.filedialog.askopenfilename()
        var_stageFile.set(stagefile)
    #确定按钮
    def confirm():
        if var_userFile.get()!='' and var_stageFile.get()!='':
            if var_userFile.get().endswith('.txt') != True :
                tk.messagebox.showinfo(title='提示', message='用户文件格式必须为.txt格式')
            elif var_stageFile.get().endswith('.xml') != True :
                tk.messagebox.showinfo(title='提示', message='单据文件格式必须为.xml格式')
            elif os.path.exists(var_userFile.get()) == False:
                tk.messagebox.showinfo(title='提示', message='用户文件不存在,请重新选择')
            elif os.path.exists(var_stageFile.get()) == False:
                tk.messagebox.showinfo(title='提示', message='Stage文件不存在,请重新选择')
            else:
                data_dict = {}
                data_list = []
                data_list.append(var_userFile.get())
                data_list.append(var_stageFile.get())
                data_dict['record'] = data_list
                recordFile = open('Data/record.txt', 'w')
                recordFile.write(str(data_dict))
                recordFile.close()
                window.destroy()
                index.indexUI(var_userFile.get(),var_stageFile.get())
        elif var_userFile.get()!='' and var_stageFile.get()=='':

            if var_userFile.get().endswith('.txt') != True:
                tk.messagebox.showinfo(title='提示', message='用户文件格式必须为.txt格式')
            elif os.path.exists(var_userFile.get()) == False:
                tk.messagebox.showinfo(title='提示', message='用户文件不存在,请重新选择')
            else:
                data_dict = {}
                data_list = []
                data_list.append(var_userFile.get())
                data_list.append('')
                data_dict['record'] = data_list
                recordFile = open('Data/record.txt', 'w')
                recordFile.write(str(data_dict))
                recordFile.close()
                window.destroy()
                index.indexUI(var_userFile.get(), os.getcwd() + '/Data/emplist.xml')
        elif var_userFile.get()=='' and var_stageFile.get()!='':
            if var_stageFile.get().endswith('.xml') != True:
                tk.messagebox.showinfo(title='提示', message='用户文件格式必须为.txt格式')
            elif os.path.exists(var_stageFile.get()) == False:
                tk.messagebox.showinfo(title='提示', message='用户文件不存在,请重新选择')
            else:
                data_dict = {}
                data_list = []
                data_list.append('')
                data_list.append(var_stageFile.get())
                data_dict['record'] = data_list
                recordFile = open('Data/record.txt', 'w')
                recordFile.write(str(data_dict))
                recordFile.close()
                window.destroy()
                index.indexUI(os.getcwd()+'/Data/User.txt', var_stageFile.get())
        elif var_userFile.get()=='' and var_stageFile.get()=='':
            window.destroy()
            index.indexUI(os.getcwd()+'/Data/User.txt', os.getcwd()+'/Data/emplist.xml')
    #退出按钮
    def cancel():
        sys.exit()


    #welcome图标
    canvas = tk.Canvas(window, height=200, width=500)
    image_file = tk.PhotoImage(file='image/welcome.jpg')
    image = canvas.create_image(0, 0, anchor='nw', image=image_file)
    canvas.place(x=20, y=20)

    userfile_label = tk.Label(window, text='用户保存路径:').place(x=30, y=200)
    stagefile_label = tk.Label(window, text='单据保存路径:').place(x=30, y=240)
    userfile_entry = tk.Entry(window, textvariable= var_userFile, width=35)
    userfile_entry.bind('<Double-Button-1>', chooseuserfile)
    userfile_entry.place(x=150, y=203)

    stagefile_entry = tk.Entry(window, textvariable=var_stageFile, width=35)
    stagefile_entry.bind('<Double-Button-1>', choosestagefile)
    stagefile_entry.place(x=150, y=243)

    confirm = tk.Button(window, width=6, text='确定', command=confirm).place(x=420, y=190)
    cancel = tk.Button(window, width=6, text='退出', command=cancel).place(x=420, y=240)
    window.mainloop()



