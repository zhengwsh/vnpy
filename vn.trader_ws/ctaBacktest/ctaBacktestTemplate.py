# encoding: UTF-8

'''
本文件包含了CTA引擎中的策略开发用模板，开发策略时需要继承CtaTemplate类。
'''

from ctaBacktestBase import *
from vtConstant import *

########################################################################
class CtaBacktestTemplate(object):
    """CTA策略回测模板"""
    
    # 策略类的名称和作者
    className = 'CtaTemplate'
    author = EMPTY_UNICODE
    
    # MongoDB数据库的名称，K线数据库默认为1分钟
    tickDbName = TICK_DB_NAME
    barDbName = MINUTE_DB_NAME
    
    # 策略的基本参数
    name = EMPTY_UNICODE           # 策略实例名称
    vtSymbols = EMPTY_LIST        # 交易的合约vt系统代码(可设置多个合约，存放于List中)    
    productClass = EMPTY_STRING    # 产品类型（只有IB接口需要）
    currency = EMPTY_STRING        # 货币（只有IB接口需要）
    
    # 策略的基本变量，由引擎管理
    inited = False                 # 是否进行了初始化
    trading = False                # 是否启动交易，由引擎管理
    pos = 0                        # 持仓情况
    
    # 参数列表，保存了参数的名称
    paramList = ['name',
                 'className',
                 'author',
                 'vtSymbols']
    
    # 变量列表，保存了变量的名称
    varList = ['inited',
               'trading',
               'pos']

    #----------------------------------------------------------------------
    def __init__(self, ctaBktEngine, setting):
        """Constructor"""
        self.ctaBktEngine = ctaBktEngine

        # 设置策略的参数
        if setting:
            d = self.__dict__
            for key in self.paramList:
                if key in setting:
                    d[key] = setting[key]
    
    #----------------------------------------------------------------------
    def onInit(self):
        """初始化策略（必须由用户继承实现）"""
        raise NotImplementedError
    
    #----------------------------------------------------------------------
    def onStart(self):
        """启动策略（必须由用户继承实现）"""
        raise NotImplementedError
    
    #----------------------------------------------------------------------
    def onStop(self):
        """停止策略（必须由用户继承实现）"""
        raise NotImplementedError

    #----------------------------------------------------------------------
    def onTick(self, tick):
        """收到行情TICK推送（必须由用户继承实现）"""
        raise NotImplementedError

    #----------------------------------------------------------------------
    def onOrder(self, order):
        """收到委托变化推送（必须由用户继承实现）"""
        raise NotImplementedError
    
    #----------------------------------------------------------------------
    def onTrade(self, trade):
        """收到成交推送（必须由用户继承实现）"""
        raise NotImplementedError
    
    #----------------------------------------------------------------------
    def onBar(self, bar):
        """收到Bar推送（必须由用户继承实现）"""
        raise NotImplementedError
    
    #----------------------------------------------------------------------
    def buy(self, vtSymbol, price, volume, stop=False):
        """买开"""
        return self.sendOrder(CTAORDER_BUY, vtSymbol, price, volume, stop)
    
    #----------------------------------------------------------------------
    def sell(self, vtSymbol, price, volume, stop=False):
        """卖平"""
        return self.sendOrder(CTAORDER_SELL, vtSymbol, price, volume, stop)       

    #----------------------------------------------------------------------
    def short(self, vtSymbol, price, volume, stop=False):
        """卖开"""
        return self.sendOrder(CTAORDER_SHORT, vtSymbol, price, volume, stop)          
 
    #----------------------------------------------------------------------
    def cover(self, vtSymbol, price, volume, stop=False):
        """买平"""
        return self.sendOrder(CTAORDER_COVER, vtSymbol, price, volume, stop)
        
    #----------------------------------------------------------------------
    def sendOrder(self, orderType, vtSymbol, price, volume, stop=False):
        """发送委托"""
        if self.trading:
            # 如果stop为True，则意味着发本地停止单
            if stop:
                vtOrderID = self.ctaBktEngine.sendStopOrder(vtSymbol, orderType, price, volume, self)
            else:
                vtOrderID = self.ctaBktEngine.sendOrder(vtSymbol, orderType, price, volume, self) 
            return vtOrderID
        else:
            # 交易停止时发单返回空字符串
            return ''        
        
    #----------------------------------------------------------------------
    def cancelOrder(self, vtOrderID):
        """撤单"""
        # 如果发单号为空字符串，则不进行后续操作
        if not vtOrderID:
            return
        
        if STOPORDERPREFIX in vtOrderID:
            self.ctaBktEngine.cancelStopOrder(vtOrderID)
        else:
            self.ctaBktEngine.cancelOrder(vtOrderID)
    
    #----------------------------------------------------------------------
    def insertTick(self, vtSymbol, tick):
        """向数据库中插入tick数据"""
        self.ctaBktEngine.insertData(self.tickDbName, vtSymbol, tick)
    
    #----------------------------------------------------------------------
    def insertBar(self, vtSymbol, bar):
        """向数据库中插入bar数据"""
        self.ctaBktEngine.insertData(self.barDbName, vtSymbol, bar)
        
    #----------------------------------------------------------------------
    def loadTick(self, vtSymbol, days):
        """读取tick数据"""
        return self.ctaBktEngine.loadTick(self.tickDbName, vtSymbol, days)
    
    #----------------------------------------------------------------------
    def loadBar(self, vtSymbol, days):
        """读取bar数据"""
        return self.ctaBktEngine.loadBar(self.barDbName, vtSymbol, days)
    
    #----------------------------------------------------------------------
    def writeCtaLog(self, content):
        """记录CTA日志"""
        content = self.name + ':' + content
        self.ctaBktEngine.writeCtaLog(content)
        
    #----------------------------------------------------------------------
    def putEvent(self):
        """发出策略状态变化事件"""
        self.ctaBktEngine.putStrategyEvent(self.name)
        
    #----------------------------------------------------------------------
    def getEngineType(self):
        """查询当前运行的环境"""
        return self.ctaBktEngine.engineType
    
    #----------------------------------------------------------------------
    def getDirection(self,  vtSymbol):
        """查询持仓方向"""
        print self.ctaBktEngine.mainEngine.qryPosition('CTP')
        return self.ctaBktEngine.mainEngine.qryPosition('CTP')

    #----------------------------------------------------------------------
    def getPositionLong(self,  vtSymbol):
        """查询多头持仓仓位"""
        position = event.dict_['data'].__getattribute__('position')
        if self.getDirection(vtSymbol) == 1:
            if self.ctaBktEngine.mainEngine.qryPosition('CTP') != 0:
                return self.ctaBktEngine.mainEngine.qryPosition('CTP')
            else:
                return 0

    #----------------------------------------------------------------------
    def getPositionShort(self,  vtSymbol):
        """查询空头持仓仓位"""
        position = event.dict_['data'].__getattribute__('position')
        if self.getDirection(vtSymbol) == 2:
            if self.ctaBktEngine.mainEngine.qryPosition('CTP') != 0:
                return self.ctaBktEngine.mainEngine.qryPosition('CTP')
            else:
                return 0
