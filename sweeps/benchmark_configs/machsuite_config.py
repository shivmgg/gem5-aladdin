#!/usr/bin/env python
# MachSuite benchmark definitions.

from design_sweep_types import *

aes_aes = Benchmark("aes-aes", "aes", "common/harness.c")
aes_aes.set_kernels(["aes256_encrypt_ecb"])
aes_aes.set_main_id(0x00000010)
aes_aes.add_array("ctx", 96, 1, PARTITION_CYCLIC)
aes_aes.add_array("k", 32, 1, PARTITION_CYCLIC)
aes_aes.add_array("buf", 16, 1, PARTITION_CYCLIC)
aes_aes.add_array("rcon", 1, 1, PARTITION_COMPLETE)
aes_aes.add_array("sbox", 256, 1, PARTITION_CYCLIC)
aes_aes.add_loop("aes_addRoundKey_cpy", 138, 16)
aes_aes.add_loop("aes_subBytes", 122, 16)
aes_aes.add_loop("aes_addRoundKey", 130, 16)
aes_aes.add_loop("aes256_encrypt_ecb", 210, 32)
aes_aes.add_loop("aes256_encrypt_ecb", 213, 8)
aes_aes.add_loop("aes256_encrypt_ecb", 219, 13)
aes_aes.set_exec_cmd("%(source_dir)s/aes/aes/aes-aes-gem5-accel")
aes_aes.set_run_args("%(source_dir)s/aes/aes/input.data %(source_dir)s/aes/aes/check.data")

bfs_bulk = Benchmark("bfs-bulk", "bulk", "common/harness.c")
bfs_bulk.set_kernels(["bfs"])
bfs_bulk.set_main_id(0x00000030)
bfs_bulk.add_array("nodes", 512, 8, PARTITION_CYCLIC)
bfs_bulk.add_array("edges", 4096, 8, PARTITION_CYCLIC)
bfs_bulk.add_array("level", 256, 1, PARTITION_CYCLIC)
bfs_bulk.add_array("level_counts", 10, 8, PARTITION_CYCLIC)
bfs_bulk.add_loop("bfs", 60, 1)
bfs_bulk.add_loop("bfs", 63, 256)
bfs_bulk.add_loop("bfs", 67, 0)
bfs_bulk.set_exec_cmd("%(source_dir)s/bfs/bulk/bfs-bulk-gem5-accel")
bfs_bulk.set_run_args("%(source_dir)s/bfs/bulk/input.data %(source_dir)s/bfs/bulk/check.data")

bfs_queue = Benchmark("bfs-queue", "queue", "common/harness.c")
bfs_queue.set_kernels(["bfs"])
bfs_queue.set_main_id(0x00000040)
bfs_queue.add_array("queue", 256, 8, PARTITION_CYCLIC)
bfs_queue.add_array("nodes", 512, 8, PARTITION_CYCLIC)
bfs_queue.add_array("edges", 4096, 8, PARTITION_CYCLIC)
bfs_queue.add_array("level", 256, 1, PARTITION_CYCLIC)
bfs_queue.add_array("level_counts", 10, 8, PARTITION_CYCLIC)
bfs_queue.add_loop("bfs", 77, 10)
bfs_queue.add_loop("bfs", 79, 1)
bfs_queue.add_loop("bfs", 86, 0)
bfs_queue.set_exec_cmd("%(source_dir)s/bfs/queue/bfs-queue-gem5-accel")
bfs_queue.set_run_args("%(source_dir)s/bfs/queue/input.data %(source_dir)s/bfs/queue/check.data")

fft_strided = Benchmark("fft-strided", "fft", "common/harness.c")
fft_strided.set_kernels(["fft"])
fft_strided.set_main_id(0x00000050)
fft_strided.add_array("real", 1024, 8, PARTITION_CYCLIC)
fft_strided.add_array("img", 1024, 8, PARTITION_CYCLIC)
fft_strided.add_array("real_twid", 1024, 8, PARTITION_CYCLIC)
fft_strided.add_array("img_twid", 1024, 8, PARTITION_CYCLIC)
fft_strided.add_loop("fft", 19, 512)
fft_strided.add_loop("fft", 18, 1)
fft_strided.set_exec_cmd("%(source_dir)s/fft/strided/fft-strided-gem5-accel")
fft_strided.set_run_args("%(source_dir)s/fft/strided/input.data %(source_dir)s/fft/strided/check.data")

