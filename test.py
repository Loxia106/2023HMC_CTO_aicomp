# docs/gen_ref_nav.py
from pathlib import Path
import mkdocs_gen_files

PKG = "yourpkg"               # 패키지명
SRC = Path("src") / PKG       # 코드 루트 (src 레이아웃이 아니면 Path(".")/PKG)

nav = mkdocs_gen_files.Nav()

for path in sorted(SRC.rglob("*.py")):
    if path.name == "__init__.py":
        mod_name = ".".join([PKG, *path.relative_to(SRC).parts[:-1]]) or PKG
        doc_path = Path("reference", *path.relative_to(SRC).parts[:-1], "index.md")
    else:
        mod_name = ".".join([PKG, *path.relative_to(SRC).with_suffix("").parts])
        doc_path = Path("reference", *path.relative_to(SRC).with_suffix(".md").parts)

    # 내비게이션 구성
    parts = doc_path.parts[1:-1] if doc_path.name == "index.md" else doc_path.parts[1:]
    if parts:
        nav[tuple(parts)] = doc_path.as_posix()

    with mkdocs_gen_files.open(doc_path, "w") as f:
        print(f"# `{mod_name}`", file=f)
        print(f"\n::: {mod_name}\n", file=f)

    mkdocs_gen_files.set_edit_path(doc_path, path)

# 사이드바용 요약 파일
with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
