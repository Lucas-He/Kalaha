# -*- coding: utf-8 -*-
import tkinter as tk
import numpy as np
import Kalaha
import gc


class Kalaha_GUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=1200, height=200)
        # Field Length Text
        self.Label_FL = tk.Label(self, text="Field length N:", anchor="w")
        self.Label_FL.pack(side="left")
        self.Label_FL.place(y=5,x=0,height=30, width=100)
        # Field Length Entry
        self.entry_FL = tk.Entry(self)
        self.entry_FL.pack(side="left", padx=20)
        self.entry_FL.place(y=5,x=100,height=30, width=50)
        # Filling Text
        self.Label_Fi = tk.Label(self, text="Filling M:", anchor="w")
        self.Label_Fi.pack(side="left")
        self.Label_Fi.place(y=5,x=160, height=30, width=100)
        # Filling Entry
        self.entry_Fi = tk.Entry(self)
        self.entry_Fi.pack(side="left", padx=20)
        self.entry_Fi.place(y=5,x=260, height=30, width=50)
        # Depth Text
        self.Label_depth = tk.Label(self, text="Search depth d:", anchor="w")
        self.Label_depth.pack(side="left")
        self.Label_depth.place(y=5,x=320, height=30, width=100)
        # Depth Entry
        self.entry_depth = tk.Entry(self)
        self.entry_depth.pack(side="left", padx=20)
        self.entry_depth.place(y=5,x=420, height=30, width=50)
        # Start Button
        self.button_Start = tk.Button(self, text="Start", command = self.start)
        self.button_Start.pack(side="right")
        self.button_Start.place(y=5,x=480,height=30, width=100)
        # Auto Move Button
        self.button_Auto = tk.Button(self, text="Auto Move", command = self.auto)
        self.button_Auto.pack(side="right")
        self.button_Auto.place(y=5,x=580,height=30, width=100)
        # Undo Move Button
        self.button_Undo = tk.Button(self, text="Undo Move", command = self.undo)
        self.button_Undo.pack(side="right")
        self.button_Undo.place(y=5,x=800,height=30, width=100)
        # Fail Text
        self.Label_fail = tk.Label(self, text="", anchor="w")
        self.Label_fail.pack(side="left")
        self.Label_fail.place(y=5,x=700, height=30, width=100)
        # Field Length Info Text
        self.Label_FLI = tk.Label(self, text="2-20", anchor="w")
        self.Label_FLI.pack(side="left")
        self.Label_FLI.place(y=35,x=100, height=30, width=50)
        # Filling Info Text
        self.Label_FiI = tk.Label(self, text="1-10", anchor="w")
        self.Label_FiI.pack(side="left")
        self.Label_FiI.place(y=35,x=260, height=30, width=50)
        # Depth Info Text
        self.Label_DI = tk.Label(self, text="2-10", anchor="w")
        self.Label_DI.pack(side="left")
        self.Label_DI.place(y=35,x=420, height=30, width=50)
        #---------------------------------#
        self.game_over = 0
        self.move_list = []
        self.player = 1
        self.dest = 0
        self.last_move = 0
        self.n = 4
        self.m = 3
        self.depth = 2
        self.field = np.zeros((2, self.n)).astype(int) + self.m
        self.goals = np.zeros(2).astype(int)
        
        
    def start(self):
        self.destroy_old_field()
        try:
            self.game_over = 0
            self.move_list = []
            self.player = 1
            self.dest = 0
            self.last_move = 0
            self.n = int(self.entry_FL.get())
            self.m = int(self.entry_Fi.get())
            self.depth = int(self.entry_depth.get())
            if (self.n < 2 or self.n > 20 or self.m < 1 or self.m > 10 or self.depth < 2 or self.depth > 10):
                self.fail()
            else:
                self.Label_fail.configure(text="")
                self.field = np.zeros((2, self.n)).astype(int) + self.m
                self.goals = np.zeros(2).astype(int)
                self.create_visual_field()
                self.dest = 1
        except ValueError:
            self.dest = 0
            self.fail()
        
    def destroy_old_field(self):
        if self.dest==1:
            for u in self.field_buttons:
                u.destroy()
            for u in self.goal_labels:
                u.destroy()
 
    def create_visual_field(self):
        self.field_buttons = []
        self.button_count = 0
        for i in range(2):
            for j in range(self.n):
                self.field_buttons.append(tk.Button(self, command=lambda k=self.n * i + j: self.change_field(pos=k)))
                self.field_buttons[self.button_count].pack(side="left", padx=20)
                self.field_buttons[self.button_count].place(y=80 + i * 50, x=100 + j * 50, height=50, width=50)
                self.field_buttons[self.button_count].configure(bg="white", text="%d"%self.m)
                self.button_count += 1
        self.goal_labels = []
        self.goal_labels.append(tk.Label(self, text="0", anchor="w"))
        self.goal_labels.append(tk.Label(self, text="0", anchor="w"))
        self.goal_labels[0].pack(side="left")
        self.goal_labels[0].place(y=80,x=50,height=100, width=50)
        self.goal_labels[0].configure(bg="white")
        self.goal_labels[1].pack(side="left")
        self.goal_labels[1].place(y=80,x=100 + self.n*50 ,height=100, width=50)
        self.goal_labels[1].configure(bg="white")

    def change_field(self, pos=0):
        if not self.game_over:
            if self.player == 0:
                if pos < self.n and self.field[self.player, pos] != 0:
                    ui = Kalaha.apply_move(self.field, self.goals, self.player, pos)
                    self.player = (self.player + 1) % 2
                    self.update_visual_field(pos)
                    self.last_move = pos
                    self.move_list.append(ui)
            else:
                if pos >= self.n and self.field[self.player, pos%self.n] != 0:
                    ui = Kalaha.apply_move(self.field, self.goals, self.player, pos%self.n)
                    self.player = (self.player + 1) % 2
                    self.update_visual_field(pos)
                    self.last_move = pos
                    self.move_list.append(ui)
                
    def auto(self):
        if not self.game_over:
            if self.player == 0:
                cm, cv = Kalaha.start_minimax(self.field, self.goals, self.player, sp=1, md=self.depth)
                aui = Kalaha.apply_move(self.field, self.goals, self.player, cm)
                self.player = (self.player + 1) % 2
                self.update_visual_field(cm)
                self.last_move = cm
                self.move_list.append(aui)
            else:
                cm, cv = Kalaha.start_minimax(self.field, self.goals, self.player, sp=-1, md=self.depth)
                aui = Kalaha.apply_move(self.field, self.goals, self.player, cm)
                self.player = (self.player + 1) % 2
                self.update_visual_field(self.n + cm)
                self.last_move = self.n + cm
                self.move_list.append(aui)
    
    def undo(self):
        if len(self.move_list) != 0:
            self.player = (self.player + 1) % 2
            Kalaha.undo_move(self.field, self.goals, self.player, self.move_list[-1])
            del self.move_list[-1]
            self.update_visual_field(self.last_move)
        
    
    def update_visual_field(self, green_space):
        self.field_buttons[self.last_move].configure(bg="white")
        for i in range(2):
            for j in range(self.n):
                self.field_buttons[i*self.n + j].configure(text="%d"%self.field[i, j])
        self.goal_labels[0].configure(text="%d"%self.goals[0])
        self.goal_labels[1].configure(text="%d"%self.goals[1])
        self.field_buttons[green_space].configure(bg="green")
    
    def fail(self):
        text_fail = "Check Inputs!"
        self.Label_fail.configure(text=text_fail)
            
if __name__ == "__main__":
    root = tk.Tk()
    app=Kalaha_GUI(parent=root)
    app.pack(fill="both", expand=True)
    #Example(root).pack(fill="both", expand=True)
    root.mainloop()
    app.close()
    layout = None
    window = None
    gc.collect()
