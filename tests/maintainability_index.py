import os
import radon.metrics

exclude_dirs = ("venv", "build", ".git", ".idea", "__pycache__")
exclude_files = ("__init__.py", "maintainability_index.py")

scores = []
for address, dirs, files in os.walk(".."):
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    files = list(filter(lambda x: x.endswith(".py") and x not in exclude_files, files))
    for file in files:
        path = os.path.join(address, file)
        with open(path, mode="r") as fp:
            score = radon.metrics.mi_visit(fp.read(), True)
            print(f"{path}: {score:.4f}")
            scores.append(score)

print(f"Average MI: {sum(scores) / len(scores):.4f}")
