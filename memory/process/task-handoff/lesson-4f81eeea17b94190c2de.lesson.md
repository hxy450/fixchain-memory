# 要靠其他文件或任务补实现的功能，登记成带负责方、验证方式和源端确定值的移交项，不只写在注释或动作摘要里

ID：`lesson-4f81eeea17b94190c2de` · 版本：14

[本主题](index.md)

## 何时使用

页面转换、切片实现、基础设施实现或接线阶段，本文件的功能需要别的文件补调用点、或要由后续步骤补值才完整时（包括留下前向引用、TODO 占位、需要在入口调用的初始化函数），以及读到上游留给本文件的移交说明时；以及修复轮核出、但决定本轮不修的相邻偏差时

## 适用情境

写码者确认某项行为在当前文件里无法闭合（例如非入口组件的平台回调要由入口页转发、宿主回调留给接线切片、脚手架身份值留给后续步骤、新建的 init 要由入口调用、UI 转换阶段先留业务占位），工程提供了移交登记约定（如带 owner/what/verify 的 HANDOFF 标记、前向引用登记表、返回信封中的字段）；或接线者在上游文件头读到要求本文件转发的说明。也包括写者读到源端宿主或子类对共享组件的改写、自己不能改共享文件，只在转换报告里记“保真缺口”；以及 UI 阶段规格写明交互留给后续切片，写者准备照兄弟页写成真实但不符合源端的实现。

## 原因

文件头注释和报告里的开放问题不进入任何检查：编译、结构审计都会放行，后续编排与复核也容易按“已处理”理解；登记只写动作摘要时，写前已读到的源端细节在交接中丢失，接手者只能猜。来源中页面转换者已从 SDK 注释核到平台限制，也起草了指向壳页切片的移交，落盘时删掉，只留文件头说明；资源任务在返回里只写“归属后续步骤”；另一应用里转换者读到了更新卡的确切网址、克隆名的本地化后缀和“以编辑草稿为克隆内容”，登记只写“更新卡外链”“复制并重建列表栈”，接手者没读源码，写了猜测的网址和按持久化数据、原名克隆。第三个应用里，网络层实现者写了必须在入口调用的 init，回报却写“无待接线项”；UI 转换留下的 TODO 只写了调用名，写引导完成标记和失败提示这两项在交接中丢失。另一应用中，UI 转换者读到容器按持久化的选中项恢复当前页、切页时回写选中项，却只留下只含 P-ID 的前向钩子，接线者照钩子名接线，恢复与回写都丢了；另一转换者把选城后回天气 Tab、列表为空进入添加页也只登记为槽名。另一应用的修复轮读到源端省份门控，把无条件调用列为既有偏差，却以“不在本轮范围”保留且未登记；上下文压缩后这条判断丢失，后续诊断把同一问题误判为服务端故障。

## 做法

1. 按工程的移交约定登记：写明负责方（具体切片或阶段）、要补什么、如何验证；验证断言难写时改用切片级断言（如 slice:N），移交本身保留。 负责方必须在计划账本中确有对应 Step、wires 或工件：resolve_by 不沿用派工前缀里的切片编号，也不指向计划中只做 stub、没有 wires 的切片；拿不准就先读目标切片计划。
2. 登记里写入已读到的源端确定值与出处：网址、常量、比较符、参数来源（持久化值还是编辑草稿）、字段变换、完成后的导航（延后的跳转写明规格导航表或源端 Intent 给出的目标页，不只登记触发事件名）；UI 转换阶段先留业务占位时，TODO 里写清源端完整的成功与失败动作（写标记、跳转、关页、失败提示），只写调用名不够。
3. 按分工保留应由别人处理的值时，在返回里逐项列出保留的键或片段，以及应接手的步骤；新建的初始化函数需要在入口调用而本任务不能改入口时，列出文件、生命周期方法和调用语句，不写“无前向引用”。
4. 接线时读到上游文件要求本文件转发或补调用点，就在本文件实现；派工不允许或实现不了时作为阻塞项上报。接手者从登记里取不到确切值时，打开出处源码取值，取不到就登记缺口，不写推测值。
5. 派工只允许写本文件、而源端依赖的共享组件或工具还没有目标文件时，在本文件按源实现等价逻辑并登记待收敛项（指向将来的共享实现与负责切片），或登记前向引用交给后续切片；不要静默省略，也不让未登记的页内实现留到交付。
6. 修复轮核出、但本轮不修的相邻偏差，当轮写入持久的偏差台账（如迁移报告的“已知未修偏差”），写明源端条件与文件位置；不只留在思考或会话上下文里，压缩会丢掉这类判断。
7. 当场做不完的源行为登记为占位，不只写进报告的“保真缺口”；UI 阶段规格写明交互留给后续切片时登记占位，不照兄弟页写成与源端不符的真实实现。

