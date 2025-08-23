#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from optionstrader.crew import Optionstrader

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Run the crew.
    """
    inputs = {
        'index': 'Nifty50',
        'date': "31 July 2025",
        'assignment': "31 July 2025",
    }
    
    try:
        result = Optionstrader().crew().kickoff(inputs=inputs)
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")