fft_transpose = Benchmark("fft-transpose", "fft", "common/harness.c")
fft_transpose.set_kernels(["fft1D_512"])
fft_transpose.set_main_id(0x00000060)
fft_transpose.add_array("fft1D_512.reversed", 8, 4, PARTITION_COMPLETE)
fft_transpose.add_array("DATA_x", 512, 8, PARTITION_CYCLIC)
fft_transpose.add_array("DATA_y", 512, 8, PARTITION_CYCLIC)
fft_transpose.add_array("data_x", 8, 8, PARTITION_COMPLETE)
fft_transpose.add_array("data_y", 8, 8, PARTITION_COMPLETE)
fft_transpose.add_array("smem", 576, 8, PARTITION_CYCLIC)
fft_transpose.add_array("work_x", 512, 8, PARTITION_CYCLIC)
fft_transpose.add_array("work_y", 512, 8, PARTITION_CYCLIC)
fft_transpose.add_loop("fft1D_512", 154, 64)
fft_transpose.add_loop("fft1D_512", 178, 8)
fft_transpose.add_loop("fft1D_512", 201, 64)
fft_transpose.add_loop("fft1D_512", 215, 64)
fft_transpose.add_loop("fft1D_512", 231, 64)
fft_transpose.add_loop("fft1D_512", 246, 64)
fft_transpose.add_loop("fft1D_512", 271, 64)
fft_transpose.add_loop("fft1D_512", 297, 8)
fft_transpose.add_loop("fft1D_512", 321, 64)
fft_transpose.add_loop("fft1D_512", 336, 64)
fft_transpose.add_loop("fft1D_512", 352, 64)
fft_transpose.add_loop("fft1D_512", 367, 64)
fft_transpose.add_loop("fft1D_512", 392, 64)
fft_transpose.set_exec_cmd("%(source_dir)s/fft/transpose/fft-transpose-gem5-accel")
fft_transpose.set_run_args("%(source_dir)s/fft/transpose/input.data %(source_dir)s/fft/transpose/check.data")

gemm_blocked = Benchmark("gemm-blocked", "bbgemm", "common/harness.c")
gemm_blocked.set_kernels(["bbgemm"])
gemm_blocked.set_main_id(0x00000070)
gemm_blocked.add_array("m1", 4096, 4, PARTITION_CYCLIC)
gemm_blocked.add_array("m2", 4096, 4, PARTITION_CYCLIC)
gemm_blocked.add_array("prod", 4096, 4, PARTITION_CYCLIC)
gemm_blocked.add_loop("bbgemm", 54, 1)
gemm_blocked.add_loop("bbgemm", 55, 1)
gemm_blocked.add_loop("bbgemm", 56, 64)
gemm_blocked.add_loop("bbgemm", 57, 0)
gemm_blocked.add_loop("bbgemm", 61, 0)
gemm_blocked.set_exec_cmd("%(source_dir)s/gemm/blocked/gemm-blocked-gem5-accel")
gemm_blocked.set_run_args("%(source_dir)s/gemm/blocked/input.data %(source_dir)s/gemm/blocked/check.data")

gemm_ncubed = Benchmark("gemm-ncubed", "gemm", "common/harness.c")
gemm_ncubed.set_kernels(["gemm"])
gemm_ncubed.set_main_id(0x00000080)
gemm_ncubed.add_array("m1", 4096, 4, PARTITION_CYCLIC)
gemm_ncubed.add_array("m2", 4096, 4, PARTITION_CYCLIC)
gemm_ncubed.add_array("prod", 4096, 4, PARTITION_CYCLIC)
gemm_ncubed.add_loop("gemm", 50, 1)
gemm_ncubed.add_loop("gemm", 51, 64)
gemm_ncubed.add_loop("gemm", 54, 0)
gemm_ncubed.set_exec_cmd("%(source_dir)s/gemm/ncubed/gemm-ncubed-gem5-accel")
gemm_ncubed.set_run_args("%(source_dir)s/gemm/ncubed/input.data %(source_dir)s/gemm/ncubed/check.data")

