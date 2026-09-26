我们试图定义一种以人为中心的Agent Harness。目前的Agent Harness如Codex，Claude Code等突出的是Agent无干预长时间运行的能力。它们的设计哲学是它们能够接管人类的工作，在无人类干预的情况下端到端地给出结果。包括近期火爆的loop工程，以及自进化Agent，其指向的目标都是Agent在工作中需要越来越少的人类干预，最终自动运行。这种把人类从工作流程中去掉的Agent设计哲学对于人类不愿意做的事情非常有用，然而对于人类真正关心的事情，实际上是剥夺了人类对自己意义的掌控和参与。我认为需要一种与人更好协作的新的Agent范式，它非常人类中心，不替代人类做他必要的劳动，而是提供必要的、甚至人类自己也没意识到的辅助，让人类在帮助中成长为更好的自己。

这也是一种更加highly-efficient的使用token的方式。对于人类关注的任务，任何AI generated但无法触动人类，无法让人类认同的内容都是在浪费token。例如，我可以让AI生成这种Agent harness的核心功能，但是于我没有任何触动，于后续的设计思考没有任何帮助。我可以说这部分token就是完全被浪费了的。

**拉屎递纸原则**
目前的Agent harness是，人类想拉屎，然后Agent把屎拉出来了，要求人类批准这坨屎是人类的屎。人类中心的Agent harness是，人类想拉屎，Agent做好马桶、纸巾，递上手机，让人畅快拉屎。不需要人审批，不需要人同意。
很多所谓 human-in-the-loop 其实只是：agent 把人的工作做了，然后把人降级成审批按钮。这仍然是在剥夺人的主体动作。人看似在 loop 里，实际上已经不在 work 里。人类中心 harness 更像：

> **agent 不替人完成主体动作，而是布置让人能更顺畅完成主体动作的环境。**

这里真正的区别是：

| 类型                     | Agent 做什么          | 人做什么         |
| ---------------------- | ------------------ | ------------ |
| 当前 agent harness       | 替人执行主体任务，然后请求批准    | 审批 / 驳回      |
| human-centered harness | 准备环境、材料、工具、节奏、恢复状态 | 亲自完成有意义的主体动作 |

这也说明“人类中心”不是“多问人几次”“多让人批准几次”。那只是把剥夺变得礼貌一点。真正的人类中心是：**人不需要批准自己正在做的事，因为事情本来就是人在做。**

放回 founder-skill：

错误形态是：

> founder 想判断一个 idea 值不值得做，agent 直接分析完，给出结论，让 founder approve。

正确形态是：

> founder 想判断一个 idea，agent 把访谈材料整理好，把过去的旧思考链路展示出来，让founder可以顺畅地标出矛盾标，整理产品假设，分析下一步动作，自己进入判断。

所谓让证据更清楚，假设更暴露等功能本身不重要，重要的是它们是否服务于这个原则：

> **主体动作不可替代：不要替代主体动作，只消除主体动作周围的摩擦。**

它对 harness 设计的影响很大：
- 最好的 AI 输出有时是不输出，而是把材料摆好。
- 最好的自动化有时不是完成任务，而是让人更容易进入状态。
- 最差的 token 浪费，是 AI 抢先生成一堆“正确但无触动”的内容。
- 评测不该只看 agent 有没有完成任务，而要看人有没有更顺畅地完成自己的任务。
- approval 不是主体性的证据，参与才是。

所以重新定义这个 harness：
> Human-centered Agent Harness 是一种环境支架型 agent harness。它不以端到端替人完成任务为目标，而以维护人的主体动作、降低其周边摩擦、增强其判断与参与为目标。

一种对human-centered的常见误区是`judgment-preserving` ，它强调的是：Agent 不应该替人完成关键判断。它可以整理证据、暴露假设、指出矛盾、准备候选动作，但最终的取舍、承诺、风险下注和意义判断仍然属于人。这个概念已经比普通的 `human-in-the-loop` 更进一步，因为它不满足于“让人审批”，而是要求系统保留人的判断权。

但“主体动作”比 `judgment-preserving` 还更准确。因为人真正需要被保护的，不只是判断这一种心理活动，而是那些构成“我正在亲自做这件事”的核心动作。判断只是其中一种。写作、研究、创业、学习、创作、谈话、决定人生方向，都可能是这种主体动作。

