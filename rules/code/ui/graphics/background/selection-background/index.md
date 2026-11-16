# 按选择对象分图片、单色、渐变生成的背景

agent 会看到什么：读到的源方法按选择对象的 url、colors 数量、orientation 分支生成图片、ColorDrawable 或 GradientDrawable；交回的绑定或测试只覆盖 url 一支

## 规矩

- rule-5a63a704aa2d｜源方法按选择对象分图片、单色、渐变几支时，目标绑定逐支实现，不只迁 url 分支｜读到：源方法按一个选择对象分支：url 非空加载图片；否则 colors.size == 1 生成 ColorDrawable，colors.size == 2 按 orientation 生成 GradientDrawable；写错：目标绑定只读选择对象的 `url` 字段设图片源，没有任何 `colors` / `orientation` 处理；`url` 为空时不清图片
- rule-d55300486850｜背景类绑定的测试只有 url 用例时，补齐单色、双色加方向、选择为空几种输入｜读到：源方法按选择对象的 url、colors 数量和 orientation 分支生成 ColorDrawable / GradientDrawable；写错：目标测试只有图库 `url` 一种输入的用例，没有 `colors` 长度 1、长度 2 和选择为空的用例，就宣称这个源方法已迁移
