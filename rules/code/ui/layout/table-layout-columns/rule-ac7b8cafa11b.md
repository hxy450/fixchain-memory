# TableLayout 的 stretchColumns/shrinkColumns 不是等分，按自然宽加均分余量算列宽

审的是：代码
触发（任一种）：
- 读到：源布局 `TableLayout` 带 `android:stretchColumns="*"` / `android:shrinkColumns="*"`，单元格有 paddingStart / paddingEnd；写错的样子：目标每行用两个 `.layoutWeight(1)` 或 `.width('50%')` 等分列宽
适用范围：源端 TableLayout 用 stretchColumns / shrinkColumns 分配列宽，迁到 ArkUI 行列布局时
做法：
- 先求每列最宽单元格的自然宽：文字宽用 this.getUIContext().getMeasureUtils().measureText({ textContent, fontSize, … }) 测（返回 px），再加单元格左右 padding；或用 onAreaChange 取单元格实际宽
- 列宽 = 该列自然宽 + (行宽 − 各列自然宽之和) / 可伸缩列数；余量为负且列可收缩时同样按列数均摊减少
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- 列宽由该列最宽的单元格决定；stretchable 的列扩展以填满剩余空间，shrinkable 的列收缩以放进父容器：TableLayout 列宽的语义（出处：android.widget.TableLayout 类注释）
- extraSpace = (size - totalWidth) / count；maxWidths[i] += extraSpace：余量（可为负）按列数均分加到每列的自然宽上（出处：android.widget.TableLayout#mutateColumnsWidth）
- measureText(options: MeasureOptions): number，返回 px：测文字自然宽（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，MeasureUtils.measureText、UIContext.getMeasureUtils）
- measureTextSize(options: MeasureOptions): SizeOptions：同族接口：MeasureUtils.measureTextSize，同时测宽高（出处：鸿蒙 SDK 的 ets/api/@ohos.arkui.UIContext.d.ts，MeasureUtils.measureTextSize）
- 用 measureText 测最宽标签和数值后按 TableLayout 公式分配，列宽与源端一致：验证过的做法（出处：卡里修好并验证过）
来源：1 张卡，1 个应用
- case-9cfde635e67a08373fe6（omni-notes-hmos）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4；取值 5 ← 诊断
