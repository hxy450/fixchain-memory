# 新登记占位的必要性和写法

agent 会看到什么：实现或转换时新登记的 UNC / forward-ref-uncertain 占位、待收敛项、交给收口者的 HANDOFF，以及 FWD-REF 和登记里写的源方法名

## 规矩

- rule-a9d7f224ea89｜已知用户可见差异且有可行实现路线时，当场完成，不用 UNC 占位换编译通过；确需延后按账本归属填 resolve_by｜读到：实现者自己已识别出用户可见的行为差异，也想到了可行的实现路线；写错：代码 TODO 挂上 `UNC` 编号的 forward-ref-uncertain 占位，resolve_by 照派工前缀写某个 Slice，而 plans/slices 账本里这一页归别的 Slice；返回报告没列这项降级
- rule-1853e5a37863｜能从源 XML 和位图确定的图片几何量直接落实，不登记或保留为不确定占位｜读到：源 XML 里图片是 wrap_content + adjustViewBounds，位图在源资源里可读；写错：registry 把它登记成 forward-ref-uncertain，文字写「adjustViewBounds→layoutWeight+Contain 等价」这类未验证的「等价」，推给后续阶段
- rule-980e58a3782c｜共享工具未建成而页面先内联格式函数时，登记待收敛并在收口时删页内同名函数｜读到：派工写「公共组件库未完成，同页内联等价实现优先」或「Base 组件未建时以 FWD-REF 或内联等价实现」；写错：页面里内联了和共享工具同名的格式函数，登记里没有指向共享模块的待收敛项；或转换报告把「HALF_UP 近似源 HALF_EVEN」记成已知偏差了事
- rule-9995f854c249｜FWD-REF 和登记里引用的源方法名要读过完整定义，不写拼出来的名字｜读到：源码里要移交的判断或动作调用了某个方法，查的时候 grep 只命中一行分支（如菜单分支里的那一行调用）；写错：`FWD-REF` 说明或登记表（registry）里写的源方法名在源码里不存在（由两个真实方法名拼成），或只写了动作的方法、漏了可见性判断的前置条件
- rule-7736f5eefd5b｜跳转移交给收口者时写 HANDOFF 条目或保留 FWD-REF，不只在报告里写待定｜读到：占位登记表里这个 P-ID 的触发条件包含路由到结果页；源端成功后启动结果页；写错：报告里只写「由 closer 决定是否跳转」，FWD-REF 已删，也没有带 owner / what / verify 的 HANDOFF；或收口者只凭 Store 交接把 P-ID 改成 resolved、勾选了集成点
- rule-1287ed030719｜源码已写明、ArkUI 能直接实现的行为不登记 forward-ref-uncertain，按源码实现｜读到：页面规格标 Confidence: medium；源码已写明这项行为（如 collapsedFraction 连续折叠），pitfall 条目也给了 ArkUI 的实现方向；写错：占位登记或代码注释里出现 `UNC` 编号的 forward-ref-uncertain 条目（如「// TODO: …-UNC-… this page approximates it」），登记的是源码已写明的行为，理由是 confidence medium 或「与兄弟页一致」
- rule-64a001778a40｜计划让找不到目标的点击登记 pending/forward-ref 时，改成实现任务，空点击记为未对齐｜读到：规格里每个可点击入口已有源码目标（WebView 页 URL、详情页参数）；写错：计划写「找不到目标时登记 pending/forward-ref」，或占位登记里登记的是可见入口的点击处理（`FWD-REF` 编号），回报里概括成「点击语义已对齐」
- rule-0697dbdf7934｜跳转先用同形本地参数类时，FWD-REF 写明收口改为 import 目标页导出的参数类｜读到：写跨页跳转时目标页由别的 converter 并行生成，它的参数类还不能 import；写错：跳转类 FWD-REF 只写「目标页注册后确认路由名与参数字段」「生成后路由名生效」，没写收口时要改为 import 目标页导出的参数类
- rule-9c409b9dff4c｜页面转换先于多语言服务时，先登记「页面文案接入 i18n t()」的 FWD-REF 再写字面量｜读到：源页面文案来自运行期 i18n 键（如 i18next 的 `t('…')`），页面 spec 写语言切换后刷新全部文案；目标端的 i18n 服务由后续切片提供；通用规范要求合法延期必须是已登记的占位，「待接入 xxx 后替换」式散文一律 FAIL；写错：placeholder-registry 新登记的 P-ID 里没有页面文案接 i18n 的一行，页面里只有「i18n 服务接管前先用字面量」的散文注释
- rule-f33d0eb5cfed｜占位因「库源不可见」登记 forward-ref-uncertain 时，不以视觉对齐为 resolve_by｜读到：页面规格写「三方库内部 UI 不可见 → 自研 / 近似」；写错：占位登记里有 `forward-ref-uncertain` 的 `UNC` 条目，原因是「AAR 无源可查 / 库源不可见」，resolve_by 写「Slice N Step 3a 视觉对齐」
