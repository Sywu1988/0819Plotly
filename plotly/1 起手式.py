import pandas as pd
import plotly.express as px

# 讀取銷售資料
df = pd.read_csv('data/sales.csv')

# 按業務單位分組，計算總業績金額
sales_by_unit = df.groupby('業務單位')['銷售金額'].sum().reset_index()
sales_by_unit = sales_by_unit.sort_values('銷售金額', ascending=False)
# 文字有編碼   文字是圖片  系統裡面 會有文字去對圖片 001-->我    002-->你
 
# to_csv 沒有設定ecoding  預設utf-8是我  
sales_by_unit .to_csv('data/業務整理結果.csv', encoding ='big5') 

# PX.bar 使用 plotly.express 建立柱狀圖
fig = px.bar(
    sales_by_unit,
    x='業務單位',
    y='銷售金額',
    text=sales_by_unit['銷售金額'].apply(lambda x: f'{x:,.0f}'),
    title='各業務單位業績金額柱狀圖',
    labels={'業務單位': '業務單位', '銷售金額': '業績金額'},
    #https://www.w3schools.com/colors/colors_names.asp
    color_discrete_sequence=['DeepPink']
)


# 設定文字標籤位置
# textposition 參數常用選項如下:
# 'inside'：文字顯示於 bar 內部
# 'outside'：文字顯示於 bar 外部
# 'auto'：自動選擇顯示位置
# 'none'：不顯示文字
fig.update_traces(textposition='outside')

# 設定圖表高度
fig.update_layout(height=600)

# 顯示圖表
fig.show()

