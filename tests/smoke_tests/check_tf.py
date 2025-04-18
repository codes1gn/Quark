
import tensorflow as tf

def check_tensorflow():
    # Check TensorFlow version
    print(f"TensorFlow Version: {tf.__version__}")

    # Check if CUDA is available
    print(f"CUDA Available: {tf.test.is_built_with_cuda()}")

    # Check GPU devices
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        print("GPU Devices:")
        for gpu in gpus:
            print(f"  - {gpu.name}")
    else:
        print("No GPU devices found.")

    # Check CUDA and cuDNN versions using an alternative approach
    try:
        from tensorflow.python.platform import build_info
        if hasattr(build_info, 'build_info'):
            print(f"CUDA Version: {build_info.build_info.get('cuda_version', 'Not Found')}")
            print(f"cuDNN Version: {build_info.build_info.get('cudnn_version', 'Not Found')}")
        else:
            print("CUDA Version: Not Found (build_info missing)")
            print("cuDNN Version: Not Found (build_info missing)")
    except Exception as e:
        print(f"Error retrieving CUDA/cuDNN version: {e}")

    # Check TensorFlow library location
    print(f"TensorFlow Library Location: {tf.__file__}")

if __name__ == "__main__":
    check_tensorflow()
