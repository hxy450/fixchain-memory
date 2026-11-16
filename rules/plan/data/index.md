# 数据、网络与日志

源端有 Retrofit Service、BuildConfig.BASE_URL、鉴权拦截器、Room Migration、偏好标记，或者台账列了日志边界，计划和契约要写网络层、数据库、偏好接口、日志任务时

## 触发族

- [计划里的网络层任务](network-layer-task/index.md)（1 条）：源工程有 Retrofit Service、BuildConfig.BASE_URL、鉴权拦截器，计划的网络层任务只写「HTTP 请求封装」，规格产物里没有 API 清单
- [系统契约里的偏好接口清单](pref-interface/index.md)（1 条）：行为提取里有由偏好标记控制、显示后写回标记的一次性 UI，系统契约或计划的偏好接口只列了各设置开关的 get/set
- [数据库迁移里建了又改名的 *_new 表](migration-temp-table/index.md)（1 条）：源端 Migration.migrate 里 CREATE TABLE x_new、拷数据、DROP 旧表后 RENAME 回原名，对照或修复工作清单把 x_new 列成目标缺的表
- [台账列出的日志边界](log-boundaries/index.md)（1 条）：决策台账写「Android 日志对应边界统一改用该封装」并列出生命周期、网络、同步等边界，审计结论或整改计划里日志只有库版本、保留天数、等级这类配置条目
- [活性探针和冒烟清单选的接口](smoke-probe-endpoints/index.md)（1 条）：API 规格里有枚举类型的 query 参数或请求字段；放行数据层前的活性探针或冒烟清单只列了站点信息、校验登录这类不带枚举参数的接口
