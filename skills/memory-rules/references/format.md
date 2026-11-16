# 规矩的格式

给写规矩的人看：一条规矩由哪些栏组成、每栏怎么写、写出来呈现成什么样。最后有两条完整的例子，一条代码类、一条规格类（文件在同目录的 `examples\` 下，都过了检查脚本）。

## 1. 一条规矩是什么

一条规矩只讲一件事：一个触发对一个做法。审的人（任务刚做完时来审的 agent）看一处就能判断适不适用；照做之后这条里没有剩下的事。

- **触发**写审的人看得到的东西：这个子代理读过的东西里有什么（`read`），它交回的产物里写错成什么样（`wrong`）。
- **做法**写能直接照着写的写法，并带上查清的知识：能查清的写结果和出处；因为随应用而变查不清的，写怎么查。
- 规矩跟子代理完成的任务挂钩：规格、计划与派工、代码、资源四种产物都按同一套写法。同一张卡可以在几种产物上各出一条。

## 2. 结构化原件

合并后的规矩存在 `store\rules\<规矩号>.json`；一张卡提炼出的候选规矩存在 `store\candidates\<卡号>.json`（见第 6 节），候选里不写 `id`、`general`、`status`、`sources` 四栏，由后面的脚本补。

```json
{
  "id": "rule-<12 位十六进制>",
  "title": "触发在前、做法在后的一句话，不超过 60 字",
  "product": "规格 | 计划与派工 | 代码 | 资源",
  "triggers": [
    {"read": "这个子代理读过的东西里看得到的写法；没有就写空字符串",
     "wrong": "它交回的产物里写错的样子：出现了什么，或者少了什么；没有就写空字符串"}
  ],
  "scope": "适用范围，一句话",
  "exceptions": [{"text": "卡里写明的不适用情形", "support": ["case-…#recommendation:2"]}],
  "how": [{"text": "一步做法，带确切写法", "support": ["case-…#recommendation:2"]}],
  "values": [{"value": "确切的值或写法", "meaning": "它是什么", "source": "出处，写到文件加符号名，不带本机路径", "support": []}],
  "lookups": [{"what": "要针对这个应用查的是什么", "where": "去哪类来源的哪个文件里、按什么找", "how": "找到之后怎么读出值"}],
  "why": "一句话：不这样做会出什么错",
  "keys": {"read": ["读过的东西里会出现的词"], "product": ["产物里会出现的词"]},
  "probe": null,
  "unverified": ["没能核实的点"],
  "alternatives_unverified": ["知识库里查到、但卡里没验证过的替代写法"],
  "siblings_checked": "搜了什么词、另有几个接口带它；或者「无：」加原因",
  "refs": [{"what": "…", "kind": "harmony-dts | android-sdk | android-lib | oh-docs", "where": "来源里的相对路径（依赖库写 group:artifact:version 加包内路径），加符号名", "quote": "逐字原文，不超过 200 字", "version": "…"}],
  "sources": ["case-…"],
  "general": false,
  "status": "active | disputed"
}
```

| 栏 | 谁写 | 呈现给审的人 | 说明 |
|---|---|---|---|
| `title` | 提炼 | 是 | 触发在前、做法在后，不超过 60 字 |
| `product` | 提炼 | 是 | 审的是哪种产物 |
| `triggers` | 提炼 | 是 | 第一个触发还进第三层索引的那一行 |
| `scope`、`exceptions`、`how`、`why` | 提炼 | 是（`why` 不呈现在正文里，但计入长度） | |
| `values`、`lookups`、`unverified` | 提炼 | 是 | |
| `keys`、`probe` | 提炼 | 否，给召回用 | |
| `siblings_checked`、`alternatives_unverified`、`refs` | 提炼 | 否，留作核对 | |
| `id`、`sources`、`general`、`status` | 合并、归族的脚本 | `sources` 折成「来源：N 张卡，M 个应用」 | |

## 3. 各栏怎么写

**`title`**：触发在前、做法在后的一句话，例如「TextView 带文字阴影属性时，目标用 Text.textShadow，不用 .shadow」。不写成话题（「关于阴影」）或提醒（「注意阴影」）。

**`product`**：「规格」「计划与派工」「代码」「资源」之一，说明这条规矩审的是哪种产物。一张卡里同一件事既要求规格写明、又要求代码照写的，拆成两条，各标各的产物。文档类的产物这样归：

| 产物 | 包括 |
|---|---|
| 规格 | 规格页、源码理解笔记、决策台账、验收条目 |
| 计划与派工 | 任务拆分、派工说明、移交项和占位的登记、覆盖清单和跳过清单 |
| 代码 | 目标端的源代码（.ets、.ts 等） |
| 资源 | 目标端的资源文件、工程配置（element、media、module.json5 等） |

**`triggers`**：两栏至少写一栏。
- `read`：读过的东西里看得到的写法——安卓源文件里的 XML 标签和属性、类名、方法名、资源类型、取值词；规格、派工说明、映射参考里的说法。
- `wrong`：交回的产物里写错的样子——出现了什么写法，或者少了什么。
- 代码和资源类的规矩，写了的那一栏里至少有一个代码标识符（如 `TextView`、`android:shadowRadius`、`.shadow(`、`wrap_content`）。规格和派工类的规矩，`wrong` 一定要写：文档里看得到的说法，或缺的那一项。
- 流水线里固定出现的记号也算看得到的写法：规格、派工、代码注释和报告里固定的大写记号和编号（如占位登记、移交项用的那些），以及反引号括起来的原样字面量。不许为了过检查编造占位标识符（`<Class>.<method>`、`stopXxx` 这类）。
- 同一件事在不同写法下（View 的 XML、Java 代码、Compose）触发不同，各写一个触发，放在同一条规矩里。只写卡里出现过的写法。
- 卡里的情形带着条件（背景不透明、主题是某一族、某个属性没写）时，条件写进触发或 `scope`，不写成无条件的默认。
- 只写平台和公共库的词，不写出事应用自己的类名、资源名、控件 id、文件名。

**`scope`**：适用范围，一句话。只写范围，不写例外。

**`exceptions`**：卡里写明的不适用情形，每项标 `support`。卡里没说的不要加，尤其不要写「规格、计划或台账另有选择时可以不照做」。声明里写明的版本要求（`@since`）可以写进 `scope`，注明出自声明，这不算自己加的例外。

**`how`**：1–3 步，每步是能直接照着写的写法：目标接口的确切调用、源端每个值对应到哪个参数；规格类的写规格里该有的那一句或那一项。每步标 `support`（「卡号#diagnosis」或「卡号#recommendation:N」）。

**`values`**：查实的写法和取值。`value` 是确切的签名或值，`meaning` 说它是什么（同族接口注明「同族接口」），`source` 是呈现出来的唯一出处：
- 鸿蒙 SDK：「鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.textShadow」；HarmonyOS 专有能力：「鸿蒙 SDK 的 hms/ets/…，符号名」；
- Android 平台资源：「Android SDK 平台资源 data/res/values/attrs.xml，资源名（按应用的 compileSdk 取对应平台）」；
- 安卓框架源码：「android.widget.TextView#setShadowLayer」；
- 依赖库：「androidx.appcompat:appcompat 包内 res/values/values.xml，资源名（按应用依赖的版本）」；
- 官方文档：文件名加小节名；
- 出自卡的：「卡里修好并验证过」。
来自卡的值 `support` 标卡的结论；来自知识库的值 `support` 写空列表，并在 `refs` 里有对应出处。一条规矩不超过 8 项，同族接口最多写 3 个。

**`lookups`**：随应用而变、写不成确定值的（主题、compileSdk、依赖库版本、应用资源）：`what` 要查什么，`where` 去哪类来源的哪个文件、按什么找（可以是源工程或目标工程里的某一类文件，写文件类型和找法，不写某个应用的文件名），`how` 找到之后怎么读出值。可以附一个带条件的例子（「例：某主题下是某值」），不写成让人照抄的答案。

**`why`**：一句话，不这样做会出什么错。

**`keys`**：给召回用的词，`read` 是读过的东西里会出现的词，`product` 是产物里会出现的词，每栏 3–12 个。代码和资源类只用平台和公共库的词；规格和派工类可以用文档里固定出现的说法（中文或记号）。

**`probe`**：写错的样子如果能表达成在产物文件里搜一个正则，写成 `{"pattern": "…", "note": "搜到说明什么"}`；表达不了的写 `null`。正则按 Python `re` 的语法，要能编译，不要写能匹配空串的。

**`unverified`**：这条规矩里没能核实的点（包括卡里观察到的行为出自和本机不同的 SDK 版本）。**`alternatives_unverified`**：知识库里查到、但卡里没验证过的替代写法，不写进 `how` 和 `values`。**`siblings_checked`**：同族接口搜了什么词、另有几个接口带它；做法不落在具体接口上的，或落在事件名、通用方法这类没有专门参数类型可搜的接口上的，写「无：」加原因。

**`refs`**：只给检查脚本核对引文用，不呈现，但它是库的一部分，换一台机器也要能核对，所以不写任何本机路径。`where` 写来源里的相对路径加符号名：鸿蒙 SDK 写 SDK 根目录（DevEco Studio 的 `sdk/default`）下的路径，如 `openharmony/ets/component/text.d.ts TextAttribute.textShadow`；Android SDK 写 SDK 根目录下带平台版本的路径，如 `platforms/android-36/data/res/values/attrs.xml TextAppearance shadowRadius`；依赖库写坐标加包内路径，如 `androidx.appcompat:appcompat:1.7.1 res/values/values.xml Base.TextAppearance.AppCompat`；文档写文档库里的路径，如 `zh-cn/application-dev/quick-start/app-configuration-file.md 配置文件标签`。路径一律用 `/`。`quote` 是逐字原文、不超过 200 字，检查脚本按本机配的根目录（`work/sources.local.json`）找到文件核对；`kind` 是 `harmony-dts`、`android-sdk`、`android-lib`、`oh-docs` 之一。怎么找、怎么写见 `knowledge-sources.md`。

**`general`**（归族时才有）：`true` 表示这是触发族上的通用查法：看到哪一类写法，去哪查、怎么读出值，再写成显式写法。它不列取值表。

**`status`**（合并时才有）：`active`，或说法冲突时的 `disputed`（冲突写明在 `unverified` 或合并理由里）。

## 4. 长度和条数

- 正文（title、triggers、scope、exceptions、why、how 合计）不超过 800 字；通用查法不超过 600 字。
- 一张卡通常写 1–4 条，最多 8 条。
- `how` 1–3 步；`keys` 每栏 3–12 个；`quote` 不超过 200 字。
- 各栏（包括 `refs`）里不能出现本机的路径、盘符、用户目录，除 `refs` 外也不能出现行号，也不能出现出事应用的名字、「本例」「本应用」「该应用」、转录文件名。

## 5. 呈现的样子

第四层 `rules\<产物>\<主题>\<触发族>\<规矩号>.md` 的正文，没有内容的段不出：

```
# <title>

审的是：<product>
触发（任一种）：
- 读到：<read>；写错的样子：<wrong>
适用范围：<scope>
不适用的情形：<exceptions>
做法：
- <how>
已核实的写法和取值（核实时用的是鸿蒙 SDK API <N>）：
- <value>：<meaning>（出处：<source>）
针对本应用要查的：
- <what>：<where>；<how>
未核实：<unverified>
来源：<N> 张卡，<M> 个应用
```

第三层索引里每条规矩一行：

```
- <规矩号>｜<title>｜读到：<第一个触发的 read>；写错：<第一个触发的 wrong>
```

用 `skills\memory-rules\scripts\render.py <文件>` 渲染，加 `--index` 出索引行。

## 6. 候选文件：一张卡的输出

```json
{"case": "case-…", "rules": [ … ], "left_out": [ … ], "corrections": [ … ], "gaps": [ … ], "conflicts": [ … ]}
```

- `rules`：这张卡的候选规矩，每条是第 2 节的格式去掉 `id`、`general`、`status`、`sources`。`support` 只引这张卡自己的结论。
- `left_out`：卡里没写成规矩的内容，`{"text": "…", "reason": "…"}`，`reason` 是「没有产物里看得到的触发」（纯流程上的提醒）、「要上机或截图才能做」「只对出事应用成立」「针对经验库本身的建议」之一，或「其他：…」。一条规矩都写不出来时 `rules` 写空列表，原因写在这里。
- `corrections`：按声明改正了卡里写错的签名、参数个数、默认值、单位、枚举值，`{"was": "…", "now": "…", "ref": "…"}`。
- `gaps`：想查而没查实的。
- `conflicts`：知识库和卡里做法的冲突、卡内自相矛盾的地方（不改做法，记在这里）。

## 7. 例子一：代码类（文字阴影）

出自一张卡的第 3 条建议（TextView 的文字阴影要转成 `Text.textShadow`）；取值都查了本机的鸿蒙 SDK 和 Android SDK，同族接口一并写上。这张卡的其他建议在实际提炼时会各成一条，样例里记在 `left_out`。

```json
{
  "case": "case-4f627840679361f165a3",
  "rules": [
    {
      "title": "TextView 带文字阴影属性时，目标用 Text.textShadow，不用 .shadow",
      "product": "代码",
      "triggers": [
        {
          "read": "TextView 或它引用的样式里有 android:shadowColor / shadowRadius / shadowDx / shadowDy",
          "wrong": "对应的 Text 上写的是 .shadow(...)，或者没有阴影"
        }
      ],
      "scope": "安卓 TextView（含它引用的 style、textAppearance）带文字阴影属性，迁成 ArkUI Text 时",
      "exceptions": [],
      "how": [
        {
          "text": "写成 Text(...).textShadow({ radius: <shadowRadius>, color: <shadowColor>, offsetX: <shadowDx>, offsetY: <shadowDy> })；.shadow(...) 只留给组件框阴影",
          "support": [
            "case-4f627840679361f165a3#recommendation:3"
          ]
        }
      ],
      "values": [
        {
          "value": "textShadow(value: ShadowOptions | Array<ShadowOptions>): TextAttribute",
          "meaning": "Text 的文字阴影，可传一个或一组 ShadowOptions",
          "source": "鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.textShadow",
          "support": []
        },
        {
          "value": "ShadowOptions 的 radius、offsetX、offsetY 单位是 px",
          "meaning": "源端四个值照搬数值，不乘密度，不转成 vp",
          "source": "鸿蒙 SDK 的 ets/component/common.d.ts，ShadowOptions",
          "support": []
        },
        {
          "value": "shadowRadius、shadowDx、shadowDy 的 format 是 float",
          "meaning": "源端这几个值是不带单位的浮点数，TextView 用 getFloat 读出后原样交给 setShadowLayer",
          "source": "Android SDK 平台资源 data/res/values/attrs.xml，TextAppearance 的 shadowRadius（按应用的 compileSdk 取对应平台）；android.widget.TextView#readTextAppearance",
          "support": []
        },
        {
          "value": "shadow(value: ShadowOptions | ShadowStyle): T",
          "meaning": "给组件本身加阴影，不是文字阴影",
          "source": "鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.shadow",
          "support": []
        },
        {
          "value": "textShadow(value: ShadowOptions | Array<ShadowOptions>): SpanAttribute",
          "meaning": "同族接口：Span 的文字阴影",
          "source": "鸿蒙 SDK 的 ets/component/span.d.ts，SpanAttribute.textShadow",
          "support": []
        },
        {
          "value": "textShadow(value: ShadowOptions | Array<ShadowOptions>): TextClockAttribute",
          "meaning": "同族接口：TextClock 的文字阴影",
          "source": "鸿蒙 SDK 的 ets/component/text_clock.d.ts，TextClockAttribute.textShadow",
          "support": []
        },
        {
          "value": "textShadow(value: ShadowOptions | Array<ShadowOptions>): TextTimerAttribute",
          "meaning": "同族接口：TextTimer 的文字阴影",
          "source": "鸿蒙 SDK 的 ets/component/text_timer.d.ts，TextTimerAttribute.textShadow",
          "support": []
        }
      ],
      "lookups": [],
      "why": "写成 .shadow(...) 时阴影投在组件框上，不在文字笔画上",
      "keys": {
        "read": [
          "TextView",
          "android:shadowColor",
          "android:shadowRadius",
          "android:shadowDx",
          "android:shadowDy",
          "textAppearance",
          "setShadowLayer"
        ],
        "product": [
          "Text",
          "textShadow",
          "shadow",
          "ShadowOptions",
          "radius",
          "offsetX",
          "offsetY"
        ]
      },
      "probe": {
        "pattern": "\\.shadow\\(\\s*\\{",
        "note": "组件上写了 .shadow({…})；这个组件若是由带 shadow* 属性的 TextView 转来的 Text，应改成 .textShadow"
      },
      "unverified": [
        "同一个 radius 数值两边的模糊程度是否一样"
      ],
      "alternatives_unverified": [],
      "siblings_checked": "搜 textShadow(value: ShadowOptions：鸿蒙 SDK ets/component 下有 TextAttribute、SpanAttribute、TextClockAttribute、TextTimerAttribute 四个，另三个写进了 values",
      "refs": [
        {
          "what": "Text 的 textShadow 签名",
          "kind": "harmony-dts",
          "where": "openharmony/ets/component/text.d.ts TextAttribute.textShadow",
          "quote": "textShadow(value: ShadowOptions | Array<ShadowOptions>): TextAttribute;",
          "version": "API 23（HarmonyOS 6.1.0）"
        },
        {
          "what": "ShadowOptions.radius 的单位",
          "kind": "harmony-dts",
          "where": "openharmony/ets/component/common.d.ts ShadowOptions.radius",
          "quote": "Blur radius of the shadow and the unit is px.",
          "version": "API 23（HarmonyOS 6.1.0）"
        },
        {
          "what": "ShadowOptions.offsetX 的单位",
          "kind": "harmony-dts",
          "where": "openharmony/ets/component/common.d.ts ShadowOptions.offsetX",
          "quote": "Offset of the shadow along the x-axis. Unit is px. Default value is 0.",
          "version": "API 23（HarmonyOS 6.1.0）"
        },
        {
          "what": "ShadowOptions.offsetY 的单位",
          "kind": "harmony-dts",
          "where": "openharmony/ets/component/common.d.ts ShadowOptions.offsetY",
          "quote": "Offset of the shadow along the y-axis. Unit is px. Default value is 0.",
          "version": "API 23（HarmonyOS 6.1.0）"
        },
        {
          "what": "TextAppearance 的 shadowRadius 是 float",
          "kind": "android-sdk",
          "where": "platforms/android-36/data/res/values/attrs.xml TextAppearance shadowRadius",
          "quote": "<attr name=\"shadowRadius\" format=\"float\" />",
          "version": "android-36"
        },
        {
          "what": "TextView 用 getFloat 读 shadowDx",
          "kind": "android-sdk",
          "where": "sources/android-36.1/android/widget/TextView.java TextView#readTextAppearance",
          "quote": "attributes.mShadowDx = appearance.getFloat(attr, attributes.mShadowDx);",
          "version": "android-36.1"
        },
        {
          "what": "读出的值原样传给 setShadowLayer",
          "kind": "android-sdk",
          "where": "sources/android-36.1/android/widget/TextView.java TextView#applyTextAppearance",
          "quote": "setShadowLayer(attributes.mShadowRadius, attributes.mShadowDx, attributes.mShadowDy, attributes.mShadowColor);",
          "version": "android-36.1"
        },
        {
          "what": "组件的 shadow 是给组件加阴影",
          "kind": "harmony-dts",
          "where": "openharmony/ets/component/common.d.ts CommonMethod.shadow",
          "quote": "Applies a shadow effect to the component. * * @param { ShadowOptions | ShadowStyle } value - Shadow of the component.",
          "version": "API 23（HarmonyOS 6.1.0）"
        },
        {
          "what": "Span 的 textShadow（同族）",
          "kind": "harmony-dts",
          "where": "openharmony/ets/component/span.d.ts SpanAttribute.textShadow",
          "quote": "textShadow(value: ShadowOptions | Array<ShadowOptions>): SpanAttribute;",
          "version": "API 23（HarmonyOS 6.1.0）"
        },
        {
          "what": "TextClock 的 textShadow（同族）",
          "kind": "harmony-dts",
          "where": "openharmony/ets/component/text_clock.d.ts TextClockAttribute.textShadow",
          "quote": "textShadow(value: ShadowOptions | Array<ShadowOptions>): TextClockAttribute;",
          "version": "API 23（HarmonyOS 6.1.0）"
        },
        {
          "what": "TextTimer 的 textShadow（同族）",
          "kind": "harmony-dts",
          "where": "openharmony/ets/component/text_timer.d.ts TextTimerAttribute.textShadow",
          "quote": "textShadow(value: ShadowOptions | Array<ShadowOptions>): TextTimerAttribute;",
          "version": "API 23（HarmonyOS 6.1.0）"
        }
      ]
    }
  ],
  "left_out": [
    {
      "text": "映射参考与组件 API 语义冲突时以 API 语义为准，并同步修正参考里的 shadow* 与 layout_gravity 条目",
      "reason": "没有产物里看得到的触发"
    },
    {
      "text": "建议 1、2、4（背景层高度、叠层定位、图像效果）实际提炼时各写成规矩；格式样例只展开文字阴影这一条",
      "reason": "其他：格式样例只展开一条"
    }
  ],
  "corrections": [],
  "gaps": [],
  "conflicts": []
}
```

呈现出来：

```
# TextView 带文字阴影属性时，目标用 Text.textShadow，不用 .shadow

审的是：代码
触发（任一种）：
- 读到：TextView 或它引用的样式里有 android:shadowColor / shadowRadius / shadowDx / shadowDy；写错的样子：对应的 Text 上写的是 .shadow(...)，或者没有阴影
适用范围：安卓 TextView（含它引用的 style、textAppearance）带文字阴影属性，迁成 ArkUI Text 时
做法：
- 写成 Text(...).textShadow({ radius: <shadowRadius>, color: <shadowColor>, offsetX: <shadowDx>, offsetY: <shadowDy> })；.shadow(...) 只留给组件框阴影
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- textShadow(value: ShadowOptions | Array<ShadowOptions>): TextAttribute：Text 的文字阴影，可传一个或一组 ShadowOptions（出处：鸿蒙 SDK 的 ets/component/text.d.ts，TextAttribute.textShadow）
- ShadowOptions 的 radius、offsetX、offsetY 单位是 px：源端四个值照搬数值，不乘密度，不转成 vp（出处：鸿蒙 SDK 的 ets/component/common.d.ts，ShadowOptions）
- shadowRadius、shadowDx、shadowDy 的 format 是 float：源端这几个值是不带单位的浮点数，TextView 用 getFloat 读出后原样交给 setShadowLayer（出处：Android SDK 平台资源 data/res/values/attrs.xml，TextAppearance 的 shadowRadius（按应用的 compileSdk 取对应平台）；android.widget.TextView#readTextAppearance）
- shadow(value: ShadowOptions | ShadowStyle): T：给组件本身加阴影，不是文字阴影（出处：鸿蒙 SDK 的 ets/component/common.d.ts，CommonMethod.shadow）
- textShadow(value: ShadowOptions | Array<ShadowOptions>): SpanAttribute：同族接口：Span 的文字阴影（出处：鸿蒙 SDK 的 ets/component/span.d.ts，SpanAttribute.textShadow）
- textShadow(value: ShadowOptions | Array<ShadowOptions>): TextClockAttribute：同族接口：TextClock 的文字阴影（出处：鸿蒙 SDK 的 ets/component/text_clock.d.ts，TextClockAttribute.textShadow）
- textShadow(value: ShadowOptions | Array<ShadowOptions>): TextTimerAttribute：同族接口：TextTimer 的文字阴影（出处：鸿蒙 SDK 的 ets/component/text_timer.d.ts，TextTimerAttribute.textShadow）
未核实：同一个 radius 数值两边的模糊程度是否一样
来源：1 张卡，1 个应用
```

第三层索引的一行（候选还没有规矩号，暂用「卡号#序号」）：

```
- case-4f627840679361f165a3#1｜TextView 带文字阴影属性时，目标用 Text.textShadow，不用 .shadow｜读到：TextView 或它引用的样式里有 android:shadowColor / shadowRadius / shadowDx / shadowDy；写错：对应的 Text 上写的是 .shadow(...)，或者没有阴影
```

## 8. 例子二：规格类（自绘画布的单位契约）

出自另一张卡的第 1 条建议：规格阶段对自绘画布只写一份单位契约。审的是规格文档，所以 `wrong` 写规格里看得到的说法；取值查了 `canvas.d.ts` 和 `Graphics.d.ts`，卡里上机看到的行为写成「卡里修好并验证过」。这张卡里讲代码怎么写的建议，实际提炼时另写成代码类的规矩。

```json
{
  "case": "case-caa0a4c6289286b0e6ba",
  "rules": [
    {
      "title": "自绘画布的规格只写一份单位契约，写明上下文构造和各量的单位",
      "product": "规格",
      "triggers": [
        {
          "read": "安卓自定义 View 在 onSizeChanged 的 int px 尺寸上推导布局，Paint.setTextSize / measureText 按 px 算字号和间距",
          "wrong": "规格里画布单位的说法不止一处且互相矛盾（字体串写 px、坐标映射写 vp），或者没写 CanvasRenderingContext2D 用哪个构造、默认按什么单位"
        }
      ],
      "scope": "把安卓自绘 View 迁成 ArkUI Canvas 时，规格里写画布单位的那一节",
      "exceptions": [],
      "how": [
        {
          "text": "规格里只写一份画布单位契约：上下文怎么构造（new CanvasRenderingContext2D(settings) 按默认 vp，或 new CanvasRenderingContext2D(settings, LengthMetricsUnit.PX) 按 px），以及字体串后缀、measureText 结果、ctx.width、触点坐标、窗口避让值和 dp 常量各自的单位",
          "support": [
            "case-caa0a4c6289286b0e6ba#recommendation:1"
          ]
        },
        {
          "text": "各功能的映射表都引用这一份契约，不各写各的单位",
          "support": [
            "case-caa0a4c6289286b0e6ba#recommendation:1"
          ]
        }
      ],
      "values": [
        {
          "value": "constructor(settings?: RenderingContextSettings, unit?: LengthMetricsUnit)",
          "meaning": "CanvasRenderingContext2D 的构造，第二个参数定单位",
          "source": "鸿蒙 SDK 的 ets/component/canvas.d.ts，CanvasRenderingContext2D.constructor",
          "support": []
        },
        {
          "value": "LengthMetricsUnit.DEFAULT = 0（vp）、LengthMetricsUnit.PX = 1",
          "meaning": "单位模式的两个取值，DEFAULT 是 vp",
          "source": "鸿蒙 SDK 的 ets/api/arkui/Graphics.d.ts，LengthMetricsUnit",
          "support": []
        },
        {
          "value": "默认构造的上下文按 vp 解释字号和坐标；改成 LengthMetricsUnit.PX 构造后字号、测宽、几何、触点与安卓 View/Paint 同为 px",
          "meaning": "契约里写哪种构造，决定了其余各量要不要换算",
          "source": "卡里修好并验证过",
          "support": [
            "case-caa0a4c6289286b0e6ba#diagnosis"
          ]
        },
        {
          "value": "constructor(width: number, height: number, settings?: RenderingContextSettings, unit?: LengthMetricsUnit)",
          "meaning": "同族接口：OffscreenCanvasRenderingContext2D 的构造，同样用 unit 定单位",
          "source": "鸿蒙 SDK 的 ets/component/canvas.d.ts，OffscreenCanvasRenderingContext2D.constructor",
          "support": []
        },
        {
          "value": "constructor(width: number, height: number, unit: LengthMetricsUnit)",
          "meaning": "同族接口：OffscreenCanvas 的构造",
          "source": "鸿蒙 SDK 的 ets/component/canvas.d.ts，OffscreenCanvas.constructor",
          "support": []
        },
        {
          "value": "constructor(unit?: LengthMetricsUnit)",
          "meaning": "同族接口：DrawingRenderingContext 的构造",
          "source": "鸿蒙 SDK 的 ets/component/canvas.d.ts，DrawingRenderingContext.constructor",
          "support": []
        }
      ],
      "lookups": [],
      "why": "单位没定下来时各写者按各自理解混用：px 字号被当成 vp、measureText 偏小、已换算的触点和没换算的几何比较而点不中",
      "keys": {
        "read": [
          "onSizeChanged",
          "Paint",
          "setTextSize",
          "measureText",
          "Canvas",
          "onDraw",
          "dp"
        ],
        "product": [
          "CanvasRenderingContext2D",
          "LengthMetricsUnit",
          "LengthMetricsUnit.PX",
          "measureText",
          "vp2px",
          "px",
          "vp"
        ]
      },
      "probe": null,
      "unverified": [],
      "alternatives_unverified": [],
      "siblings_checked": "搜 LengthMetricsUnit：canvas.d.ts 里构造带它的有 Path2D、ImageBitmap、ImageData、CanvasRenderingContext2D、OffscreenCanvasRenderingContext2D、OffscreenCanvas、DrawingRenderingContext；和画布上下文单位契约相关的后三个写进 values",
      "refs": [
        {
          "what": "CanvasRenderingContext2D 带 unit 的构造",
          "kind": "harmony-dts",
          "where": "openharmony/ets/component/canvas.d.ts CanvasRenderingContext2D.constructor",
          "quote": "constructor(settings?: RenderingContextSettings, unit?: LengthMetricsUnit);",
          "version": "API 23（HarmonyOS 6.1.0）"
        },
        {
          "what": "LengthMetricsUnit 的默认是 vp",
          "kind": "harmony-dts",
          "where": "openharmony/ets/api/arkui/Graphics.d.ts LengthMetricsUnit",
          "quote": "The default length metrics unit, in vp. * * @syscap SystemCapability.ArkUI.ArkUI.Full * @crossplatform * @atomicservice * @since 12 */ DEFAULT = 0,",
          "version": "API 23（HarmonyOS 6.1.0）"
        },
        {
          "what": "LengthMetricsUnit.PX",
          "kind": "harmony-dts",
          "where": "openharmony/ets/api/arkui/Graphics.d.ts LengthMetricsUnit.PX",
          "quote": "The pixel length metrics unit. * * @syscap SystemCapability.ArkUI.ArkUI.Full * @crossplatform * @atomicservice * @since 12 */ PX = 1",
          "version": "API 23（HarmonyOS 6.1.0）"
        },
        {
          "what": "OffscreenCanvasRenderingContext2D 带 unit 的构造（同族）",
          "kind": "harmony-dts",
          "where": "openharmony/ets/component/canvas.d.ts OffscreenCanvasRenderingContext2D.constructor",
          "quote": "constructor(width: number, height: number, settings?: RenderingContextSettings, unit?: LengthMetricsUnit);",
          "version": "API 23（HarmonyOS 6.1.0）"
        },
        {
          "what": "OffscreenCanvas 带 unit 的构造（同族）",
          "kind": "harmony-dts",
          "where": "openharmony/ets/component/canvas.d.ts OffscreenCanvas.constructor",
          "quote": "constructor(width: number, height: number, unit: LengthMetricsUnit);",
          "version": "API 23（HarmonyOS 6.1.0）"
        },
        {
          "what": "DrawingRenderingContext 带 unit 的构造（同族）",
          "kind": "harmony-dts",
          "where": "openharmony/ets/component/canvas.d.ts DrawingRenderingContext.constructor",
          "quote": "Create DrawingRenderingContext with setting LengthMetricsUnit.",
          "version": "API 23（HarmonyOS 6.1.0）"
        },
        {
          "what": "DrawingRenderingContext 的构造签名（同族）",
          "kind": "harmony-dts",
          "where": "openharmony/ets/component/canvas.d.ts DrawingRenderingContext.constructor",
          "quote": "constructor(unit?: LengthMetricsUnit);",
          "version": "API 23（HarmonyOS 6.1.0）"
        }
      ]
    }
  ],
  "left_out": [
    {
      "text": "接手他人写下的单位约定与规格冲突时，先用平台声明或一次 ctx.width / measureText 日志求证再统一",
      "reason": "没有产物里看得到的触发"
    },
    {
      "text": "建议 2、3（按源端运算域选构造、逐项换算跨域输入）实际提炼时写成代码类规矩；格式样例只展开规格这一条",
      "reason": "其他：格式样例只展开一条"
    }
  ],
  "corrections": [],
  "gaps": [],
  "conflicts": []
}
```

呈现出来：

```
# 自绘画布的规格只写一份单位契约，写明上下文构造和各量的单位

审的是：规格
触发（任一种）：
- 读到：安卓自定义 View 在 onSizeChanged 的 int px 尺寸上推导布局，Paint.setTextSize / measureText 按 px 算字号和间距；写错的样子：规格里画布单位的说法不止一处且互相矛盾（字体串写 px、坐标映射写 vp），或者没写 CanvasRenderingContext2D 用哪个构造、默认按什么单位
适用范围：把安卓自绘 View 迁成 ArkUI Canvas 时，规格里写画布单位的那一节
做法：
- 规格里只写一份画布单位契约：上下文怎么构造（new CanvasRenderingContext2D(settings) 按默认 vp，或 new CanvasRenderingContext2D(settings, LengthMetricsUnit.PX) 按 px），以及字体串后缀、measureText 结果、ctx.width、触点坐标、窗口避让值和 dp 常量各自的单位
- 各功能的映射表都引用这一份契约，不各写各的单位
已核实的写法和取值（核实时用的是鸿蒙 SDK API 23）：
- constructor(settings?: RenderingContextSettings, unit?: LengthMetricsUnit)：CanvasRenderingContext2D 的构造，第二个参数定单位（出处：鸿蒙 SDK 的 ets/component/canvas.d.ts，CanvasRenderingContext2D.constructor）
- LengthMetricsUnit.DEFAULT = 0（vp）、LengthMetricsUnit.PX = 1：单位模式的两个取值，DEFAULT 是 vp（出处：鸿蒙 SDK 的 ets/api/arkui/Graphics.d.ts，LengthMetricsUnit）
- 默认构造的上下文按 vp 解释字号和坐标；改成 LengthMetricsUnit.PX 构造后字号、测宽、几何、触点与安卓 View/Paint 同为 px：契约里写哪种构造，决定了其余各量要不要换算（出处：卡里修好并验证过）
- constructor(width: number, height: number, settings?: RenderingContextSettings, unit?: LengthMetricsUnit)：同族接口：OffscreenCanvasRenderingContext2D 的构造，同样用 unit 定单位（出处：鸿蒙 SDK 的 ets/component/canvas.d.ts，OffscreenCanvasRenderingContext2D.constructor）
- constructor(width: number, height: number, unit: LengthMetricsUnit)：同族接口：OffscreenCanvas 的构造（出处：鸿蒙 SDK 的 ets/component/canvas.d.ts，OffscreenCanvas.constructor）
- constructor(unit?: LengthMetricsUnit)：同族接口：DrawingRenderingContext 的构造（出处：鸿蒙 SDK 的 ets/component/canvas.d.ts，DrawingRenderingContext.constructor）
来源：1 张卡，1 个应用
```

第三层索引的一行：

```
- case-caa0a4c6289286b0e6ba#1｜自绘画布的规格只写一份单位契约，写明上下文构造和各量的单位｜读到：安卓自定义 View 在 onSizeChanged 的 int px 尺寸上推导布局，Paint.setTextSize / measureText 按 px 算字号和间距；写错：规格里画布单位的说法不止一处且互相矛盾（字体串写 px、坐标映射写 vp），或者没写 CanvasRenderingContext2D 用哪个构造、默认按什么单位
```
