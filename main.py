import os,time
import cv2

def connect():
    os.system('adb connect 127.0.0.1:62001')

def click(x, y):
    os.system('adb -s '+ device +' shell input tap %s %s>nul' % (x, y))

def screenshot():
    path = os.path.abspath('.') + '\images.png'
    os.system('adb -s '+ device +' shell screencap /data/screen.png>nul')
    os.system('adb -s '+ device +' pull /data/screen.png %s>nul' % path)

def resize_img(img_path):
    img1 = cv2.imread(img_path, 0)
    img2 = cv2.imread('images.png', 0)
    height, width = img1.shape[:2]
    
    ratio = 1920 / img2.shape[1]
    size = (int(width/ratio), int(height/ratio))
    return cv2.resize(img1, size, interpolation = cv2.INTER_AREA)

def Image_to_position(image, m = 0):
    image_path = 'images/' + str(image) + '.png'
    screen = cv2.imread('images.png', 0)
    template = resize_img(image_path)
    methods = [cv2.TM_CCOEFF_NORMED, cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR_NORMED]
    image_x, image_y = template.shape[:2]
    result = cv2.matchTemplate(screen, template, methods[m])
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(image,max_val)
    if max_val > 0.9:
        global center
        center = (max_loc[0] + image_y / 2, max_loc[1] + image_x / 2)
        return center
    else:
        return False

def runBatch(images):
    for image in images:
        while True:
            if Image_to_position(image) != False:
                if image=='timeadd':
                    for _ in range(0,35):
                        click(center[0], center[1])
                elif image=='cancel_white' or image=='ok_blue' or image=='ok_white':
                    click(center[0], center[1])
                    time.sleep(0.5)
                else:
                    click(center[0], center[1])
                break
            else:
                if image=='skip':
                    click(100, 100)
                screenshot()

def login(username,password):
    for image in ['ID','password','login']:
        while True:
            if Image_to_position(image) != False:
                click(center[0], center[1])
                if image=='ID':
                    os.system('adb -s '+ device +' shell input text "'+ username +'"')
                elif image=='password':
                    os.system('adb -s '+ device +' shell input text "'+ password +'"')
                break
            else:
                click(1870,50)
                screenshot()

def getaccount(txtname):
    lines=[]
    with open(txtname, 'r') as f:
        lines=f.readlines()
        return lines

def tryCmd(image):
    screenshot()
    for _ in range(0,2):
        if Image_to_position(image) != False:
            if image=='cancel_white' or image=='ok_blue' or image=='ok_white':
                click(center[0], center[1])
                time.sleep(0.5)
            else:
                click(center[0], center[1])
            return True
        else:
            screenshot()
    return False

if __name__ == '__main__':
    
    accountList=getaccount('accountlist.txt')
    
    connect()
    global device
    device = os.popen('adb devices').read().split('\n')[1].split('\t')[0]
    print("connect with",device)
    screenshot()
    
    for i in range(len(accountList)):
        
        login(accountList[i].split(' ')[0],accountList[i].split(' ')[1][0:-1])
        print("login with",accountList[i].split(' ')[0])
            
        runBatch(['skip','close_white'])

        for _ in range(0,2):
            runBatch(['add_blue','ok_blue','ok_white'])

        runBatch(['explor','masterbatch','left','10-1','timeadd'])
        runBatch(['run','ok_blue','skip2','ok_white'])

        if tryCmd('ok_white'):
            runBatch(['run','ok_blue','skip2','ok_white'])

        runBatch(['cancel_white'])
        tryCmd('cancel_white')
        
        '''
        地下城战斗
        '''
        runBatch(['explor_blue','underground_fes','vh','ok_blue','floor1','challenge_blue'])
        runBatch(['peko','kyaru','u1','kokoro','getassist','assist','battlestart','ok_blue'])
        time.sleep(5)
        runBatch(['next_step'])
        time.sleep(3)
        runBatch(['ok_white','withdraw','ok_blue'])
        
        runBatch(['mainpage','backtotitle','ok_blue'])


    #退出程序
    os.system('adb kill-server')
