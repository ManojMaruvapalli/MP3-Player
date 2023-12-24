from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3



root = Tk()
root.title('MP3 Player')
#root.iconbitmap(r'D:\New folder\Mp3.ico')
root.geometry("500x350")

pygame.mixer.init()

def add_song():
    song = filedialog.askopenfilename(initialdir = "Libraries\Music", title = "Choose a Song", filetypes=(("mp3 files","*.mp3"),))
    song_box.insert(END, song)

def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir = "Libraries\Music", title = "Choose a Song", filetypes=(("mp3 files","*.mp3"),))
    for song in songs:
        song_box.insert(END, song)

def delete_song():
    stop()
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()

def delete_all_songs():
    stop()
    song_box.delete(0,END)
    pygame.mixer.music.stop()

def play_time():
    if stopped:
	    return
    current_time = pygame.mixer.music.get_pos() / 1000
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
    song = song_box.get(ACTIVE)
    song_mut = MP3(song)
    song_length=song_mut.info.length
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    status_bar.config(text=f'Time Elapsed: {converted_current_time}  of  {converted_song_length}  ')
    status_bar.after(1000, play_time)


def play():
    song = song_box.get(ACTIVE)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    play_time()

global stopped
stopped = False    
def stop():
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

    status_bar.config(text='')
    global stopped
    stopped = True

global paused
paused = False

def pause(is_paused):
    global paused
    paused= is_paused

    if paused == True:
        pygame.mixer.music.unpause()
        paused = False

    else:
        pygame.mixer.music.pause()
        paused = Trueṇ
    


def next_song():
    one = song_box.curselection()
    one = one[0]+1
    song = song_box.get(one)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    song_box.selection_clear(0,END)
    song_box.activate(one)
    song_box.selection_set(one,last=None)


def previous_song():
    one = song_box.curselection()
    one = one[0]-1
    song = song_box.get(one)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    song_box.selection_clear(0,END)
    song_box.activate(one)
    song_box.selection_set(one,last=None)


song_box=Listbox(root,bg = "black",fg = "white",width=60, selectbackground = "grey", selectforeground ="black")
song_box.pack(pady = 20)

back_button_img = PhotoImage(file = r"New folder\back.png")
forward_button_img = PhotoImage(file = r"New folder\forward.png")
play_button_img = PhotoImage(file = r"New folder\play.png")
pause_button_img = PhotoImage(file = r"New folder\pause.png")
stop_button_img = PhotoImage(file = r"New folder\stop.png") 




controls_frame = Frame(root)
controls_frame.pack() 



back_button = Button(controls_frame, image = back_button_img,borderwidth = 0,command = previous_song)
forward_button = Button(controls_frame, image = forward_button_img,borderwidth = 0,command= next_song)
play_button = Button(controls_frame, image = play_button_img,borderwidth = 0, command = play)
pause_button = Button(controls_frame, image = pause_button_img,borderwidth = 0, command = lambda: pause(paused))
stop_button = Button(controls_frame, image = stop_button_img,borderwidth = 0, command = stop)


back_button.grid(row=0,column=0,padx=10)
forward_button.grid(row=0,column=1,padx=10)
play_button.grid(row=0,column=2,padx=10)
pause_button.grid(row=0,column=3,padx=10)
stop_button.grid(row=0,column=4,padx=10)



my_menu = Menu(root)
root.config(menu=my_menu)

add_song_menu = Menu(my_menu)
my_menu.add_cascade(label = "Add Songs", menu = add_song_menu)
add_song_menu.add_command(label="Add One Song to Playlist", command=add_song)
add_song_menu.add_command(label="Add Many Song to Playlist", command=add_many_songs)

remove_song_menu=Menu(my_menu)
my_menu.add_cascade(label="Remove songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete a song from Playlist", command=delete_song)
remove_song_menu.add_command(label="Delete all songs from Playlist", command=delete_all_songs)

status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

root.mainloop()
