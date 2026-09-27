# 迁移源端异步结果回调时，按成功、失败分支列出全部副作用（跳转与关页、提示、标记写入），计划与代码逐项对上

ID：`lesson-ac7a2e17b8d88c3cee7b` · 版本：1

[本主题](index.md)

## 何时使用

界面、流程实现与页面接线阶段，把源页面对异步操作结果的观察（LiveData observe 等）改成目标页面的 await 结果、try/catch 或路由枚举，并决定各分支的跳转与反馈时

## 适用情境

源 Activity 在结果观察回调里按成功/失败分支同时做几件事（写本地标记、跳页并 finish、showToast）；目标 ViewModel 方法只更新状态，或把失败折叠成返回值，由页面决定导航和提示；页面里可能留有“登录成功跳 X”的注释或 TODO。

## 原因

分支动作在转述计划、改写异步调用时最容易被概括成“失败留页”“调用登录”这样一句话，其余副作用随之丢掉；只接上调用、不处理结果时，编译和页面显示都正常，点完没有去向或失败没有提示。来源两例：启动链路迁移者读过源端失败分支的 showToast，自己的梳理里也写着“失败 → toast”，到计划只剩导航，代码照计划漏了提示；页面接线者读到 TODO 和“登录成功跳主页”的注释，只接上登录调用，不等结果、不跳转，还删了 TODO。

## 做法

1. 从源端的结果观察者（如 initObserve 里对 xxxFinished 的处理）按分支列出全部动作：跳转与关页、toast/弹窗、标记写入；计划和代码逐项对照，不把分支简化成只导航或只留页。
2. 让页面拿到结果：await ViewModel 返回的成败，或监听对应状态；ViewModel 吞掉异常时把失败结果返回页面，由页面负责提示。
3. 源失败分支有 showToast 时，在目标对应的失败处调用 UIContext.getPromptAction().showToast，文案取源字符串资源的对应值。
4. 转写源注释（如“失败留在当前页，用户可重试”）后，核对注释之后的源语句是否都已落地；可 grep 源页面与目标页面的 showToast 和跳转调用，逐一核对数量与分支。

## 来源（按需复核）

经验是有适用范围的历史建议。核查来源时同时看结论与 unknown；来源卡未随阅读包复制。

- case-9618601c4a21f2f18560 · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`10793c91445a2decfc9cc9eea42fc503ac20aff67e08a5839155cdcbb7315014`
- case-dac1fda1c66cbfa8bc78 · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`327a69f40b88de436b6e1cc3e5fa25fe0fcde6bb6611ab8792280a580e4cfbd4`
