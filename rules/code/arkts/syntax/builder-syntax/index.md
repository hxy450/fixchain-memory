# build() 和 @Builder 里的组件语法

agent 会看到什么：产物里组件语法写在不带 @Builder 的普通方法里，或 build() / @Builder 的组件树压成一行、if 块后带分号、条件分支不带花括号

## 规矩

- rule-286dc84944c6｜普通方法里写了 Column / Row 等组件语法时，改为 @Builder 并用 this.方法() 调用｜写错：组件语法写在不带 @Builder 的普通 private 方法里（方法体内有 Column() {...}、Row() {...} 等尾随闭包），build() 里以 this.方法(x) 调用；编译报 UI component 'Column' cannot be used in this place
- rule-de4030e26093｜build() / @Builder 组件树压成一行、if 块后带分号或不带花括号时，拆成多行并补花括号｜写错：build() 或 @Builder 里组件树写在一行用分号拼接，if 块后接分号：`if (...) { this.…() }; if (...) {...}`，或 `} else {...}; Text(...)`