kmp_kmp = Benchmark("kmp-kmp", "kmp", "common/harness.c")
kmp_kmp.set_kernels(["kmp"])
kmp_kmp.set_main_id(0x00000090)
kmp_kmp.add_array("pattern", 4, 1, PARTITION_COMPLETE)
kmp_kmp.add_array("input", 32411, 1, PARTITION_CYCLIC)
kmp_kmp.add_array("kmpNext", 4, 4, PARTITION_COMPLETE)
kmp_kmp.add_loop("CPF", 40, 4)
kmp_kmp.add_loop("CPF", 41, 1)
kmp_kmp.add_loop("kmp", 76, 32411)
kmp_kmp.add_loop("kmp", 77, 1)
kmp_kmp.set_exec_cmd("%(source_dir)s/kmp/kmp/kmp-kmp-gem5-accel")
kmp_kmp.set_run_args("%(source_dir)s/kmp/kmp/input.data %(source_dir)s/kmp/kmp/check.data")

md_grid = Benchmark("md-grid", "md", "common/harness.c")
md_grid.set_kernels(["md"])
md_grid.set_main_id(0x000000A0)
md_grid.add_array("n_points", 64, 4, PARTITION_CYCLIC)
md_grid.add_array("d_force", 1920, 8, PARTITION_CYCLIC)
md_grid.add_array("position", 1920, 8, PARTITION_CYCLIC)
md_grid.add_loop("md", 55, 1)
md_grid.add_loop("md", 56, 1)
md_grid.add_loop("md", 57, 1)
md_grid.add_loop("md", 59, 1)
md_grid.add_loop("md", 60, 1)
md_grid.add_loop("md", 61, 1)
md_grid.add_loop("md", 65, 0)
md_grid.add_loop("md", 71, 0)
md_grid.set_exec_cmd("%(source_dir)s/md/grid/md-grid-gem5-accel")
md_grid.set_run_args("%(source_dir)s/md/grid/input.data %(source_dir)s/md/grid/check.data")

md_knn = Benchmark("md-knn", "md", "common/harness.c")
md_knn.set_kernels(["md_kernel"])
md_knn.set_main_id(0x000000B0)
md_knn.add_array("d_force_x", 256, 8, PARTITION_CYCLIC)
md_knn.add_array("d_force_y", 256, 8, PARTITION_CYCLIC)
md_knn.add_array("d_force_z", 256, 8, PARTITION_CYCLIC)
md_knn.add_array("position_x", 256, 8, PARTITION_CYCLIC)
md_knn.add_array("position_y", 256, 8, PARTITION_CYCLIC)
md_knn.add_array("position_z", 256, 8, PARTITION_CYCLIC)
md_knn.add_array("NL", 4096, 8, PARTITION_CYCLIC)
md_knn.add_loop("md_kernel", 58, 256)
md_knn.add_loop("md_kernel", 65, 0)
md_knn.set_exec_cmd("%(source_dir)s/md/knn/md-knn-gem5-accel")
md_knn.set_run_args("%(source_dir)s/md/knn/input.data %(source_dir)s/md/knn/check.data")

nw_nw = Benchmark("nw-nw", "needwun", "common/harness.c")
nw_nw.set_kernels(["needwun"])
nw_nw.set_main_id(0x000000C0)
nw_nw.add_array("SEQA", 128, 1, PARTITION_CYCLIC)
nw_nw.add_array("SEQB", 128, 1, PARTITION_CYCLIC)
nw_nw.add_array("alignedA", 256, 1, PARTITION_CYCLIC)
nw_nw.add_array("alignedB", 256, 1, PARTITION_CYCLIC)
nw_nw.add_array("A", 16641, 4, PARTITION_CYCLIC)
nw_nw.add_array("ptr", 16641, 1, PARTITION_CYCLIC)
nw_nw.add_loop("needwun", 46, 129)
nw_nw.add_loop("needwun", 49, 129)
nw_nw.add_loop("needwun", 54, 128)
nw_nw.add_loop("needwun", 55, 0)
nw_nw.add_loop("needwun", 99, 1)
nw_nw.set_exec_cmd("%(source_dir)s/nw/nw/nw-nw-gem5-accel")
nw_nw.set_run_args("%(source_dir)s/nw/nw/input.data %(source_dir)s/nw/nw/check.data")

