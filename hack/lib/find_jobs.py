from __future__ import print_function
import json, sys, yaml;

def find_jobs_for_branch(jobs, branch):
  found = []
  for job in jobs:
    if 'branches' not in job:
      found.append(job)
      continue
    if branch in job['branches']:
      found.append(job)
      continue
  return sorted(found, key=lambda job: job['name'])

errors = 0
y = yaml.load(open(sys.argv[1]))
if sys.argv[2] in y['postsubmits']:
  for job in find_jobs_for_branch(y['postsubmits'][sys.argv[2]], sys.argv[3]):
    print(f"postsubmit: {job['name']}")
if sys.argv[2] in y['presubmits']:
  for job in find_jobs_for_branch(y['presubmits'][sys.argv[2]], sys.argv[3]):
    print(f"presubmit: {job['name']}{'' if 'always_run' in job else ' [opt]'}")
