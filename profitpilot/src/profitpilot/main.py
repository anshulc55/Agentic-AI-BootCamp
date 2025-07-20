#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from profitpilot.crew import Profitpilot

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    inputs = {
        'sector': 'Technology'
    }
    
    try:
        result = Profitpilot().crew().kickoff(inputs=inputs)
        print(f"Profitpilot crew completed successfully at {datetime.now()}.")
        print(f"Result: {result}")
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


