.PHONY: all build debug clean profile report-profile bench bench-all cuobjdump todo

CMAKE := cmake

BUILD_DIR := build
BENCH_DIR := __bench_cache__
BENCHMARK_DIR := __profile_cache__
CUDA_COMPUTE_CAPABILITY ?= sm_35
DEVICE_IDX ?= 0
KERNEL ?= 1

GPU_CC=$(shell nvidia-smi --id=0 --query-gpu=compute_cap --format=csv,noheader)
ifeq ($(GPU_CC),3.0)
    CUDA_COMPUTE_CAPABILITY := 30
else ifeq ($(GPU_CC),3.5)
    CUDA_COMPUTE_CAPABILITY := 35
else ifeq ($(GPU_CC),3.7)
    CUDA_COMPUTE_CAPABILITY := 37
else ifeq ($(GPU_CC),5.0)
    CUDA_COMPUTE_CAPABILITY := 50
else ifeq ($(GPU_CC),5.2)
    CUDA_COMPUTE_CAPABILITY := 52
else ifeq ($(GPU_CC),5.3)
    CUDA_COMPUTE_CAPABILITY := 53
else ifeq ($(GPU_CC),6.0)
    CUDA_COMPUTE_CAPABILITY := 60
else ifeq ($(GPU_CC),6.1)
    CUDA_COMPUTE_CAPABILITY := 61
else ifeq ($(GPU_CC),6.2)
    CUDA_COMPUTE_CAPABILITY := 62
else ifeq ($(GPU_CC),7.0)
    CUDA_COMPUTE_CAPABILITY := 70
else ifeq ($(GPU_CC),7.2)
    CUDA_COMPUTE_CAPABILITY := 72
else ifeq ($(GPU_CC),7.5)
    CUDA_COMPUTE_CAPABILITY := 75
else ifeq ($(GPU_CC),8.0)
    CUDA_COMPUTE_CAPABILITY := 80
else ifeq ($(GPU_CC),8.6)
    CUDA_COMPUTE_CAPABILITY := 86
else ifeq ($(GPU_CC),8.9)
    CUDA_COMPUTE_CAPABILITY := 89
else ifeq ($(GPU_CC),9.0)
    CUDA_COMPUTE_CAPABILITY := 90
else
    $(error Unsupported GPU compute capability: $(GPU_CC))
endif

all: build

GPU_NAMES := $(shell nvidia-smi --query-gpu=gpu_name --format=csv,noheader)

query-gpu-arch:
	@echo "Checking GPU architectures..."
	@echo "Found GPU-CC = "$(CUDA_COMPUTE_CAPABILITY)

build: query-gpu-arch
	@mkdir -p $(BUILD_DIR)
	@cd $(BUILD_DIR) && $(CMAKE) -DCMAKE_BUILD_TYPE=Release .. \
		-DCUDA_COMPUTE_CAPABILITY=$(CUDA_COMPUTE_CAPABILITY) \
		-DCMAKE_C_COMPILER_LAUNCHER=ccache \
		-DCMAKE_CXX_COMPILER_LAUNCHER=ccache \
		-DCMAKE_C_COMPILER=clang \
		-DCMAKE_CXX_COMPILER=clang++ \
		-DCMAKE_CUDA_COMPILER=nvcc \
		-DCMAKE_CUDA_FLAGS="-O3 -maxrregcount=128 --ptxas-options=-v --expt-relaxed-constexpr" \
		-GNinja
	@ninja -C $(BUILD_DIR)


clean:
	@rm -rf $(BUILD_DIR)
	@rm -rf $(BENCH_DIR)