来源支持：38 张卡 · 已知 14 次迁移（部分未记录） · 已知 13 个应用（部分未记录）

## 来源（按需复核）

- [case-036361d8949e7daf5247](../../../store/cases/case-036361d8949e7daf5247/c13fd2d3c873845a6b80e49b91ae8bf21a59ba21b8c781410440623289dcfa79.json) · 结论：recommendation:1
  卡片版本：`c13fd2d3c873845a6b80e49b91ae8bf21a59ba21b8c781410440623289dcfa79`
- [case-07655e78d2a5ab769146](../../../store/cases/case-07655e78d2a5ab769146/abd71acc4b5a73c206e8a4f93e18a878cb83cb6a9531a303afdac6bceea12b2c.json) · 结论：recommendation:3
  卡片版本：`abd71acc4b5a73c206e8a4f93e18a878cb83cb6a9531a303afdac6bceea12b2c`
- [case-0ac442a09e1e8ee36a8a](../../../store/cases/case-0ac442a09e1e8ee36a8a/a8ef5f4a3b6e86969bb09b0df9de25820f2b67887ac0349a98141071b3b6b276.json) · 结论：recommendation:1
  卡片版本：`a8ef5f4a3b6e86969bb09b0df9de25820f2b67887ac0349a98141071b3b6b276`
- [case-1446bd8a3fc8a14b0a94](../../../store/cases/case-1446bd8a3fc8a14b0a94/fb6e49bb5629713c24983914208eda2fefbcb3374a3527d8ea29e518d7f15e63.json) · 结论：recommendation:4
  卡片版本：`fb6e49bb5629713c24983914208eda2fefbcb3374a3527d8ea29e518d7f15e63`
- [case-1cad884865343910ce02](../../../store/cases/case-1cad884865343910ce02/27369625dcbbe450f68beab2e162e179bde87573f0d20d5282655293b42e24d3.json) · 结论：recommendation:2
  卡片版本：`27369625dcbbe450f68beab2e162e179bde87573f0d20d5282655293b42e24d3`
- [case-1f17a64b74c60410dad7](../../../store/cases/case-1f17a64b74c60410dad7/8e0d833e1ec049602448b98b40481752caa27492fad8263692b5827d57da6ae7.json) · 结论：recommendation:2
  卡片版本：`8e0d833e1ec049602448b98b40481752caa27492fad8263692b5827d57da6ae7`
- [case-2880da61086b19aff2a4](../../../store/cases/case-2880da61086b19aff2a4/73345ae8b0a7d830ecb8996008d7c6c86c777fee1e5d5f115931faea4d82fc25.json) · 结论：diagnosis, recommendation:1, recommendation:2
  卡片版本：`73345ae8b0a7d830ecb8996008d7c6c86c777fee1e5d5f115931faea4d82fc25`
- [case-2906493a39c662495a11](../../../store/cases/case-2906493a39c662495a11/5503aea0839a4e315ea963b02fa35fa9972a6a153c491c611c21b9a9e339c608.json) · 结论：recommendation:5
  卡片版本：`5503aea0839a4e315ea963b02fa35fa9972a6a153c491c611c21b9a9e339c608`
