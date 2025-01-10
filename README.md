# Ollama LLM API

A Ollama LLM API Web Frame Based Tornado！

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
# todo
```

接口返回：`json`

```python
# todo
```

### 2. 大语言模型生成(Generate)

请求地址：`ip:端口号/generate`

请求方式：`post`

请求参数：`json`

```python
# todo
```

接口返回：`json`

```python
# todo
```

### 3. 大语言模型对话(Chat)

请求地址：`ip:端口号/chat`

请求方式：`post`

请求参数：`json`

```python
# todo
```

接口返回：`json`

```python
# todo
```

### 4. 大语言模型向量化(Embedding)

请求地址：`ip:端口号/embedding`

请求方式：`post`

请求参数：`json`

```python
# todo
```

接口返回：`json`

```python
# todo
```

### 5. 大语言模型提示工程(Prompt)

请求地址：`ip:端口号/prompt`

请求方式：`post`

请求参数：`json`

```python

# todo
```

接口返回：`json`

```python
# todo
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