sort_merge = Benchmark("sort-merge", "merge", "common/harness.c")
sort_merge.set_kernels(["mergesort"])
sort_merge.set_main_id(0x000000D0)
sort_merge.add_array("temp", 4096, 4, PARTITION_CYCLIC)
sort_merge.add_array("a", 4096, 4, PARTITION_CYCLIC)
sort_merge.add_loop("merge", 37, 2048)
sort_merge.add_loop("merge", 41, 2048)
sort_merge.add_loop("merge", 48, 1)
sort_merge.add_loop("mergesort", 72, 1)
sort_merge.add_loop("mergesort", 73, 1)
sort_merge.set_exec_cmd("%(source_dir)s/sort/merge/sort-merge-gem5-accel")
sort_merge.set_run_args("%(source_dir)s/sort/merge/input.data %(source_dir)s/sort/merge/check.data")

sort_radix = Benchmark("sort-radix", "radix", "common/harness.c")
sort_radix.set_kernels(["ss_sort"])
sort_radix.set_main_id(0x000000E0)
sort_radix.add_array("a", 2048, 4, PARTITION_CYCLIC)
sort_radix.add_array("b", 2048, 4, PARTITION_CYCLIC)
sort_radix.add_array("bucket", 2048, 4, PARTITION_CYCLIC)
sort_radix.add_array("sum", 128, 4, PARTITION_CYCLIC)
sort_radix.add_loop("last_step_scan", 62, 128)
sort_radix.add_loop("last_step_scan", 63, 0)
sort_radix.add_loop("local_scan", 42, 0)
sort_radix.add_loop("local_scan", 41, 128)
sort_radix.add_loop("sum_scan", 53, 128)
sort_radix.add_loop("hist", 82, 512)
sort_radix.add_loop("hist", 83, 0)
sort_radix.add_loop("update", 96, 512)
sort_radix.add_loop("update", 97, 0)
sort_radix.add_loop("init", 73, 2048)
sort_radix.add_loop("ss_sort", 113, 1)
sort_radix.set_exec_cmd("%(source_dir)s/sort/radix/sort-radix-gem5-accel")
sort_radix.set_run_args("%(source_dir)s/sort/radix/input.data %(source_dir)s/sort/radix/check.data")

spmv_crs = Benchmark("spmv-crs", "crs", "common/harness.c")
spmv_crs.set_kernels(["spmv"])
spmv_crs.set_main_id(0x000000F0)
spmv_crs.add_array("val", 1666, 8, PARTITION_CYCLIC)
spmv_crs.add_array("cols", 1666, 4, PARTITION_CYCLIC)
spmv_crs.add_array("rowDelimiters", 495, 4, PARTITION_CYCLIC)
spmv_crs.add_array("vec", 494, 8, PARTITION_CYCLIC)
spmv_crs.add_array("out", 494, 8, PARTITION_CYCLIC)
spmv_crs.add_loop("spmv", 50, 494)
spmv_crs.add_loop("spmv", 54, 0)
spmv_crs.set_exec_cmd("%(source_dir)s/spmv/crs/spmv-crs-gem5-accel")
spmv_crs.set_run_args("%(source_dir)s/spmv/crs/input.data %(source_dir)s/spmv/crs/check.data")

