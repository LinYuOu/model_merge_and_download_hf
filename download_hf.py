import os
import importlib
util = importlib.import_module('importlib.util')
if util.find_spec("huggingface_hub") is None:
    os.system("pip install huggingface_hub")

# os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"


from huggingface_hub import snapshot_download
from time import sleep
import argparse
import hashlib
# python download_hf.py --repo_id zai-org/CogVideoX-5b --local_dir hf

parser = argparse.ArgumentParser()
parser.add_argument('repo_id')
parser.add_argument('--local-dir', '--local_dir', type=str, default=None)
# 默认我们设置cache_dir为local_dir
parser.add_argument('--cache-dir', '--cache_dir', type=str, default=None)
# 默认的话会下载model，设置为None也是下载model
parser.add_argument('--repo-type', '--repo_type', type=str, default="model")
args, unknown = parser.parse_known_args()

if args.local_dir:
    args.local_dir = os.path.realpath(os.path.expanduser(args.local_dir))
else:
    args.local_dir = args.repo_id.split('/')[-1]
    
os.makedirs(args.local_dir, exist_ok=True)
if not args.cache_dir:
    args.cache_dir = args.local_dir
else:
    args.cache_dir = os.path.realpath(os.path.expanduser(args.cache_dir))

while True:
    try:
        # import pdb; pdb.set_trace()
        snapshot_path = snapshot_download(
            repo_id=args.repo_id,
            repo_type=args.repo_type,
            # allow_patterns="cogagent-chat.zip",
            local_dir=args.local_dir,
            cache_dir=args.cache_dir,
            resume_download=True,
        )
        break
    except Exception as e:
        print(e)
        print("60秒后重启！！！！！！")
        sleep(3)

######################################################################################################
######################################################################################################

def get_check_dir():
    REPO_ID_SEPARATOR = "--"
    def repo_folder_name(*, repo_id, repo_type):
        """Return a serialized version of a hf.co repo name and type, safe for disk storage
        as a single non-nested folder.
    
        Example: models--julien-c--EsperBERTo-small
        """
        # remove all `/` occurrences to correctly convert repo to directory name
        parts = [f"{repo_type}s", *repo_id.split("/")]
        return REPO_ID_SEPARATOR.join(parts)
    check_dir = os.path.join(args.cache_dir, repo_folder_name(repo_id=args.repo_id, repo_type=args.repo_type))
    check_dir = os.path.join(check_dir, "blobs")
    return check_dir

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as file:
        while (chunk := file.read(8192)):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

def rm_wrong_file(folder_path):
    complete = 0
    remove_list, ignored_list = [], []
    for root, _, files in os.walk(folder_path):
        for file in files:
            assert "blobs" in root, f"检查路径{folder_path}错误，里面不包含blobs，程序终止"
            file_path = os.path.join(root, file)
            # 区分git-sha1 etag的小文件和sha256 etag的大文件
            if len(file) <= 40:
                ignored_list.append(file_path)
                continue
            
            sha256_hash = calculate_sha256(file_path)
            # filename_without_extension, _ = os.path.splitext(file)
            
            if sha256_hash != file:
                remove_list.append(file_path)
            else:
                complete += 1

    for file_path in remove_list:
        try:
            os.remove(file_path)
        except OSError as e:
            print(f"无法删除文件: {file_path}，错误: {e}")

    print(f"共有{complete+len(ignored_list)+len(remove_list)}个文件被检查，{complete}个文件完整，{len(ignored_list)}个文件被忽略，{len(remove_list)}个文件被删除")
    print("以下文件被忽略：")
    print("\n".join(ignored_list))
    print("以下文件被删除：")
    print("\n".join(remove_list))

print(f"文件下载目录为：'{snapshot_path}'")
print(f"sha256 etag大文件的cache检查目录为：'{get_check_dir()}'")
# 检查每个下载到cache的文件sha256值是否和文件名完全相等，删除sha256值和文件名不相等的文件
rm_wrong_file(get_check_dir())

######################################################################################################
######################################################################################################

maybe_wrong = False
# 再次重新下载被删掉的文件
while True:
    try:
        snapshot_download(
            repo_id=args.repo_id,
            repo_type=args.repo_type,
            # allow_patterns="cogagent-chat.zip",
            local_dir=args.local_dir,
            cache_dir=args.cache_dir,
            resume_download=True,
        )
        break
    except Exception as e:
        print(e)
        maybe_wrong = True
        print("60秒后重启！！！！！！")
        sleep(3)

if maybe_wrong:
    print("可能下载到的文件还有错误，请重新执行本脚本，并查看上面的错误是什么错误")
else:
    print("下载完成，所有文件无误")