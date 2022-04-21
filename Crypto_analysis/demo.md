# Binance 

## Data collection

### Market quotes

> Raw data

* Open
* High 
* Low
* Close
* Volume
* Asset

> Calculated data

* Log price
* Direction
* Previous 7 days
* One day price change
* daily return
* volumn change
* Standard devareiation

> Resources

https://binance-docs.github.io/apidocs/spot/en/

### Technical indicators
#### [Overlap Studies](https://mrjbq7.github.io/ta-lib/func_groups/overlap_studies.html)

```
BBANDS               Bollinger Bands
DEMA                 Double Exponential Moving Average
EMA                  Exponential Moving Average
HT_TRENDLINE         Hilbert Transform - Instantaneous Trendline
KAMA                 Kaufman Adaptive Moving Average
MA                   Moving average
MAMA                 MESA Adaptive Moving Average
MAVP                 Moving average with variable period
MIDPOINT             MidPoint over period
MIDPRICE             Midpoint Price over period
SAR                  Parabolic SAR
SAREXT               Parabolic SAR - Extended
SMA                  Simple Moving Average
T3                   Triple Exponential Moving Average (T3)
TEMA                 Triple Exponential Moving Average
TRIMA                Triangular Moving Average
WMA                  Weighted Moving Average
```

#### [Momentum Indicators](https://mrjbq7.github.io/ta-lib/func_groups/momentum_indicators.html)

```
ADX                  Average Directional Movement Index
ADXR                 Average Directional Movement Index Rating
APO                  Absolute Price Oscillator
AROON                Aroon
AROONOSC             Aroon Oscillator
BOP                  Balance Of Power
CCI                  Commodity Channel Index
CMO                  Chande Momentum Oscillator
DX                   Directional Movement Index
MACD                 Moving Average Convergence/Divergence
MACDEXT              MACD with controllable MA type
MACDFIX              Moving Average Convergence/Divergence Fix 12/26
MFI                  Money Flow Index
MINUS_DI             Minus Directional Indicator
MINUS_DM             Minus Directional Movement
MOM                  Momentum
PLUS_DI              Plus Directional Indicator
PLUS_DM              Plus Directional Movement
PPO                  Percentage Price Oscillator
ROC                  Rate of change : ((price/prevPrice)-1)*100
ROCP                 Rate of change Percentage: (price-prevPrice)/prevPrice
ROCR                 Rate of change ratio: (price/prevPrice)
ROCR100              Rate of change ratio 100 scale: (price/prevPrice)*100
RSI                  Relative Strength Index
STOCH                Stochastic
STOCHF               Stochastic Fast
STOCHRSI             Stochastic Relative Strength Index
TRIX                 1-day Rate-Of-Change (ROC) of a Triple Smooth EMA
ULTOSC               Ultimate Oscillator
WILLR                Williams' %R
```

#### [Volume Indicators](https://mrjbq7.github.io/ta-lib/func_groups/volume_indicators.html)

```
AD                   Chaikin A/D Line
ADOSC                Chaikin A/D Oscillator
OBV                  On Balance Volume
```

#### [Volatility Indicators](https://mrjbq7.github.io/ta-lib/func_groups/volatility_indicators.html)

```
ATR                  Average True Range
NATR                 Normalized Average True Range
TRANGE               True Range
```

#### [Price Transform](https://mrjbq7.github.io/ta-lib/func_groups/price_transform.html)

```
AVGPRICE             Average Price
MEDPRICE             Median Price
TYPPRICE             Typical Price
WCLPRICE             Weighted Close Price
```

#### [Cycle Indicators](https://mrjbq7.github.io/ta-lib/func_groups/cycle_indicators.html)

```
HT_DCPERIOD          Hilbert Transform - Dominant Cycle Period
HT_DCPHASE           Hilbert Transform - Dominant Cycle Phase
HT_PHASOR            Hilbert Transform - Phasor Components
HT_SINE              Hilbert Transform - SineWave
HT_TRENDMODE         Hilbert Transform - Trend vs Cycle Mode
```

#### [Pattern Recognition](https://mrjbq7.github.io/ta-lib/func_groups/pattern_recognition.html)

