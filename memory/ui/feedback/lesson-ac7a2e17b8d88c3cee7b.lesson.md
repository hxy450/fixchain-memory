# 迁移源端异步结果回调时，按成功、失败分支（含失败类型）列出全部副作用并逐项落地，每个结果态都有渲染或提示

ID：`lesson-ac7a2e17b8d88c3cee7b` · 版本：9

[本主题](index.md)

## 何时使用

界面、流程实现与页面接线阶段，把源页面对异步操作结果的观察（LiveData observe、回调）改成目标的 await 结果、try/catch 或状态监听，决定各分支的跳转、反馈、状态写入与资源收尾时；替换 TODO 或前向引用、按核查清单接线时

## 适用情境

源 Activity、Fragment 或控制器在结果回调里按成功、失败（及失败类型）分支同时做几件事：写本地标记、跳页并 finish、showToast 或弹窗、更新计数、close 资源；目标 ViewModel 方法只更新状态、吞掉异常或只返回 boolean（失败类型另存），由页面决定导航和提示；页面可能留有“成功跳 X”的注释或 TODO，规格状态接口列出 error 等结果态，核查清单可能由抽取器生成、只列出部分弹窗调用。

## 原因

分支动作在转述计划、改写异步调用或按清单接线时，最容易被概括成“失败留页”“调用登录”这样一句话，其余副作用随之丢掉；只接上调用、不处理结果时，编译和页面显示都正常，点完没有去向、失败没有提示，或定义了结果态却没有分支渲染它。

## 做法

1. 从源端结果观察者（如 initObserve 里对完成事件的处理）按分支列出全部动作：跳转与关页、toast/弹窗、标记写入、状态更新、资源收尾（close、cancel），计划与代码逐项对照并按源顺序落地；规格验收只写用户可见结果时，仍按源码补齐收尾。不把分支简化成只导航或只留页，也不给源端没有动作的分支添加清零或默认值覆盖（区块级的失败保留旧值见 lesson-a82d821385bf8fb3feb0）。
2. 让页面拿到结果：await ViewModel 返回的成败，或监听对应状态；ViewModel 吞掉异常时把失败结果返回页面，由页面负责提示。源失败分支有 showToast 时，在目标对应失败处调用 UIContext.getPromptAction().showToast，文案取源字符串资源的对应值。
3. 状态接口列出的每个结果态（含 error）都在 build 里有渲染分支，每个 catch 写入的状态都有消费它的分支，不同操作不借用同一个状态；确要留给接线阶段时，在占位登记里写明“某态需渲染什么”，不只登记状态回填。
4. 源端按失败类型给不同反馈（如权限被拒弹“去设置”引导框、启动失败才 toast），而目标方法只返回 boolean、类型另存时，宿主读取失败类型分派 UI：权限被拒显示“取消／去设置”引导弹窗，确认后打开系统设置的本应用详情页（Want 带当前应用 bundleName；显式 Want 的包名与参数按 lesson-4bea916d1ff67e51d455 核对），其他失败类型保留原 toast。
5. 以源端回调为清单核对，不以抽取器生成的核查清单为准：在源文件补查 AlertDialog.Builder、Settings.ACTION_APPLICATION_DETAILS_SETTINGS 等清单外的弹窗与跳转；转写源注释（如“失败留在当前页，用户可重试”）后核对注释之后的源语句都已落地，可检索两端的 showToast 与跳转调用逐一对数。

来源支持：8 张卡 · 6 次迁移 · 6 个应用

## 来源（按需复核）

- [case-2f11f734c53d33bee770](../../../store/cases/case-2f11f734c53d33bee770/df8821d7d8f96d34ab58ab850b2ead61a6460456ffb80a548e22d0421a5c0f15.json) · 结论：recommendation:3, recommendation:4
  卡片版本：`df8821d7d8f96d34ab58ab850b2ead61a6460456ffb80a548e22d0421a5c0f15`
- [case-3eb3514a903386524e37](../../../store/cases/case-3eb3514a903386524e37/1236f09edef125248d0e00d310ba34a2b80cc47b92e7ad721d0a7a13a4f89aa6.json) · 结论：recommendation:5
  卡片版本：`1236f09edef125248d0e00d310ba34a2b80cc47b92e7ad721d0a7a13a4f89aa6`
- [case-766f31f27e3feb426eb4](../../../store/cases/case-766f31f27e3feb426eb4/063edaee6e569759de04205fb992c40c13efa6f80b313fae8049fe972318d4c4.json) · 结论：recommendation:4
  卡片版本：`063edaee6e569759de04205fb992c40c13efa6f80b313fae8049fe972318d4c4`
- [case-845435c8343c4c012e1f](../../../store/cases/case-845435c8343c4c012e1f/68ab16b9112c85d3355a0548d963fe9e347178c301269162dfa692892d0551b5.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`68ab16b9112c85d3355a0548d963fe9e347178c301269162dfa692892d0551b5`
- [case-8c249997059a2524ea7b](../../../store/cases/case-8c249997059a2524ea7b/921750461c1e7e278c419ca26c21b17048d692c94b180c54164c66f94aafa6e6.json) · 结论：recommendation:4
  卡片版本：`921750461c1e7e278c419ca26c21b17048d692c94b180c54164c66f94aafa6e6`
- [case-902b42725495e1b86fdd](../../../store/cases/case-902b42725495e1b86fdd/ce0d6a5b9a6bd056dfb7f7eb5cdd44f2e82bf50b645f7c36eb4ac30f0f0ec6d8.json) · 结论：recommendation:3
  卡片版本：`ce0d6a5b9a6bd056dfb7f7eb5cdd44f2e82bf50b645f7c36eb4ac30f0f0ec6d8`
- [case-9618601c4a21f2f18560](../../../store/cases/case-9618601c4a21f2f18560/870a2d98075a73dc88a2cfd3ac2fb801bc3d216cf1120c6f9583496d9f1c6941.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`870a2d98075a73dc88a2cfd3ac2fb801bc3d216cf1120c6f9583496d9f1c6941`
- [case-dac1fda1c66cbfa8bc78](../../../store/cases/case-dac1fda1c66cbfa8bc78/ab39f6b4fbefd2e63757c8197e2298157f2bd77d5bb063c598f2afdc61bcab08.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`ab39f6b4fbefd2e63757c8197e2298157f2bd77d5bb063c598f2afdc61bcab08`
