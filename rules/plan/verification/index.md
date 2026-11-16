# 验证报告与验收结论

交回的验证汇总、视觉校验、阶段报告、差异清单、巡检单、收尾一致性结论里有 PASS、✔、BLOCKED 判定，或者有要真机、截图才能确认的项时

## 触发族

- [临时占位的页面和完成标记](page-placeholder-done/index.md)（2 条）：阶段完成只要求报告文件存在，交回的阶段报告、覆盖清单把正文只写「开发中」或写死样例数据的页面也打了 ✔
- [验证汇总里的交互缺失条目](interaction-missing/index.md)（1 条）：验证子代理报告某页「点击无效」「仅滑动可切」这类 DIFF 条目，修复派工把整页概括成「布局级，不阻塞」，交互缺失没派修
- [收尾一致性结论里的富文本链接](rich-text-links/index.md)（1 条）：源端有多处 HtmlCompat.fromHtml / setMovementMethod(LinkMovementMethod) 调用点，前面环节转述「已页内自渲染解决」，收尾结论凭转述写「通过」
- [没核对过外观的安全控件](security-control-look/index.md)（1 条）：派工要求把自绘外观的按钮改用 SaveButton 等安全控件、又禁止编译或没有真机，交付说明里没有「外观待真机核对」，代码注释却把这套写法定成范式
- [差异清单里「由组件承担」的验收项](component-claimed-items/index.md)（1 条）：规格的性能类验收项有源 ViewModel 的预取方法作锚点，差异清单或最终报告写「无对等低层 API，由页面态 Image 组件缓存承担」，目标文件里没有对应方法和调用，也没有占位
- [因宿主不可达记 BLOCKED 的功能点](blocked-host/index.md)（1 条）：功能点清单里有依赖某个宿主页面才能走到的功能点，验证汇总多轮把它们记 BLOCKED（宿主不可达），没有待补项、负责批次或静态检查结论
- [巡检或评审建议里的加载门](loading-gate-advice/index.md)（1 条）：巡检或评审条目写「设置载入并同步页面状态前阻止交互」「载入完成后才呈现可交互内容」，没写加载失败时页面怎么离开加载态
- [无真机时用显式 Want 打开系统设置](settings-want-device-check/index.md)（1 条）：读到派工禁止编译或没有设备，代码用显式 Want 指定系统设置应用的 bundleName；交付报告或验证清单里没有「打开系统设置需真机确认」，也没有点击后确认设置应用处于前台的检查
- [基线截图没拍到本体的弹层](popup-baseline-unverified/index.md)（1 条）：读到 Android 基线截图没有拍到弹层展开后的本体，view.xml 是合成的、bounds 为空；视觉校验结论按源结构把这个弹层判为 PASS，弹层内卡片几何没有标为未核
- [同会话已记为未接线或 deferred 的 AC 的验证判定](deferred-ac-verdict/index.md)（1 条）：同一会话里已记录某条 AC「未接线」或 deferred（如深色模式未接线）；环境降级时批量写的 impl-claims / verification 仍把它判 pass（静态代理检查），标侧文件不存在或 DarkColors 没有任何消费点
