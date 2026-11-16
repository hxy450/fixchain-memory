# 组件自身 Drawable 背景的预览层

agent 会看到什么：读到源端选中背景后改组件自身的背景 Drawable（setBackground）再 invalidate() 重绘；产物里在 Stack 底部另加背景层，上面仍叠着不透明的占位层或成品静态预览图，测试也没断言占位层 backgroundColor 跟着切换

## 规矩

- rule-5b409fff68dd｜在预览 Stack 底部新增背景层时，上方不透明的占位层随所选背景改成透明｜读到：源端选中背景后改的是组件自身的背景 Drawable，再触发重绘（invalidate），背景是组件渲染的一部分；写错：目标在 Stack 第一层新建背景层，上面原样叠着铺满的 Row().backgroundColor(白色) 占位层或其他不透明层，已选背景时这些层仍不透明
- rule-55a854f96e59｜源端背景是组件自身 Drawable、目标只有成品静态预览图时，用 blendMode 合成或登记缺口｜读到：源端背景作为组件自身的 Drawable 随组件重绘；写错：目标预览是一张成品静态图 Image(…).objectFit(ImageFit.Contain) 叠在背景层上面，没有合成；回执只写一句「静态预览图无法对背景重着色」，没有登记缺口
- rule-85c4b96597ad｜外观选项的测试要覆盖每个兜底分支，断言已选背景时占位层 backgroundColor 跟着切换｜写错：外观选项的测试只断言调用了设置背景的方法、状态写回、透明度不作用于预览图，没有断言兜底分支上方不透明层的 backgroundColor 随所选背景切换
