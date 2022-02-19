import pandas as pd
import requests
import io
import os
import matplotlib.dates as mdates    #處理日期
import matplotlib.pyplot as plt
import yfinance as yf
import mplfinance as mpf
from matplotlib.figure import Figure
from flask import Flask, flash, redirect, url_for, render_template, send_from_directory, request

app = Flask(__name__)
app.secret_key = 'test'
TWSE_URL = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&'

@app.route("/index")
def index():
    return render_template('index.html') 

@app.route("/search_Stock", methods=['POST','GET'])
def search_Stock():
    if request.method == "POST" :
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
        stockNumber = request.form.get('stockNumber')

        if not startDate :
            flash('請輸入查詢日期')
            return redirect(url_for('error'))
        if not stockNumber :
            flash('請輸入股票代號')
            return redirect(url_for('error'))
        else :
            folder = os.path.join('static', 'images')
            # yfinance
            df = yf.download(stockNumber +'.TW',start = startDate, end = endDate)
            fig = create_figure_yfinance(stockNumber, df)
            filepath = 'static/images/stock.png'
            fig.savefig(filepath, dpi = 200)
            full_filename = os.path.join(folder, 'stock.png')
            return render_template("index.html", image_names = full_filename)

            '''
            # 台灣證券交易所API 取法
            info = list()
            resp = requests.get(TWSE_URL + '&date=' + date + '&stockNo=' + stockNumber)
            if resp.status_code != 200:
                return None
            else:
                datas = resp.json()
                if datas['data']:
                    
                    for data in datas['data']:
                        record = {
                            'date': data[0],
                            '開盤價': data[3],
                            '最高價': data[4],
                            '最低價': data[5],
                            '收盤價': data[6],
                            '成交筆數': data[8]
                        }
                        info.append(record)
                    stock_pd = pd.json_normalize(info)

                    fig = create_figure(stockNumber, stock_pd)
                    img = io.BytesIO()
                    filepath = 'static/images/image.png'
                    fig.savefig(filepath, dpi = 300)

                    return render_template("index.html", figure = fig)
                    # 顯示整個畫面
                    #output = io.BytesIO()
                    #FigureCanvas(fig).print_png(output)
                    #return Response(output.getvalue(), mimetype='image/png')
            '''
    else :
        return redirect('static/404.html') 

@app.route('/error')
def error():
    return redirect('static/500.html') 

def create_figure_yfinance(stockNumber, dataFrame):
    # 定義畫布和大小
    fig, ax=plt.subplots(figsize=(20,10))
    # 設定x軸 range
    ax.xaxis_date()
    # x軸日期範圍、旋轉角度
    plt.xticks(range(len(dataFrame.index.values)), rotation=90)
    # 定義標題
    plt.title(stockNumber)
    plt.xlabel('日期')
    plt.ylabel('價格')
    # 自定義圖表外觀
    colorStyle = mpf.make_marketcolors(
        up = "red",
        down = "green",
        edge = "black" #蠟燭邊框
    )
    # 保存為自訂的外觀，base_mpf_style系統樣式，marketcolors自定義樣式
    style = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=colorStyle)
    mpf.plot(dataFrame, type = 'candle',mav=(5,10,20,60), style = style, ax = ax) # 蠟燭圖
    return fig
'''
def create_figure(stockNumber, stock_pd):
    fig = Figure()
    fig.suptitle(stockNumber, fontsize = 14, fontweight='bold')
    #設定x軸主刻度顯示格式（日期）
    fig.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    #設定x軸主刻度間距
    fig.gca().xaxis.set_major_locator(mdates.DayLocator(interval=30))
    # 定義畫布和大小
    fig,ax=plt.subplots(figsize=(10,5))
    # 畫折線圖
    ax.plot(stock_pd.date, stock_pd['收盤價'],color='skyblue',label=stockNumber)
    # 定義y軸
    ax.set_ylabel(stockNumber,color='skyblue',fontsize=20)
    ax.tick_params(axis='y',labelcolor='skyblue')

    # 定義label
    ax.legend(loc='upper left')
    return fig
'''

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8888)