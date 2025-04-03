import requests
import urllib3
import json
import os

file_url = 'https://patch-diff.githubusercontent.com/raw/bharath-b-rh/common-problems/pull/1.diff'
http     = urllib3.PoolManager()
response = http.request('GET', file_url)
diff     = response.data.decode('utf-8')

from unidiff import PatchSet

patch_set = PatchSet(diff)

change_list = []
model_name = 'mistralai/Mixtral-8x7B-Instruct-v0.1'
max_context_size = 32768
response_size = 1000
current_diff = ""

endpoint = 'https://api.together.xyz/inference'
TOGETHER_API_KEY = os.environ['TOGETHER_API_KEY']

SYSTEM_CONTENT = """You are a code reviewer, a language model designed to review code changes in git diff format.
Your task is to provide constructive and concise feedback for the PR, and also provide meaningful code suggestions.

Example PR Diff:
======
diff --git a/file1.go b/file1.go
index xxxx..yyyy zzzz
--- a/file1.go
+++ b/file1.go
@@ -12,5 +12,5 @@
  code line 1 that remained unchanged in the PR
  code line 2 that remained unchanged in the PR
- code line that was removed in the PR
+ code line added in the PR
  code line 3 that remained unchanged in the PR

@@ ... @@ func example():
...

diff --git a/file2.go b/file2.go
...
======

Consider only the lines between the line starting with '@@' and the line starting with 'diff'.

Recommend best coding practices.
Code suggestions guidelines:
- Provide up to 2 code suggestions. Try to provide diverse and insightful suggestions.
- Focus on important suggestions like fixing code problems, issues and bugs. As a second priority, provide suggestions for meaningful code improvements like performance, vulnerability, modularity, and best practices.
- Avoid making suggestions that have already been implemented in the PR code. For example, if you want to add logs, or change a variable to const, or anything else, make sure it isn't already in the PR code.
- Don't suggest to add docstring, type hints, or comments.
- Suggestions should focus on the new code added in the PR diff (lines starting with '+') or code removed in the PR diff (lines starting with '-')
- Don't comment on unchanged lines in the PR diff (lines starting with ' ')
- When quoting variables or names from the code, use backticks (`) instead of single quote (').
- If the content is good, don't comment on it.
- Suggest and generate the unit test code which can be added for the changes in the PR.

The output must be a YAML object equivalent to type $PRReview, according to the following Pydantic definitions. The YAML should contain the relevant lines along with the '+' or '-' prefix from the provided PR diff for each file.

class CodeSuggestion(BaseModel):
    file: str = Field(description="the relevant file full path")
    relevant_line: str = Field(description="consecutive line(s) taken from the relevant file, to which the suggestion applies. The code line(s) should start with a '+' or '-'. Make sure to output the line(s) exactly as it appears in the relevant file")
    suggestion: str = Field(description="a concrete suggestion for meaningfully improving the new PR code. Also describe how, specifically, the suggestion can be applied to new PR code. Add tags with importance measure that matches each suggestion ('important' or 'medium'). Do not make suggestions for updating or adding docstrings, renaming PR title and description, or linter like. Suggest what unit test scenarios can be added with the code snippet.")

class PRReview(BaseModel):
    review: Review
    code_feedback: List[CodeSuggestion]

Example output YAML file:

```yaml
review:
    - file: go.mod
      relevant_lines: |
          + xxx
          + xxx
      suggestion: |
          xxx
          xxx
    - file: pkg/controller.go
      relevant_lines: |
          + xxx
          - xxx
      suggestion: |
          xxx
          xxx
    - file: pkg/controller.go
      relevant_lines: |
          - xxx
          + xxx
      suggestion: |
          xxx
          xxx
```
"""

PROMPT = """Improve this content.
Don't comment on file names or other meta data, just the actual text.
Make sure to give very concise feedback per file.
Answer should be a valid YAML, and nothing else.
At the end provide a detailed summary of the changes made in the pr.
"""

count = 0
for patched_file in patch_set:
    count = count + 1
    file_path = patched_file.path  # file name
    if "vendor/" in file_path \
    or file_path == "go.mod" \
    or file_path == "go.sum" \
    or file_path == "Makefile" \
    or file_path == "README.md" \
    or file_path == "LICENSE" \
    or file_path == ".gitignore":
        continue

    if len(current_diff) + len(str(patched_file)) + response_size < max_context_size:
        current_diff = current_diff + str(patched_file)
        if count != len(patch_set):
            continue

    prompt_template=f'''SYSTEM: {SYSTEM_CONTENT}

    USER: This is the PR diff: {current_diff}. {PROMPT}

    ASSISTANT:
    '''

    res = requests.post(endpoint, json={
        "model": model_name,
        "prompt": prompt_template,
        "top_p": 1,
        "top_k": 40,
        "temperature": 0,
        "repetition_penalty": 1,
    }, headers={
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "User-Agent": "Test"
    })

    print(res.json()['choices'][0]['text'])

    current_diff = str(patched_file)
