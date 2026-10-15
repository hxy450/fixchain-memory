# TextView 未写文字色时按默认 textAppearance 链与主题代际解析，EditText 取 editTextColor

ID：`lesson-e9f02c6de64ad68b5b48` · 版本：2

[本主题](index.md)

## 何时使用

规格提取与界面实现阶段，为源端没写 textColor 的 TextView/AppCompatTextView/EditText，或只写了 textAppearance（如 ?android:attr/textAppearanceMedium）的文本确定文字色与字号时；为顶部对齐、决定纵向排布的单行 TextView 定高时

## 适用情境

源布局里的 TextView 没有 textColor、textAppearance、style，或只声明 textAppearance；目标 ArkUI Text 不写 fontColor 时取 ArkUI 默认近黑；工程里可能已有按“主文字色”写的先例、注释或提醒。也包括 TextView 默认 includeFontPadding=true，而 ArkUI Text 没有对应属性。

## 例外与边界

- 主题覆盖了 textViewStyle、textAppearanceSmall 或相关颜色属性时，按覆盖后的值解析，不直接套用下面的默认链

## 原因

TextView 的默认文字色来自 textViewStyle 的默认 textAppearance（Widget.TextView 为 ?attr/textAppearanceSmall），各 TextAppearance 引用的颜色属性又因主题代际而异，EditText 则取 editTextColor；凭“未写颜色即主文字色”的直觉、ArkUI 默认近黑或相邻控件的硬编码值填写，正文会整体变深或变浅。

## 做法

1. TextView 没有 textColor、textAppearance、style 时，按 textViewStyle → textAppearance（默认 ?attr/textAppearanceSmall）→ 该 TextAppearance 的 textColor 属性 → 主题中的颜色值解析，给 ArkUI Text 显式写 fontColor，不留给 ArkUI 默认近黑，也不沿用旧实现、相邻组件或同组控件的值。
2. 各代际的默认链不同，按所用主题在 SDK 或 aar 中核对：基础与 Holo 主题（android-36.1 styles.xml、styles_holo.xml）Large、Medium 继承 TextAppearance 的 textColorPrimary，Small 为 textColorSecondary；框架 Material（styles_material.xml）Large 为 textColorPrimary、Medium 为 textColorSecondary、Small 为 textColorTertiary；AppCompat 的 TextAppearance.AppCompat.Medium、Small 同样分别为 textColorSecondary、textColorTertiary（appcompat 1.7.1 values.xml），API 21 起 AppCompat 主题继承框架 Theme.Material（values-v21 的 Platform.V21.AppCompat*），颜色值取自框架主题。例：AppCompat 或框架 Material 浅色主题下未写颜色的 TextView 取 textColorTertiary，即 secondary_text_material_light #8A000000（android-36.1 themes_material.xml 与 colors_material.xml；白底约 #757575，深色主题为 #B3FFFFFF）；Holo 暗色主、次、提示色依次为 #F3F3F3、#BEBEBE、#808080（android-36.1 colors_holo.xml 的 bright/dim/hint_foreground_holo_dark）。
3. 只声明 textAppearance 时，按该 TextAppearance 同时展开字号与 textColor；EditText 未写 textColor 取 editTextColor（主文字色，例：AppCompat 浅色为 #DE000000，即 android-36.1 Theme.Material.Light 的 textColorPrimary：黑色 87%），未写 textColorHint 取提示色；源端显式写的颜色（如 @android:color/white）单列，不绑到主题文字色令牌。
4. TextView 默认 includeFontPadding=true，而 ArkUI Text 没有对应属性：顶部对齐、决定纵向排布的单行文字按 includeFontPadding=true 时的行框（取字体度量的 top/bottom 而非 ascent/descent，见 sources/android-36.1 android/text/BoringLayout.java）补纵向差或显式定高，并在转换报告写明取值依据。
5. 规格提取时，页面规格列出 TextView 的文本和字号时同时写明未声明颜色时的提供方与解析值；目标缺对应语义色资源时补齐 base 与 dark 两套。

来源支持：8 张卡 · 3 次迁移 · 3 个应用

## 来源（按需复核）

- [case-64a967d716ed18688332](../../../store/cases/case-64a967d716ed18688332/ca7bfbe7434eda2cf305ccfefcdcb5447cbdd6a9fd3090899a3b3d48d9f6ff2e.json) · 结论：recommendation:3, recommendation:1
  卡片版本：`ca7bfbe7434eda2cf305ccfefcdcb5447cbdd6a9fd3090899a3b3d48d9f6ff2e`
- [case-701f2e2280bcc31423bd](../../../store/cases/case-701f2e2280bcc31423bd/f3ba6e8fd8e3b02acb710d8e9c4e889fa2e3cfd632ab2397ed300b3104f1c6c7.json) · 结论：recommendation:4
  卡片版本：`f3ba6e8fd8e3b02acb710d8e9c4e889fa2e3cfd632ab2397ed300b3104f1c6c7`
- [case-784ba4ab52f98f7156b6](../../../store/cases/case-784ba4ab52f98f7156b6/4dadc2a29166ec34c2d95e895727d71c2b35c547fb4a45b745dabb5e89d47ed5.json) · 结论：diagnosis, recommendation:1
  卡片版本：`4dadc2a29166ec34c2d95e895727d71c2b35c547fb4a45b745dabb5e89d47ed5`
- [case-8ec9b17b9de9183f6d89](../../../store/cases/case-8ec9b17b9de9183f6d89/d013c1695e2d6ad2b873e6f8a3b10630d8ecb7249e11b7e809a1880e7e50e264.json) · 结论：recommendation:2
  卡片版本：`d013c1695e2d6ad2b873e6f8a3b10630d8ecb7249e11b7e809a1880e7e50e264`
- [case-9ec2a14cbd1df18e3620](../../../store/cases/case-9ec2a14cbd1df18e3620/c255ebcbedb756457733a07005af242eaf3f9e63560661c2b1ecc0acec7de0c9.json) · 结论：diagnosis, recommendation:1, recommendation:2, recommendation:3
  卡片版本：`c255ebcbedb756457733a07005af242eaf3f9e63560661c2b1ecc0acec7de0c9`
- [case-c3ff122a5abfda1fa55d](../../../store/cases/case-c3ff122a5abfda1fa55d/96c80bfff7f5cf6fc15aca07941c0cdce602be25ebd347262fb4f28be641a783.json) · 结论：recommendation:2
  卡片版本：`96c80bfff7f5cf6fc15aca07941c0cdce602be25ebd347262fb4f28be641a783`
- [case-e6fd5f0c4d37710c1d97](../../../store/cases/case-e6fd5f0c4d37710c1d97/1a35da48a7e70d948e47b59d418531da3855775e938ecc8feefef7596b5e3741.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`1a35da48a7e70d948e47b59d418531da3855775e938ecc8feefef7596b5e3741`
- [case-f103fbdcad4e6eeb7569](../../../store/cases/case-f103fbdcad4e6eeb7569/5d706aafc0da45514a48a3782137ff1793911c77a2acd5a116101a82ec0d0ba3.json) · 结论：recommendation:5
  卡片版本：`5d706aafc0da45514a48a3782137ff1793911c77a2acd5a116101a82ec0d0ba3`
