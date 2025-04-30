import torch

print("PyTorch version:", torch.__version__)
print("CUDA version (compiled):", torch.version.cuda)
print("CUDA available (runtime):", torch.cuda.is_available())
print("CUDA device count:", torch.cuda.device_count())

if torch.cuda.is_available():
    print("Current device:", torch.cuda.current_device())
    print("Device name:", torch.cuda.get_device_name(torch.cuda.current_device()))

x = torch.rand(3, 3).cuda()
y = torch.rand(3, 3).cuda()
z = x + y
print("Computation result on GPU:\n", z)
