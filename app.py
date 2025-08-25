from flask import Flask, render_template, jsonify
import pandas as pd
import akshare as ak
import numpy as np 

app = Flask(__name__)

_stock_data_cache = None

def get_stock_realtime_data():
    """
    获取东方财富网 A 股实时行情数据
    """
    global _stock_data_cache
    try:
        df = ak.stock_zh_a_spot_em()
        if df.empty:
            print("没有获取到实时行情数据")
            return pd.DataFrame()

        df.replace({np.nan: None}, inplace=True)

        df.rename(columns={
            "代码": "symbol", "名称": "name", "最新价": "latest_price",
            "涨跌幅": "change_percent", "涨跌额": "change_amount", "成交量": "volume",
            "成交额": "turnover", "振幅": "amplitude", "最高": "high",
            "最低": "low", "今开": "open", "昨收": "previous_close",
            "量比": "volume_ratio", "换手率": "turnover_rate", "市盈率-动态": "pe_ratio",
            "市净率": "pb_ratio", "总市值": "market_cap_total", "流通市值": "market_cap_float",
            "涨速": "speed_increase", "5分钟涨跌": "change_5min", "60日涨跌幅": "change_60day",
            "年初至今涨跌幅": "change_ytd"
        }, inplace=True)
        
        _stock_data_cache = df.to_dict('records')
        return _stock_data_cache

    except Exception as e:
        print(f"获取数据时发生错误: {e}")
        return _stock_data_cache if _stock_data_cache else []

@app.route('/')
def index():
    """
    主页路由
    """
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    """
    数据API路由
    """
    data = get_stock_realtime_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)