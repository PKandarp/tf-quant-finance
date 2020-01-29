# Lint as: python3
"""Payoff function tests."""

import numpy as np
import tensorflow.compat.v2 as tf

from tf_quant_finance.experimental.lsm_algorithm import payoff as payoff_utils
from tensorflow.python.framework import test_util  # pylint: disable=g-direct-tensorflow-import


@test_util.run_all_in_graph_and_eager_modes
class PayoffTest(tf.test.TestCase):

  def test_put_payoff_function(self):
    """Tests the put payoff function returns the right numbers."""
    # See Longstaff, F.A. and Schwartz, E.S., 2001. Valuing American options by
    # simulation: a simple least-squares approach.
    samples = [[1.0, 1.09, 1.08, 1.34],
               [1.0, 1.16, 1.26, 1.54],
               [1.0, 1.22, 1.07, 1.03],
               [1.0, 0.93, 0.97, 0.92],
               [1.0, 1.11, 1.56, 1.52],
               [1.0, 0.76, 0.77, 0.90],
               [1.0, 0.92, 0.84, 1.01],
               [1.0, 0.88, 1.22, 1.34]]
    # Expand dims to reflect that `samples` represent sample paths of
    # a 1-dimensional process
    for dtype in (np.float32, np.float64):
      # Create payoff functions for 2 different strike values
      payoff_fn = payoff_utils.make_basket_put_payoff([1.1, 1.2], dtype=dtype)
      sample_paths = tf.convert_to_tensor(samples, dtype=dtype)
      sample_paths = tf.expand_dims(sample_paths, -1)
      # Actual payoff
      payoff = payoff_fn(sample_paths)
      # Expected payoffs at the final time
      expected_payoff = [[0, 0],
                         [0, 0],
                         [0.07, 0.17],
                         [0.18, 0.28],
                         [0, 0],
                         [0.2, 0.3],
                         [0.09, 0.19],
                         [0, 0]]
    self.assertAllClose(expected_payoff, payoff, rtol=1e-8, atol=1e-8)

if __name__ == '__main__':
  tf.test.main()
