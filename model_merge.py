import shutil
from safetensors.torch import load_file, save_file
import glob
import os
from concurrent.futures import ThreadPoolExecutor

# -------------------------
# 配置
# -------------------------
ckpt1_dir = "/mnt/afs/oulinyu/ICASSP2026/swift_exp_grpo/megatron_output/Qwen3-Omni-30B-A3B-Instruct/v1-20251127-215010/checkpoint-372"  # grpo模型
ckpt2_dir = "/mnt/afs/likehan/icassp2026-hd/.sft_model_full_tasks/v2-20251121-140457-hf"  # sft模型
module_to_replace = "thinker"  # 想替换的模块名
num_shards = 15  # 分片数量
new_ckpt_dir = ckpt1_dir + "-thinker-from-ckpt1-fixed"  # 新模型保存目录
os.makedirs(new_ckpt_dir, exist_ok=True)

# -------------------------
# 1. 从 ckpt1 提取 thinker 权重
# -------------------------
ckpt1_files = sorted(glob.glob(f"{ckpt1_dir}/model-*.safetensors"))
thinker_dict = {}

for file_path in ckpt1_files:
    shard = load_file(file_path)
    for k, v in shard.items():
        if k == module_to_replace or k.startswith(module_to_replace + "."):
            thinker_dict[k] = v
    del shard

print(f"从 ckpt1 找到模块 '{module_to_replace}' 参数数: {len(thinker_dict)}")
if len(thinker_dict) == 0:
    raise RuntimeError(f"⚠️ 在 ckpt1 中未找到模块 '{module_to_replace}'，请检查名称。")

# -------------------------
# 2. 遍历 ckpt2 分片，替换 thinker 模块
# -------------------------
ckpt2_files = sorted(glob.glob(f"{ckpt2_dir}/model-*.safetensors"))

def process_and_save_shard_old(i, file_path):
    shard = load_file(file_path)
    # 替换 thinker 模块
    for k, v in thinker_dict.items():
        shard[k] = v
    # 保存到新目录
    new_path = f"{new_ckpt_dir}/model-{i+1:05d}-of-{num_shards:05d}.safetensors"
    save_file(shard, new_path)
    print(f"✅ 保存分片 {i+1}/{num_shards}")

def process_and_save_shard(i, file_path):
    shard = load_file(file_path)
    # 只替换存在的 thinker 参数
    for k, v in thinker_dict.items():
        if k in shard:
            shard[k] = v
    # 保存到新目录
    new_path = f"{new_ckpt_dir}/model-{i+1:05d}-of-{num_shards:05d}.safetensors"
    save_file(shard, new_path)
    print(f"✅ 保存分片 {i+1}/{num_shards}")


# 并行写入
with ThreadPoolExecutor(max_workers=min(num_shards, 8)) as executor:
    futures = [executor.submit(process_and_save_shard, i, f) for i, f in enumerate(ckpt2_files)]
    for f in futures:
        f.result()
        
# -------------------------
# 3. 拷贝非 model-*.safetensors 的其他文件
# -------------------------
other_files = [f for f in os.listdir(ckpt2_dir) if not f.startswith("model-") or not f.endswith(".safetensors")]
for file_name in other_files:
    src_path = os.path.join(ckpt2_dir, file_name)
    dst_path = os.path.join(new_ckpt_dir, file_name)
    shutil.copy2(src_path, dst_path)
    print(f"📄 拷贝文件 {file_name}")

print(f"🎉 模块 '{module_to_replace}' 已从 ckpt1 替换到 ckpt2，新模型保存到 {new_ckpt_dir}")