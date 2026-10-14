# ui/text

文字外观：主题与默认样式继承、TextView行高

[上一级](../index.md)

## 本级经验

- [把主题与默认样式继承的文字外观解析成具体值，并显式设置TextView行高](lesson-c5f30aef1c67f6891b0b.lesson.md)
  - 时机：规格提取与界面实现阶段，为使用textAppearance*或未写textColor的TextView、继承平台默认样式的Button确定字色、字重、大小写、行高与最小尺寸时
  - 情境：源控件用?android:attr/textAppearance*、依赖应用主题的textColorPrimary，或Button只套了改背景/字色的自定义style（未改其余默认属性）；目标用Text或自组合按钮实现。