- [case-2b9869554cf9027174a0](../../../store/cases/case-2b9869554cf9027174a0/399f7b12747efb0e2c5ee69d85083f67576d91c11b7c8f93adacb6d0713f92f6.json) · 结论：diagnosis, recommendation:2, recommendation:3
  卡片版本：`399f7b12747efb0e2c5ee69d85083f67576d91c11b7c8f93adacb6d0713f92f6`
- [case-3094b57f19bdd601c03e](../../../store/cases/case-3094b57f19bdd601c03e/9d34746173f7a47aae89f921c5b451e93ee5312a94b4f1bd66a04f4d6df54dff.json) · 结论：recommendation:3
  卡片版本：`9d34746173f7a47aae89f921c5b451e93ee5312a94b4f1bd66a04f4d6df54dff`
- [case-37a2c6aacb67d1fc0aee](../../../store/cases/case-37a2c6aacb67d1fc0aee/528d09b041c06639c78c05521087576cda7b79594f84cb4fcc278d8c2c62a75b.json) · 结论：diagnosis, recommendation:2, recommendation:3
  卡片版本：`528d09b041c06639c78c05521087576cda7b79594f84cb4fcc278d8c2c62a75b`
- [case-3ca3658855acd903c4ca](../../../store/cases/case-3ca3658855acd903c4ca/d0ba935e82dce8bcb9f5694089a9e6dbc438222f1b51a6dcd0b46a87967216cb.json) · 结论：recommendation:5
  卡片版本：`d0ba935e82dce8bcb9f5694089a9e6dbc438222f1b51a6dcd0b46a87967216cb`
- [case-4171cd43bbb420b4ee40](../../../store/cases/case-4171cd43bbb420b4ee40/0effbd77c7fda6b589b47193aaa322f49d48b23605a26ca7e52f15d9786494aa.json) · 结论：recommendation:3, recommendation:4
  卡片版本：`0effbd77c7fda6b589b47193aaa322f49d48b23605a26ca7e52f15d9786494aa`
- [case-47b9e1107e4e4ecd40bd](../../../store/cases/case-47b9e1107e4e4ecd40bd/87b0c345ca3fa21bf70b01c74e3a2714a0880c4a2e5531942fe4d81a24d85b98.json) · 结论：recommendation:6
  卡片版本：`87b0c345ca3fa21bf70b01c74e3a2714a0880c4a2e5531942fe4d81a24d85b98`
- [case-4ecfc0b10264caacad49](../../../store/cases/case-4ecfc0b10264caacad49/23ae043b4ec073a5f76c24cd0e8182ec63aae669f723a247cb685df9abde36f2.json) · 结论：diagnosis, recommendation:1
  卡片版本：`23ae043b4ec073a5f76c24cd0e8182ec63aae669f723a247cb685df9abde36f2`
- [case-56249562721f5dc59148](../../../store/cases/case-56249562721f5dc59148/96d52a064d3d02462086e833baf21aa8445479ee8ee000c27f3518b1a0190861.json) · 结论：recommendation:2
  卡片版本：`96d52a064d3d02462086e833baf21aa8445479ee8ee000c27f3518b1a0190861`
- [case-5dc757ad90507a893798](../../../store/cases/case-5dc757ad90507a893798/18a2456f40974f82b2393cee85af61357923b351dd4954b8d0c59ab3a2a01bfb.json) · 结论：recommendation:3
  卡片版本：`18a2456f40974f82b2393cee85af61357923b351dd4954b8d0c59ab3a2a01bfb`
- [case-64c8bd68e3bebd236c4d](../../../store/cases/case-64c8bd68e3bebd236c4d/f72244f7e6abf869ef8b6d570535554f85813bc64a8527e19c39c5b8e5134599.json) · 结论：recommendation:3
  卡片版本：`f72244f7e6abf869ef8b6d570535554f85813bc64a8527e19c39c5b8e5134599`
