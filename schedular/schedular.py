# Install croniter if not already installed
# !pip install croniter

from croniter import croniter
from datetime import datetime

def get_next_run_time(cron_expr, base_time=None):
    """
    Function to get the next run time from a cron expression.
    
    Args:
        cron_expr (str): The cron expression in the form of a string.
        base_time (datetime, optional): The base time to start calculation from. Defaults to current time.
    
    Returns:
        datetime: The next time the cron job will run.
    """
    if base_time is None:
        base_time = datetime.now()

    # Initialize croniter with the cron expression and base time
    cron = croniter(cron_expr, base_time)
    
    # Get the next scheduled run time
    next_run = cron.get_next(datetime)
    
    return next_run

# Example usage:
cron_expression = "*/5 * * * *"  # Every 5 minutes
next_time = get_next_run_time(cron_expression)
print(f"The next scheduled run time is: {next_time}")
