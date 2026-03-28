import os


def collect_project_for_analysis():
    # Папки, которые мы игнорируем (там очень много лишнего текста)
    exclude_dirs = {".git", "__pycache__", ".venv", "venv", ".pytest_cache", ".idea", ".vscode"}
    # Расширения файлов, которые нам интересны
    include_extensions = (".py", ".txt", ".toml", ".yaml", ".yml", ".env.example", ".md")

    output_filename = "project_structure_and_code.txt"

    with open(output_filename, "w", encoding="utf-8") as outfile:
        for root, dirs, files in os.walk("."):
            # Удаляем ненужные папки из обхода
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                if file.endswith(include_extensions) and file != os.path.basename(__file__):
                    file_path = os.path.join(root, file)
                    outfile.write(f"\n\n{'=' * 30}\n")
                    outfile.write(f"PATH: {file_path}\n")
                    outfile.write(f"{'=' * 30}\n\n")

                    try:
                        with open(file_path, "r", encoding="utf-8") as infile:
                            outfile.write(infile.read())
                    except Exception as e:
                        outfile.write(f"ОШИБКА ЧТЕНИЯ ФАЙЛА: {e}")

    print(f"✅ Готово! Весь твой проект собран в файл: {output_filename}")


if __name__ == "__main__":
    collect_project_for_analysis()
