def test_import_order():
    print("Testing import order for TensorFlow and PyTorch...\n")

    # Test 1: Import TensorFlow first, then PyTorch
    print("Test 1: Import TensorFlow first, then PyTorch")
    try:
        import tensorflow as tf
        print(f"Successfully imported TensorFlow: {tf.__version__}")
        import torch
        print(f"Successfully imported PyTorch: {torch.__version__}")
        print("Test 1: PASSED\n")
    except Exception as e:
        print(f"Test 1: FAILED with error: {e}\n")

    # Test 2: Import PyTorch first, then TensorFlow
    print("Test 2: Import PyTorch first, then TensorFlow")
    try:
        import torch
        print(f"Successfully imported PyTorch: {torch.__version__}")
        import tensorflow as tf
        print(f"Successfully imported TensorFlow: {tf.__version__}")
        print("Test 2: PASSED\n")
    except Exception as e:
        print(f"Test 2: FAILED with error: {e}\n")

    print("Import order test completed.")

if __name__ == "__main__":
    test_import_order()
