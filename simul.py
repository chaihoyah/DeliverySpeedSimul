import numpy as np
import matplotlib.pyplot as plt

def get_meanvel(mot, traf_v, traf_s):
    return (mot-traf_v)**(1/traf_s) + traf_v
# set velocity
frozenmot_v = 40
mot_v = 100

# set traffic variables
traffic_score = 2
traffic_v = 30

# get mean velocity
frozenmot_meanvel = get_meanvel(frozenmot_v, traffic_v, traffic_score)
frozenmot_meanvel_min = frozenmot_meanvel*1000/60
mot_meanvel = get_meanvel(mot_v, traffic_v, traffic_score)
mot_meanvel_min = mot_meanvel*1000/60
print("냉토바이 평균속도:",frozenmot_meanvel,"km/h")
print("냉토바이 분당 이동거리:",frozenmot_meanvel_min,"m")
print("일반 평균속도:",mot_meanvel,"km/h")
print("일반 분당 이동거리:",mot_meanvel_min,"m")

# set area and time limit (left top (0,0), right bottom (6000,5000))
width = 5000
center_x = width/2
height = 4000
center_y = height/2
time_lim = 120

total_orders = 10
# set random place and time
randplace1 = []
randplace2 = []
randtime1 = []
randtime2 = []
for i in range(total_orders):
    _x = np.random.randint(1,width+1)
    _y = np.random.randint(1,height+1)
    randplace1.append([_x,_y])
    _x = np.random.randint(1,width+1)
    _y = np.random.randint(1,height+1)
    randplace2.append([_x,_y])

    _t = np.random.randint(1,time_lim+1)
    randtime1.append(_t)
    _t = np.random.randint(1,time_lim+1)
    randtime2.append(_t)

randplace1 = np.array(randplace1)
randplace2 = np.array(randplace2)
randtime1 = np.sort(np.array(randtime1))
copy = randtime1.copy()
randtime2 = np.sort(np.array(randtime2))
print("냉토바이 배달장소:",randplace1)
print("일반 배달장소:",randplace2)
print("냉토바이 배달시간:",randtime1)
print("일반 배달시간:",randtime2)
# state 0: waiting state 1: moving(before finishing order) state 2: passing on the product state 3: moving(to the center)
curr_time = 1
is_frozenfinished = False
frozen_pos = [center_x, center_y]
frozen_state = 0
frozen_remainingdist = 0
frozen_count = 0
frozen_orderq = []
frozen_finishedtime = []
frozen_starttime = []
frozen_endtime = []

mot_delay = 2
is_motfinished = False
mot_pos = [center_x, center_y]
mot_state = 0
mot_remainingdist = 0
mot_count = 0
mot_orderq = []
mot_finishedtime = []

is_motfinished2 = False
mot_pos2 = [3000, 2500]
mot_state2 = 0
mot_remainingdist2 = 0
mot_count2 = 0
mot_orderq2 = []
mot_finishedtime2 = []
mot_starttime = []
mot_endtime = []

def push_order():
    global randtime1
    global randplace1
    global randtime2
    global randplace2
    one = len(randtime1[np.where(randtime1 == curr_time)])
    two = len(randtime2[np.where(randtime2 == curr_time)])
    for time in range(one):
        frozen_orderq.append([randtime1[0], randplace1[0]])
        mot_orderq2.append([randtime1[0], randplace1[0]])
        randtime1 = randtime1[1:]
        randplace1 = randplace1[1:]
    for time in range(two):
        mot_orderq.append([randtime2[0], randplace2[0]])
        randtime2 = randtime2[1:]
        randplace2 = randplace2[1:]

