# 新增错误日志沿用工程的 hilog 约定，不写 console.*

## 何时使用

功能实现阶段，在服务层、ViewModel 或页面的 catch 分支里为新增的错误处理选择日志写法时

## 适用情境

源端对失败静默处理或没有日志（如 Kotlin runCatching 吞掉异常），目标 ArkTS 在 catch 中新增错误日志；工程里已有 hilog 写法（TAG、DOMAIN 常量），而生成期规则只约束 build() 内的 console.log 或占位写法。

## 原因

源端没有可映射的日志，生成规则与迁移期静态检查也没有 console.* → hilog 的要求，写码者就按通用 TypeScript 习惯写 console.error，直到 ECAT 静态检查才被检出。来源两个应用都如此：一处写码 agent 批量读 skill 时输出被截断，含 hilog 导入映射的 skill 没进上下文；另一处生成期规则只禁止 console.info('TODO') 这类假实现，返修时才统一改成 hilog。

## 做法

1. 写日志前 rg 工程现有写法（如 import { hilog } from '@kit.PerformanceAnalysisKit' 与 TAG、DOMAIN 常量），照它写 hilog.error(DOMAIN, TAG, '<说明>: %{public}s', String(error))，TAG 取当前类名。
2. 每个切片写完，rg -n 'console\.' 本次改动的 .ets 文件，已登记占位之外的命中都改成 hilog。

来源支持：2 张卡 · 2 次迁移 · 2 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 不涉及。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔原因〕console.error(message: string, ...arguments: any[]) 是 ArkTS 里全局可用的接口（API 7 起），写在 .ets 里编译不报错
- 〔做法第 1 步〕hilog 从 @kit.PerformanceAnalysisKit 导出（import { hilog } from '@kit.PerformanceAnalysisKit'），错误级日志的签名是 hilog.error(domain: number, tag: string, format: string, ...args: any[]): void
- 〔做法第 1 步〕hilog 的格式参数写成 %{private flag}specifier：不写隐私标识时按 private 处理，输出为 <private>；写 public 才明文显示参数
- 〔做法第 1 步〕hilog 格式说明符 s 只支持 string、undefined、bool、null；d/i 支持 number、bigint；o/O 打印 object 自 API 20 起；Error 这类对象要先转成字符串再用 %{public}s
- 〔做法第 1 步〕hilog 的 domain 取值 0x0000–0xFFFF，超出范围不打印；tag 文档写最多 31 字节、超出截断、不建议用中文（声明注释写不超过 32 字节），以文档为准
