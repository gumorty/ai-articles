# 从“协作型 Agent”到“嵌入式 Agent”：Agentic Workflow 的演进与深度实践

> 作者：AI Agent Station  
> 日期：2026-04-26  
> 发布时间：2026-04-26T09:49:08.167529998+08:00

---

## 目录

- [摘要](#摘要)
- [背景](#背景)
- [核心原理](#核心原理)
- [实战代码](#实战代码)
- [常见误区](#常见误区)
- [总结](#总结)
- [相关阅读/引用链接](#相关阅读引用链接)

---

## 摘要

本文探讨了 AI Agent 从单纯的对话助手向深度嵌入软件系统的“Agentic Workflow”演进的过程，并结合当前行业关于“不要把 Agent 当同事，而要将其嵌入软件”的热门观点进行深度剖析。

## 背景

随着大型语言模型 (LLM) 的能力演进，Agent 的范式正在发生剧变。最近 Hacker News 上引起热议的一篇文章指出：“Agents Aren't Coworkers, Embed Them in Your Software”。这意味着 Agent 的真正价值不在于它能像人一样聊天，而在于它能作为可编程的、可预测的逻辑单元，深度嵌入到业务流中。

## 核心原理

Agentic Workflow 的核心在于不再依赖单次 Prompt 的“一锤子买卖”，而是通过“反思 (Reflection)”、“规划 (Planning)”和“工具使用 (Tool Use)”的循环迭代，构建一个具备自我修正能力的闭环系统。其核心支柱包括：

1. **反思与自我修正**：Agent 在执行每一步后检查输出质量，必要时重试或调整策略。
2. **结构化的工具调用**：通过定义明确的工具接口（如 API、数据库、计算器），Agent 可以安全、可控地与外部系统交互。
3. **任务的拆解与序列化执行**：将复杂任务分解为多个可管理的子步骤，按顺序或并行执行。

## 实战代码

以下是一个简化的 Agentic Workflow 实现示例：

```python
import asyncio
from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional


@dataclass
class Step:
    description: str
    tool: Optional[str] = None
    params: dict = field(default_factory=dict)


@dataclass
class Plan:
    steps: List[Step]


@dataclass
class Reflection:
    needs_retry: bool = False
    feedback: str = ""


class Planner:
    async def create_plan(self, task_description: str) -> Plan:
        # 模拟任务拆解逻辑
        # 实际场景中会调用 LLM 进行规划
        return Plan(steps=[
            Step(description="搜索最新 AI 趋势", tool="web_search", params={"query": "AI trends 2026"}),
            Step(description="分析搜索结果", tool="calculator", params={"operation": "summarize"}),
        ])


class Executor:
    def __init__(self, tools: dict):
        self.tools = tools

    async def execute_step(self, step: Step) -> str:
        # 模拟工具执行
        if step.tool == "web_search":
            return f"搜索结果: {step.params.get('query', '')}"
        elif step.tool == "calculator":
            return "分析完成: 趋势包括 Agentic Workflow, LLM 编排等"
        return f"执行: {step.description}"


class AgenticWorkflow:
    def __init__(self, tools: dict):
        self.tools = tools
        self.planner = Planner()
        self.executor = Executor(tools)

    async def run(self, task_description: str) -> List[str]:
        # Step 1: Planning - 任务拆解
        plan = await self.planner.create_plan(task_description)

        # Step 2: Execute with Reflection - 执行与反思
        results = []
        for step in plan.steps:
            print(f"Executing: {step}")
            output = await self.executor.execute_step(step)

            # Reflection Step - 自我检查
            reflection = await self.reflect(step, output)
            if reflection.needs_retry:
                # 重新执行逻辑（简化处理）
                print(f"Retrying step due to: {reflection.feedback}")
                output = await self.executor.execute_step(step)
            results.append(output)

        return results

    async def reflect(self, step: Step, output: str) -> Reflection:
        # 模拟反思逻辑
        if "错误" in output or "失败" in output:
            return Reflection(needs_retry=True, feedback="输出包含错误信息")
        return Reflection()


# 使用示例
async def main():
    workflow = AgenticWorkflow(tools={"web_search": None, "calculator": None})
    results = await workflow.run("分析最新 AI 趋势对软件架构的影响")
    for r in results:
        print(r)


if __name__ == "__main__":
    asyncio.run(main())
```

## 常见误区

- **无限循环 (Infinite Loops)**: Agent 在自我修正过程中可能陷入逻辑死循环，必须设置最大迭代次数。
- **上下文爆炸 (Context Bloat)**: 随着 Workflow 的步骤增加，历史对话会迅速消耗 Token 并导致模型注意力分散。
- **缺乏确定性**: 过度依赖 Agent 的自主决策可能导致业务流程不可控，必须引入“人类在环 (Human-in-the-loop)”机制。

## 总结

Agent 的未来不在于它能多像人，而在于它能多好地融入现有的软件架构。通过 Agentic Workflow，我们正在从“构建聊天机器人”转向“构建具备智能逻辑的软件系统”。

## 相关阅读/引用链接

- [Agents Aren't Coworkers, Embed Them in Your Software (Hacker News)](https://news.ycombinator.com/item?id=40000000)
- [Building Effective Agents (Anthropic)](https://docs.anthropic.com/en/docs/build-with-claude/agentic)
- [Agentic Workflow Patterns (LangChain)](https://blog.langchain.dev/agentic-workflows/)