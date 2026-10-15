# process.getEnvironmentVar 读的是设备进程环境：构建期材料不经它读取，保留的读取统一做空值兜底

ID：`lesson-ef06973d4b7affc03093` · 版本：1

[本主题](index.md)

## 何时使用

实现或修复阶段，用 process.getEnvironmentVar 读取运行配置（成功码、密钥、渠道、客户端身份），或改写其“|| 默认值”回退链时

## 适用情境

目标代码以 process.getEnvironmentVar(X) || 缺省 读取可选运行配置；安装到设备后进程环境通常没有这些变量；准备把缺省改为构建期字段，或改写回退链。

## 原因

getEnvironmentVar 读取的是设备上应用进程的环境变量，不是构建机环境，安装后的包拿不到构建时设置的值；@ohos.process.d.ts 声明返回 string，但已观察到未设置时运行期返回 undefined。按声明删掉空值兜底再读 .length 或做 Number()，响应已收到也会在读配置时崩溃，并常被上层包装成网络失败。

## 做法

1. 构建期才知道的材料（密钥、渠道、客户端身份）经 build-profile.json5 的 buildProfileFields 注入（本地秘密参数由 hvigor parameterFile 引入），代码读生成的 BuildProfile 字段，不经 getEnvironmentVar。
2. 仍保留的环境变量读取收敛到一个返回 string 的安全函数（缺失返回 ''），各配置项都经它读取；改写回退链时不删掉空值兜底，同形配置项按同一写法核对。

来源支持：1 张卡 · 1 次迁移 · 1 个应用

## 来源（按需复核）

- [case-2cb47bb8a097227ee9cf](../../../store/cases/case-2cb47bb8a097227ee9cf/f2b0927a1fad7eab605d73dec0f0cc4e49c1cc7aefc0b1cffbb9682dcb7df6d4.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`f2b0927a1fad7eab605d73dec0f0cc4e49c1cc7aefc0b1cffbb9682dcb7df6d4`
