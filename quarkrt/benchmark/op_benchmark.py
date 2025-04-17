import time

import iree.compiler
import iree.runtime
import numpy as np
import torch
import torch.utils.benchmark as benchmark

__all__ = ["torch_op_benchmark", "tf_op_benchmark",
           "quark_op_benchmark", "quark_model_benchmark", "torch_model_benchmark"]


# TODO(albert): default is 'ms'
def torch_model_benchmark(
    model, inputs, warmups=0, repetitions=1, measure_count=1, device="cpu"
):
    # print("benchmarking pytorch on model @" + str(model))
    # TODO: move this into quark.utils.get_gpu_device
    if device == "cpu":
        _device = torch.device("cpu")
    elif device == "gpu":
        assert (
            torch.cuda.is_available()
        ), "Selected gpu for benchmark, but not available"
        _device = torch.device("cuda:0")
    else:
        assert 0, "Unsupported device"

    if len(inputs) == 1:
        timer = benchmark.Timer(
            stmt="model(input)", globals={"model": model, "input": inputs[0].to(_device)}
        )
    elif len(inputs) == 3:
        timer = benchmark.Timer(
            stmt="model(output, input, grad, retain_graph=True)",
            globals={"model": model, "output": inputs[0].to(_device),
                     "input": [inp.to(_device) for inp in inputs[1]], "grad": inputs[2].to(_device)}
        )
    else:
        assert 0, "inputs length = {}".format(len(inputs))

    # run benchmarks by repetition time, organise measures in list
    results = []
    for i in range(measure_count):
        results += timer.timeit(repetitions).times

    # from 's' to 'ms'
    results = [1000.0 * result / repetitions for result in results]
    # get rid of warmup period measures
    if warmups == 0:
        return results
    else:
        return results[warmups:-1]

# TODO(albert): annotate types
# TODO(albert): support dtype selection
# TODO(albert): refactor whole program, use dataclass and other fancy features
# TODO(albert): extract device to class


def torch_op_benchmark(
    operator, operands_shape, warmups=0, repetitions=1, measure_count=1, device="cpu"
):
    # TODO: move this into quark.utils.get_gpu_device
    if device == "cpu":
        _device = torch.device("cpu")
    elif device == "gpu":
        assert (
            torch.cuda.is_available()
        ), "Selected gpu for benchmark, but not available"
        _device = torch.device("cuda:0")
    else:
        assert 0, "Unsupported device"

    if operator == "matmul":
        assert len(operands_shape) == 2
        lhs_data = np.random.randn(*operands_shape[0]).astype(np.float32)
        rhs_data = np.random.randn(*operands_shape[1]).astype(np.float32)
        lhs, rhs = [torch.from_numpy(i).to(_device)
                    for i in [lhs_data, rhs_data]]

        def bench_func(lhs, rhs):
            return torch.matmul(lhs, rhs)
        timer = benchmark.Timer(
            stmt="torch.matmul(lhs, rhs)", globals={"lhs": lhs, "rhs": rhs}
        )
        # timer = benchmark.Timer(
        #     stmt="_lhs = lhs.to(_device);_rhs = rhs.to(_device);torch.bmm(_lhs, _rhs)", globals={"lhs": lhs, "rhs": rhs, "_device": _device}
        # )
    elif operator == "batch-matmul":
        assert len(operands_shape) == 2
        lhs_data = np.random.randn(*operands_shape[0]).astype(np.float32)
        rhs_data = np.random.randn(*operands_shape[1]).astype(np.float32)
        lhs, rhs = [torch.from_numpy(i).to(_device)
                    for i in [lhs_data, rhs_data]]

        def bench_func(lhs, rhs):
            return torch.bmm(lhs, rhs)
        timer = benchmark.Timer(
            stmt="torch.matmul(lhs, rhs)", globals={"lhs": lhs, "rhs": rhs}
        )
        # timer = benchmark.Timer(
        #     stmt="_lhs = lhs.to(_device);_rhs = rhs.to(_device);torch.bmm(_lhs, _rhs)", globals={"lhs": lhs, "rhs": rhs, "_device": _device}
        # )
    else:
        # TODO: make this assert more reasonable, for unhandled ops
        assert 0, "To benchmark unknown operator"

    # run benchmarks by repetition time, organise measures in list
    results = []
    for i in range(measure_count):
        results += timer.timeit(repetitions).times

    results = [val * 1000.0 for val in results]
    # for _ in range(measure_count):
    #     start_time = time.time()
    #     for _a in range(repetitions):
    #         bench_func(lhs, rhs)
    #     end_time = time.time()
    #     avg_time = end_time - start_time
    #     results.append(avg_time / float(repetitions) * 1000.0)
    # results = [val * 1000.0 / repetitions for val in results]

    # get rid of warmup period measures
    if warmups == 0:
        return results
    else:
        return results[warmups:-1]


