# Helper runner to execute the example while ensuring the project root is on sys.path
import os
import sys
import runpy

# Compute project root directory (parent of the 'bendrix' package dir)
this_dir = os.path.dirname(os.path.abspath(__file__))
if this_dir not in sys.path:
    sys.path.insert(0, this_dir)

# Run the example module as a module so that package imports work
if __name__ == "__main__":
    # Use runpy to execute the example module in its package context
    runpy.run_module('bendrix.examples.example_propped_cantilever', run_name='__main__')
