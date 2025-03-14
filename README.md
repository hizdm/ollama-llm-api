# Ollama LLM API Web Frame

基于Tornado与Ollama的大语言模型能力调用框架（A Ollama LLM API Web Frame Based Tornado！）

# [目录]

```shell
.
├── app.py               # 项目入口文件
├── conf                 # 配置文件目录
│ └── global.ini         # 基础配置文件
├── controller           # 控制层
│ ├── base.py            # 控制层基类
│ ├── auth.py            # 认证类
│ ├── chat.py            # LLM对话类
│ ├── embeddings.py      # 编码类
│ ├── generate.py        # LLM生成类
│ ├── prompt.py          # 提示工程类
│ ├── rag.py             # LLM检索增强生成类
│ ├── strategy.py        # LLM调用策略类（todo）
│ ├── chroma.py          # 向量数据库操作类
│ └── home.py            # 默认首页类
├── library              # 基础类库
│ ├── jwt                # JWT验证基类
│ │ └── jwt.py
│ ├── log                # 日志操作基类
│ │ └── loghelper.py
│ ├── mysql              # MySQL操作基类
│ │ └── mysqlhelper.py
│ ├── redis              # Redis操作基类
│ │ └── redishelper.py
│ ├── oracle             # Oracle操作基类
│ │ └── oraclehelper.py
│ ├── neo4j              # Neo4j操作基类（部分）
│ │ └── neo4jhelper.py
│ ├── chromadb           # ChromaDB操作基类
│ │ └── chromahelper.py
│ └── util               # 公共方法工具
│ └── util.py
├── log                  # 日志存放目录
│ └── log.txt
├── model                # 模型层
│ ├── base.py            # 模型基类
│ └── llm.py             # LLM类
├── README.md
├── requirements.txt     # 框架安装包 pip install -r requirements.txt 
├── router               # 路由分发层
│ └── urls.py            # 路由分发文件 
├── static               # 资源层
└── template             # 模板层
 └── 404.html            # 404页面
```

# [准备]

安装依赖包`pip install -r requirements.txt`

# [基础配置]

```shell
# APP基础配置
[app]
port = 8000    # 本项目默认端口
debug = True   # True：开启调试模式

# JWT相关配置
[jwt]
secret = q1w2e3r4t5
expire = 7
algorithm = HS256

# MySQL写库
[mysql_w]
host = 192.168.1.1
port = 3306
db = 
user = 
password = 
charset = utf8

# MySQL读库
[mysql_r]
host = 192.168.1.1
port = 3306
db = 
user = 
password = 
charset = utf8

# Redis
[redis]
host = localhost
port = 6379
db = 0
password = 

# Log
[log]
mode = time
when = D
interval = 1

# LLM
[llm]
host = 192.168.16.8:11434 # Ollama服务

# 大模型能力访问策略
[strategy]
# 间隔x秒访问一次
interval = 5
# 在total_time内能够访问times次
times = 30
total_time = 3600
total_son_time = 86400

# 聊天参数
[chat]
temperature = 0.8
num_keep = 5
num_ctx = 1024

# 内容生成参数
[generate]
temperature = 0.8
num_keep = 5
num_ctx = 1024
```

# [启动]

`python3 app.py --port=自定义端口号（不加默认8000）`

# [接口]

请求地址：`ip:端口号/接口名称`

请求方式：`post`

请求参数：

**Headers**

```
Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MzU2MjgyOTgsImlhdCI6MTczNTAyMzQ5OCwiaXNzIjoidG9ybmFkbyIsInBheWxvYWQiOnsidWlkIjoiZWI1N2I1NzIzZSIsInVuYW1lIjoiIn19.ubA-P8ehTzOftnS0nDqedJgQYAL3mu3sx2pjJzs3E64
```

**Body**

```html
{
  "uid": "用户ID",
  "secret": "用户密码",
  "prompt": "提示工程标识", // 可选
  "model":"gemma2:latest",
  "pid": "项目ID",
  "content": "hello"
}
```