- [case-74192ad19ea88a31750b](../../../store/cases/case-74192ad19ea88a31750b/26f7ae0418e6dd6e5aa696876d4ecf0054271a1dbd8a8458dc0a1a8c62388566.json) · 结论：recommendation:1
  卡片版本：`26f7ae0418e6dd6e5aa696876d4ecf0054271a1dbd8a8458dc0a1a8c62388566`
- [case-76fcde297f6a5406e58f](../../../store/cases/case-76fcde297f6a5406e58f/4fe7565a766323ef4f1d2f178dcd030e8db4d702b78336c519b17cf80d48da0d.json) · 结论：recommendation:4
  卡片版本：`4fe7565a766323ef4f1d2f178dcd030e8db4d702b78336c519b17cf80d48da0d`
- [case-7aad6dd3649e8ed51a17](../../../store/cases/case-7aad6dd3649e8ed51a17/698a09982d97a56c5d6e5616d835be92d2ad703bf9dd02dbaa4cc04bdac4e0dc.json) · 结论：recommendation:1
  卡片版本：`698a09982d97a56c5d6e5616d835be92d2ad703bf9dd02dbaa4cc04bdac4e0dc`
- [case-7b64dd743c1260eb910f](../../../store/cases/case-7b64dd743c1260eb910f/298567a76aee47097df89ce461b5d22ce36838d3b34afa1f21008596f2358535.json) · 结论：recommendation:3
  卡片版本：`298567a76aee47097df89ce461b5d22ce36838d3b34afa1f21008596f2358535`
- [case-8128c57ee5fb2e4f49d1](../../../store/cases/case-8128c57ee5fb2e4f49d1/d0184e877064d037eceb8bc968cb0949b5d0bffb239f02ec1d1a93bf7a391713.json) · 结论：recommendation:3
  卡片版本：`d0184e877064d037eceb8bc968cb0949b5d0bffb239f02ec1d1a93bf7a391713`
- [case-8555b02fdd531952938b](../../../store/cases/case-8555b02fdd531952938b/2c653cb3c662f222539425f30a42c5c464378add268afd8085c556bada7a052d.json) · 结论：recommendation:1
  卡片版本：`2c653cb3c662f222539425f30a42c5c464378add268afd8085c556bada7a052d`
- [case-8ffd5b5f684871fbeb3a](../../../store/cases/case-8ffd5b5f684871fbeb3a/48358a1b56ec7bb9e5a8f6f37ed576ef2bfcd0bf3547cfaff10333c86766d289.json) · 结论：recommendation:2
  卡片版本：`48358a1b56ec7bb9e5a8f6f37ed576ef2bfcd0bf3547cfaff10333c86766d289`
- [case-90117ca805576dda1534](../../../store/cases/case-90117ca805576dda1534/d69f7835e048a354e4c7c612b2f7e0328d97fd7ba75e120259ab9422d1065342.json) · 结论：recommendation:4
  卡片版本：`d69f7835e048a354e4c7c612b2f7e0328d97fd7ba75e120259ab9422d1065342`
- [case-9618601c4a21f2f18560](../../../store/cases/case-9618601c4a21f2f18560/870a2d98075a73dc88a2cfd3ac2fb801bc3d216cf1120c6f9583496d9f1c6941.json) · 结论：recommendation:4
  卡片版本：`870a2d98075a73dc88a2cfd3ac2fb801bc3d216cf1120c6f9583496d9f1c6941`
- [case-9720ed67e580c21dbd65](../../../store/cases/case-9720ed67e580c21dbd65/e28f20a327f221aadfca37acb42f61db9e173a49a49fc0416d970ee8aeafb602.json) · 结论：recommendation:2
  卡片版本：`e28f20a327f221aadfca37acb42f61db9e173a49a49fc0416d970ee8aeafb602`