def tf_op_benchmark(
    operator, operands_shape, warmups=0, repetitions=1, measure_count=1, device="cpu"
):
    import tensorflow as tf

    if device == "cpu":
        _device = tf.device("/CPU:0")
    elif device == "gpu" and tf.config.experimental.list_physical_devices("GPU"):
        _device = tf.device("/GPU:0")
    else:
        assert 0, "Unsupported device"

    if operator == "matmul":
        assert len(operands_shape) == 2
        with _device:
            lhs_data = tf.random.normal(operands_shape[0], dtype=tf.float32)
            rhs_data = tf.random.normal(operands_shape[1], dtype=tf.float32)

        def bench_func(lhs, rhs):
            with _device:
                return tf.matmul(lhs, rhs)
    elif operator == "batch-matmul":
        assert len(operands_shape) == 2
        with _device:
            lhs_data = tf.random.normal(operands_shape[0], dtype=tf.float32)
            rhs_data = tf.random.normal(operands_shape[1], dtype=tf.float32)

        def bench_func(lhs, rhs):
            with _device:
                return tf.batch_matmul(lhs, rhs)

    else:
        assert 0, "Unsupported operator in tensorflow_benchmark"

    results = []
    for _ in range(measure_count):
        start_time = time.time()
        for _a in range(repetitions):
            bench_func(lhs_data, rhs_data)
        end_time = time.time()
        avg_time = end_time - start_time
        results.append(avg_time / float(repetitions) * 1000.0)
    if warmups == 0:
        return results
    else:
        return results[warmups:-1]


def quark_op_benchmark(oppath_vmfb, operands_shape, warmups=0, repetitions=1, measure_count=1, device='cpu', verbose=False):
    from quark.utils import destringify, stringify_tensor

    if device == "cpu":
        _device = "local-task"
    elif device == "gpu":
        _device = "cuda"
    else:
        assert 0, "Unsupported device"

    config = iree.runtime.system_api.Config(_device)
    vmi = iree.runtime.VmInstance()
    with open(oppath_vmfb, 'rb') as file:
        binary_data = file.read()
    vmm = iree.runtime.VmModule.from_flatbuffer(vmi, binary_data)

    input_data = []
    for operand_shape in operands_shape:
        input_data.append(stringify_tensor(operand_shape))

    def bench_func():
        return iree.runtime.benchmark_module(
            vmm,
            entry_function="matmul",
            inputs=input_data,
            device=_device,
            batch_size=repetitions,
            benchmark_repetitions=measure_count,
            batch_concurrency=1,
            benchmark_min_time="1s",
            print_statistics=verbose
        )

    bench_result = bench_func()
    if measure_count > 1:
        forward_timecost = [destringify(measure.time, unit='ms')
                            for measure in bench_result[0:measure_count]]
    else:
        forward_timecost = [destringify(bench_result[0].time, unit='ms')]
    return forward_timecost


def quark_model_benchmark(oppath_vmfb, entry_func, operands_shape, warmups=0, repetitions=1, measure_count=1, device='cpu', record_mem=False, verbose=False):
    from quark.utils import destringify, stringify_tensor

    if device == "cpu":
        _device = "local-task"
    elif device == "gpu":
        _device = "cuda"
    else:
        assert 0, "Unsupported device"

    config = iree.runtime.system_api.Config(_device)
    vmi = iree.runtime.VmInstance()
    with open(oppath_vmfb, 'rb') as file:
        binary_data = file.read()
    vmm = iree.runtime.VmModule.from_flatbuffer(vmi, binary_data)

    input_data = []
    for operand_shape in operands_shape:
        # print(operand_shape)
        input_data.append(stringify_tensor(operand_shape))
        # print(input_data)

    def bench_func():
        return iree.runtime.benchmark_module(
            vmm,
            entry_function=entry_func,
            inputs=input_data,
            device=_device,
            batch_size=repetitions,
            benchmark_repetitions=measure_count,
            batch_concurrency=1,
            benchmark_min_time="1s",
            print_statistics=verbose
        )

    bench_result = bench_func()
    print(bench_result)
    if measure_count > 1:
        forward_timecost = [destringify(measure.time, unit='ms')
                            for measure in bench_result[0:measure_count]]
    else:
        forward_timecost = [destringify(bench_result[0].time, unit='ms')]
    if record_mem:
        return forward_timecost
    else:
        return forward_timecost