### 1. 接口认证(Auth)

请求地址：`ip:端口号/auth`

请求方式：`post`

请求参数：`json`

```python
{
    "uid": "eb57b5723e",
    "secret": "50296e332969d0fe35dfd5a61c016d25"
}
```

接口返回：`json`

```python
{
    "code": 0,
    "message": "success",
    "data": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3MzU2MjgyOTgsImlhdCI6MTczNTAyMzQ5OCwiaXNzIjoidG9ybmFkbyIsInBheWxvYWQiOnsidWlkIjoiZWI1N2I1NzIzZSIsInVuYW1lIjoiIn19.ubA-P8ehTzOftnS0nDqedJgQYAL3mu3sx2pjJzs3E64"
}
```

```sql
CREATE TABLE `t_consumer` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `consumer_no` char(20) NOT NULL DEFAULT '' COMMENT '厂商编号',
  `consumer_name` char(20) NOT NULL DEFAULT '' COMMENT '厂商名称',
  `password` char(32) NOT NULL DEFAULT '' COMMENT '密码',
  `status` tinyint(3) NOT NULL DEFAULT '1' COMMENT '状态(0:无效, 1:有效)',
  `descriptions` varchar(500) NOT NULL DEFAULT '' COMMENT '备注说明',
  `create_time` int(11) NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int(11) NOT NULL DEFAULT '0' COMMENT '更新时间',
  `last_login_time` int(11) NOT NULL DEFAULT '0' COMMENT '最后登录时间',
  `last_logout_time` int(11) NOT NULL DEFAULT '0' COMMENT '最后登出时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `consumer_no` (`consumer_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='厂商接入表'
