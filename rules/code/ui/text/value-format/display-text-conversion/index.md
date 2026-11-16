# 数据值转显示文本的转换和格式化

agent 会看到什么：读到源端显示前用 when / switch 穷举表、转换函数、带默认参数的格式化函数，或把 Float 直接放进字符串；产物里直接 toString()、.join、原值透传、模板串，或另写的格式化函数默认值和源端不同

## 规矩

- rule-cca53ec73e3e｜给展示型 UiModel 赋值时，code 或 ID 字段先迁源端的转换函数或目录查表，不用 join 或原值透传｜读到：源端同一页面在显示前对数据字段先调转换函数（提醒 code → 文案、重复规则 → 文案）或目录查表（getIcon(id)、getColor(id) → 图片、颜色）；写错：宿主或适配层给 UiModel 的文本、图标字段直接赋数据层原值：code 数组 .join('、')、规则类型字段原样当文案、图标和颜色字段直接传 ID
- rule-305d6fb39d8f｜数据网关遇到接口里的数值状态码时，经源端同表映射成文案，不用 toString()｜读到：源端工具类用穷举表（`when` / `switch`）把接口返回的数值码（如天气码、AQI、风向码）映射成文案；规格 AC 要求按源端同表映射；写错：网关里写 `code.toString()` 直接当描述，或把数值字段直接赋给描述字段，没有调用映射函数
- rule-0f499c75bc6b｜复刻源端格式化函数时按源签名核对默认参数，优先调用已实现的工具函数，不在页内重写｜读到：源端 Kotlin 格式化函数签名带 Boolean 默认参数（如分钟不补零、秒补零），调用处不传参只用默认值；写错：目标在页内另写同名格式化函数，默认值和源不同（如分钟也 padStart(2, '0')），注释里写错源端默认值
- rule-e4b66757983c｜源码把 Float 直接格式化进字符串时，按 Float.toString 输出并保留 .0｜读到：stringResource(R.string.x, floatValue) 或字符串模板里直接放 Float（如 roundToDecimals() 的结果）；写错：目标写成 `${value}` 模板串或 toStringShort(value)，12.0 显示成「12」
- rule-22c52514a1d6｜复刻目标侧没有的源端格式化 helper 时，先读函数体，按原式实现除数、小数和单位后缀｜读到：源端调用点把一个静态格式化 helper 的返回值直接拼进显示文案，只补括号不补单位（形如 `" (" + helper(w, h) + ")"`），单位后缀和小数规则在 helper 内部（如 String.format("%.2f")）；写错：目标自写的等价 helper 除数和小数位凭记忆写（如 toFixed(1)），返回值没有单位后缀，注释里的公式和表达式对不上
- rule-e3b2236bad82｜Java 把资源 int 与字符串相加时，目标显示资源 id 数字，不换成资源文案｜读到：Java 源码 `R.string.x + ": " + e.getMessage()` 这类资源 int 直接与 String 相加后显示；写错：ArkTS 写成先取资源文案再拼接（如 getStringSync / resText($r('app.string.x')) 后接 `: ${detail}`），显示出了文字
