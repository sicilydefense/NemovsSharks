from graphics import Canvas
import random
import time

'''
NEMO vs SHARKS
----------------
Ezgi Gümüştekin
'''
canvas = Canvas()

#Values
DELAY = 0.02

frameWidth = 1200
frameHeight = 600
canvas.set_canvas_size(frameWidth, frameHeight )
canvas.set_canvas_title('NEMO vs SHARKS')

nemox = 10 #x1
nemoy = 10 #y1
MIN_KOPEKBALIGI_X = 200
MAX_KOPEKBALIGI_X = 250
MIN_KOPEKBALIGI_Y = 100
MAX_KOPEKBALIGI_Y = 140

#This funtion create sharks and add them to list
def kopekbaligi_spawn_maker(kopekbaligi_list, total_kopekbaligi_number, kopekbaligi_dic):
    kopekbaligi_list.append(canvas.create_image_with_size(frameWidth, random.randint(0, frameHeight),random.randint(MIN_KOPEKBALIGI_X ,MAX_KOPEKBALIGI_X), random.randint(MIN_KOPEKBALIGI_Y ,MAX_KOPEKBALIGI_Y), "kopekbaligi.png" ))
    if total_kopekbaligi_number != len(kopekbaligi_list):
        last_kopekbaligi = int(canvas.find_all()[-1])
        total_kopekbaligi_number = last_kopekbaligi
    kopekbaligi_dic[kopekbaligi_list[-1]] = - random.randint(3, 6) #The reason we put a list in the dictionary is to give each new shark different speeds.(key - value)
    total_kopekbaligi_number += 1
    return kopekbaligi_list, total_kopekbaligi_number, kopekbaligi_dic

#This function restarts the game
def restart_game():
    restart_game = 1
    while restart_game == 1:
        restart = canvas.get_new_key_presses()
        for press in restart:
            print(press.keysym)
            if press.keysym == "x":
                canvas.delete_all()
                restart_game = 0
                main()
            time.sleep(DELAY)
        time.sleep(DELAY)
        canvas.update()

#Main code
def main():
    kopekbaligi_list = []
    total_kopekbaligi_number = 0
    sharks_spawn = 0

    #Creating codes of objects
    canvas.create_image_with_size(0, 0, frameWidth, frameHeight, 'denizalti.jpg')
    nemo = canvas.create_image_with_size(nemox , nemoy, nemox + 50, nemoy + 30, 'balik.png')
    kapak = canvas.create_image_with_size(0, 0, frameWidth, frameHeight, 'denizalti.png')
    tik = time.perf_counter()
   
    kopekbaligi_dic = {}
    healt_count = 1
   
    openning_count = 1

    #Start screen
    while openning_count  == 1:
        new_key = canvas.get_new_key_presses()
        for press in new_key:
            if press.keysym == "space":
                canvas.delete(kapak)
                openning_count -= 1
        time.sleep(DELAY)
        canvas.update()

    #Game running part
    while healt_count > 0:
        #Control of nemo
        mouse_x = canvas.get_mouse_x()
        mouse_y = canvas.get_mouse_y()
        if ((mouse_x - (nemox/2)) > 0 and (mouse_x + (nemox/2)) < frameWidth) and ((mouse_y - (nemox/2)) > 0 and (mouse_y + (nemox/2)) < frameHeight): #This part was written with the mouse to keep Nemo inside.
            canvas.move(nemo, mouse_x - canvas.get_left_x(nemo) - (nemox/2) - 30, mouse_y - canvas.get_top_y(nemo) - (nemoy/2) - 20) #nemo/2 is to match Nemo to the middle of the mouse.
        
        sharks_spawn += 1
        if sharks_spawn % 40 == 0: #to prevent the game from collapsing after overfilling with sharks.
            for i in range(random.randint(0,4)): #number of sharks per second
                kopekbaligi_list, total_kopekbaligi_number, kopekbaligi_dic = kopekbaligi_spawn_maker(kopekbaligi_list, total_kopekbaligi_number, kopekbaligi_dic)
            
        #Game over condation
        for kopekbaligi in kopekbaligi_list:
            canvas.move(kopekbaligi, kopekbaligi_dic[kopekbaligi], 0) 
            
            if len(canvas.find_overlapping(canvas.get_left_x(nemo), canvas.get_top_y(nemo), canvas.get_left_x(nemo) + nemox, canvas.get_top_y(nemo) + nemoy )) > 2: #When 3 objects overlap, the game is over.
                healt_count = healt_count - 1
            if (canvas.get_left_x(kopekbaligi) + canvas.get_width(kopekbaligi) ) < 0:
                kopekbaligi_list.remove(kopekbaligi)
                canvas.delete(kopekbaligi)
    
        time.sleep(DELAY)
        canvas.update()

    #Time count
    tak = time.perf_counter()
    time_pass = round(tak - tik, 4) #The round function does a rounding operation based on the number of digits of the other number next to it.
    
    #Game Over screen
    text = canvas.create_text((frameWidth / 2) , (frameHeight / 2) - 50, "Your Duration") 
    canvas.set_color(text, "snow" )
    canvas.set_font(text, "Times New Roman", 40)
    time_text = canvas.create_text(frameWidth / 2, frameHeight / 2, str(time_pass))
    canvas.set_color(time_text, "gainsboro" )
    canvas.set_font(time_text, "Times New Roman", 40)
    restart_text = canvas.create_text(frameWidth / 2, (frameHeight / 2) + 100, '''Press 'x' to Play Again''')
    canvas.set_color(restart_text,'snow')
    canvas.set_font(restart_text, 'Times New Roman', 30)

    restart_game()

    canvas.update()
    canvas.mainloop()


if __name__ == '__main__':
    main()