```

### 2. 大语言模型生成(Generate)

请求地址：`ip:端口号/generate`

请求方式：`post`

请求参数：`json`

```python
{
    "model":"qwen2.5-coder:14b",
    "stream": 0,
    "content": "hello"
}
```

接口返回：`json`

```python
{
     "code": 0,
     "message": "success",
     "data": "Hello! How can I assist you today?"
}
```

### 3. 大语言模型对话(Chat)

请求地址：`ip:端口号/chat`

请求方式：`post`

请求参数：`json`

```python
{
    "model":"qwen2.5-coder:14b",
    "is_stream": 0,
    "content": "hello"
}
```

接口返回：`json`

```python
{
      "code": 0,
      "message": "success",
      "data": "Hello! How can I assist you today? Feel free to ask any questions or let me if there 's anything specific you'd like help with."
}
```

### 4. 大语言模型向量化(Embedding)

请求地址：`ip:端口号/embeddings`

请求方式：`post`

请求参数：`json`

```python
{
    "model": "nomic-embed-text:latest",
    "content": "hello"
}
```

接口返回：`json`

```python
{"code": 0, "message": "success", "data": [["embedding", [0.4177246689796448, -0.13325326144695282, -4.122463703155518,
-0.32404303550720215, 0.80072021484375, 1.052087426185608, 0.29077091813087463, -0.06169068068265915,
-0.34643927216529846, -0.921196699142456, -0.21998178958892822, 1.2134253978729248, 1.3571751117706299,
1.3454275131225586, 1.0591459274291992, -1.259490966796875, 0.6774221658706665, -1.1086382865905762,
-0.9199817180633545, 0.6317816972732544, 0.22389008104801178, -1.5680041313171387, 0.11692361533641815,
-0.13756756484508514, 4.04655647277832, -0.10167273879051208, 0.4419674277305603, 1.9607921838760376,
0.03586838021874428, -0.5319384932518005, 0.47573745250701904, -0.4382959306240082, 0.3607851564884186,
0.07212815433740616, 0.6450861692428589, -0.4413173794746399, -0.09516683220863342, 0.2642088532447815,
0.385660856962204, 0.4501361548900604, -0.4141048789024353, -0.2295873910188675, 0.21838536858558655,
-0.6659966707229614, 1.2068297863006592, 0.17145293951034546, -0.5173124670982361, 0.3172549307346344,
1.2591221332550049, -1.022400975227356, -0.09571494162082672, -0.09888774901628494, -0.5202874541282654,
0.9945341348648071, 0.7864720821380615, 1.2888339757919312, 1.3589282035827637, 0.47779810428619385, 0.5150671601295471,
0.6043456792831421, 0.8914076089859009, 1.1133886575698853, 0.4527231752872467, 1.654554843902588, -0.05691621080040932,
-0.74994957447052, -0.2547203600406647, 0.8894925117492676, 1.1139535903930664, -0.09660613536834717, 1.689900517463684,
0.06349998712539673, 0.44432780146598816, -0.056753404438495636, 0.35097068548202515, 0.48431092500686646,
0.13852344453334808, -0.6776961088180542, -0.5865663290023804, -0.8880387544631958, 0.7099635004997253,
-1.445121169090271, 1.72169828414917, -1.3487513065338135, 0.3838651478290558, -0.7357455492019653,
-0.43988674879074097, -0.006518019363284111, -1.223907470703125, 0.15967343747615814, 1.1620436906814575,
0.14857566356658936, -0.274158239364624, 0.8765993714332581, -0.90379798412323, 0.1396045982837677, -0.7423909306526184,
0.010721374303102493, -1.216160535812378, -1.3165944814682007, -0.13420628011226654, 0.455128014087677,
-0.10749001055955887, 0.20468910038471222, 1.352968692779541, 1.010650873184204, -0.867705225944519,
-0.9001132249832153, -0.8851782083511353, -0.7181078195571899, -1.2638813257217407, 0.5576611757278442,
-0.28379562497138977, 0.10749446600675583, 0.013367561623454094, 0.11005605012178421, 0.9258909225463867,
-2.2393555641174316, 0.9527855515480042, 0.9036204814910889, -1.6794118881225586, 0.2474585622549057,
0.11674825847148895, 0.9352896809577942, 0.6184035539627075, 1.1599135398864746, -2.1230154037475586,
-0.3540322184562683, -0.10469437390565872, 0.2480550855398178, 0.15893329679965973, -0.8110037446022034,
-0.2226528376340866, -0.8005982637405396, 0.8146076202392578, 0.2299482822418213, -0.951104998588562,
-0.5091917514801025, 0.8661842346191406, 0.22916805744171143, 0.4803885817527771, 0.43317973613739014,
0.5462969541549683, -1.1629939079284668, -0.8376170992851257, -0.7156546711921692, 1.7647128105163574,
-1.1347261667251587, 0.4077656865119934, -0.16891783475875854, 0.33510372042655945, 0.9268081188201904,
0.5135332345962524, 0.09149084985256195, 0.6225268840789795, -0.39596468210220337, -0.29748624563217163,
0.011882703751325607, 0.9096624851226807, -0.7254464030265808, 0.25389736890792847, -0.7726792097091675,
-1.1168138980865479, 0.18003901839256287, -0.21048423647880554, -1.3698508739471436, 0.0406387522816658,
0.9716694355010986, 1.0779428482055664, 0.943698525428772, -0.30214715003967285, -1.0829890966415405,
-0.2557104229927063, -0.06546428799629211, -0.07191452383995056, 0.10158441960811615, -0.1936158835887909,
-1.4992573261260986, 0.5837054252624512, -0.2765963077545166, 0.465243935585022, -1.3628677129745483,
0.6706970930099487, 0.7320171594619751, -0.8951674699783325, -0.49164968729019165, 0.06334692239761353,
0.2949768304824829, -0.36170271039009094, -0.6227151155471802, -0.7368403673171997, 0.16272394359111786,
-1.3821667432785034, -0.8866837620735168, -0.2608051598072052, -0.40328264236450195, 0.6148175001144409,
0.38774093985557556, 1.3053276538848877, -0.7184016704559326, -1.19380784034729, -0.28450679779052734,
-0.0971066802740097, 0.040306586772203445, 0.35346460342407227, 2.2812891006469727, 0.6865811347961426,
0.6672511100769043, 0.807096004486084, 0.4420804977416992, 2.0062215328216553, -1.4481256008148193, -0.8031497001647949,
-0.4520108103752136, -0.0748397707939148, 0.04515592008829117, 0.6548863053321838, -0.6945332884788513,
0.0520571693778038, 0.5851107835769653, 0.5888630151748657, -0.9577502012252808, 0.49787646532058716,
-0.23262986540794373, 1.0939202308654785, -0.5503659248352051, -0.33702459931373596, 0.0004832856357097626,
-1.7156081199645996, 0.4574683606624603, -1.3114500045776367, -1.1788594722747803, 0.7254166603088379,
0.48035770654678345, -0.1684725284576416, 0.5156183242797852, 1.063166618347168, 1.5116409063339233,
-0.18988633155822754, -0.6422422528266907, -0.7048389911651611, 1.1243482828140259, 0.9561952352523804,
0.11428980529308319, -1.5576024055480957, 0.5940040349960327, -0.4113195538520813, 0.17836883664131165,
0.12844568490982056, 0.11620347946882248, -0.44129499793052673, -0.2165653556585312, -0.8100118637084961,
0.7420567274093628, 0.7978862524032593, -0.9989995956420898, -0.8674666881561279, 0.5748886466026306,
-0.5698719620704651, -1.0370421409606934, 0.6231722831726074, -2.1915342807769775, 0.42848271131515503,
-1.4179952144622803, -1.19602370262146, 0.40725046396255493, -1.1366488933563232, 0.19790689647197723,
1.0187153816223145, -0.7996505498886108, 0.033810265362262726, 0.3111758828163147, 0.36167478561401367,
0.8219051361083984, -0.7321966290473938, -0.00483144074678421, 0.1294994354248047, 0.4728536903858185,
-0.9696071743965149, -0.2180565446615219, -0.4274121820926666, -1.0144203901290894, -1.3923964500427246,
-0.626604437828064, 0.12071588635444641, 1.0566015243530273, 0.5372341275215149, 0.6965490579605103,
-0.23122619092464447, 0.2705659866333008, 0.5678843259811401, 0.30992424488067627, 0.6359207630157471,
1.5365313291549683, -0.61556476354599, 0.06308899819850922, 0.6636948585510254, 0.42357686161994934,
-0.8969253301620483, -0.3039291799068451, -0.528114914894104, 1.0905534029006958, 1.2822842597961426,
-0.8086476922035217, -0.07762021571397781, 0.1058209240436554, 0.7164251804351807, -0.5419406890869141,
1.332825779914856, 0.4371476471424103, -1.663109540939331, 0.8950622081756592, -1.529535174369812, -0.16176006197929382,
-0.9325605630874634, 0.6092790365219116, -0.21119555830955505, 0.8389074206352234, 1.7634391784667969,
1.0934202671051025, -0.49916011095046997, -1.1485077142715454, -0.14208953082561493, -1.1625332832336426,
0.3841014504432678, 0.48025378584861755, 0.6136027574539185, 1.4422794580459595, 0.7997428774833679,
-0.6367535591125488, 0.5632121562957764, 0.2720657289028168, -1.136037826538086, -0.6382749676704407,
-0.6662725210189819, 0.8603644371032715, 0.25182825326919556, -0.12355376780033112, -0.6194515228271484,
1.735809087753296, 0.5092204213142395, -0.5784528255462646, 0.5669412612915039, -0.47601404786109924,
-0.5670076608657837, -0.908171534538269, -0.4016379117965698, 0.06113908439874649, -0.6168662905693054,
-0.25078555941581726, -0.4333025813102722, 1.1025480031967163, -0.7335144281387329, 0.6490698456764221,
0.3187607526779175, -0.0069856662303209305, 0.7585229277610779, 0.9260412454605103, 0.3208552300930023,
-0.6142023205757141, -0.12217321246862411, -0.2861784100532532, 0.8342176675796509, -0.14662384986877441,
-0.9187445044517517, 0.6739925146102905, 0.33324846625328064, 0.202062726020813, 0.8076725602149963, 0.3048321604728699,
-1.038994550704956, -0.5482060313224792, -0.1634521186351776, 0.8155890703201294, 0.9125843048095703,
0.36597543954849243, -1.9764375686645508, -0.908653199672699, 0.33503666520118713, 0.1778860092163086,
-0.3101433515548706, -0.25972920656204224, 0.9589694738388062, -0.8992874622344971, 0.9368440508842468,
1.133148193359375, 0.9020882844924927, 0.057410139590501785, 0.10150682181119919, 0.21071571111679077,
-0.03353015333414078, -0.03421273082494736, -0.35798853635787964, 0.36099863052368164, -0.27952009439468384,
-0.053899068385362625, 1.063576102256775, 0.28343573212623596, -0.5282092690467834, -0.1112862229347229,
-0.6983050107955933, 0.05266726016998291, 0.2413758933544159, -1.89854896068573, 0.1550675928592682,
0.32042479515075684, -0.7518885731697083, -0.6511745452880859, -0.05880007892847061, -0.664555013179779,
1.3126881122589111, 0.0390452966094017, 0.346741646528244, -1.0260971784591675, -0.09962011873722076,
0.3449612855911255, 1.0314639806747437, -0.9759234189987183, -0.7001016139984131, 0.4522054195404053,
1.0740923881530762, 1.1879873275756836, 0.6109992265701294, 0.033369600772857666, -0.3101652264595032,
1.8177062273025513, 0.4694279432296753, 1.0182974338531494, 0.4775978922843933, -1.5102739334106445,
-0.1676819622516632, 0.08044534176588058, 0.9270672798156738, 0.680352509021759, -0.7816929221153259,
-0.6825438737869263, 0.36288750171661377, -0.37748873233795166, 0.24157080054283142, 0.53595370054245,
1.3547632694244385, -0.5799009203910828, -1.7390347719192505, 0.052469950169324875, 0.7102916836738586,
2.7588768005371094, 2.3308424949645996, -0.8310858011245728, -1.507584810256958, -0.3681079149246216, 0.313771516084671,
0.4946560859680176, 0.4319736361503601, 0.15734554827213287, 1.9341850280761719, -1.3951542377471924,
1.0541033744812012, -0.13599102199077606, 0.23692332208156586, 0.6958023905754089, 0.7351124286651611,
0.5303710699081421, -0.384688138961792, 0.02848595194518566, -0.10237128287553787, -1.2322086095809937,
0.2644656300544739, -0.19056767225265503, 0.07920783758163452, 0.8369110822677612, -1.4134794473648071,
-0.7642820477485657, 0.3491225838661194, -0.6584544777870178, -0.9320321083068848, 0.4893595278263092,
0.21772289276123047, -0.4165966808795929, 0.08207813650369644, 0.8468722701072693, 0.2535897493362427,
0.26749882102012634, -1.5645753145217896, -0.4681969881057739, 0.36891043186187744, 1.1299347877502441,
-0.012978751212358475, 0.7290095090866089, 0.286776065826416, 0.4998883306980133, 0.6146937608718872,
0.15113748610019684, 0.6548582315444946, 0.27922701835632324, -0.15269088745117188, -0.24548815190792084,
-1.4591946601867676, 0.8474768996238708, -0.6048011779785156, -0.386991947889328, 0.12003758549690247,
0.2764210104942322, -0.20838679373264313, 0.5610456466674805, 0.14165249466896057, 0.11918243765830994,
0.683102011680603, -1.8131628036499023, -0.457584023475647, 0.14004673063755035, -0.25036025047302246,
0.25346410274505615, -0.14485806226730347, 0.9109225869178772, 1.4933239221572876, -0.9866718053817749,
0.7447571754455566, -0.40553802251815796, -1.0357095003128052, 1.757613182067871, -0.11095479130744934,
-1.5563955307006836, 0.05807304382324219, 0.33618593215942383, -1.906266212463379, 1.3632320165634155,
-0.23243525624275208, -0.24587959051132202, 1.0148530006408691, 0.3540225923061371, -0.02256004512310028,
0.039047971367836, -0.5570934414863586, -1.2201730012893677, -0.028178848326206207, -0.2175186574459076,
-0.4656018316745758, 0.8590382933616638, 0.10969293862581253, 0.22518938779830933, -1.28903329372406,
0.49389883875846863, -0.10572419315576553, -0.4123743772506714, 0.935005784034729, 0.794722318649292,
-0.7928248047828674, -0.2783527672290802, 0.587145984172821, -0.08752238750457764, -0.5441970825195312,
-1.329467535018921, -0.10199165344238281, -0.9771257638931274, -0.9616992473602295, -1.7170863151550293,
-0.3764774203300476, 0.25765419006347656, -0.633002758026123, -1.2584757804870605, 1.772308588027954, 0.663449764251709,
-0.0004904046654701233, -0.18924546241760254, 0.7640331983566284, -0.4336100220680237, 0.1494646817445755,
-0.8317335844039917, -0.06475399434566498, -0.5100842118263245, -0.38133493065834045, -1.3099725246429443,
1.1995413303375244, -0.9658960700035095, -0.03682757914066315, 0.39938491582870483, 0.7384294867515564,
-0.06486857682466507, -1.7432336807250977, -0.6020278930664062, -0.10911718755960464, -0.3303265869617462,
-0.5588316321372986, 1.2618467807769775, -0.2291782796382904, 0.4626249372959137, 0.06216838210821152,
-1.225090742111206, 1.2725250720977783, -0.40052640438079834, -0.15469351410865784, 0.079623743891716,
0.7213783860206604, -0.622144877910614, -0.41161221265792847, 1.47829270362854, -0.25473934412002563,
-1.4470165967941284, -0.4404633045196533, -0.3744121193885803, -0.6841357350349426, 0.05531812459230423,
1.4527103900909424, -1.0533907413482666, -0.23920050263404846, 1.7962260246276855, 0.8860530853271484,
1.043647289276123, 0.14960679411888123, -0.14977005124092102, 1.4646860361099243, 0.8172522783279419,
-0.7132530212402344, 0.38354772329330444, 1.093090534210205, -0.36137616634368896, -0.3386450409889221,
-0.3144609332084656, 0.37381798028945923, -1.084084391593933, -0.7714964151382446, -0.6136724948883057,
1.093865156173706, 0.2397141009569168, 0.595959484577179, -0.5801156759262085, -0.9538086652755737, -1.013102412223816,
-0.7866687774658203, 1.2225899696350098, 0.5394245386123657, -1.012178659439087, -2.2485129833221436,
-0.33004868030548096, 0.07256774604320526, 0.6301918029785156, 0.7879634499549866, 0.10561492294073105,
0.06508972495794296, 0.8183872103691101, 2.3065738677978516, -0.2808349132537842, 0.7081736326217651,
0.26950931549072266, 1.1290979385375977, -0.46610453724861145, 0.6364613771438599, 0.47768181562423706,
0.9036747217178345, 0.23606708645820618, 1.4109148979187012, 0.9326632618904114, 0.5789893865585327, 0.5080506205558777,
-0.07264839112758636, -0.5658066868782043, 0.4277423620223999, -0.4146958589553833, -2.0495457649230957,
0.5300242900848389, -0.5674393177032471, 0.38476240634918213, -2.1308674812316895, -1.5941693782806396,
0.979069709777832, -0.29471439123153687, -0.30929747223854065, 0.7076057195663452, -1.685978889465332,
-0.12799569964408875, -0.2614041864871979, -0.6632020473480225, -0.3441908359527588, -0.922184944152832,
-1.364058017730713, 1.226973056793213, 1.1589255332946777, 0.3907186686992645, 0.9529649019241333, -0.17001774907112122,
-0.27815720438957214, -0.33683285117149353, -0.2540264129638672, 1.0839701890945435, 0.7255538702011108,
-1.6163445711135864, 1.3923522233963013, 0.0492769330739975, -1.1751476526260376, -2.00050950050354,
-0.07424799352884293, -1.251451849937439, -0.21819990873336792, -0.07387411594390869, -0.8538421392440796,
-0.03302979841828346, -0.48128074407577515, 0.6580181121826172, -0.7524355053901672, 1.215439796447754,
-1.370696783065796, -0.2487758994102478, 0.12109863758087158, 0.5291311740875244, -0.33881574869155884,
-0.3212284445762634, -0.09762484580278397, 0.8126620054244995, -0.9693195819854736, -0.01079326868057251,
-0.28184446692466736, 1.1014677286148071, 0.22874116897583008, 1.3950245380401611, 0.2506973147392273,
0.111285001039505, -0.8977347016334534, -0.06774626672267914, -0.1823837161064148, 1.454819679260254, 2.012608051300049,
0.41962730884552, -1.2010846138000488, -0.5230493545532227, -0.8501806259155273, 0.01266465149819851,
0.5372905731201172, -0.6997848749160767, 0.1512237787246704, -0.8147101402282715, -0.3123737573623657,
-0.4330131709575653, -1.407504916191101, 1.0747170448303223, -0.39280593395233154, 0.17208541929721832,
-0.009660644456744194, -1.7791235446929932, -0.24436843395233154, -0.27289074659347534, -1.0749565362930298,
-1.6633203029632568, -0.04109370708465576, 2.1240437030792236, -0.022999614477157593, -1.086424708366394,
0.7191278338432312, 0.7635329961776733, -0.5008650422096252, -0.16694100201129913, 0.6944338083267212,
-0.11048552393913269, -0.383224219083786, -0.36161014437675476, 0.6681673526763916, 0.28039100766181946,
-0.1730455905199051, 1.0773851871490479, 1.3552210330963135, -0.7194526195526123, 1.1428495645523071,
-0.238936185836792, 0.3701133728027344, 0.6236987709999084, 0.04964395612478256, -0.3325982689857483,
-1.8059077262878418, -0.4663667678833008]]]}
```

### 5. 大语言模型提示工程(Prompt)

请求地址：`ip:端口号/prompt`

请求方式：`post`

请求参数：`json`

```python

