import torch
print(torch.__version__)
print(torch.version.cuda)

print(torch.cuda.is_available())  # Should print: True
print(torch.cuda.device_count())  # Should print: 1 (or more, if you have multiple GPUs)
print(torch.cuda.get_device_name(0))  # Should print your GPU's name