# data

数据层：网络地址与请求鉴权、序列化解析、模型映射、本地持久化及多阶段数据流程在迁移中的语义保持

[上一级](../../index.md)

## 子主题

- [model](model/index.md) — 持久化枚举、字段单位、关联键、展示字段与查询层派生状态在模型之间映射时的源端语义保持（8 条）
- [network-auth](network-auth/index.md) — 鉴权凭证、会话密钥与拦截器公共参数的获取来源、注入格式、失效判定及其写入侧生产者（5 条）
- [network-endpoint](network-endpoint/index.md) — 服务地址、环境与构建期运行配置的来源与注入，baseUrl 与 path 的拼接，以及网络权限声明（5 条）
- [network-request](network-request/index.md) — POST 请求体的字段来源与表单/JSON 编码选择，以及请求参数与响应加解密的移植与空值、失败回退（4 条）
- [parsing](parsing/index.md) — JSON 与二进制字节流到类型化模型的编解码规则：类型宽窄收窄、空值语义、取值层级与大整数精度（10 条）
- [preferences](preferences/index.md) — 偏好键值存储：装载时机与同步读写、批量提交原子性、读点缺省值与默认值落盘（4 条）
- [storage](storage/index.md) — 本地持久化：relationalStore 建表与版本迁移、自增主键写入、预置数据内容与播种时机、fileIo 目录操作（11 条）
- [sync](sync/index.md) — 同步、扫描等多阶段数据流程的并发触发语义、进度与终态事件发布粒度，以及缓存写入等副作用步骤（6 条）
