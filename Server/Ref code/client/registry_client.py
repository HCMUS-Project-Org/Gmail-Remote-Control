import json

# Tkinter
import tkinter as tk
import tkinter.font as font
from tkinter import Canvas, filedialog
from tkinter.filedialog import asksaveasfile


BUFSIZ = 32768


class Registry_UI(Canvas):
    def __init__(self, parent, client):
        Canvas.__init__(self, parent)
        self.label_font = font.Font(family="Helvetica", size=9, weight='bold')
        self.button_font = font.Font(
            family="Helvetica", size=12, weight='bold')

        self.configure(
            # window,
            bg="#011111",
            height=600,
            width=1000,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.place(x=0, y=0)
        # copy socket connection to own attribute
        self.client = client
        # attributes of registry keys/values
        self.action_ID = None
        self.key = None
        self.name = None
        self.data = None
        self.data_type = 1
        # attributes for response of action
        self.res1 = None
        self.res2 = None
        # initialize status ready to use
        self.status = True

        ##########Tkinter widgets############################
        # KEY
        self.key_label = tk.Label(
            self, text='Key', anchor="e", bg="#011111", fg="white", font=self.label_font, relief="flat")
        self.key_label.place(x=50, y=50, width=90, height=30)
        self.key_txt = tk.Text(self, bg="#333939", fg="white", border=0)
        self.key_txt.place(x=150, y=50, width=300, height=30)
        self.ex1 = tk.Label(
            self, text='Ex: HKEY_CURRENT_USER\SOFTWARE\MyKey', anchor='w', fg="white",  bg="#011111")
        self.ex1.place(x=150, y=81, width=300, height=30)

        # NAME VALUE
        self.name_label = tk.Label(
            self, text='Name Value', anchor="e", bg="#011111", fg="white", font=self.label_font, relief="flat")
        self.name_label.place(x=50, y=150, width=90, height=30)
        self.name_txt = tk.Text(self, bg="#333939", fg="white", border=0)
        self.name_txt.place(x=150, y=150, width=200, height=30)
        self.ex2 = tk.Label(
            self, text='Use only for Get Value / Set Value', anchor='w', fg="white",  bg="#011111")
        self.ex2.place(x=150, y=181, width=300, height=30)

        # DATA VALUE
        self.data_label = tk.Label(
            self, text='Data Value', anchor="e", bg="#011111", fg="white", font=self.label_font, relief="flat")
        self.data_label.place(x=50, y=250, width=90, height=30)
        self.data_txt = tk.Text(self, bg="#333939", fg="white", border=0)
        self.data_txt.place(x=150, y=250, width=200, height=30)
        self.ex3 = tk.Label(
            self, text='Use only for Set Value', anchor='w', fg="white", bg="#011111")
        self.ex3.place(x=150, y=281, width=300, height=30)

        # DATA TYPE
        self.data_type_label = tk.Label(
            self, text='Data Type', anchor="e", bg="#011111", fg="white", font=self.label_font, relief="flat")
        self.data_type_label.place(x=50, y=350, width=90, height=30)
        self.data_type_txt = tk.Text(self, bg="#333939", fg="white", border=0)
        self.data_type_txt.place(x=150, y=350, width=215, height=30)
        self.data_type_txt.insert(tk.END, 'Input an integer number')
        self.ex4 = tk.Label(self, text='0 - REG_SZ',
                            anchor='w', fg="white", bg="#011111")
        self.ex4.place(x=150, y=381, width=100, height=30)
        self.ex5 = tk.Label(self, text='1 - REG_BINARY',
                            anchor='w', fg="white", bg="#011111")
        self.ex5.place(x=250, y=381, width=100, height=30)
        self.ex6 = tk.Label(self, text='2 - REG_DWORD',
                            anchor='w', fg="white", bg="#011111")
        self.ex6.place(x=150, y=405, width=100, height=30)
        self.ex7 = tk.Label(self, text='3 - REG_QWORD',
                            anchor='w', fg="white", bg="#011111")
        self.ex7.place(x=250, y=405, width=100, height=30)
        self.ex8 = tk.Label(self, text='4 - REG_MULTI_SZ',
                            anchor='w', fg="white", bg="#011111")
        self.ex8.place(x=150, y=430, width=100, height=30)
        self.ex9 = tk.Label(self, text='5 - REG_EXPAND_SZ',
                            anchor='w', fg="white", bg="#011111")
        self.ex9.place(x=250, y=430, width=125, height=30)

        # REG CONTENT
        self.content = tk.Text(self, bg="#333939", fg="white", border=0)
        self.content.place(x=500, y=50, width=450, height=350)
        self.content.configure(font=('Helvetica', 16))

        '''
        self.data_type_lst = tk.StringVar(self)
        self.data_type_lst.set("Value type")
        self.data_type = tk.OptionMenu(self, self.data_type_lst, "String", "Binary", "DWORD", "QWORD", "Multi-String", "Expandable String", command = self.change_value_type)
        self.data_type.grid(row = 5, column = 2, columnspan = 2)
        self.data_type.config(width = 20)
        '''

        self.btn_get_value = tk.Button(
            self, text='Get Value', font=self.button_font, bg="#E9B04B", fg="#011111", command=lambda: self.get_value(), relief="flat")
        self.btn_get_value.place(x=50, y=500, width=105, height=40)

        self.btn_set_value = tk.Button(
            self, text='Set Value', font=self.button_font, bg="#E9B04B", fg="#011111", command=lambda: self.set_value(), relief="flat")
        self.btn_set_value.place(x=165, y=500, width=105, height=40)

        self.btn_create_key = tk.Button(
            self, text='Create Key', font=self.button_font, bg="#E9B04B", fg="#011111", command=lambda: self.create_key(), relief="flat")
        self.btn_create_key.place(x=280, y=500, width=105, height=40)

        self.btn_delete_key = tk.Button(
            self, text='Delete Key', font=self.button_font, bg="#E9B04B", fg="#011111", command=lambda: self.delete_key(), relief="flat")
        self.btn_delete_key.place(x=395, y=500, width=105, height=40)

        self.btn_open = tk.Button(self, text='OPEN FILE', bg="#E9B04B", font=self.button_font,
                                  fg="#011111", command=lambda: self.open_file(), relief="flat")
        self.btn_open.place(x=500, y=410, width=120, height=50)

        self.btn_send_detail = tk.Button(
            self, text='SEND DETAIL', font=self.button_font, bg="#E9B04B", fg="#011111", command=lambda: self.send_detail(), relief="flat")
        self.btn_send_detail.place(x=630, y=410, width=320, height=50)

        # a button to stop receiving and return to main interface
        self.btn_back = tk.Button(self, text='Back', bg="#75532D", font=self.button_font, fg="white",
                                  command=lambda: self.click_back(), relief="flat")
        self.btn_back.place(x=850, y=500, width=100, height=50)

    def get_input(self):
        self.key = self.key_txt.get("1.0", "end").rstrip()
        self.name = self.name_txt.get("1.0", "end").rstrip()
        self.data = self.data_txt.get("1.0", "end").rstrip()
        dtypes = ['REG_SZ', 'REG_BINARY', 'REG_DWORD',
                  'REG_QWORD', 'REG_MULTI_SZ', 'REG_EXPAND_SZ']
        try:
            t_num = int(self.data_type_txt.get("1.0", "end").rstrip())
            if(0 <= t_num and t_num <= 5):
                self.data_type = dtypes[t_num]
            else:
                self.data_type = dtypes[0]
        except:
            self.data_type = dtypes[0]

    def get_value(self):
        self.get_input()
        self.action_ID = 1
        self.send_msg()

    def set_value(self):
        self.get_input()
        self.action_ID = 2
        self.send_msg()

    def create_key(self):
        self.get_input()
        self.action_ID = 3
        self.send_msg()

    def delete_key(self):
        self.get_input()
        self.action_ID = 4
        self.send_msg()

    def send_detail(self):
        self.get_input()
        s = self.content.get("1.0", "end")
        self.key = s
        self.action_ID = 0
        self.send_msg()

    def open_file(self):
        file = filedialog.askopenfilename()
        if file == None or file == '':
            return
        self.content.delete("1.0", 'end')
        s = ""
        with open(file, 'r') as input_file:
            s = input_file.read()
        for line in s:
            self.content.insert(tk.END, line)

    def send_msg(self):
        msg = {'ID': self.action_ID, 'path': self.key, 'name_value': self.name,
               'value': self.data, 'v_type': self.data_type}
        msg = json.dumps(msg)
        msg_bytes = bytes(msg, 'utf8')
        msg_sz = str(len(msg_bytes))
        self.client.sendall(bytes(msg_sz, 'utf8'))
        self.client.sendall(msg_bytes)
        self.res1 = self.client.recv(BUFSIZ).decode('utf8')
        self.res2 = self.client.recv(BUFSIZ).decode('utf8')
        if self.action_ID == 1:
            if '0' in self.res1:
                tk.messagebox.showerror(
                    title='Thông báo', message='Thao tác không hợp lệ')
            else:
                tk.messagebox.showinfo(title='Thông báo', message=self.res2)
        else:
            if '0' in self.res1:
                tk.messagebox.showerror(
                    title='Thông báo', message='Thao tác không hợp lệ')
            else:
                tk.messagebox.showinfo(title='Thông báo', message='Thành công')

    def click_back(self):
        self.status = False
        self.client.sendall(bytes("STOP_EDIT_REGISTRY", "utf8"))
        return
