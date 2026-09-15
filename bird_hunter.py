from tkinter import Tk, Canvas, ALL
import random
import time

def menu():
    global pos, timer_start
    c.delete(ALL)

    change_pos()

    update_data()

    draw_birds()
    draw_terrain()

    w.update()
    if menu_bin==0:
        w.after("idle",menu)
    elif menu_bin==1:
        c.create_rectangle([0,0,WIDTH,HEIGHT],fill="black",outline="")
        c.create_text(WIDTH//2,HEIGHT//2, text="Loading...", fill="White", font=(f"Helvetica 20 bold"))
        w.update()
        time.sleep(2)
        start_game()
        timer_start=time.time()
        w.after("idle",game)
        
def game():
    global timer_start, menu_bin, score, timer_passes, birds
    c.delete(ALL)

    time_left = int(timer_start + 60 - time.time())
    if time_left%5==0 and time_left not in timer_passes:
        timer_passes.append(time_left)
        size = random.randint(4,6)
        birds.append(
            [-100 if random.randint(0,1) else (len(terrain)+2)*50,random.randint(-10,HEIGHT+1)]*2+
            [random.randint(0,1),size,random.randint(0,len(colors)-1),"",size-3])

    # print(len(birds))

    change_pos()

    update_data()

    draw_birds()
    draw_terrain()

    c.create_text(50, 50, text=f"{time_left}", fill="red", font=(f"Helvetica 50 bold"))

    w.update()
    if timer_start+60<=time.time():
        menu_bin=0
        start_menu(score)
        w.after("idle",menu)
    else:
        w.after("idle",game)

def change_pos():
    global pos
    x=(w.winfo_pointerx()-w.winfo_rootx())
    if 0<=x<=WIDTH and abs(x/WIDTH-0.5)>0.1:
        pos+=(x/WIDTH-0.5)*0.1
        if pos<0:pos=0
        elif pos>len(terrain)-(WIDTH//100)-1:pos=len(terrain)-(WIDTH//100)-1

def start_menu(score=-1):
    global pos, terrain, birds
    
    for i in range(20):
        terrain.append([random.randint(-50,50),random.randint(0,10),random.randint(0,len(colors)-1)])
    
    pos=(len(terrain)-(WIDTH//100)-1)//2

    birds.clear()

    for i in ["Play","Bird Hunter","By Classicgreat"]:
        birds.append([((len(terrain)-(WIDTH//100)-1)//2)*100+random.randint(-100,100),random.randint(100,HEIGHT-200)]*2+[random.randint(0,1),random.randint(4,6),random.randint(0,len(colors)-1),i,1])
    
    if score!=-1:
        birds.append([((len(terrain)-(WIDTH//100)-1)//2)*100+random.randint(-100,100),random.randint(100,HEIGHT-200)]*2+[random.randint(0,1),random.randint(4,6),random.randint(0,len(colors)-1),f"Score: {score}",1])

def start_game():
    global pos, terrain, birds, score
    
    for i in range(random.randint(20,25)):
        terrain.append([random.randint(-50,50),random.randint(0,10),random.randint(0,len(colors)-1)])

    # print(i)

    birds.clear()
    
    pos=(len(terrain)-(WIDTH//100)-1)//2

    score=0

def update_data():
    global birds, menu_bin, score

    delet=set()

    for i in range(len(birds)):
        if birds[i][8]<=0:
            birds[i][2]=birds[i][0]
            birds[i][3]=HEIGHT
        else:
            birds[i][4]=1-birds[i][4]
        
        birds[i][0]+=((birds[i][2]-birds[i][0])//max(1,abs(birds[i][2]-birds[i][0])))*2
        birds[i][1]+=((birds[i][3]-birds[i][1])//max(1,abs(birds[i][3]-birds[i][1])))*2
        
        if birds[i][2]-1<=birds[i][0]<=birds[i][2]+1 and birds[i][3]-1<=birds[i][1]<=birds[i][3]+1:
            if birds[i][8]<=0:
                delet.add(i)
                if menu_bin==0 and birds[i][7]=="Play":
                    menu_bin=1
            else:
                birds[i][2],birds[i][3]=random.randint(0,len(terrain)*100),random.randint(0,HEIGHT-200)

    for i in sorted(delet,reverse=True):
        score+=1
        birds.pop(i)
    delet.clear()

def draw_birds():
    global pos,birds
    d=[]
    for i in range(len(birds)):
        d.append(draw_bird(birds[i][0]-pos*100,birds[i][1],birds[i][2]>birds[i][0],birds[i][4],birds[i][5],birds[i][6],birds[i][7],birds[i][8]<=0))
        c.tag_bind(d[-1] , "<ButtonPress-1>", lambda checked, index=i: bird_xp(index))

def bird_xp(i):
    birds[i][8]-=1
    # print(data[i][8],i)

def draw_bird(x,y,vec,wing,k,color,text,dead):
    v=(1 if vec else -1)
    w=(-1 if wing else 1)
    c.create_oval(x+3*v,y-5*k,x-(3*k+2)*v,y-9*k+2,fill=colors[color],outline="")
    c.create_oval(x,y-4*k,x+3*k*v,y-9*k,fill=colors[color],outline="")
    c.create_oval(x-7*k,y-7*k,x+7*k,y+7*k,fill=colors[color],outline="")
    c.create_polygon([x+10*k*v,y,x+6*k*v,y+2*k,x+6*k*v,y-2*k], fill="orange")

    c.create_oval(x,y-4*k,x+4*k*v,y,fill="black")
    c.create_oval(x+3/5*k*v,y-3*k-2,x+(3*k+2)*v,y-3/5*k,fill="white")
    if dead==1:
        c.create_line(x+k*v,y-3*k,x+3*k*v,y-k,fill="black",width=3/5*k)
        c.create_line(x+3*k*v,y-3*k,x+k*v,y-k,fill="black",width=3/5*k)

    c.create_line(x-5*k*v,y,x-4*k*v,y+2*k*w,fill="black",width=3/5*k)
    c.create_line(x-4*k*v,y+2*k*w,x-2*k*v,y+k,fill="black",width=3/5*k)

    c.create_text(x+17*k*v, y, text=text, fill="black", font=(f"Helvetica {int(3*k)} bold"))

    return c.create_oval(x-7*k,y-7*k,x+7*k,y+7*k,fill="",outline="")

def draw_terrain():
    global pos, terrain
    l=[0,HEIGHT]
    for i in range(len(terrain)):
        l+=[(i-pos)*100,HEIGHT-200-terrain[i][0]]
        if terrain[i][1]<3:
            draw_tree((i-pos)*100,HEIGHT-200-terrain[i][0],(terrain[i][2]+3)*10)
        elif terrain[i][1]==3:
            draw_house((i-pos)*100,HEIGHT-200-terrain[i][0],terrain[i][2])
        elif terrain[i][1]<6:
            draw_cloud((i-pos)*100,HEIGHT-200-terrain[i][0],(terrain[i][2]+1)*50)
    c.create_polygon(l+[WIDTH,HEIGHT],fill="green",outline="")

def draw_tree(x,y,k):
    c.create_line([x,HEIGHT,x,y-300],width=20,fill="brown")
    c.create_oval(x-k,y-50,x+k,y-320,fill="green",outline="")
    return c.create_line([x,y-10,x,y-300],width=10,fill="")

def draw_house(x,y,color):
    c.create_polygon([x-100,HEIGHT,x-100,y-100,x+100,y-100,x+100,HEIGHT],fill=colors[color],outline="")
    c.create_polygon([x-100,y-100,x,y-150,x+100,y-100],fill="orange",outline="")
    c.create_polygon([x-40,y-10,x-40,y-80,x+40,y-80,x+40,y-10],fill="khaki",outline="")
    c.create_line([x,y-10,x,y-80],width=7,fill=colors[color])
    c.create_line([x-40,y-40,x+40,y-40],width=7,fill=colors[color])
    return c.create_polygon([x-100,HEIGHT,x-100,y-100,x+100,y-100,x+100,HEIGHT],fill="",outline="")

def draw_cloud(x,y,size):
    c.create_oval(x-size,y-160-size,x+size,y-210-size,fill="white",outline="")
    return c.create_oval(x-size,y-450,x+size,y-500,fill="",outline="")

WIDTH = 1600
HEIGHT = 800
colors = ["red","green","blue","yellow","white","black","orange","gold"]

birds = [] # x, y, dx, dy, wings, size, color, text, xp
terrain = [] # y, tree/house/cloud, k
timer_passes = []
pos = 0
menu_bin = 0
timer_start = 0
score = 0

start_menu()

w=Tk()
w.title("Bird Hunter")
w.geometry(f"{str(WIDTH)}x{str(HEIGHT)}")
w.resizable(width=False,height=False)

c=Canvas(w,bg="lightblue",width=WIDTH,height=HEIGHT)
c.place(x=0, y=0)

menu()

w.mainloop()