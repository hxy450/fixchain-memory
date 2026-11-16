# TextView 没写行高时的行距

agent 会看到什么：读到 TextView 只有 textAppearance 或 textSize、没写 android:lineHeight 和 android:includeFontPadding（单行撑起行高、多行正文，或 targetSdk < 28 时含日文等回退字体的文字）；产物里对应 Text 有没有 .lineHeight(...)、首末行的 padding，或用 .margin 凑行间距

## 规矩

- rule-a1c61eb9d80b｜未声明行高的单行 TextView 撑起行高时，Text 按源字体 top..bottom 写 lineHeight｜读到：TextView 只有 textAppearance 或 textSize，没写 android:lineHeight，也没写 android:includeFontPadding="false"，高度是 wrap_content，它的文字撑起所在行或容器的高度；写错：对应的 Text 只写 fontSize/fontColor/padding，没有 .lineHeight(...)，或用 .margin 凑行间距
- rule-a3f09f7fa45e｜未声明行高的多行 TextView，行距取 ascent..descent，首末行差额补 padding｜读到：多行正文 TextView（如对话框的 message）只有 textAppearance，没写 android:lineHeight，也没写 android:includeFontPadding；写错：对应的 Text 没有 .lineHeight(...)；或者每行都按单行行框 top..bottom 设了 lineHeight；或者首行上方、末行下方没补 font padding
- rule-2215ea9e144a｜源 targetSdk < 28 时，含日文等回退字体的正文和标题用固定 lineHeight 锁行距｜读到：源工程 targetSdkVersion 小于 28，TextView 没写 android:fallbackLineSpacing，正文或标题里有日文等由回退字体绘制的文字；写错：对应的 Text 没有固定 .lineHeight(...)，含 CJK 的行比拉丁文字的行高
