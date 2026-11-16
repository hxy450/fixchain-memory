# HANDOFF 和待分配 P-ID 的登记

agent 会看到什么：「由某入口装配 / 接线阶段决定」的散文注释、上游报告的 open_question、Base handoff 里的 Suggested P-ID、留给后续批次的媒体尺寸，和源码 // HANDOFF: 行、registry、被点名切片的派工之间对不对得上

## 规矩

- rule-4c09dd55a84f｜要靠别的文件或 slice 补调用点才生效时，登记 HANDOFF，不用散文注释代替｜读到：占位规则写着要靠别处调用点才算完成的，须写 `// HANDOFF: owner/what/verify` 并登记；写错：文件头只写散文说明“转发由某入口装配或接线阶段决定”，或报告里只列 open_question，没有 `// HANDOFF:` 行，登记表里也没有对应条目
- rule-824e52967a51｜上游报告点名“由某 slice 决定”的问题，要写进该 slice 的派工｜读到：上游报告的 open_question 或子文件头写着某项转发“由某入口装配 / 接线阶段决定”；写错：被点名 slice 的派工里没有这一项，只要求直嵌子组件且“其余逐字不动”
- rule-9eb699458094｜Base 自检把文档里「由 X 调用 / 待闭环」逐条对上源码 HANDOFF 或 registry｜写错：handoff 文档或交付说明里有「由启动装配 owner 调用」「待闭环」「Suggested P-ID Allocations…未写入源码 marker、未修改共享 registry」，自检却以 HANDOFF 计数为 0 报通过
- rule-adbfa9b8b46a｜汇总 Base handoff 时，建议 P-ID 登记进 registry 并写进 owner 切片接线项｜读到：Base handoff 里有「Suggested P-ID Allocations / 交主线程分配的建议」（带 owner、resolve_by）；写错：汇总后的 registry 里没有这个 P-ID，owner 切片在 feature-plan 里的 integration_points 和 placeholders_planned 也没有这项（如 placeholders_planned: []）
- rule-237720a5dbb2｜媒体留给后续批次拷贝时，图片尺寸仍在本页写定或登记成可机械校验的交接｜读到：源布局里有 wrap_content 的位图 ImageView，媒体文件留给后续批次拷贝；派工公共规则要求交给别处的尺寸工作必须机械化登记；写错：交接里只写「媒体待后续批次资源 sweep」，没有图片的显示尺寸，也没有可机械校验的尺寸交接项
- rule-1d5d65afb02b｜AC 的目标符号落在他切片或共享文件时，登记 FWD-REF 或 HANDOFF，不写散文｜读到：规格的 AC 把入口标在别的切片或共享文件的符号上（「标:某页面 VM 的长按处理方法」），占位协议规定跨文件移交须登记 FWD-REF / HANDOFF、散文注释一律 FAIL；写错：只在文件头写「长按手势识别归某 VM」这类散文，或推理里决定 Skip；依赖他方状态的方法写成 `return false; // … 注入后升级` 的散文桩，registry 里没有对应 P-ID
- rule-1d6bb8379206｜转换者确认行为归宿主文件实现时，登记 FWD-REF/handoff，不只写头注释｜读到：规格要求某行为由宿主页实现（如「宿主页 onBackPress 需优先判定侧栏开合」）；写错：转换产物只在头注释写「归宿主 onBackPress」，FWD-REF / handoff 登记里没有指向宿主文件的条目
- rule-5986ab42064c｜内容组件发现宿主缺遮罩、焦点兜底等承载参数时，登记占位并写入确定值｜读到：内容组件由宿主页的 openCustomDialog 承载，宿主那边的承载参数（遮罩、打开后聚焦）还没设；写错：宿主侧要补的参数只写在转换报告的 Handoff 表或 handback 建议里，占位登记里没有对应的占位（如 P-S4 一类），后续宿主接线切片的派工也没带上
