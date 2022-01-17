"""
由於範例檔案與測試檔案必然有時距不等的問題
我們只考慮兩組骨架運動的相似性，經搜尋後發現DTW

嘗試使用DTW作單骨架點的資料處理與評分，並對不同骨架點(如左手、左肩)給予不同的權重以達到較合理的綜合評分

由於mediapipe具有每個點的x,y,z數據，且範圍皆在-1~1
我們使用歐氏距離作為DTW參考
"""
"""
此時的問題:由於DTW要求的是相似片段的lowest cost，若兩個動作之間有的不只是相(時間)差，動作差異也過大(例如完全反向運動)
會容易產生無法找到正確對應的狀況，比如第一組的動作對應到第二組等等...
"""
import numpy as np

def dp(A,B): 
  a = len(A)
  b = len(B)
  
  #initialize
  cost_matrix = np.zeros(a+1,b+1)
  for i in range (1,a+1):
    cost_matrix[i,0] = np.inf
  for i in range (1,b+1):
    cost_matrix[0,i] = np.inf
  
  #定義歐氏距離，此處暫時使用二維投影，但應該可以改為三維並不影響結果
  def D(v1,v2):
    temp = 0
    if len(v1) == len(v2):
      for i in range len(v1):
        temp += v1[i]**2 + v2[i]**2
    return np.sqrt(temp)
  
  #依DTW規則填入cost matrix 
  for i in range(1,a+1):
      for j in range(1,b+1):
        cost_matrix[i][j] = D(A[i],B[j]) + min(cost_matrix[i-1][j],cost_matrix[i-1][j-1],cost_matrix[i][j-1]) 
  
