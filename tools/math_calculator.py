# Based on https://python.langchain.com/docs/versions/migrating_chains/llm_math_chain/

import math

import numexpr
from langchain_core.tools import tool

from utils.errors import ToolError
from utils.logging import get_logger

logger = get_logger("math_calculator")


@tool
def calculator(expression: str) -> str:
    """
    Calculate expression using Python's numexpr library.

    Expression should be a single line mathematical expression
    that solves the problem.

    Examples:
        "37593 * 67" for "37593 times 67"
        "37593**(1/5)" for "37593^(1/5)"
    """
    local_dict = {"pi": math.pi, "e": math.e}

    try:
        return str(
            numexpr.evaluate(
                expression.strip(),
                global_dict={},  # restrict access to globals
                local_dict=local_dict,  # add common mathematical functions
            )
        )
    except Exception as e:
        logger.error(f"Math evaluation failed for '{expression}': {e}")
        raise ToolError(f"Math evaluation failed for '{expression}': {e}")
