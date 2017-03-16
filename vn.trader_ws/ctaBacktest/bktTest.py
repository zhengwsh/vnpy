
from ctaBacktestEngine import *
from strategy.strategyAtrRsi import *

# 创建回测引擎
engine = BacktestingEngine()

# 设置引擎的回测模式为K线
engine.setBacktestingMode(engine.BAR_MODE)

# 设置回测用的数据起始日期
engine.setStartDate('20160101')

# 载入历史数据到引擎中
engine.setDatabase(MINUTE_DB_NAME, 'IF0000')

# 设置产品相关参数
engine.setSlippage(0.2)     # 股指1跳
engine.setRate(0.3/10000)   # 万0.3
engine.setSize(300)         # 股指合约大小    

# 在引擎中创建策略对象
engine.initStrategy(DoubleEmaDemo, {})

# 开始跑回测
engine.runBacktesting()

# 显示回测结果
# spyder或者ipython notebook中运行时，会弹出盈亏曲线图
# 直接在cmd中回测则只会打印一些回测数值
engine.showBacktestingResult()
    