# 迁移源端异步结果回调时，按成功、失败分支（含失败类型）列出全部副作用（跳转与关页、提示、引导弹窗、标记写入），计划与代码逐项对上

ID：`lesson-ac7a2e17b8d88c3cee7b` · 版本：6

[本主题](index.md)

## 何时使用

界面、流程实现与页面接线阶段，把源页面对异步操作结果的观察（LiveData observe 等）改成目标页面的 await 结果、try/catch 或路由枚举，并决定各分支的跳转、反馈与状态写入时；把源端控制器的多段启动流程（登录 → 权限 → 启动）接到宿主页时；修补某个结果分支的文案或常量时；把源端“需登录才能继续”的操作回调迁成目标登录拦截时

## 适用情境

源 Activity/Fragment 在结果观察回调里按成功/失败分支同时做几件事（写本地标记、跳页并 finish、showToast、更新计数）；目标 ViewModel 方法只更新状态，或把失败折叠成返回值，由页面决定导航和提示；页面里可能留有“登录成功跳 X”的注释或 TODO。也包括源端按失败类型给不同反馈（权限被拒弹“去设置”引导框，启动失败才 toast），目标 ViewModel 方法只返回 boolean、失败类型另存；接线任务的核查清单只列出部分弹窗调用（如 MessageDialog.show），用 AlertDialog.Builder 构造的弹窗不在清单里。也包括源端回调先按信封成功分流、成功分支内再按 data 是否含某键分流，错误码从 data 层读取并位于成功分支的 else 中，而目标把同名错误码判断放在成功分支之外。 也包括源端登录拦截带结果回调：未登录时拉起登录，登录成功后继续原操作（如应用用户所点的选项），失败或取消才中止；目标现成的登录守卫只负责跳转并返回 false，没有成功回调。

## 原因

分支动作在转述计划、改写异步调用时最容易被概括成“失败留页”“调用登录”这样一句话，其余副作用随之丢掉；只接上调用、不处理结果时，编译和页面显示都正常，点完没有去向或失败没有提示。来源两例：启动链路迁移者读过源端失败分支的 showToast，自己的梳理里也写着“失败 → toast”，到计划只剩导航，代码照计划漏了提示；页面接线者读到 TODO 和“登录成功跳主页”的注释，只接上登录调用，不等结果、不跳转，还删了 TODO。反方向也会出错：另一应用的首页计数请求失败时被置 0，而源端只在成功回调里更新计数，失败时保留原值。另一应用中，添加城市的接线者读到定位成功跳主页、重复添加弹 Toast，输出仍停在本页、失败无提示；定位入口只写了成功分支，拒绝授权与服务关闭都静默。另一应用的接线者读到了源端权限拒绝的引导弹窗与目标 ViewModel 记录的失败类型，仍把所有启动失败统一为一个 toast；清单里没有 AlertDialog.Builder 构造的引导框，预检结论就已漏掉该分支。另一应用的复核者已读到源端完整的分支结构，修补上限提示文案时仍沿用目标里错位的错误码判断，只补了文案；真实的上限响应落入成功分支直接重启心跳，弹窗不可达。另一应用的生成者写前读到并多次复述“登录成功后才应用所点指标”，却因目标登录守卫没有成功回调、上一任务用的是中止模式，只写了“跳登录并中止”，注释仍称对齐源端回调，完成报告也未说明省略了成功分支。

## 做法

