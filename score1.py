"""
由於範例檔案與測試檔案必然有時距不等的問題
我們只考慮兩組骨架運動的相似性，經搜尋後發現Dynamic Time Wrapping(DTW)似乎可用

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
  
  #接著，最末端的數字(終點)代表minimun cost,也就是經過對時間伸縮之後，使兩曲線點集合重合仍需要的調整值
  #注意到若兩組數據(A,B)存在類似平移關係時，終點數字可能會變得像k(點數量)*L(平移量)，因此，直接以此數據判斷相似程度並不是好方法
  #同時，可以嘗試獲得最佳對應路徑，也就是cost_matrix中，自起點至終點的總合最小路徑
  #當路徑越接近斜直線(包含越多45度路徑)時，可以代表點的相對關係較為接近
  #因此，參考影片使用路徑長/(矩陣長+寬)作為一般化的相似性數值，較終點值更適合
