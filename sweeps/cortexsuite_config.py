#!/usr/bin/env python
# CortexSuite benchmark definitions

from design_sweep_types import *

disparity = Benchmark("disparity", "disparity/src/c/script_disparity")
disparity.set_kernels(["computeSAD", "integralImage2D2D",
                       "finalSAD", "findDisparity"])
disparity.add_loop("computeSAD", 16, UNROLL_ONE)
disparity.add_loop("computeSAD", 18)
disparity.add_loop("integralImage2D2D", 16)
disparity.add_loop("integralImage2D2D", 19, UNROLL_ONE)
disparity.add_loop("integralImage2D2D", 20)
disparity.add_loop("integralImage2D2D", 25, UNROLL_ONE)
disparity.add_loop("integralImage2D2D", 26)
disparity.add_loop("finalSAD", 18, UNROLL_ONE)
disparity.add_loop("finalSAD", 20)
disparity.add_loop("findDisparity", 16, UNROLL_ONE)
disparity.add_loop("findDisparity", 18)
disparity.add_array("Ileft", 12742, 4, PARTITION_CYCLIC)
disparity.add_array("Iright_moved", 12742, 4, PARTITION_CYCLIC)
disparity.add_array("SAD", 12742, 4, PARTITION_CYCLIC)
disparity.add_array("SAD", 12742, 4, PARTITION_CYCLIC)
disparity.add_array("integralImg", 12742, 4, PARTITION_CYCLIC)
disparity.add_array("Ileft", 12742, 4, PARTITION_CYCLIC)
disparity.add_array("Iright_moved", 12742, 4, PARTITION_CYCLIC)
disparity.add_array("SAD", 12742, 4, PARTITION_CYCLIC)
disparity.add_array("integralImg", 12742, 4, PARTITION_CYCLIC)
disparity.add_array("retSAD", 12290, 4, PARTITION_CYCLIC)
disparity.add_array("integralImg", 12742, 4, PARTITION_CYCLIC)
disparity.add_array("retSAD", 12290, 4, PARTITION_CYCLIC)
disparity.add_array("retSAD", 12290, 4, PARTITION_CYCLIC)
disparity.add_array("minSAD", 12290, 4, PARTITION_CYCLIC)
disparity.add_array("retDisp", 12290, 4, PARTITION_CYCLIC)
disparity.generate_separate_kernels(separate=True, enforce_order=True)
disparity.use_local_makefile()

CORTEXSUITE = [disparity]
