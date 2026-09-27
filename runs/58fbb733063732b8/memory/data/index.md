# data

数据层：网络请求与鉴权、本地数据库的建表与版本迁移、预置数据播种、JSON 解析（资源与接口响应层级）、模型类型映射（含 64 位整数与字段单位）、文件系统操作

[上一级](../index.md)

## 子主题

- [files](files/index.md) — 文件系统操作：fileIo 建目录、移动与复制在目标已存在时的行为与幂等写法
- [model](model/index.md) — 模型类型之间的映射：持久化枚举字符串与页面本地类型，大整数 id（源端 Long 或 String 承接）的保精度解析，跨模型数值字段的单位
- [network](network/index.md) — 网络层：服务地址与环境、URL 拼接、拦截器注入的公共请求头、请求体字段、登录凭证来源与失效踢登
- [parsing](parsing/index.md) — JSON 解析：打包资源的字段必填与空值语义，接口响应容器 Bean 的取值层级
- [schema](schema/index.md) — Room 到 relationalStore 的库名、schema 版本、建表语句与升级路径
- [seeding](seeding/index.md) — 预置（种子）数据的播种时机、主键写入与补充插入
