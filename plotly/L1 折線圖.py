import plotly.express as px
import pandas as pd

# 建立範例資料
df = pd.DataFrame({
    '月份': ['1月', '2月', '3月', '4月', '5月', '6月'] * 3,
    '營收': [120, 150, 180, 200, 230, 260,
           80, 100, 130, 160, 180, 210,
           60, 70, 90, 110, 130, 150],
    '產品': ['A產品'] * 6 + ['B產品'] * 6 + ['C產品'] * 6
})

df.to_csv('data/sample.csv')


# 建立折線圖
fig = px.line(
    df,
    x='月份',
    y='營收',
    color='產品',
    # line  其實是點圖的延伸 所以先畫點在畫線
    # makers就是決定你要不要特別強調資料點 要不要標註出來
    markers=True,  # 顯示資料點
    title='各產品月營收變化趨勢',
    labels={'月份': 'Month', '營收': 'Revenue (萬元)'}
)

fig.show()