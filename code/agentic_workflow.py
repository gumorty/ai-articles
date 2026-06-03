"""
Agentic Workflow 示例代码

本模块实现了一个简化的 Agentic Workflow 系统，
展示了任务规划、执行和反思的核心模式。
"""

import asyncio
from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional


@dataclass
class Step:
    """工作流中的一个执行步骤"""
    description: str
    tool: Optional[str] = None
    params: dict = field(default_factory=dict)


@dataclass
class Plan:
    """任务执行计划，包含多个步骤"""
    steps: List[Step]


@dataclass
class Reflection:
    """执行反思结果"""
    needs_retry: bool = False
    feedback: str = ""


class Planner:
    """
    任务规划器
    
    负责将复杂任务拆解为可执行的步骤序列。
    实际场景中应集成 LLM 进行智能规划。
    """

    async def create_plan(self, task_description: str) -> Plan:
        """
        根据任务描述创建执行计划
        
        Args:
            task_description: 任务描述文本
            
        Returns:
            Plan: 包含多个步骤的执行计划
        """
        # 模拟任务拆解逻辑
        # 实际场景中会调用 LLM 进行规划
        return Plan(steps=[
            Step(description="搜索最新 AI 趋势", tool="web_search", params={"query": "AI trends 2026"}),
            Step(description="分析搜索结果", tool="calculator", params={"operation": "summarize"}),
        ])


class Executor:
    """
    步骤执行器
    
    负责调用具体工具执行计划中的每个步骤。
    """

    def __init__(self, tools: dict):
        """
        初始化执行器
        
        Args:
            tools: 可用工具字典，key 为工具名，value 为工具实例
        """
        self.tools = tools

    async def execute_step(self, step: Step) -> str:
        """
        执行单个步骤
        
        Args:
            step: 待执行的步骤
            
        Returns:
            str: 执行结果文本
        """
        # 模拟工具执行
        if step.tool == "web_search":
            return f"搜索结果: {step.params.get('query', '')}"
        elif step.tool == "calculator":
            return "分析完成: 趋势包括 Agentic Workflow, LLM 编排等"
        return f"执行: {step.description}"


class AgenticWorkflow:
    """
    Agentic Workflow 主类
    
    实现规划-执行-反思的循环模式。
    """

    def __init__(self, tools: dict):
        """
        初始化工作流
        
        Args:
            tools: 可用工具字典
        """
        self.tools = tools
        self.planner = Planner()
        self.executor = Executor(tools)

    async def run(self, task_description: str) -> List[str]:
        """
        运行工作流
        
        Args:
            task_description: 任务描述
            
        Returns:
            List[str]: 所有步骤的执行结果列表
        """
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
        """
        对执行结果进行反思
        
        Args:
            step: 已执行的步骤
            output: 执行结果
            
        Returns:
            Reflection: 反思结果，指示是否需要重试
        """
        # 模拟反思逻辑
        if "错误" in output or "失败" in output:
            return Reflection(needs_retry=True, feedback="输出包含错误信息")
        return Reflection()


async def main():
    """主函数：演示工作流的使用"""
    workflow = AgenticWorkflow(tools={"web_search": None, "calculator": None})
    results = await workflow.run("分析最新 AI 趋势对软件架构的影响")
    for r in results:
        print(r)


if __name__ == "__main__":
    asyncio.run(main())