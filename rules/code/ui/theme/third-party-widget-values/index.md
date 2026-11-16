# 三方 UI 库控件的尺寸和动画取值

agent 会看到什么：读到布局或代码里三方 UI 库的类名和自定义属性（com.getbase.floatingactionbutton.FloatingActionsMenu 的 fab_*、Crouton 的 Configuration.Builder().setInAnimation）；产物里自研替代组件上自定的圆角、内边距、Column space、rotate 角度和 transition 时长

## 规矩

- rule-7a4af47f855e｜输入里出现库的类名或属性时，自研组件照库产物里的布局和动画值写，不自造参数｜读到：布局 XML 根元素是 com.getbase.floatingactionbutton.FloatingActionsMenu，带 fab_labelStyle、fab_labelsPosition，子钮 fab_size="mini"；写错：自写的 FAB 菜单组件自定标签圆角和内边距、Column({ space }) 子钮间距、.rotate({ angle: 45 })、OPACITY+scale 过渡时长，都不是库值
