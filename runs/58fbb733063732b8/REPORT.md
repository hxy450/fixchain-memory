# REPORT：android-panorama-map-vest7（harmony-panorama-map-vest1）session → memory

- migration_id：`b732e9f2-3b17-42ec-a7e4-51abb6e40d05`，材料 304 份 Codex 转录（5 main + 299 子代理/guardian），archive sha256 `c5aeeca6…`
- 结果：17 个修复问题 → 17 张 `status: valid` 正式卡（其中 7 张带部分 unresolved 目标）→ 共享库新增 20 条、更新 5 条 lesson
- 经验库：ingest 后 `61c70939…`，**发布 revision `7ae3d79af96af82ab8fe486bbbde2f1855ce3f2074b76ed0ab0a7bc57fc6d221`**（133 条 active，125 张卡）
- 阅读包：`C:\Users\hongy\projects\_migloop-multiapp-memory-20260927\runs\58fbb733063732b8\memory\index.md`
- 用时：2026-09-27T18:41:57Z → 19:41Z，约 60 分钟。17 个制卡子代理共计约 4.33M tokens（逐个回执合计）；主编排会话 token 数不可取得。

## 范围与边界

- 生成结束 `2026-09-03T02:06:01.239Z`：main-01a060e7 L7230，a2h-execute 最终汇报（最后一个生成期子代理 stage3_fv1_final_closer 于 02:05:40 结束）。之后都是生成后的 verify、报错修复、1:1 对齐和高德 SDK 接入。
- 观察截止 `2026-09-06T09:34:12.089Z`：材料最后一条记录。
- 盘点方法：对生成结束后所有调用做机械扫描，覆盖 apply_patch 的 Update/Add/Delete/Move，以及 exec 写入型命令和回执；逐条读取 5 个主会话的用户消息与子代理 FINAL；关键补丁正文逐条核读。清单见 `repair-tasks.yaml`，派工在 `dispatch/`。

## 问题 → 最终卡

| job | 问题 | 最终卡 | 未决目标 |
|---|---|---|---|
| issue-5fcc464cf9b9cd1034f1 | 启动停在 Splash：首屏当 Navigation 根内容 + 异步装配竞态 | cards/issue-5fcc464cf9b9cd1034f1/case-2.json | — |
| issue-7bc774bebe74d00dfa24 | AppStorageV2 key 含连字符 | cards/issue-7bc774bebe74d00dfa24/case-1.json | — |
| issue-500cf2e63e19988f0420 | 图片被追加 21845/1431000589 尺寸（收口 icon 自愈脚本） | cards/issue-500cf2e63e19988f0420/case-final.json | — |
| issue-1740a4d06903ea105e81 | Swiper 子页 onReady 用 context.pathStack 覆盖根栈 | cards/issue-1740a4d06903ea105e81/case-1.json | SearchLocationPage（非 Swiper 页，无故障） |
| issue-646efd504782bd3dec69 | Swiper enabled(false) 使子树不可点 | cards/issue-646efd504782bd3dec69/case-2.json | — |
| issue-224eb9de83aa652829f4 | 应用身份/图标保留模板值 | cards/issue-224eb9de83aa652829f4/case-2.json | AppScope app.json5、string.json（无生成期写入） |
| issue-db22477c416cef2ebedd | 教程页“开始测量”未接跳转 | cards/issue-db22477c416cef2ebedd/case-2.json | — |
| issue-356f707ace6e648548be | “我的”页按另一模块同名布局生成 | cards/issue-356f707ace6e648548be/case-1.json | — |
| issue-7b90b1ebaae140988b90 | 搜索页异步初始化覆盖输入 | cards/issue-7b90b1ebaae140988b90/case-1.json | SearchLocationPage（状态文案属生成后新增 UX） |
| issue-914a0da87d6ea90ab419 | 搜索多入口路由载荷分裂 | cards/issue-914a0da87d6ea90ab419/case-2.json | SearchLocationViewModel（修复中新生） |
| issue-436d1b16d79796c667d6 | 沉浸式：px 当 vp、图标浅色、注释冒充安全区、搜索页几何 | cards/issue-436d1b16d79796c667d6/case-2.json | — |
| issue-ff24fb8ea8e66a1cadd5 | 路线/导航页被切片重写，丢失全屏底层与两态 | cards/issue-ff24fb8ea8e66a1cadd5/case-1.json | — |
| issue-02861b75cc4ec53a32d9 | 未查高德鸿蒙 SDK 就定为受控降级 | cards/issue-02861b75cc4ec53a32d9/case-2.json | entry/oh-package.json5（无生成期写入） |
| issue-f9c6cd0dc22c13bdcdd8 | 定位权限全授予判定；接入地图未接相机/坐标转换 | cards/issue-f9c6cd0dc22c13bdcdd8/case-1.json | — |
| issue-31b1116c0e0aec40a307 | 原生地图在 Swiper 子页的触摸与生命周期 | cards/issue-31b1116c0e0aec40a307/case-1.json | — |
| issue-15e27ba62ddc28121b8e | 高德搜索 SDK 漏设隐私、PoiQueryV2 空城市 | cards/issue-15e27ba62ddc28121b8e/case-1.json | PoiService（修复期新增排序） |
| issue-adacd41d159c24498006 | 搜索栏点击挂子控件，返修又删整栏事件 | cards/issue-adacd41d159c24498006/case-2.json | SideComponent（无生成偏差） |

