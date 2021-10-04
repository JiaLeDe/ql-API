## 所有API：
#### 获取值：http://ip:端口/api/envs
#### 更改状态禁用(启动)：http://ip:端口/api/envs/disable   (http://ip:端口/api/envs/enable)
#### 移动顺序http://ip:端口/api/envs/第一步获取到的_id值/move


### 一：获取环境变量的值
##### 1.首先获取token，在ql/config/auto.json中，token的值(现已可自动获取，必须将脚本放到ql/scricp目录下)
##### 2.发送请求的目标url格式：http://ip:端口/api/envs
##### 3.请求头格式：header={'Authorization':'Bearer '+token}，token的值是1中获取到的，可以不使用UA。
##### 4.向url发送get请求，获取到环境变量的值，类型如下：
##### 
	{"code": 200,
	"data": [{
		"value": "pt_key=xxxx; pt_pin=xxxx;",
		"_id": "xxxxx",
		"created": xxxxxxx,
		"status": 1,
		"timestamp": "Wed Sep xx 2021 xx:xx:xx GMT+0800 (中国标准时间)",
		"position": 4999999999.5,
		"name": "xxxxx",
		"remarks": "xxxxxxxx"
	}, {
		"value": "pt_key=xxxx; pt_pin=xxxx;",
		"_id": "xxxxx",
		"created": xxxxxxx,
		"status": 1,
		"timestamp": "Wed Sep xx 2021 xx:xx:xx GMT+0800 (中国标准时间)",
		"position": 4999999999.5,
		"name": "xxxxx",
		"remarks": "xxxxxxxx"
	}]
	}
  ##### 
 
#####   value:环境变量的值
#####   _id:值标识
#####   created：创建时间
#####   status：当前状态（1表示禁用，2表示启用）
#####   timestamp：最后一次更改时间
#####   name：环境变量的名称
#####   remarks：备注


### 二：更改状态
##### 1.发送请求的目标url格式：http://ip:端口/api/envs/disable
##### 2.请求体格式：body = _id   (_id是第一步中获取到的，body的格式一定要是List格式！！！)
##### 3.向目标url发送PUT请求，要特别注意，是PUT请求。
##### 4.启用格式和禁用一样


### 二：添加变量值
##### 1.发送请求的目标url格式：http://ip:端口/api/envs
##### 2.请求体格式如下：   (_id是第一步中获取到的，body的格式一定要是List格式！！！)
#### 
	[{
	    "value": "222",
	    "name": "111",
	    "remarks": "333"
	}]
 ####
##### 3.向目标url发送POST请求,POST请求！！！

### 三：移动顺序
##### 1.url格式：http://ip:端口/api/envs/第一步获取到的_id值/move
##### 2.header不变，body是json格式，如下：
##### 
	{
	    "fromIndex": 遍历第一步中的data时，data数组的下标
	    "toIndex": 想要移动的位置
	}
 #####
##### 3.发送PUT请求！！！！！

## 如果有什么不懂的可以讨论，因为用jd脚本的比较多，所以本人写了个py来检测到期并通知（目前仅添加了企业微信机器人通知，如有需要或者bug可以提案）
