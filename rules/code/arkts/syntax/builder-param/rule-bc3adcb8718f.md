# @BuilderParam 换写的测试不把 content: this. 直传定成契约，改断言尾随闭包或箭头包装

审的是：代码
触发（任一种）：
- 写错的样子：测试里用 grep 一类的断言要求源码必须匹配 `content: this\.` 加成员 `@Builder` 名，把直传写法定成契约
适用范围：为内联内容改交给自定义组件 @BuilderParam 的换写写边界测试时
做法：
- 断言改成要求尾随闭包 `Comp({ ... }) {` 或箭头包装 `(): void => { this.…() }`，并拒绝 `content: this.` 直传成员 @Builder
来源：1 张卡，1 个应用
- case-8081ee8b9265d77fd5a8（记得日历）：做法第 1 步 ← 建议 3、诊断
