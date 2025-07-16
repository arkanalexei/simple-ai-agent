class AppError(Exception):
  """
  Base exception for all errors in the agent system.
  """
  def __init__(self, message: str):
      super().__init__(message)
      self.message = message


class ToolError(AppError):
  """
  Raised when a tool (e.g. math calculator, weather fetcher) fails to complete.
  This includes API errors, evaluation failures, or unsupported inputs.
  """
  pass
