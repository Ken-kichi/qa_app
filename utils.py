import os


def get_pdf_paths(folder_path: str) -> list[str]:
    """フォルダ内のすべてのPDFファイルのリストを返します。

    Args:
        folder_path (str): フォルダへのパス。

    Returns:
        list[str]: PDFファイルのリスト。
    """

    pdf_files = []
    for root, _dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))
    return pdf_files
