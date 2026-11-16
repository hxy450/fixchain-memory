# 定义 BaseResponse 等共享类型时，字段类型取自共享模型表或 Android Bean，复用已有定义

审的是：代码
触发（任一种）：
- 读到：只读到响应壳的字段名（code / msg / time / data），没读共享模型类型表或 Android BaseResponse 的声明（如 val time: String）；写错的样子：网络层另写一份 BaseResponse，字段类型自选（如 time: number），和模型层已有的共享定义不一致
适用范围：模型层、网络层并行写共享类型时
做法：
- 字段类型从共享模型规格表或 Android Bean 取；已有共享定义就 import 复用，不另写一份
- 只读到字段名时先查类型来源，再定类型，不自行在 number / string 之间选
针对本应用要查的：
- 共享类型每个字段的声明类型：规格里的共享模型类型表，或源工程里对应的 Bean / 响应壳类；照声明类型写目标字段类型，同时按宽松转换规则读取
来源：1 张卡，1 个应用
- case-853ca988d9a2683b1c8d（app_hnaccurateweather_live_android）：做法第 1 步 ← 建议 4、诊断；做法第 2 步 ← 建议 4