while not is_frozenfinished or not is_motfinished or not is_motfinished2:
    push_order()
    if frozen_state == 0:
        if len(frozen_orderq)>0:
            frozen_starttime.append(curr_time)
            frozen_state = 1
            frozen_remainingdist = np.abs(frozen_orderq[0][1] - frozen_pos).sum()
        elif len(randtime1) == 0:
            is_frozenfinished = True
    elif frozen_state == 1:
        frozen_remainingdist -= frozenmot_meanvel_min
        if frozen_remainingdist<0:
            frozen_endtime.append(curr_time)
            frozen_state = 2
            frozen_count = 3
            frozen_pos = frozen_orderq[0][1].copy()
    elif frozen_state == 2:
        if frozen_count>0:
            frozen_count -= 1
        else:
            frozen_count = 0
            frozen_orderq = frozen_orderq[1:]
            frozen_finishedtime.append(curr_time)
            if len(frozen_orderq) == 0:
                frozen_state = 3
            else:
                frozen_starttime.append(curr_time)
                frozen_remainingdist = np.abs(frozen_orderq[0][1] - frozen_pos).sum()
                frozen_state = 1
    elif frozen_state == 3:
        if len(frozen_orderq) == 0:
            if len(randtime1) == 0:
                is_frozenfinished = True
            if frozen_pos[0] < center_x and frozen_pos[1] < center_y:
                dist_x = abs(frozen_pos[0] - center_x)
                dist_y = abs(frozen_pos[0] - center_y)
                frozen_pos[0] += int(frozenmot_meanvel_min*(dist_x)/(dist_x+dist_y))
                frozen_pos[1] += int(frozenmot_meanvel_min*(dist_y)/(dist_x+dist_y))
                if(frozen_pos[0] >= center_x):
                    frozen_pos[0] = center_x
                if(frozen_pos[1] >= center_y):
                    frozen_pos[1] = center_y
            elif frozen_pos[0] > center_x and frozen_pos[1] < center_y:
                dist_x = abs(frozen_pos[0] - center_x)
                dist_y = abs(frozen_pos[0] - center_y)
                frozen_pos[0] -= int(frozenmot_meanvel_min*(dist_x)/(dist_x+dist_y))
                frozen_pos[1] += int(frozenmot_meanvel_min*(dist_y)/(dist_x+dist_y))
                if(frozen_pos[0] <= center_x):
                    frozen_pos[0] = center_x
                if(frozen_pos[1] >= center_y):
                    frozen_pos[1] = center_y
            elif frozen_pos[0] < center_x and frozen_pos[1] > center_y:
                dist_x = abs(frozen_pos[0] - center_x)
                dist_y = abs(frozen_pos[0] - center_y)
                frozen_pos[0] += int(frozenmot_meanvel_min*(dist_x)/(dist_x+dist_y))
                frozen_pos[1] -= int(frozenmot_meanvel_min*(dist_y)/(dist_x+dist_y))
                if(frozen_pos[0] >= center_x):
                    frozen_pos[0] = center_x
                if(frozen_pos[1] <= center_y):
                    frozen_pos[1] = center_y
            elif frozen_pos[0] > center_x and frozen_pos[1] > center_y:
                dist_x = abs(frozen_pos[0] - center_x)
                dist_y = abs(frozen_pos[0] - center_y)
                frozen_pos[0] -= int(frozenmot_meanvel_min * (dist_x) / (dist_x + dist_y))
                frozen_pos[1] -= int(frozenmot_meanvel_min * (dist_y) / (dist_x + dist_y))
                if (frozen_pos[0] <= center_x):
                    frozen_pos[0] = center_x
                if (frozen_pos[1] <= center_y):
                    frozen_pos[1] = center_y
            else:
                if frozen_pos[0] != center_x or frozen_pos[1] != center_y:
                    frozen_pos[0] = center_x
                    frozen_pos[1] = center_y
        else:
            frozen_starttime.append(curr_time)
            frozen_remainingdist = np.abs(frozen_orderq[0][1] - frozen_pos).sum()
            frozen_state = 1

    if mot_state == 0:
        if len(mot_orderq)>0:
            mot_count = mot_delay
            mot_state = 1
            mot_remainingdist = np.abs(mot_orderq[0][1] - [center_x-1000,center_y-1000]).sum()
        elif len(randtime2) == 0:
            is_motfinished = True
    elif mot_state == 1:
        if mot_count>0:
            mot_count -=1
        else:
            mot_remainingdist -= mot_meanvel_min
            if mot_remainingdist<0:
                mot_state = 2
                mot_count = 3
                mot_pos = mot_orderq[0][1].copy()
    elif mot_state == 2:
        if mot_count>0:
            mot_count -= 1
        else:
            mot_count = 0
            mot_orderq = mot_orderq[1:]
            mot_finishedtime.append(curr_time)
            if len(mot_orderq) == 0:
                if len(randtime2) == 0:
                    is_motfinished = True
                mot_state = 0
            else:
                mot_count = mot_delay
                mot_remainingdist = np.abs(mot_orderq[0][1] - [center_x-1000,center_y-1000]).sum()
                mot_state = 1
    if mot_state2 == 0:
        if len(mot_orderq2)>0:
            mot_starttime.append(curr_time)
            mot_count2 = mot_delay
            mot_state2 = 1
            mot_remainingdist2 = np.abs(mot_orderq2[0][1] - [center_x-1000,center_y-1000]).sum()
        elif len(randtime1) == 0:
            is_motfinished2 = True
    elif mot_state2 == 1:
        if mot_count2>0:
            mot_count2 -= 1
        else:
            mot_remainingdist2 -= mot_meanvel_min
            if mot_remainingdist2<0:
                mot_endtime.append(curr_time)
                mot_state2 = 2
                mot_count2 = 3
                mot_pos2 = mot_orderq2[0][1].copy()
    elif mot_state2 == 2:
        if mot_count2>0:
            mot_count2 -= 1
        else:
            mot_count2 = 0
            mot_orderq2 = mot_orderq2[1:]
            mot_finishedtime2.append(curr_time)
            if len(mot_orderq2) == 0:
                if len(randtime1) == 0:
                    is_motfinished2 = True
                mot_state2 = 0
            else:
                mot_starttime.append(curr_time)
                mot_count2 = mot_delay
                mot_remainingdist2 = np.abs(mot_orderq2[0][1] - [center_x-1000,center_y-1000]).sum()
                mot_state2 = 1
    curr_time+=1

