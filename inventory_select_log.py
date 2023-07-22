import logging

logging.basicConfig(filename='main.log',filemode='w',format='%(asctime)s - %(message)s', level=logging.INFO)

sim_log = list()

# 
with open('/Users/akshitshishodia/tracker/roboDK /simulation.log',"r") as f:
    for line in f :
        try:
            sim_log.append(line.split()[4])
        except:
            break

sim_log = list(map(lambda x : float(x),sim_log))
sim_log = list(map(lambda x : (x-45)/35 +1,sim_log))
sim_log = list(map(lambda x : str(x),sim_log))

iou_log = list()
with open('/Users/akshitshishodia/tracker/iou.log','r') as f:
    for line in f:
        try:
            iou_log.append(line.split()[4])
        except:
            pass

for idx,i in enumerate(iou_log):
    if i == 'neither':
        continue
    else:
        res = i[0]+' '+sim_log[int(idx/2)]
        logging.info(res)

