import sys
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import hashlib

def random_int(name):
    hash_value = hashlib.sha256(name.encode()).digest()  # 32-byte hash
    return int.from_bytes(hash_value[:8], 'big')

def anonymize_log(log, out_dir, hash_val):
    logfile_comps = log.name.split('_')
    jobid = logfile_comps[-3].split('-')[0][2:]
    rand_val = random_int(log.name)
    new_log = out_dir / Path(f'{jobid}-{rand_val}.darshan')
    command = ["darshan-convert",
               "--bzip2",
               "--obfuscate_uid",
               "--obfuscate_exe",
               "--obfuscate_names",
               f"--key={hash_val}",
               log,
               new_log]
    result = subprocess.run(command)
    if result.returncode != 0:
        print(f'failed to anonymize input log {log} (ouptut={new_log})')
    return result.returncode

def anonymize_logs_in_parallel(log_files, out_dir, hash_val, max_workers=32):
    n_success = 0
    # a ThreadPoolExecutor is sufficient for parallelizing this, as we are
    # ultimately spawning new subprocesses to anonymize each log
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {executor.submit(anonymize_log, log, out_dir, hash_val): log for log in log_files}
        for future in future_map:
            log = future_map[future]
            result = future.result()
            if result == 0:
                n_success += 1
    return n_success

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python darshan-logs-anonymize.py <input_log_dir> <output_log_dir> <hash_val>')
        sys.exit(1)
    log_dir = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    hash_val = sys.argv[3]

    log_files = list(log_dir.rglob("*.darshan"))
    n_success = anonymize_logs_in_parallel(log_files, out_dir, hash_val)

    total = len(log_files)
    print(f"total: {total}")
    print(f"successes: {n_success}")
    print(f"failures: {total-n_success}")