print("냉토바이 주문별 배달시간",frozen_finishedtime)
print("일반 주문별 배달시간 - 냉토바이와 같은 샘플",mot_finishedtime2)
print("일반 주문별 배달시간 - 냉토바이와 다른 랜덤 샘플", mot_finishedtime)
print(frozen_starttime)
print(frozen_endtime)
print(mot_starttime)
print(mot_endtime)
plt.rcParams['figure.figsize'] = [12,6]

fig, ax = plt.subplots()
frozen_endtime = np.array(frozen_endtime)+1
mot_endtime = np.array(mot_endtime)+1
fro_move = [(i,k-i) for i,k in zip(frozen_starttime,frozen_endtime)]
fro_pass = [(i,3) for i in frozen_endtime]
gen_move = [(i,k-i) for i,k in zip(mot_starttime,mot_endtime)]
gen_pass = [(i,3) for i in mot_endtime]
print(fro_move)
print(fro_pass)
fromove = ax.broken_barh(fro_move, (20,9), facecolors='tab:blue', label="salact:frozen_moving")
fropass = ax.broken_barh(fro_pass, (20,9), facecolors='tab:orange', label="salact:frozen_passing")
genmove = ax.broken_barh(gen_move, (10,9), facecolors='tab:blue', label="general:mot_moving")
genpass = ax.broken_barh(gen_pass, (10,9), facecolors='tab:orange', label="general:mot_passing")
ax.set_ylim(5,35)
ax.set_xticks(copy)
ax.grid(True)
ax.set_yticks([15,25])
ax.set_yticklabels(['general', 'salact'])
plt.legend(handles =[fromove, fropass, genmove, genpass])
plt.show()