```
CDL2CROWS            Two Crows
CDL3BLACKCROWS       Three Black Crows
CDL3INSIDE           Three Inside Up/Down
CDL3LINESTRIKE       Three-Line Strike
CDL3OUTSIDE          Three Outside Up/Down
CDL3STARSINSOUTH     Three Stars In The South
CDL3WHITESOLDIERS    Three Advancing White Soldiers
CDLABANDONEDBABY     Abandoned Baby
CDLADVANCEBLOCK      Advance Block
CDLBELTHOLD          Belt-hold
CDLBREAKAWAY         Breakaway
CDLCLOSINGMARUBOZU   Closing Marubozu
CDLCONCEALBABYSWALL  Concealing Baby Swallow
CDLCOUNTERATTACK     Counterattack
CDLDARKCLOUDCOVER    Dark Cloud Cover
CDLDOJI              Doji
CDLDOJISTAR          Doji Star
CDLDRAGONFLYDOJI     Dragonfly Doji
CDLENGULFING         Engulfing Pattern
CDLEVENINGDOJISTAR   Evening Doji Star
CDLEVENINGSTAR       Evening Star
CDLGAPSIDESIDEWHITE  Up/Down-gap side-by-side white lines
CDLGRAVESTONEDOJI    Gravestone Doji
CDLHAMMER            Hammer
CDLHANGINGMAN        Hanging Man
CDLHARAMI            Harami Pattern
CDLHARAMICROSS       Harami Cross Pattern
CDLHIGHWAVE          High-Wave Candle
CDLHIKKAKE           Hikkake Pattern
CDLHIKKAKEMOD        Modified Hikkake Pattern
CDLHOMINGPIGEON      Homing Pigeon
CDLIDENTICAL3CROWS   Identical Three Crows
CDLINNECK            In-Neck Pattern
CDLINVERTEDHAMMER    Inverted Hammer
CDLKICKING           Kicking
CDLKICKINGBYLENGTH   Kicking - bull/bear determined by the longer marubozu
CDLLADDERBOTTOM      Ladder Bottom
CDLLONGLEGGEDDOJI    Long Legged Doji
CDLLONGLINE          Long Line Candle
CDLMARUBOZU          Marubozu
CDLMATCHINGLOW       Matching Low
CDLMATHOLD           Mat Hold
CDLMORNINGDOJISTAR   Morning Doji Star
CDLMORNINGSTAR       Morning Star
CDLONNECK            On-Neck Pattern
CDLPIERCING          Piercing Pattern
CDLRICKSHAWMAN       Rickshaw Man
CDLRISEFALL3METHODS  Rising/Falling Three Methods
CDLSEPARATINGLINES   Separating Lines
CDLSHOOTINGSTAR      Shooting Star
CDLSHORTLINE         Short Line Candle
CDLSPINNINGTOP       Spinning Top
CDLSTALLEDPATTERN    Stalled Pattern
CDLSTICKSANDWICH     Stick Sandwich
CDLTAKURI            Takuri (Dragonfly Doji with very long lower shadow)
CDLTASUKIGAP         Tasuki Gap
CDLTHRUSTING         Thrusting Pattern
CDLTRISTAR           Tristar Pattern
CDLUNIQUE3RIVER      Unique 3 River
CDLUPSIDEGAP2CROWS   Upside Gap Two Crows
CDLXSIDEGAP3METHODS  Upside/Downside Gap Three Methods
```

#### [Statistic Functions](https://mrjbq7.github.io/ta-lib/func_groups/statistic_functions.html)

```
BETA                 Beta
CORREL               Pearson's Correlation Coefficient (r)
LINEARREG            Linear Regression
LINEARREG_ANGLE      Linear Regression Angle
LINEARREG_INTERCEPT  Linear Regression Intercept
LINEARREG_SLOPE      Linear Regression Slope
STDDEV               Standard Deviation
TSF                  Time Series Forecast
VAR                  Variance
```

Resources: https://mrjbq7.github.io/ta-lib/

### Global Currency

```
CNY/USD    China
JPY/USD    Japanese
EUR/USD    Euro
GBP/USD    British
INR/USD    India
BRL/USD    Brazil
CAD/USD		 Canada
KRW/USD	   South Korea
```

> Resource

https://www.bis.org/statistics/xrusd.htm

### BlockChain information

| Feature name                     | Explanation                                                  |
| -------------------------------- | ------------------------------------------------------------ |
| utxo-count                       | A UTXO is **the amount of digital currency remaining after a cryptocurrency transaction is executed**. |
| cost-per-transaction-percent     | *Cost* % *of Transaction* Volume*A* chart showing miners revenue as *percentage of* the *transaction* volume. |
| hash-rate                        | Hash rate is **a measure of the total computational power being used by a proof-of-work cryptocurrency network to process transactions in a blockchain**. It can also be a measure of how fast a cryptocurrency miner's machines complete these computations. |
| n-transactions-excluding-popular | The total number of *transactions excluding* those involving the network's 100 most *popular*addresses. |
| difficulty                       | A relative measure of how difficult it is to mine a new block for the blockchain. |
| mempool-size                     | The aggregate size in bytes of transactions waiting to be confirmed. |
| output-volume                    | The total value of all transaction *outputs* per day. This includes coins returned to the sender as change. |
| fees-usd-per-transaction         | *Fees Per Transaction* (*USD*)Average *transaction fees in USD per transaction*. |
| transaction-fees-usd             | Total Transaction Fees (USD). The total USD value of all transaction fees paid to miners. This does not include coinbase block rewards. |
| n-unique-addresses               | The total number of *unique addresses* used on the *blockchain*. |
| mempool-count                    | The *mempool* is where all the valid transactions wait to be confirmed by the *Bitcoin* network. |
| transactions-per-second          | Transaction Rate Per SecondThe number of transactions added to the mempool per second. |
| mempool-growth                   | *Mempool* Size *Growth*The rate at which the *mempool* is *growing* in bytes per second. |
| my-wallet-n-users                | The total number of unique Blockchain.com wallets created.   |
| miners-revenue                   | *Miners Revenue* (USD)Total value in USD of coinbase block rewards and transaction fees paid to miners. |
| n-payments                       | The total number of confirmed payments per day.              |
| estimated-transaction-volume     | *Estimated Transaction* Value (USD)The total *estimated* value in USD of *transactions* on the *blockchain*. |
| n-transactions                   | The total number of transactions on the blockchain.          |
| transaction-fees                 | The total BTC value of all transaction fees paid to miners. This does not include coinbase block rewards. |
| estimated-transaction-volume-usd | *Estimated Transaction* Value (*USD*)The total *estimated* value in *USD* of *transactions* on the *blockchain*. |
| cost-per-transaction             | A chart showing miners revenue divided by the number of transactions. |

> Resource

https://www.blockchain.com/charts/n-transactions



  