from huggingface_hub import snapshot_download
from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer
import torch
import asyncio

print("CUDA Count: ", torch.cuda.device_count())
for i in range(torch.cuda.device_count()):
    print(f"GPU {i}: {torch.cuda.get_device_name(i)}")

# https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B
model_dir = snapshot_download(repo_id="unsloth/DeepSeek-R1-Distill-Qwen-7B-GGUF", local_dir="./models/unsloth/DeepSeek-R1-Distill-Qwen-7B-GGUF")

print(f"Model successfully downloaded.")

# Load the tokenizer and model from the local directory
# tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
# model = AutoModelForCausalLM.from_pretrained(model_dir, trust_remote_code=True,
#                                                device_map="auto")  # use GPU if available

# # Generate text
# prompt = "Once upon a time"

# inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
# inputs = {key: value.to(model.device) for key, value in inputs.items()}

# output_ids = model.generate(inputs["input_ids"], 
#                             attention_mask=inputs["attention_mask"],
#                             pad_token_id=tokenizer.pad_token_id,
#                             # max_new_tokens=4096/4/8,
#                             max_length=50,
#                             do_sample=True,
#                             temperature=0.6)

# output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

# print(output_text)

# async def stream_generate(prompt):
#     """Generate text and stream it live."""
#     inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
#     inputs = {key: value.to(model.device) for key, value in inputs.items()}

#     # Stream generation
#     stream = model.generate(
#         inputs["input_ids"],
#         attention_mask=inputs["attention_mask"],
#         pad_token_id=tokenizer.pad_token_id,
#         max_new_tokens=4096/4/8,
#         do_sample=True,
#         temperature=0.6,
#         streamer=TextIteratorStreamer(tokenizer, skip_prompt=True)
#     )

#     async for text in stream:
#         print(text, end="", flush=True)  # Print characters as they are generated
#         await asyncio.sleep(0)  # Yield control to other tasks

# asyncio.run(stream_generate(prompt))