spmv_ellpack = Benchmark("spmv-ellpack", "ellpack", "common/harness.c")
spmv_ellpack.set_kernels(["ellpack"])
spmv_ellpack.set_main_id(0x00000100)
spmv_ellpack.add_array("nzval", 4940, 8, PARTITION_CYCLIC)
spmv_ellpack.add_array("cols", 4940, 4, PARTITION_CYCLIC)
spmv_ellpack.add_array("vec", 494, 8, PARTITION_CYCLIC)
spmv_ellpack.add_array("out", 494, 8, PARTITION_CYCLIC)
spmv_ellpack.add_loop("ellpack", 58, 494)
spmv_ellpack.add_loop("ellpack", 60, 0)
spmv_ellpack.set_exec_cmd("%(source_dir)s/spmv/ellpack/spmv-ellpack-gem5-accel")
spmv_ellpack.set_run_args("%(source_dir)s/spmv/ellpack/input.data %(source_dir)s/spmv/ellpack/check.data")

stencil_stencil2d = Benchmark("stencil-stencil2d", "stencil", "common/harness.c")
stencil_stencil2d.set_kernels(["stencil"])
stencil_stencil2d.set_main_id(0x00000110)
stencil_stencil2d.add_array("orig", 8580, 4, PARTITION_CYCLIC)
stencil_stencil2d.add_array("sol", 8580, 4, PARTITION_CYCLIC)
stencil_stencil2d.add_array("filter", 9, 4, PARTITION_COMPLETE)
stencil_stencil2d.add_loop("stencil", 48, 1)
stencil_stencil2d.add_loop("stencil", 49, 64)
stencil_stencil2d.add_loop("stencil", 51, 0)
stencil_stencil2d.add_loop("stencil", 52, 0)
stencil_stencil2d.set_exec_cmd("%(source_dir)s/stencil/stencil2d/stencil-stencil2d-gem5-accel")
stencil_stencil2d.set_run_args("%(source_dir)s/stencil/stencil2d/input.data %(source_dir)s/stencil/stencil2d/check.data")

stencil_stencil3d = Benchmark("stencil-stencil3d", "stencil3d", "common/harness.c")
stencil_stencil3d.set_kernels(["stencil3d"])
stencil_stencil3d.set_main_id(0x00000120)
stencil_stencil3d.add_array("orig", 16384, 4, PARTITION_CYCLIC)
stencil_stencil3d.add_array("sol", 16384, 4, PARTITION_CYCLIC)
stencil_stencil3d.add_loop("stencil3d", 59, 1)
stencil_stencil3d.add_loop("stencil3d", 60, 30)
stencil_stencil3d.add_loop("stencil3d", 61, 0)
stencil_stencil3d.set_exec_cmd("%(source_dir)s/stencil/stencil3d/stencil-stencil3d-gem5-accel")
stencil_stencil3d.set_run_args("%(source_dir)s/stencil/stencil3d/input.data %(source_dir)s/stencil/stencil3d/check.data")

viterbi_viterbi = Benchmark("viterbi-viterbi", "viterbi", "common/harness.c")
viterbi_viterbi.set_kernels(["viterbi"])
viterbi_viterbi.set_main_id(0x00000130)
viterbi_viterbi.add_array("Obs", 128, 4, PARTITION_CYCLIC)
viterbi_viterbi.add_array("transMat", 4096, 4, PARTITION_CYCLIC)
viterbi_viterbi.add_array("obsLik", 4096, 4, PARTITION_BLOCK)
viterbi_viterbi.add_array("v", 4096, 4, PARTITION_BLOCK)
viterbi_viterbi.add_loop("viterbi", 53, 1)
viterbi_viterbi.add_loop("viterbi", 55, 32)
viterbi_viterbi.add_loop("viterbi", 56, 0)
viterbi_viterbi.add_loop("viterbi", 67, 1)
viterbi_viterbi.set_exec_cmd("%(source_dir)s/viterbi/viterbi/viterbi-viterbi-gem5-accel")
viterbi_viterbi.set_run_args("%(source_dir)s/viterbi/viterbi/input.data %(source_dir)s/viterbi/viterbi/check.data")

_BENCHMARKS = [bfs_bulk, sort_merge, spmv_ellpack, bfs_queue,
               stencil_stencil3d, sort_radix, kmp_kmp,
               nw_nw, md_grid, fft_strided, aes_aes, md_knn, fft_transpose,
               gemm_blocked, stencil_stencil2d,
               spmv_crs, gemm_ncubed, viterbi_viterbi]
_SUITE_NAME = "MACHSUITE"
