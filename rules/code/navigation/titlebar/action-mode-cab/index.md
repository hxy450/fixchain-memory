# ActionMode 多选上下文操作栏（CAB）

agent 会看到什么：读到源端 ActionMode.Callback 显示多选 CAB 盖住 Toolbar（onCreateActionMode 里 getMenuInflater().inflate 复用页面菜单、onActionItemClicked 入口统一门控，targetSdk ≥ 35 的 edge-to-edge）；产物里自绘 CAB 栏的菜单项和溢出的填充、批量动作分发函数里的门控、CAB 期间状态栏区的色块和工具栏投影

## 规矩

- rule-5ad75513d49f｜同一菜单复用于 ActionMode/CAB 时，未声明 showAsAction 的项按两种缺省分别填充｜读到：ActionMode.Callback 的 onCreateActionMode 里用 mode.getMenuInflater().inflate(...) 复用页面菜单，有 <item> 没写 app:showAsAction；写错：CAB 栏和 CAB 溢出复制一份固定清单，或两种填充用同一个缺省值（未声明项在 CAB 里也一律进溢出）
- rule-fa999a1f2bf9｜源端在 onActionItemClicked 入口统一门控时，目标在分发入口统一接门控，不只接个别分支｜读到：源端 ActionMode.Callback.onActionItemClicked 入口对除一个例外列表外的所有动作，先调同一个门控方法（如密码校验），通过后再分发；写错：目标的批量动作分发函数（switch / case）只在删除、清空等个别 case 里调门控，其余动作直接执行；或照页面 FWD-REF 占位注释列出的局部分支接线
- rule-a1abeb21724b｜源端 edge-to-edge 下自绘 CAB 时，CAB 期间状态栏区铺 status guard、隐藏工具栏投影｜读到：页面用 ActionMode.Callback 显示多选 CAB 覆盖 Toolbar，应用 targetSdk ≥ 35（edge-to-edge 强制）；写错：自绘 CAB 栏只是一行 Row 盖在工具栏上，CAB 期间状态栏区没有 status guard 色块，工具栏投影仍露出；或注释写「CAB 不覆盖状态栏区」
