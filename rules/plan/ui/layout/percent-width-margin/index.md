# match_parent 加水平 margin 的派工交代

agent 会看到什么：源布局里有 match_parent 或两侧约束 0dp 又带水平 margin 的视图，页面转换的派工、检查项或交给转换者的映射参考只写了 match_parent → '100%'、margin → .margin()

## 规矩

- rule-08a2192ba9fc｜派 UI 转换时，把「百分比宽不扣 margin、水平 margin 下沉为父 padding」放进转换者实际读的参考｜读到：源布局里有 match_parent（或两侧约束 0dp）又带 layout_marginHorizontal / marginStart / marginEnd 的视图；写错：派工的必读检查项、映射参考和前置 skill 里只有 match_parent → '100%'、margin → .margin()，没有「百分比宽不扣 margin」这条；它只在没分给转换者的 skill 里