在这些任务里，人的价值不只体现在最后点头或否决，而体现在亲自经历那个形成过程：困惑、试探、组织语言、面对矛盾、改变想法、做出取舍。Agent 如果直接把结果生成出来，即使结果有道理，也可能绕过了最重要的部分。它把人从自己的任务里移开，只留下一个审批位置。

所以，人类中心的 Agent Harness 不应该把目标设为“替人完成更多主体动作”，而应该识别哪些动作必须由人亲自完成，并围绕这些动作布置环境。它要做的是准备材料、降低摩擦、恢复状态、递上工具、提醒风险、保存痕迹，而不是替人把那件事做掉。

`AI Architect` 的三个原则：`frictionless interaction`、`contextual intelligence`、`proactive intelligence`，和 human-centered harness 不是同一层级的概念。前三者更像产品能力原则，回答的是：一个 AI-native system 怎样更自然地进入用户工作流，怎样理解上下文，怎样在合适的时候主动出现。Human-centered harness 则更像一条人机关系原则，回答的是：这些能力到底应该服务谁，以及在什么地方必须停止替代。

换句话说，`frictionless interaction` 不是让人更少参与，而是让人更少被无意义摩擦打断；`contextual intelligence` 不是让系统掌握更多材料后替人判断，而是让系统更准确地知道哪些材料该摆到人面前；`proactive intelligence` 不是让 agent 更主动地接管任务，而是让它更敏锐地发现何时应该准备环境、递上工具、提醒风险或浮出候选动作。

Human-centered harness 可以看作这三个原则的约束条件和目标函数。没有 human-centered 的约束，三者很容易走向“更顺滑地替代人”：低摩擦变成无需人参与，上下文智能变成代替人理解，主动智能变成后台接管。加上 human-centered harness 后，三者的方向会被重新校准：低摩擦是为了让人更顺畅地完成主体动作；上下文智能是为了让人的判断材料更清楚；主动智能是为了在不夺权的前提下，提前布置好人需要的工作场。

所以可以压成一句话：

> AI Architect 三原则定义了 AI-native 产品应具备的能力形态；Human-centered harness 定义了这些能力应服从的人机关系边界。前三者回答“系统怎样更聪明地协作”，后者回答“这种聪明不能把人从自己的主体动作中移开”。

**和当前的Agent harness的关系**
当前的Agent harness提供了Agent执行任务的必要能力。Human-centered agent则是当前Agent以上的更高一层功能，一种新的交互方式。我认为可能不是一种新的Agent架构范式，而是定义一种更好的人机交互关系。
当前 agent harness 提供的是 agent 执行任务所需的基础能力：读写文件、调用工具、执行命令等。这些是 agent 能“做事”的底座。Human-centered agent 关心的不是 agent 能不能做事，而是当 agent 有能力做事之后，它应该以什么方式参与人的工作。所以它更像一层人机协作协议。所以，Human-centered agent 不是“更弱的 agent”，也不是“更保守的 agent”。它可以使用很强的底层 harness，只是它对“强”的定义不同。

当前 autonomous harness 的强，是：

> agent 能否端到端完成任务。

Human-centered harness 的强，是：

> agent 能否准确识别哪些部分不该替人完成，并把人的主体动作支持得更顺畅。

这也让“拉屎递纸”这个比喻非常清楚：问题不是 agent 有没有能力把事情做完，而是它是否理解这件事本来就不该由它替人完成。它应该提供环境、工具、上下文和节奏，而不是把人的核心行为外包掉。

### 特征
**Intention Recognition and Goal Alignment**
应该识别用户意图，跟用户长期的目标对齐。

**Frictionless Interaction**

**Contextual Intelligence**

**Proactive Intelligence**


## HC Agent Product Definition Belief

### 核心问题


### 用户和关键场景


### MVP
给定一组本地文件，以及一个操作台。Agent阅读用户当前操作，尝试推断用户当前想要输入的prompt。然后


## 从当前的Agent范式看
当前的Agent范式是ReAct（还是Agent loop？）：给定一个prompt，generate-tool use，loop until finish。Loop工程，一个大点的loop，just用来拓展上下文窗口。如果你能把上下文窗口无限，那就是只要输入初始prompt就好了。

尝试一个不同的agent范式？观察用户操作-推断用户目标、需要的帮助-提供帮助。
- 入口从 prompt 扩展到 human activity
- 需要一个循环：不希望停顿然后反复去prompt