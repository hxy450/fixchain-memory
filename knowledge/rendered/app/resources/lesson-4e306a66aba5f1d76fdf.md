# VectorDrawable 转 SVG 时 viewBox 取 viewport、width/height 取显示尺寸，vector 根的 android:tint 按解析色烘焙到每个可见 path

## 何时使用

资源迁移阶段，编写 VectorDrawable 到 SVG 的批量转换脚本时

## 适用情境

源 vector 的 android:width/height（dp 显示尺寸）与 viewportWidth/Height（路径坐标系）常不相等，部分 fillColor 引用主题属性；也有 vector 根写 android:tint（含框架 color state list，如 control_checkable_material），path 的 fillColor 却是字面色（如不透明黑），并带 fillAlpha=0 的动画用 path。

## 例外与边界

- 第 3 步的整体替换只在 vector 根没有另设 android:tintMode（按默认 src_in 混合）时成立；另设了 multiply、screen 等其他模式时，tint 是和原填色混合而不是替换，不能直接把 tint 色写进每个 path。tint 链里的主题属性（如 colorControlActivated、colorControlNormal）按应用实际使用的主题逐层解析，应用或其父主题覆盖过 colorAccent 等属性时取覆盖值，不直接套框架主题的默认。

## 原因

用同一字段同时填显示尺寸与 viewBox，路径坐标系与画布错配，图标只占画布一角或近乎空白；未解析的主题属性被写成 fill=none 后图形不可见。vector 根的 tint 按默认 SRC_IN 作用于全部 path，只在 fillColor 是 @ 或 ? 引用时才替换颜色的脚本会把字面填色原样写出，选中态图标变成黑色。

## 做法

1. 两组值分开传：viewBox 为 0 0 viewportWidth viewportHeight，width/height 取 dp 值。
2. 主题属性无法解析时用可见默认色并在映射文档列出，由代码层 fillColor 按主题着色，不写 fill=none。
3. vector 根有 android:tint 时，按 tint 链解析出的颜色替换每个可见 path 的填色（字面 fillColor 也替换），fillAlpha/strokeAlpha 为 0 的 path 保持透明；多态资源（checked/unchecked 等）按状态分别烘焙。
4. 页面阶段发现资源属转换器的同类缺陷时，回执写明系统性根因，安排全量审计或修正脚本后重跑，不只修当前页引用的文件。

## 可选检查

- 转换脚本自写或怀疑有比例异常时，按同名源 vector 全量比对 viewBox 与 viewport，抽样包含 width 与 viewport 不等的图标
- 写映射表前逐个读回输出 SVG 的 fill，与登记的解析色比对，不只抽查一两个文件

来源支持：2 张卡 · 2 次迁移 · 2 个应用

已核实的平台事实（核实时用的是 HarmonyOS 6.1.0（API 23，SDK 6.1.0.105）；OpenHarmony 文档 master 2026-11-21（提交 e42bd18a）；安卓 android-37.0 的平台资源；android-36.1 的源码。和具体应用无关，直接用，不用再查；其中的默认值只在应用自己的主题、样式、清单和代码没有另设时成立，应用有没有另设要到应用里看）：
- 〔适用情境 / 原因 / 做法第 1 步〕VectorDrawable 的 android:viewportWidth / viewportHeight 是绘制所在画布（pathData 坐标系）的宽高，android:width / height 是这个 drawable 的固有显示尺寸，两组值互相独立
- 〔原因 / 做法第 3 步〕Drawable 的默认混合模式 DEFAULT_BLEND_MODE 为 BlendMode.SRC_IN，VectorDrawable 没有另设 android:tintMode 时 tint 按它混合：用 tint 色替换所有可见像素的颜色、保留透明度，字面 fillColor 也被覆盖
- 〔适用情境 / 做法第 3 步〕平台颜色状态列表 control_checkable_material：不可用时取 colorControlNormal 并乘 disabledAlpha，checked 时取 colorControlActivated，其余取 colorControlNormal
- 〔做法第 2、3 步〕应用主题没有另设 colorControlActivated、colorControlNormal 时，Theme.Material 下 colorControlActivated 取 ?attr/colorAccent，colorControlNormal 取 ?attr/textColorSecondary
- 〔做法第 2 步〕Image 的 fillColor 只对 SVG 图生效；不设时不叠加填充色，传无效值时用系统主题默认色
