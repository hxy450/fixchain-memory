# FrameLayout 里的头像与角标

agent 会看到什么：读到固定尺寸 FrameLayout 里铺满的头像 ImageView、layout_gravity="end|bottom" 的角标、按步距重叠的头像；产物里 Stack 中角标的 .align / position、头像的 .border，以及从旧 ArkTS 片段照搬的写法

## 规矩

- rule-48ceda7eea6a｜FrameLayout 里贴右下的角标，目标用 position 按父容器坐标定位，不靠子项 .align()｜读到：固定尺寸 `<FrameLayout>` 里头像铺满，小角标 `android:layout_gravity="end|bottom"` 贴右下；写错：`Stack({ alignContent: Alignment.TopStart })` 里只给角标写 `.align(Alignment.BottomEnd)`，角标仍在左上
- rule-b86ca02212ce｜源头像控件没有描边时，目标头像不留 border，重叠头像逐属性对照源 item｜读到：源头像 item 是固定尺寸 `<FrameLayout>` 里的 `ImageView`（`android:scaleType="centerCrop"`），没有 stroke 一类描边属性，多个头像按固定步距重叠；写错：目标头像带 `.border({ width: 1, color: … })` 一类白描边（沿用目标旧代码），重叠处显出竖线
- rule-8530183b29bd｜从现有 ArkTS 片段抽取共享组件时，把旧片段当待验证草稿，逐项对照已读的源 XML｜读到：同时读到了源布局 XML（如角标 `android:layout_gravity`、头像无 stroke）和现有 ArkTS 列表项里的同一片段；写错：新共享组件照搬旧片段里与源 XML 不符的写法（如角标 `.align(Alignment.BottomEnd)`、头像 `.border`），注释却写「严格复用 Android 的尺寸和策略」
