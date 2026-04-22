import numpy as np
import matplotlib.pyplot as plt

# 店舗1の売上個数の推移
data1 = [
    155, 130, 155, 136, 149, 178, 140, 176, 194, 202, 196, 191, 213,
    235, 177, 194, 242, 246, 224, 252, 217, 207, 227, 249, 225, 223, 249,
    211, 199, 197, 216, 215, 229, 217, 157, 205, 153, 200, 163, 179, 163,
    177, 186, 175, 184, 115, 101, 125, 102, 90, 107, 110, 92, 63, 32, 102,
    109, 49, 49, 77, 47, 80, 58, 92, 73, 15, 61, 39, 53, 76, 78, 26, 68, 80, 55,
    47, 53, 93, 71, 118, 69, 123, 139, 80, 91, 105, 149, 152, 138, 121
]


# 店舗2の売上個数の推移
data2 = [
    28, 43, 95, 41, 92, 19, 83, 31, 44, 31, 72, 88, 70, 32, 62, 10, 98, 65, 55,
    46, 26, 29, 63, 80, 17, 43, 39, 73, 40, 54, 36, 45, 13, 53, 82, 47, 31, 85,
    79, 29, 29, 72, 69, 76, 84, 77, 26, 67, 58, 18, 32, 67, 41, 33, 84, 84, 99,
    50, 99, 44, 86, 89, 26, 34, 37, 37, 29, 58, 26, 39, 36, 73, 66, 67, 70, 32,
    66, 70, 27, 79, 11, 83, 47, 33, 98, 13, 10, 32, 98, 81
]

        
# figure()でグラフを表示する領域をつくり，figというオブジェクトにする
fig = plt.figure()

#add_subplot()でグラフを描画する領域を追加する
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,2,3)
ax4 = fig.add_subplot(2,2,4)

days = np.arange(1, len(data1)+1)

# 最大の販売個数を取得
max_value = max(max(data1), max(data2))

# ヒストグラムにした際の最頻値を取得
mode_hist = max(max(np.histogram(data1)[0]), max(np.histogram(data2)[0]))

# set_xlim,set_ylimを用いて表示区間を統一
ax1.hist(data1)
ax1.set_title('Sales Distribution in Store1')
ax1.set_xlim(0, max_value)
ax1.set_ylim(0, mode_hist)

ax2.hist(data2)
ax2.set_title('Sales Distribution in Store2')
ax2.set_xlim(0, max_value)
ax2.set_ylim(0, mode_hist)

ax3.plot(days,data1)
ax3.set_title('Sales Trend in Store1')
ax3.set_ylim(0, max_value)

ax4.plot(days,data2)
ax4.set_title('Sales Trend in Store2')
ax4.set_ylim(0, max_value)
plt.show()