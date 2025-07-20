#!/usr/bin/env python
import sys
import warnings
import os

from datetime import datetime

from fincore_ai.crew import FincoreAi

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Entry point to run the Financial Research Crew AI pipeline.
    This script initiates a multi-agent workflow to analyze a company's financial profile
    and generate a market insights report.
    """
    inputs = {
        'company': 'Apple'
    }

    os.makedirs('output', exist_ok=True)

    print("\n Starting financial research on:", inputs['company'])
    
    try:
        result = FincoreAi().crew().kickoff(inputs=inputs)
        print("\nFinancial research completed successfully.")
        print(result.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")