- [case-97e280ce0a8ddc7a54a1](../../../store/cases/case-97e280ce0a8ddc7a54a1/4fbcf9675b2ae7f717f11ff33565c2292c0c6ff00c290102009285e9705600e8.json) · 结论：recommendation:2
  卡片版本：`4fbcf9675b2ae7f717f11ff33565c2292c0c6ff00c290102009285e9705600e8`
- [case-9d195db79dc4cccc7d1a](../../../store/cases/case-9d195db79dc4cccc7d1a/3ef58b6e05f43ead616304c92324166e074aa81e33e4c6ecad7b4910b60126e9.json) · 结论：recommendation:6
  卡片版本：`3ef58b6e05f43ead616304c92324166e074aa81e33e4c6ecad7b4910b60126e9`
- [case-9d3828c851006d29fc06](../../../store/cases/case-9d3828c851006d29fc06/c198fe473f6d3c9d774f95de74c649d6542ab966ab417df2dcb1881819cb4366.json) · 结论：recommendation:4
  卡片版本：`c198fe473f6d3c9d774f95de74c649d6542ab966ab417df2dcb1881819cb4366`
- [case-9f9881c4a9db00d14d07](../../../store/cases/case-9f9881c4a9db00d14d07/7112bcd3f96e30d029bb4a952c0f31ba43b6c4c490f4d17be1641d5148185649.json) · 结论：recommendation:3
  卡片版本：`7112bcd3f96e30d029bb4a952c0f31ba43b6c4c490f4d17be1641d5148185649`
- [case-be2a579e8fcdcb8b0a16](../../../store/cases/case-be2a579e8fcdcb8b0a16/9c98f133d2d180ce8945ef872ba85a87c32bae1189de1efd3949fb241137d4c5.json) · 结论：recommendation:5
  卡片版本：`9c98f133d2d180ce8945ef872ba85a87c32bae1189de1efd3949fb241137d4c5`
- [case-cbf23fa7a4ed42d37671](../../../store/cases/case-cbf23fa7a4ed42d37671/013c03becf2fdb81fe5d3bb32c60d6635f41ed3de130131a61605958b50d27f5.json) · 结论：recommendation:3
  卡片版本：`013c03becf2fdb81fe5d3bb32c60d6635f41ed3de130131a61605958b50d27f5`
- [case-d9c2b75062eb57796ca2](../../../store/cases/case-d9c2b75062eb57796ca2/c0e0684d2567560ee8d44f49d9c8eb3a4d4b3cc9ba5d7380a8e25a3b0f7792e8.json) · 结论：recommendation:3
  卡片版本：`c0e0684d2567560ee8d44f49d9c8eb3a4d4b3cc9ba5d7380a8e25a3b0f7792e8`
- [case-ef4b9ae3acaea9323135](../../../store/cases/case-ef4b9ae3acaea9323135/224b39c5df19751e0b18f8c6328b47d00202ad917de1149b4faf5dde5c73fe9d.json) · 结论：diagnosis, recommendation:1
  卡片版本：`224b39c5df19751e0b18f8c6328b47d00202ad917de1149b4faf5dde5c73fe9d`
- [case-f3d590ba381f544833aa](../../../store/cases/case-f3d590ba381f544833aa/325219ee0b387ba129bb7f81d453f59f12c49ab4a600282dca41d129b45ee3f4.json) · 结论：recommendation:3
  卡片版本：`325219ee0b387ba129bb7f81d453f59f12c49ab4a600282dca41d129b45ee3f4`
- [case-fc321fcee197b47d1335](../../../store/cases/case-fc321fcee197b47d1335/c05e6553920599c50266d3ae6369c9b824cbb8e189aab08f73d7d25d4843b59b.json) · 结论：diagnosis, recommendation:1
  卡片版本：`c05e6553920599c50266d3ae6369c9b824cbb8e189aab08f73d7d25d4843b59b`
