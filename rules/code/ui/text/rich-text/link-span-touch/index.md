# TextView 里按触点命中的链接 span（ClickableSpan、LinkMovementMethod）

agent 会看到什么：读到源端用 BetterLinkMovementMethod / LinkMovementMethod 按触点找 ClickableSpan、URLSpan，在按下的那个 span 上派发点击或长按；产物里 Text 上挂组件级 LongPressGesture，回调取第一个链接，没有经 TextController 的 getLayoutManager 按坐标找字符

## 规矩

- rule-4f26261f69f8｜源端按触点命中链接 span 派发点击和长按时，目标用 LayoutManager 按触点找链接，不取首个链接｜读到：源端用 BetterLinkMovementMethod 按触点查找 ClickableSpan，在按下的那个 span 上派发点击或长按；写错：Text 上挂组件级 LongPressGesture，回调里取的是第一个链接的 URL
