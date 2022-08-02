from __future__ import print_function;
import json, sys, yaml;

def duplicate_branch_check(jobs):
  count = 0
  by_name = {job['name']: job for job in jobs}
  for job in jobs:
    for name, other in by_name.items():
      if name == job['name']:
        continue
      if job['name'].startswith(name):
        if 'branches' not in job:
          print(
              f"error: job {job['name']} is set to cover all branches and overlaps with job {other['name']}"
          )
          count += 1
          continue
        if 'branches' not in other:
          print(
              f"error: job {other['name']} is set to cover all branches and overlaps with job {job['name']}"
          )
          count += 1
          continue
        if shared := list(set(job['branches']) & set(other['branches'])):
          print(
              f"error: job {other['name']} has branch overlap with job {job['name']}: {shared}"
          )
          count += 1
  return count

y = yaml.load(open(sys.argv[1]))
errors = sum(
    duplicate_branch_check(y['postsubmits'][name])
    for name in y['postsubmits'])
for name in y['presubmits']:
  errors += duplicate_branch_check(y['presubmits'][name])
if errors > 0:
  exit(1)