几个目录里另有旧的有效稿，未入库：issue-436d/224e/0286 的 case-1.json 都已被同目录的 case-2.json 取代。各目录保留草稿与 pack 回执。

## 归并取舍

- **补证/扩展已有 lesson（5 条，身份不变）：**
  - `lesson-540747e…`（禁滑的 ViewPager2）：加入“disableSwipe 而非 enabled(false)”分支。
  - `lesson-55f44e2…`（显示名双入口）：加入资源迁移合并不覆盖、编译修复不自造名称、resValue 优先。
  - `lesson-5754b7be…`（编排者兑现规范步骤）：补同类“跳过身份落地”来源。
  - `lesson-e9c6e8ef…`（沿用已有写法前核对源码）：补 onReady 取栈、连字符 key 两例。
  - `lesson-7a065e8f…`（规格与源码冲突按源端）：补同名布局、模式列举顺序两例。
- **新增 20 条，按独立触发条件组织：**
  - 导航：入口 Navigation 宿主、Swiper 子页栈来源、多入口共享载荷。
  - 启动：首屏就绪门。
  - 安全区：px→vp、系统栏图标深浅。
  - 界面：gone/listitem 几何、全屏底层骨架、点击持有节点。
  - 状态：AppStorageV2 key 字符。
  - 异步：输入初值先于 await。
  - 规格：多模块同名布局、合成快照空点击清单。
  - 新主题 `process/gates`：自愈脚本改动审阅、注释冒充检查。
  - 平台：厂商鸿蒙 SDK 先查再降级。
  - 新主题 `app/map`：高德单例隐私/Key 与 PoiQueryV2、定位权限组、占位地图替换的相机与坐标、原生地图在 Tab 页的生命周期与触摸。
- **只留在卡里、未提炼：** 具体修复值（如 21845、110101、`#FF000000`、tabData 值）、项目文件名和 OPT 编号。另外，Swiper 的 Tab 点击切页一支只有静态诊断、没有真机回归，卡中标为 unknown，未写入 lesson。

## 搁置、待核与缺口

- **搁置：** spec/报告/截图（artifact）；`tests/opt006_behavior_test.ps1`（test_support）。
- **环境类（pipeline_tooling）：** 构建临时文件、hvigor 权限、签名/bundleName 回退为 com.item.myapplication、高德控制台绑定。
- **用户临时取舍：** 启动绕过登录；OPT-006 参考另一工程新建的联系我们/隐私/意见反馈页。
- **未修复：** 广告/支付仍为降级适配层；OPT-001 周边对齐只有规格。
- **待核（未制卡）：**
  - 周边分类词重试：未入 HAP，且 Key 返回 INVALID_USER_KEY。
  - 09-06 定位按钮反馈：截止时构建未返回。
  - arkts-no-misplaced-imports 报错：未见对应写入。
- **材料缺口：** 父会话派工正文多为 encrypted_content。Android 源工程和两个参考鸿蒙仓库不在材料池，只能经转录回执取证。图标 PNG 只有回执可核。
- **环境限制（已如实处理，没有改检查器）：** 共享 inquiry 索引对这批 Codex `exec`/`apply_patch` 调用没有生成任何文件读写效应（files=0、effects=0、dispatches=0）。因此每张卡的边都先收到 `force_eligible` 反馈，再以真实调用/回执行号 force 补证后通过。agent→agent 派发边无法绑定，相关上游只写在 summary 里。