1. 从源端的结果观察者（如 initObserve 里对 xxxFinished 的处理）按分支列出全部动作：跳转与关页、toast/弹窗、标记写入、状态更新；计划和代码逐项对照，不把分支简化成只导航或只留页，也不给源端没有动作的分支添加清零、默认值覆盖。
2. 让页面拿到结果：await ViewModel 返回的成败，或监听对应状态；ViewModel 吞掉异常时把失败结果返回页面，由页面负责提示。
3. 源失败分支有 showToast 时，在目标对应的失败处调用 UIContext.getPromptAction().showToast，文案取源字符串资源的对应值；源端只在成功时更新的计数或状态，失败时保留旧值，需要可见性时另设失败/重试状态。
4. 转写源注释（如“失败留在当前页，用户可重试”）后，核对注释之后的源语句是否都已落地；可 grep 源页面与目标页面的 showToast 和跳转调用，逐一核对数量与分支。
5. 目标方法以 boolean 返回、失败类型另存时，宿主按类型分派失败 UI：权限被拒显示“去设置”引导弹窗，确认后用 startAbility 打开系统设置中本应用的详情页（参数带当前 bundleName），其他失败保留原提示。
6. 核查清单由抽取器生成时，在源文件补查 AlertDialog.Builder、Settings.ACTION_APPLICATION_DETAILS_SETTINGS 等调用，补齐清单外的弹窗分支。
7. 修补回调中任一分支的文案或常量前，先写出源端到达该分支的完整判别路径（信封成功 → data 键是否存在 → data 层错误码），与目标逐层对照；层级或判别键不同就一并修正，不只替换字符串。
8. 源端登录拦截在成功分支续做原操作、而目标登录守卫没有成功回调时，在拦截处暂存待执行动作（类型与参数），在页面重新可见（如 NavDestination.onShown）或登录态广播时一次性消费：已登录则刷新权限后执行，仍未登录则丢弃；先检索并复用工程已有的登录回流实现。注释写“对齐源端”前核对是否覆盖回调全部分支，有意简化时向用户说明省略了哪一步。

来源支持：8 张卡 · 6 次迁移 · 6 个应用

## 来源（按需复核）

- [case-3eb3514a903386524e37](../../../store/cases/case-3eb3514a903386524e37/1236f09edef125248d0e00d310ba34a2b80cc47b92e7ad721d0a7a13a4f89aa6.json) · 结论：recommendation:5
  卡片版本：`1236f09edef125248d0e00d310ba34a2b80cc47b92e7ad721d0a7a13a4f89aa6`
- [case-5b91aeeca2e493368af0](../../../store/cases/case-5b91aeeca2e493368af0/aa54f204a016acd3439a94d5a9cb4dfb52ccbcb0c6243e2813b4e1604e6dfe92.json) · 结论：diagnosis, recommendation:1
  卡片版本：`aa54f204a016acd3439a94d5a9cb4dfb52ccbcb0c6243e2813b4e1604e6dfe92`
- [case-766f31f27e3feb426eb4](../../../store/cases/case-766f31f27e3feb426eb4/063edaee6e569759de04205fb992c40c13efa6f80b313fae8049fe972318d4c4.json) · 结论：recommendation:4
  卡片版本：`063edaee6e569759de04205fb992c40c13efa6f80b313fae8049fe972318d4c4`
- [case-845435c8343c4c012e1f](../../../store/cases/case-845435c8343c4c012e1f/68ab16b9112c85d3355a0548d963fe9e347178c301269162dfa692892d0551b5.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`68ab16b9112c85d3355a0548d963fe9e347178c301269162dfa692892d0551b5`
- [case-8c249997059a2524ea7b](../../../store/cases/case-8c249997059a2524ea7b/921750461c1e7e278c419ca26c21b17048d692c94b180c54164c66f94aafa6e6.json) · 结论：recommendation:4
  卡片版本：`921750461c1e7e278c419ca26c21b17048d692c94b180c54164c66f94aafa6e6`
- [case-9618601c4a21f2f18560](../../../store/cases/case-9618601c4a21f2f18560/870a2d98075a73dc88a2cfd3ac2fb801bc3d216cf1120c6f9583496d9f1c6941.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`870a2d98075a73dc88a2cfd3ac2fb801bc3d216cf1120c6f9583496d9f1c6941`
- [case-dac1fda1c66cbfa8bc78](../../../store/cases/case-dac1fda1c66cbfa8bc78/ab39f6b4fbefd2e63757c8197e2298157f2bd77d5bb063c598f2afdc61bcab08.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`ab39f6b4fbefd2e63757c8197e2298157f2bd77d5bb063c598f2afdc61bcab08`
- [case-ecc5fcef18e883a4724e](../../../store/cases/case-ecc5fcef18e883a4724e/fca1a266ae7b054548e448f790faccf4e71283581a8607219cf2406ae0c73772.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`fca1a266ae7b054548e448f790faccf4e71283581a8607219cf2406ae0c73772`
