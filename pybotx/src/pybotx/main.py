#!/usr/bin/env python
import sys
import warnings, os

from datetime import datetime

from pybotx.crew import Pybotx

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

os.makedirs('output', exist_ok=True)

assignment = """
You want to accumulate 10-Million USD in 20, 25 and 30 years.
Write a Python program that calculates:
Monthly SIP needed (with assumed 12% annual return)
Total invested vs interest earned
Allow the user to input different target goals and durations.
"""

def run():
    """
    Run the crew.
    """
    inputs = {
        'assignment': assignment
    }
    
    try:
        result = Pybotx().crew().kickoff(inputs=inputs)
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

