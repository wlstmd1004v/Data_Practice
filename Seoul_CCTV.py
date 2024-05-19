import pandas as pd
import numpy as np

CCTV_Seoul = pd.read_csv("./CCTV_data/01. Seoul_CCTV.csv" , encoding="utf-8")
CCTV_Seoul.rename(columns={CCTV_Seoul.columns[0]: "구별"},inplace=True)

pop_Seoul = pd.read_excel("./CCTV_data/01. Seoul_Population.xls")
pop_Seoul = pd.read_excel("./CCTV_data/01. Seoul_Population.xls",header=2,usecols="B,D,G,J,N")

pop_Seoul.rename(columns={
    pop_Seoul.columns[0]: "구별",
    pop_Seoul.columns[1]: "인구수",
    pop_Seoul.columns[2]: "한국인",
    pop_Seoul.columns[3]: "외국인",
    pop_Seoul.columns[4]: "고령자",
}, inplace=True,)

CCTV_Seoul.sort_values(by="소계",ascending=True)

CCTV_Seoul["최근증가율"] = (
    (CCTV_Seoul["2016년"]+CCTV_Seoul["2015년"]+CCTV_Seoul["2014년"]) / CCTV_Seoul["2013년도 이전"] * 100
)
CCTV_Seoul.sort_values(by="최근증가율",ascending=False)

pop_Seoul.drop([0],axis=0,inplace=True)

pop_Seoul["외국인비율"] = pop_Seoul["외국인"] / pop_Seoul["인구수"] * 100
pop_Seoul["고령자비율"] = pop_Seoul["고령자"] / pop_Seoul["인구수"] * 100

pop_Seoul.sort_values(["인구수"], ascending=False)
pop_Seoul.sort_values(["외국인"], ascending=False)
pop_Seoul.sort_values(["외국인비율"], ascending=False)
pop_Seoul.sort_values(["고령자"], ascending=False)
pop_Seoul.sort_values(["고령자비율"], ascending=False)

data_result = pd.merge(CCTV_Seoul,pop_Seoul,on="구별")
del data_result["2013년도 이전"]
del data_result["2014년"]
del data_result["2015년"]
del data_result["2016년"]

data_result.set_index("구별",inplace=True)

data_result["CCTV비율"] = data_result["소계"] / data_result["인구수"]
data_result["CCTV비율"] = data_result["CCTV비율"] * 100
data_result.sort_values(by="CCTV비율",ascending=False)


import matplotlib.pyplot as plt
from matplotlib import rc

rc("font",family="Malgun Gothic")

data_result["인구수"].plot(kind="barh", figsize=(10,10))

def drawGraph():
    data_result["CCTV비율"].sort_values().plot(
        kind="barh",
        grid=True,
        title="가장 CCTV가 많은 구",
        figsize=(10,10))
    
drawGraph()

def drawGraph():
    plt.figure(figsize=(14,10))
    plt.scatter(data_result["인구수"],data_result["소계"], s=50)
    plt.xlabel("인구수")
    plt.ylabel("CCTV")
    plt.grid()
    plt.show()

drawGraph()

fp1 = np.polyfit(data_result["인구수"],data_result["소계"],1)
f1 = np.poly1d(fp1)
fx = np.linspace(100000,700000,100)

def drawGraph():
    plt.figure(figsize=(14,10))
    plt.scatter(data_result["인구수"],data_result["소계"], s=50)
    plt.plot(fx,f1(fx),ls="dashed",lw=3,color="g")
    plt.xlabel("인구수")
    plt.ylabel("CCTV")
    plt.grid()
    plt.show()
drawGraph()

data_result["오차"] = data_result["소계"] - f1(data_result["인구수"])
df_sort_f = data_result.sort_values(by="오차",ascending=False) # 내림차순
df_sort_t = data_result.sort_values(by="오차",ascending=True) # 오름차순

from matplotlib.colors import ListedColormap

# colormap 을 사용자 정의(user,define)로 세팅
color_step = ["#e74c3c","#2ecc71","#95a9a6","#2ecc71","#3498db","#3489db"]
my_cmap = ListedColormap(color_step)


def drawGraph():
    plt.figure(figsize=(14,10))
    plt.scatter(data_result["인구수"],data_result["소계"], s=50,c=data_result["오차"],cmap=my_cmap)
    plt.plot(fx,f1(fx),ls="dashed",lw=3,color="g")
    for n in range(5):
        # 상위 5개
        plt.text(
            df_sort_f["인구수"][n] * 1.02, # x좌표
            df_sort_f["소계"][n] * 0.98, # y좌표
            df_sort_f.index[n], # title
            fontsize = 14,
        )
        # 하위 5개
        plt.text(
            df_sort_t["인구수"][n] * 1.02, # x좌표
            df_sort_t["소계"][n] * 0.98, # y좌표
            df_sort_t.index[n], # title
            fontsize = 14,
        )
    plt.text(df_sort_f["인구수"][0] * 1.02 , df_sort_f["소계"][0] * 0.98,df_sort_f.index[0], fontsize=15)
    plt.xlabel("인구수")
    plt.ylabel("CCTV")
    plt.colorbar()
    plt.grid()
    plt.show()
drawGraph()

