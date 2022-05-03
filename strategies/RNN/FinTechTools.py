import pandas as pd
import numpy as np
import talib as ta


def multiple_ta(data):
    
    open = data['Open']
    high = data['High']
    low = data['Low']
    close = data['Close']
    volume = data['Volume']
    date = data['date']
        
    # ta Overlap Studies Functions && max_min_scaler
    ind_upperband, ind_middleband, ind_lowerband = ta.BBANDS(close, timeperiod=7, nbdevup=2, nbdevdn=2, matype=0) # BBANDS - Bollinger Bands
    ind_dema = ta.DEMA(close, timeperiod=7) # DEMA - Double Exponential Moving Average
    ind_ema = ta.EMA(close, timeperiod=7) # EMA - Exponential Moving Average
    ind_ht_trendline = ta.HT_TRENDLINE(close) # HT_TRENDLINE - Hilbert Transform - Instantaneous Trendline
    ind_kama = ta.KAMA(close, timeperiod=7) # KAMA - Kaufman Adaptive Moving Average
    ind_ma = ta.MA(close, timeperiod=7, matype=0) #MA - Moving average
    ind_mama,ind_fama = ta.MAMA(close, fastlimit=0.5, slowlimit=0.05) # MAMA - MESA Adaptive Moving Average
    ind_mavp = ta.MAVP(close, date, minperiod=2, maxperiod=7, matype=0)# MAVP - Moving average with variable period
    ind_midpoin = ta.MIDPOINT(close, timeperiod=7)# MIDPOINT - MidPoint over period
    ind_midprice = ta.MIDPRICE(high, low, timeperiod=14)# MIDPRICE - Midpoint Price over period
    ind_sar = ta.SAR(high, low, acceleration=0, maximum=0)# SAR - Parabolic SAR
    ind_sarext = ta.SAREXT(high, low, startvalue=0, offsetonreverse=0, accelerationinitlong=0, accelerationlong=0, accelerationmaxlong=0, accelerationinitshort=0, accelerationshort=0, accelerationmaxshort=0)#SAREXT - Parabolic SAR - Extended
    ind_sma = ta.SMA(close, timeperiod=7) # SMA - Simple Moving Average
    ind_t3 = ta.T3(close, timeperiod=5, vfactor=0) # T3 - Triple Exponential Moving Average (T3)
    ind_tema = ta.TEMA(close, timeperiod=7)# TEMA - Triple Exponential Moving Average
    ind_trima = ta.TRIMA(close, timeperiod=7)# TRIMA - Triangular Moving Average
    ind_wma = ta.WMA(close, timeperiod=7)# WMA - Weighted Moving Average
    
    # Momentum Indicator Functions
    ind_adx = ta.ADX(high, low, close, timeperiod=7)# ADX - Average Directional Movement Index
    ind_adxr = ta.ADXR(high, low, close, timeperiod=7)# ADXR - Average Directional Movement Index Rating
    ind_apo = ta.APO(close, fastperiod=12, slowperiod=26, matype=0)# APO - Absolute Price Oscillator
    ind_aroondown, ind_aroonup = ta.AROON(high, low, timeperiod=7)# AROON - Aroon
    ind_aroonosc = ta.AROONOSC(high, low, timeperiod=7)# AROONOSC - Aroon Oscillator
    ind_bop = ta.BOP(open, high, low, close)# BOP - Balance Of Power
    ind_cci = ta.CCI(high, low, close, timeperiod=7)# CCI - Commodity Channel Index
    ind_cmo = ta.CMO(close, timeperiod=7)# CMO - Chande Momentum Oscillator
    ind_dx = ta.DX(high, low, close, timeperiod=7)# DX - Directional Movement Index
    ind_macd, ind_macdsignal, ind_macdhist = ta.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)# MACD - Moving Average Convergence/Divergence
    ind_macdext, ind_macdsignalext, ind_macdhistext = ta.MACDEXT(close, fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0, signalperiod=9, signalmatype=0)# MACDEXT - MACD with controllable MA type
    ind_macdfix, ind_macdsignalfix, ind_macdhistfix = ta.MACDFIX(close, signalperiod=9)# MACDFIX - Moving Average Convergence/Divergence Fix 12/26
    ind_mfi = ta.MFI(high, low, close, volume, timeperiod=7)# MFI - Money Flow Index
    ind_minus_di = ta.MINUS_DI(high, low, close, timeperiod=7)# MINUS_DI - Minus Directional Indicator
    ind_minus_dm = ta.MINUS_DM(high, low, timeperiod=7)# MINUS_DM - Minus Directional Movement
    ind_mom = ta.MOM(close, timeperiod=7)# MOM - Momentum
    ind_plus_di = ta.PLUS_DI(high, low, close, timeperiod=7)# PLUS_DI - Plus Directional Indicator
    ind_plus_dm = ta.PLUS_DM(high, low, timeperiod=7)# PLUS_DM - Plus Directional Movement
    ind_ppo = ta.PPO(close, fastperiod=12, slowperiod=26, matype=0)# PPO - Percentage Price Oscillator
    ind_roc = ta.ROC(close, timeperiod=7)# ROC - Rate of change : ((price/prevPrice)-1)*100
    ind_rocp = ta.ROCP(close, timeperiod=7)# ROCP - Rate of change Percentage: (price-prevPrice)/prevPrice
    ind_rocr = ta.ROCR(close, timeperiod=7)# ROCR - Rate of change ratio: (price/prevPrice)
    ind_rocr100 = ta.ROCR100(close, timeperiod=7)# ROCR100 - Rate of change ratio 100 scale: (price/prevPrice)*100
    ind_rsi = ta.RSI(close, timeperiod=7)# RSI - Relative Strength Index
    ind_slowk, ind_slowd = ta.STOCH(high, low, close, fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)# STOCH - Stochastic
    ind_fastk, ind_fastd = ta.STOCHF(high, low, close, fastk_period=5, fastd_period=3, fastd_matype=0)# STOCHF - Stochastic Fast
    ind_fastkrsi, ind_fastdrsi = ta.STOCHRSI(close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)# STOCHRSI - Stochastic Relative Strength Index
    ind_trix = ta.TRIX(close, timeperiod=7)# TRIX - 1-day Rate-Of-Change (ROC) of a Triple Smooth EMA
    ind_ultosc = ta.ULTOSC(high, low, close, timeperiod1=7, timeperiod2=14, timeperiod3=28)# ULTOSC - Ultimate Oscillator
    ind_willr = ta.WILLR(high, low, close, timeperiod=7) # WILLR - Williams' %R
    
    # Volume Indicator Functions
    ind_ad = ta.AD(high, low, close, volume)  # AD - Chaikin A/D Line
    ind_adosc = ta.ADOSC(high, low, close, volume, fastperiod=3, slowperiod=10) # ADOSC - Chaikin A/D Oscillator
    ind_obv = ta.OBV(close, volume) # OBV - On Balance Volume
    
    # Volatility Indicator Functions
    ind_atr = ta.ATR(high, low, close, timeperiod=7) # ATR - Average True Range
    ind_natr = ta.NATR(high, low, close, timeperiod=7) # NATR - Normalized Average True Range
    ind_trange = ta.TRANGE(high, low, close) # TRANGE - True Range
    
    # Price Transform Functions
    ind_average = ta.AVGPRICE(open, high, low, close)# AVGPRICE - Average Price
    ind_medprice = ta.MEDPRICE(high, low)# MEDPRICE - Median Price
    ind_typprice = ta.TYPPRICE(high, low, close)# TYPPRICE - Typical Price
    ind_wclprice = ta.WCLPRICE(high, low, close)# WCLPRICE - Weighted Close Price
    
    # Cycle Indicator Functions
    ind_ht_dcperiod = ta.HT_DCPERIOD(close)# HT_DCPERIOD - Hilbert Transform - Dominant Cycle Period
    ind_ht_dcphase = ta.HT_DCPHASE(close)# HT_DCPHASE - Hilbert Transform - Dominant Cycle Phase
    ind_inphase, ind_quadrature = ta.HT_PHASOR(close)# HT_PHASOR - Hilbert Transform - Phasor Components
    ind_sine, ind_leadsine = ta.HT_SINE(close)# HT_SINE - Hilbert Transform - SineWave
    ind_integer = ta.HT_TRENDMODE(close)# HT_TRENDMODE - Hilbert Transform - Trend vs Cycle Mode
    
    # Pattern Recognition Functions
    ind_CDL2CROWS = ta.CDL2CROWS(open, high, low, close)# CDL2CROWS - Two Crows
    ind_CDL3BLACKCROWS = ta.CDL3BLACKCROWS(open, high, low, close)# CDL3BLACKCROWS - Three Black Crows
    ind_CDL3INSIDE = ta.CDL3INSIDE(open, high, low, close)# CDL3INSIDE - Three Inside Up/Down
    ind_CDL3LINESTRIKE = ta.CDL3LINESTRIKE(open, high, low, close)# CDL3LINESTRIKE - Three-Line Strike
    ind_CDL3OUTSIDE = ta.CDL3OUTSIDE(open, high, low, close)# CDL3OUTSIDE - Three Outside Up/Down
    ind_CDL3STARSINSOUTH = ta.CDL3STARSINSOUTH(open, high, low, close)# CDL3STARSINSOUTH - Three Stars In The South
    ind_CDL3WHITESOLDIERS = ta.CDL3WHITESOLDIERS(open, high, low, close)# CDL3WHITESOLDIERS - Three Advancing White Soldiers
    ind_CDLABANDONEDBABY = ta.CDLABANDONEDBABY(open, high, low, close, penetration=0)# CDLABANDONEDBABY - Abandoned Baby
    ind_CDLADVANCEBLOCK = ta.CDLADVANCEBLOCK(open, high, low, close)# CDLADVANCEBLOCK - Advance Block
    ind_CDLBELTHOLD = ta.CDLBELTHOLD(open, high, low, close)# CDLBELTHOLD - Belt-hold
    ind_CDLBREAKAWAY = ta.CDLBREAKAWAY(open, high, low, close)# CDLBREAKAWAY - Breakaway
    ind_CDLCLOSINGMARUBOZU = ta.CDLCLOSINGMARUBOZU(open, high, low, close)# CDLCLOSINGMARUBOZU - Closing Marubozu
    ind_CDLCONCEALBABYSWALL = ta.CDLCONCEALBABYSWALL(open, high, low, close)# CDLCONCEALBABYSWALL - Concealing Baby Swallow
    ind_CDLCOUNTERATTACK = ta.CDLCOUNTERATTACK(open, high, low, close)# CDLCOUNTERATTACK - Counterattack
    ind_CDLDARKCLOUDCOVER = ta.CDLDARKCLOUDCOVER(open, high, low, close, penetration=0)# CDLDARKCLOUDCOVER - Dark Cloud Cover
    ind_CDLDOJI = ta.CDLDOJI(open, high, low, close)# CDLDOJI - Doji
    ind_CDLDOJISTAR = ta.CDLDOJISTAR(open, high, low, close)# CDLDOJISTAR - Doji Star
    ind_CDLDRAGONFLYDOJI = ta.CDLDRAGONFLYDOJI(open, high, low, close)# CDLDRAGONFLYDOJI - Dragonfly Doji
    ind_CDLENGULFING = ta.CDLENGULFING(open, high, low, close)# CDLENGULFING - Engulfing Pattern
    ind_CDLEVENINGDOJISTAR = ta.CDLEVENINGDOJISTAR(open, high, low, close)# CDLEVENINGDOJISTAR - Evening Doji Star
    ind_CDLEVENINGSTAR = ta.CDLEVENINGSTAR(open, high, low, close)# CDLEVENINGSTAR - Evening Star
    ind_CDLGAPSIDESIDEWHITE = ta.CDLGAPSIDESIDEWHITE(open, high, low, close)# CDLGAPSIDESIDEWHITE - Up/Down-gap side-by-side white lines
    ind_CDLGRAVESTONEDOJI = ta.CDLGRAVESTONEDOJI(open, high, low, close)# CDLGRAVESTONEDOJI - Gravestone Doji
    ind_CDLHAMMER = ta.CDLHAMMER(open, high, low, close)# CDLHAMMER - Hammer
    ind_CDLHANGINGMAN = ta.CDLHANGINGMAN(open, high, low, close)# CDLHANGINGMAN - Hanging Man
    ind_CDLHARAMI = ta.CDLHARAMI(open, high, low, close)# CDLHARAMI - Harami Pattern
    ind_CDLHARAMICROSS = ta.CDLHARAMICROSS(open, high, low, close)# CDLHARAMICROSS - Harami Cross Pattern
    ind_CDLHIGHWAVE = ta.CDLHIGHWAVE(open, high, low, close)# CDLHIGHWAVE - High-Wave Candle
    ind_CDLHIKKAKE = ta.CDLHIKKAKE(open, high, low, close)# CDLHIKKAKE - Hikkake Pattern
    ind_CDLHIKKAKEMOD = ta.CDLHIKKAKEMOD(open, high, low, close)# CDLHIKKAKEMOD - Modified Hikkake Pattern
    ind_CDLHOMINGPIGEON = ta.CDLHOMINGPIGEON(open, high, low, close)# CDLHOMINGPIGEON - Homing Pigeon
    ind_CDLIDENTICAL3CROWS = ta.CDLIDENTICAL3CROWS(open, high, low, close)# CDLIDENTICAL3CROWS - Identical Three Crows
    ind_CDLINNECK = ta.CDLINNECK(open, high, low, close)# CDLINNECK - In-Neck Pattern
    ind_CDLINVERTEDHAMMER = ta.CDLINVERTEDHAMMER(open, high, low, close)# CDLINVERTEDHAMMER - Inverted Hammer
    ind_CDLKICKING = ta.CDLKICKING(open, high, low, close)# CDLKICKING - Kicking
    ind_CDLKICKINGBYLENGTH = ta.CDLKICKINGBYLENGTH(open, high, low, close)    # CDLKICKINGBYLENGTH - Kicking - bull/bear determined by the longer marubozu
    ind_CDLLADDERBOTTOM = ta.CDLLADDERBOTTOM(open, high, low, close)#  CDLLADDERBOTTOM - Ladder Bottom
    ind_CDLLONGLEGGEDDOJI = ta.CDLLONGLEGGEDDOJI(open, high, low, close)# CDLLONGLEGGEDDOJI - Long Legged Doji
    ind_CDLLONGLINE = ta.CDLLONGLINE(open, high, low, close)# CDLLONGLINE - Long Line Candle
    ind_CDLMARUBOZU = ta.CDLMARUBOZU(open, high, low, close)# CDLMARUBOZU - Marubozu
    ind_CDLMATCHINGLOW = ta.CDLMATCHINGLOW(open, high, low, close)# CDLMATCHINGLOW - Matching Low
    ind_CDLMATHOLD = ta.CDLMATHOLD(open, high, low, close)# CDLMATHOLD - Mat Hold
    ind_CDLMORNINGDOJISTAR = ta.CDLMORNINGDOJISTAR(open, high, low, close)# CDLMORNINGDOJISTAR - Morning Doji Star
    ind_CDLMORNINGSTAR = ta.CDLMORNINGSTAR(open, high, low, close)# CDLMORNINGSTAR - Morning Star
    ind_CDLONNECK = ta.CDLONNECK(open, high, low, close)# CDLONNECK - On-Neck Pattern
    ind_CDLPIERCING = ta.CDLPIERCING(open, high, low, close)# CDLPIERCING - Piercing Pattern
    ind_CDLRICKSHAWMAN = ta.CDLRICKSHAWMAN(open, high, low, close)# CDLRICKSHAWMAN - Rickshaw Man
    ind_CDLRISEFALL3METHODS = ta.CDLRISEFALL3METHODS(open, high, low, close)# CDLRISEFALL3METHODS - Rising/Falling Three Methods
    ind_CDLSEPARATINGLINES = ta.CDLSEPARATINGLINES(open, high, low, close)# CDLSEPARATINGLINES - Separating Lines
    ind_CDLSHOOTINGSTAR = ta.CDLSHOOTINGSTAR(open, high, low, close)# CDLSHOOTINGSTAR - Shooting Star
    ind_CDLSHORTLINE = ta.CDLSHORTLINE(open, high, low, close)# CDLSHORTLINE - Short Line Candle
    ind_CDLSPINNINGTOP = ta.CDLSPINNINGTOP(open, high, low, close)# CDLSPINNINGTOP - Spinning Top
    ind_CDLSTALLEDPATTERN = ta.CDLSTALLEDPATTERN(open, high, low, close)# CDLSTALLEDPATTERN - Stalled Pattern
    ind_CDLSTICKSANDWICH = ta.CDLSTICKSANDWICH(open, high, low, close)# CDLSTICKSANDWICH - Stick Sandwich
    ind_CDLTAKURI = ta.CDLTAKURI(open, high, low, close)# CDLTAKURI - Takuri (Dragonfly Doji with very long lower shadow)
    ind_CDLTASUKIGAP = ta.CDLTASUKIGAP(open, high, low, close)# CDLTASUKIGAP - Tasuki Gap
    ind_CDLTHRUSTING = ta.CDLTHRUSTING(open, high, low, close)# CDLTHRUSTING - Thrusting Pattern
    ind_CDLTRISTAR = ta.CDLTRISTAR(open, high, low, close)# CDLTRISTAR - Tristar Pattern
    ind_CDLUNIQUE3RIVER = ta.CDLUNIQUE3RIVER(open, high, low, close)# CDLUNIQUE3RIVER - Unique 3 River
    ind_CDLUPSIDEGAP2CROWS = ta.CDLUPSIDEGAP2CROWS(open, high, low, close)# CDLUPSIDEGAP2CROWS - Upside Gap Two Crows
    ind_CDLXSIDEGAP3METHODS = ta.CDLXSIDEGAP3METHODS(open, high, low, close)# CDLXSIDEGAP3METHODS - Upside/Downside Gap Three Methods
    
    # Statistic Functions
    ind_beta = ta.BETA(high, low, timeperiod=7) # BETA - Beta
    ind_correl = ta.CORREL(high, low, timeperiod=7)# CORREL - Pearson's Correlation Coefficient (r)
    ind_linearreg = ta.LINEARREG(close, timeperiod=7)# LINEARREG - Linear Regression
    ind_linearreg_angle = ta.LINEARREG_ANGLE(close, timeperiod=7)# LINEARREG_ANGLE - Linear Regression Angle
    ind_linearreg_intercept = ta.LINEARREG_INTERCEPT(close, timeperiod=7)# LINEARREG_INTERCEPT - Linear Regression Intercept
    ind_linearreg_slope = ta.LINEARREG_SLOPE(close, timeperiod=7)# LINEARREG_SLOPE - Linear Regression Slope
    ind_stddev = ta.STDDEV(close, timeperiod=7, nbdev=1)# STDDEV - Standard Deviation
    ind_tsf = ta.TSF(close, timeperiod=7)# TSF - Time Series Forecast
    ind_var = ta.VAR(close, timeperiod=7, nbdev=1)# VAR - Variance
    
    # Math Transform Functions
    ind_ACOS = ta.ACOS(close)# ACOS - Vector Trigonometric ACos
    ind_ASIN = ta.ASIN(close)# ASIN - Vector Trigonometric ASin
    ind_ATAN = ta.ATAN(close)# ATAN - Vector Trigonometric ATan
    ind_CEIL = ta.CEIL(close)# CEIL - Vector Ceil
    ind_COS = ta.COS(close)# COS - Vector Trigonometric Cos
    ind_COSH = ta.COSH(close)# COSH - Vector Trigonometric Cosh
    ind_EXP = ta.EXP(close)# EXP - Vector Arithmetic Exp
    ind_FLOOR = ta.FLOOR(close)# FLOOR - Vector Floor
    ind_LN = ta.LN(close)# LN - Vector Log Natural
    ind_LOG10 = ta.LOG10(close)# LOG10 - Vector Log10
    ind_SIN = ta.SIN(close)# SIN - Vector Trigonometric Sin
    ind_SINH = ta.SINH(close)# SINH - Vector Trigonometric Sinh
    ind_SQRT = ta.SQRT(close)# SQRT - Vector Square Root
    ind_TAN = ta.TAN(close)# TAN - Vector Trigonometric Tan
    ind_TANH = ta.TANH(close)    # TANH - Vector Trigonometric Tanh
    
    

    
    # Math Operator Functions
    ind_ADD = ta.ADD(high, low)# ADD - Vector Arithmetic Add
    ind_DIV = ta.DIV(high, low)#DIV - VectorDIV - Vector Arithmetic Div
    ind_MAX = ta.MAX(close, timeperiod=7)#MAX - Highest value over a specified period
    ind_MAXINDEX = ta.MAXINDEX(close, timeperiod=7)# MAXINDEX - Index of highest value over a specified period
    ind_MIN = ta.MIN(close, timeperiod=7)# MIN - Lowest value over a specified period
    ind_MININDEX = ta.MININDEX(close, timeperiod=7)# MININDEX - Index of lowest value over a specified period
    ind_min, ind_max = ta.MINMAX(close, timeperiod=30)# MINMAX - Lowest and highest values over a specified period
    ind_minidx, ind_maxidx = ta.MINMAXINDEX(close, timeperiod=7)# MINMAXINDEX - Indexes of lowest and highest values over a specified period 
    ind_MULT = ta.MULT(high, low)# MULT - Vector Arithmetic Mult
    # ta.SUB = ta.SUB(high, low)# SUB - Vector Arithmetic Substraction
    ta.SUB = high-low
    # ta.SUM = ta.SUM(close, timeperiod=7)# SUM - Summation
    ta.SUM = high+low
    
    ind_list = [
        # Overlap Studies Functions
        ind_upperband,ind_middleband,ind_lowerband,
        ind_dema,ind_ema,ind_ht_trendline, ind_kama, 
        ind_ma, ind_mama, ind_mama,ind_mavp,ind_midpoin,
        ind_midprice,ind_sar,ind_sarext,ind_sma,ind_t3,
        ind_tema,ind_trima,ind_wma, 
        
        # Momentum Indicator Functions
        ind_adx,ind_adxr,ind_apo,ind_aroondown,ind_aroonup,
        ind_aroonosc,ind_bop,ind_cci,ind_cmo,ind_dx,ind_macd, 
        ind_macdsignal, ind_macdhist,ind_macdext, ind_macdsignalext, 
        ind_macdhistext,ind_macdfix, ind_macdsignalfix, 
        ind_macdhistfix,ind_mfi,ind_minus_di,ind_minus_dm,
        ind_mom,ind_plus_di,ind_plus_dm,ind_ppo,ind_roc,
        ind_rocp,ind_rocr,ind_rocr100, ind_rsi,ind_slowk, 
        ind_slowd,ind_fastk, ind_fastd,ind_fastkrsi, ind_fastdrsi,
        ind_trix,ind_ultosc,ind_willr,
        
        # Volume Indicator Functions
        ind_ad,ind_adosc,ind_obv, 
        
        # Volatility Indicator Functions  
        ind_atr,ind_natr,ind_trange, 
        
        # Price Transform Functions
        ind_average,ind_medprice,ind_typprice,ind_wclprice, 
        
        # Cycle Indicator Functions
        ind_ht_dcperiod,ind_ht_dcphase,ind_inphase, ind_quadrature,
        ind_sine, ind_leadsine,ind_integer, 
        
        # Pattern Recognition Functions
        ind_CDL2CROWS,ind_CDL3BLACKCROWS,ind_CDL3INSIDE,ind_CDL3LINESTRIKE,
        ind_CDL3OUTSIDE, ind_CDL3STARSINSOUTH,ind_CDL3WHITESOLDIERS,
        ind_CDLABANDONEDBABY,ind_CDLADVANCEBLOCK,ind_CDLBELTHOLD,ind_CDLBREAKAWAY,
        ind_CDLCLOSINGMARUBOZU,ind_CDLCONCEALBABYSWALL,ind_CDLCOUNTERATTACK,
        ind_CDLDARKCLOUDCOVER,ind_CDLDOJI,ind_CDLDOJISTAR,ind_CDLDRAGONFLYDOJI,
        ind_CDLENGULFING,ind_CDLEVENINGDOJISTAR,ind_CDLEVENINGSTAR,
        ind_CDLGAPSIDESIDEWHITE,ind_CDLGRAVESTONEDOJI,ind_CDLHAMMER,
        ind_CDLHANGINGMAN,ind_CDLHARAMI, ind_CDLHARAMICROSS,ind_CDLHARAMICROSS,
        ind_CDLHIKKAKE,ind_CDLHIKKAKEMOD,ind_CDLHOMINGPIGEON,ind_CDLIDENTICAL3CROWS,
        ind_CDLINNECK,ind_CDLINVERTEDHAMMER, ind_CDLKICKING,ind_CDLKICKINGBYLENGTH,
        ind_CDLLADDERBOTTOM,ind_CDLLONGLEGGEDDOJI,ind_CDLLONGLINE,ind_CDLMARUBOZU,
        ind_CDLMATCHINGLOW,ind_CDLMATHOLD,ind_CDLMORNINGDOJISTAR,ind_CDLMORNINGSTAR,
        ind_CDLONNECK,ind_CDLPIERCING,ind_CDLRICKSHAWMAN,ind_CDLRISEFALL3METHODS,
        ind_CDLSEPARATINGLINES,ind_CDLSHOOTINGSTAR,ind_CDLSHORTLINE,ind_CDLSPINNINGTOP,
        ind_CDLSTALLEDPATTERN,ind_CDLSTICKSANDWICH,ind_CDLTAKURI,ind_CDLTASUKIGAP,
        ind_CDLTHRUSTING,ind_CDLTRISTAR,ind_CDLUNIQUE3RIVER,ind_CDLUPSIDEGAP2CROWS,
        ind_CDLXSIDEGAP3METHODS,    
        
        # Statistic Functions
        ind_beta,ind_correl,ind_linearreg,ind_linearreg_angle,ind_linearreg_intercept,
        ind_linearreg_slope,ind_stddev,ind_tsf,ind_var,  
        
        # Math Transform Functions
        ind_ACOS,ind_ASIN,ind_ATAN,ind_CEIL,ind_COS,ind_COSH,ind_EXP,ind_FLOOR,
        ind_LN,ind_LOG10,ind_SIN,ind_SINH,ind_SQRT,ind_TAN,ind_TANH,  
        
        # Math Operator Functions
        ind_ADD,ind_DIV,ind_MAX,ind_MAXINDEX,ind_MIN,ind_MININDEX,ind_min, ind_max,
        ind_minidx, ind_maxidx,ind_MULT,ta.SUB,ta.SUM 
        
    ]   
    
    name_list = [#OverlapStudiesFunctions
        'ind_upperband', 'ind_middleband', 'ind_lowerband', 'ind_dema', 'ind_ema',
        'ind_ht_trendline', 'ind_kama', 'ind_ma', 'ind_mama', 'ind_mama', 'ind_mavp', 'ind_midpoin', 'ind_midprice',
        'ind_sar', 'ind_sarext', 'ind_sma', 'ind_t3', 'ind_tema', 'ind_trima', 'ind_wma', 
        
        #MomentumIndicatorFunctions
        'ind_adx', 'ind_adxr', 'ind_apo', 'ind_aroondown', 'ind_aroonup', 'ind_aroonosc', 'ind_bop', 'ind_cci',
        'ind_cmo', 'ind_dx', 'ind_macd', 'ind_macdsignal', 'ind_macdhist', 'ind_macdext', 'ind_macdsignalext',
        'ind_macdhistext', 'ind_macdfix', 'ind_macdsignalfix', 'ind_macdhistfix', 'ind_mfi', 'ind_minus_di',
        'ind_minus_dm', 'ind_mom', 'ind_plus_di', 'ind_plus_dm', 'ind_ppo', 'ind_roc', 'ind_rocp', 'ind_rocr',
        'ind_rocr100', 'ind_rsi', 'ind_slowk', 'ind_slowd', 'ind_fastk', 'ind_fastd', 'ind_fastkrsi', 'ind_fastdrsi',
        'ind_trix', 'ind_ultosc', 'ind_willr', 
        
        #VolumeIndicatorFunctions
        'ind_ad', 'ind_adosc', 'ind_obv',
        
        #VolatilityIndicatorFunctions
        'ind_atr', 'ind_natr', 'ind_trange',
        
        #PriceTransformFunctions
        'ind_average', 'ind_medprice', 'ind_typprice', 'ind_wclprice',
        #CycleIndicatorFunctions
        'ind_ht_dcperiod', 'ind_ht_dcphase', 'ind_inphase', 'ind_quadrature', 'ind_sine', 'ind_leadsine', 'ind_integer',
                
        #PatternRecognitionFunctions
        'ind_CDL2CROWS', 'ind_CDL3BLACKCROWS', 'ind_CDL3INSIDE', 'ind_CDL3LINESTRIKE', 'ind_CDL3OUTSIDE', 'ind_CDL3STARSINSOUTH',
        'ind_CDL3WHITESOLDIERS', 'ind_CDLABANDONEDBABY', 'ind_CDLADVANCEBLOCK', 'ind_CDLBELTHOLD', 'ind_CDLBREAKAWAY', 'ind_CDLCLOSINGMARUBOZU',
        'ind_CDLCONCEALBABYSWALL', 'ind_CDLCOUNTERATTACK', 'ind_CDLDARKCLOUDCOVER', 'ind_CDLDOJI', 'ind_CDLDOJISTAR', 'ind_CDLDRAGONFLYDOJI',
        'ind_CDLENGULFING', 'ind_CDLEVENINGDOJISTAR', 'ind_CDLEVENINGSTAR', 'ind_CDLGAPSIDESIDEWHITE', 'ind_CDLGRAVESTONEDOJI', 'ind_CDLHAMMER',
        'ind_CDLHANGINGMAN', 'ind_CDLHARAMI', 'ind_CDLHARAMICROSS', 'ind_CDLHARAMICROSS', 'ind_CDLHIKKAKE', 'ind_CDLHIKKAKEMOD', 'ind_CDLHOMINGPIGEON',
        'ind_CDLIDENTICAL3CROWS', 'ind_CDLINNECK', 'ind_CDLINVERTEDHAMMER', 'ind_CDLKICKING', 'ind_CDLKICKINGBYLENGTH', 'ind_CDLLADDERBOTTOM',
        'ind_CDLLONGLEGGEDDOJI','ind_CDLLONGLINE', 'ind_CDLMARUBOZU', 'ind_CDLMATCHINGLOW', 'ind_CDLMATHOLD', 'ind_CDLMORNINGDOJISTAR', 'ind_CDLMORNINGSTAR',
        'ind_CDLONNECK','ind_CDLPIERCING', 'ind_CDLRICKSHAWMAN', 'ind_CDLRISEFALL3METHODS', 'ind_CDLSEPARATINGLINES', 'ind_CDLSHOOTINGSTAR',
        'ind_CDLSHORTLINE','ind_CDLSPINNINGTOP', 'ind_CDLSTALLEDPATTERN', 'ind_CDLSTICKSANDWICH', 'ind_CDLTAKURI', 'ind_CDLTASUKIGAP',
        'ind_CDLTHRUSTING', 'ind_CDLTRISTAR', 'ind_CDLUNIQUE3RIVER', 'ind_CDLUPSIDEGAP2CROWS', 'ind_CDLXSIDEGAP3METHODS',
        
        #StatisticFunctions
        'ind_beta', 'ind_correl', 'ind_linearreg', 'ind_linearreg_angle', 'ind_linearreg_intercept', 'ind_linearreg_slope',
        'ind_stddev', 'ind_tsf', 'ind_var',
        
        #MathTransformFunctions
        'ind_ACOS', 'ind_ASIN', 'ind_ATAN', 'ind_CEIL', 'ind_COS', 'ind_COSH', 'ind_EXP', 'ind_FLOOR', 'ind_LN', 'ind_LOG10',
        'ind_SIN', 'ind_SINH', 'ind_SQRT', 'ind_TAN', 'ind_TANH',
        
        #MathOperatorFunctions
        'ind_ADD', 'ind_DIV', 'ind_MAX', 'ind_MAXINDEX', 'ind_MIN', 'ind_MININDEX', 'ind_min', 'ind_max', 'ind_minidx', 'ind_maxidx',
        'ind_MULT', 'ta.SUB', 'ta.SUM'
    ]
    
    return ind_list,name_list
