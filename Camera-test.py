#可直接錄製測試版
#更新內容:可自行設定範本
import cv2
import mediapipe as mp
import numpy as np
def track(A):
    cap = cv2.VideoCapture(A)
    mpPose = mp.solutions.pose
    mpDraw = mp.solutions.drawing_utils
    C=[]
    landmarks=0
    with mpPose.Pose(min_detection_confidence=0.8,min_tracking_confidence=0.8) as pose:
        while True:
            ret, img = cap.read()
            if ret:
                imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                img.flags.writeable=False
                result = pose.process(imgRGB)
                img.flags.writeable=True
                image=cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
                if result.pose_landmarks!=None:
                    landmarks = result.pose_landmarks.landmark
                mpDraw.draw_landmarks(img,result.pose_landmarks,mpPose.POSE_CONNECTIONS)
                cv2.imshow('img',img)
            if cv2.waitKey(1) == ord(' '):
                break
            part = []
            if type(landmarks)!=int:
                for i in mpPose.PoseLandmark:
                    B = []
                    for j in range(33):
                        S = str((landmarks[j]))
                        Pos = [0,0,0,0]
                        for k in range(len(S)):
                            if S[k] == 'x':
                                Pos[0] = k
                            if S[k] == 'y':
                                Pos[1] = k
                            if S[k] == 'z':
                                Pos[2] = k
                            if S[k] == 'v':
                                Pos[3] = k
                                break
                        A = [float(S[Pos[0]+3:Pos[1]:]),float(S[Pos[1]+3:Pos[2]:]),float(S[Pos[2]+3:Pos[3]:])]
                        B.append(A)
                C.append(B)
        return C
        cv2.destroyAllWindows()
def score(A,B):
    #將範本數據(A)和測試數據(B)進行SSIM比較與評分
    pass
Y='Y'
sample='video-1642320831.mp4'
print("歡迎使用本程式，請依照以下指示進行操作")
print("目前的範本是"+sample+"請問是否更換?(Y/N)(確認不更換後將無法更換範本)")
Y=input()
while Y=='Y':
    print("請輸入範本的檔名")
    sample=input()
    print("目前的範本是"+sample+"請問是否更換?(Y/N)(確認不更換後將無法更換範本)")
    Y=input()
print("請輸入需要測試的影片檔名(錄製請輸入0)")
test=input()
print('範本分析中(按空格鍵結束分析)')
A=track(sample)
if test!='0':
    print('測試影片分析中...(按空格鍵結束分析)')
    B=track(test)
else:
    print('錄製影像即時分析中...(按空格鍵結束錄製)')
    test=int(test)
    B=track(test)
if B==[]:
    print('讀取人物骨架失敗')
else:
    score(A,B)
print('還需要繼續測試?(Y/N)')
ANS=input()
while ANS=='Y':
    print("請輸入需要測試的影片路徑")
    test=input()
    if test!='0':
        print('測試影片分析中...(按空格鍵結束分析)')
        B=track(test)
    else:
        print('錄製影像即時分析中...(按空格鍵結束錄製)')
        test=int(test)
        B=track(test)
    if B==[]:
        print('讀取人物骨架失敗')
    else:
        score(A,B)
    print('還需要繼續測試?(Y/N)')
    ANS=input()
print('謝謝使用')
