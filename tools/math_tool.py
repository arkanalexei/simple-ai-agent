
def run(query: str) -> str:
    """
    Evaluates a mathematical expression and returns the result as a string.
    
    Args:
        query (str): The mathematical expression to evaluate.
        
    Returns:
        str: The result of the evaluation.
    """
    try:
        # TODO: Bare bones evaluation of the expression
        result = eval(query)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)} is not a valid expression"