内部调用，未封装外部调用，可根据实际情况进行调整
```

接口返回：`json`

```python
内部调用，未封装外部调用，可根据实际情况进行调整
```

### 6. 大语言模型检索增强生成(RAG)

请求地址：`ip:端口号/rag`

请求方式：`post`

请求参数：`json`

```python
{
    "collection": "text2sql-001",                 # 向量数据库集合名称
    "generate_model": "codegemma:7b",             # 生成类大语言模型
    "embedding_model": "nomic-embed-text:latest", # 编码类大语言模型
    "number": 3,                                  # 检索数量（默认1）
    "content": "生成获取用户小明的手机号以及邮箱的sql"  # 问题
}
```

接口返回：`json`

```python
{
    "code": 0, 
    "message": "success",
    "data": "SELECT mobile, email FROM t_user WHERE user_name = '小明';"
}
```

```sql
// 向量数据库存储内容
CREATE TABLE `t_user` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `user_no` char(20) NOT NULL DEFAULT '' COMMENT '员工编号',
  `user_name` char(20) NOT NULL DEFAULT '' COMMENT '员工姓名',
  `department_id` int(10) unsigned NOT NULL DEFAULT 0 COMMENT '科室ID',
  `mobile` char(16) NOT NULL DEFAULT '' COMMENT '手机号',
  `email` char(40) NOT NULL DEFAULT '' COMMENT '邮箱',
  `photo` char(100) NOT NULL DEFAULT '' COMMENT '头像',
  `right_id` int(10) unsigned NOT NULL DEFAULT 0 COMMENT '权限ID',
  `title_id` int(10) unsigned NOT NULL DEFAULT 0 COMMENT '职称ID',
  `duty_id` int(10) unsigned NOT NULL DEFAULT 0 COMMENT '职务ID',
  `password` char(32) NOT NULL DEFAULT '' COMMENT '密码',
  `salt` char(8) NOT NULL DEFAULT '' COMMENT '盐',
  `sex` tinyint(3) NOT NULL DEFAULT 1 COMMENT '性别(1:未知, 2:男, 3:女)',
  `status` tinyint(3) NOT NULL DEFAULT 1 COMMENT '状态(0:无效, 1:有效)',
  `descriptions` varchar(500) NOT NULL DEFAULT '' COMMENT '备注说明',
  `create_time` int(11) NOT NULL DEFAULT 0 COMMENT '创建时间',
  `update_time` int(11) NOT NULL DEFAULT 0 COMMENT '更新时间',
  `last_login_time` int(11) NOT NULL DEFAULT 0 COMMENT '最后登录时间',
  `last_logout_time` int(11) NOT NULL DEFAULT 0 COMMENT '最后登出时间',
  PRIMARY KEY (`id`),
  UNIQUE(`user_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户表';
```

### 7. 创建向量数据库集合

请求地址：`ip:端口号/createcollection`

请求方式：`post`

请求参数：`json`

```python
{
  "collection": "test-001" # 集合名称
}
```

接口返回：`json`

```python
{
	"code": 0,
	"message": "Collection 'test-001' create success.",
	"data": []
}
```

### 8. 删除向量数据库集合

请求地址：`ip:端口号/deletecollection`

请求方式：`post`

请求参数：`json`

```python
{
  "collection": "test-001" # 集合名称
}
```

接口返回：`json`

```python
{
	"code": 0,
	"message": "Collection 'test-001' delete success.",
	"data": []
}
```

### 9. 向量数据库添加文档

请求地址：`ip:端口号/adddocument`

请求方式：`post`

请求参数：`json`

```python
{
  "collection": "test-001",     # 集合名称
  "ids": ["001", "002", "003"], # 文档ID
  "model": "nomic-embed-text:latest" # 向量模型（默认：nomic-embed-text:latest）
  "documents": ["xiaoming documents", "xiaohong documents", "xiaoqiang documents"], # 文档数据
  "metadatas": [{"source": "001.txt"}, {"source": "002.txt"}, {"source": "003.txt"}] # 文档元数据
}
```

接口返回：`json`

```python
{
	"code": 0,
	"message": "Added 3 documents to 'test-001'.",
	"data": [3]
}
```

### 10. 向量数据库查询

请求地址：`ip:端口号/querydocument`

请求方式：`post`

请求参数：`json`

```python
{
  "collection": "test-001",     # 集合名称
  "model": "nomic-embed-text:latest", # 向量模型（默认：nomic-embed-text:latest）
  "number": 3,    # 查询数量（默认：5）
  "query": "hong" # 查询内容
}
```

接口返回：`json`

```python
{
	"code": 0,
	"message": "success",
	"data": {
		"ids": [
			["002", "003", "001"]
		],
		"embeddings": null,
		"documents": [
			["xiaohong
				documents ", "
				xiaoqiang documents ", "
				xiaoming documents "]], "
				uris ": null, "
				data ": null, "
				metadatas ": [[{"
				source ":
				"002.txt"
			}, {
				"source": "003.txt"
			}, {
				"source": "001.txt"
			}
		]],
	"distances": [
		[538.5186078395823, 555.5955598005668,
			593.4459312118717
		]
	],
	"included": ["distances", "documents", "metadatas"]
}
}
```
