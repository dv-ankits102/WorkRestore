from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import win32com.client


@dataclass
class DocumentInfo:
    """Information about an open Office document."""

    application_name: str
    document_path: str
    executable: str


OFFICE_APPLICATIONS = {
    "Word.Application": "WINWORD.EXE",
    "Excel.Application": "EXCEL.EXE",
    "PowerPoint.Application": "POWERPNT.EXE",
}


def _get_word_documents() -> List[DocumentInfo]:
    """Return currently open Microsoft Word documents."""

    documents: List[DocumentInfo] = []

    try:
        word = win32com.client.GetActiveObject(
            "Word.Application"
        )

        for document in word.Documents:
            try:
                path = str(
                    document.FullName
                )

                if not path:
                    continue

                document_path = Path(path)

                if not document_path.is_file():
                    continue

                documents.append(
                    DocumentInfo(
                        application_name="WINWORD.EXE",
                        document_path=path,
                        executable=str(
                            Path(word.Path)
                            / "WINWORD.EXE"
                        ),
                    )
                )

            except Exception:
                continue

    except Exception:
        pass

    return documents


def _get_excel_documents() -> List[DocumentInfo]:
    """Return currently open Microsoft Excel workbooks."""

    documents: List[DocumentInfo] = []

    try:
        excel = win32com.client.GetActiveObject(
            "Excel.Application"
        )

        for workbook in excel.Workbooks:
            try:
                path = str(
                    workbook.FullName
                )

                if not path:
                    continue

                document_path = Path(path)

                if not document_path.is_file():
                    continue

                documents.append(
                    DocumentInfo(
                        application_name="EXCEL.EXE",
                        document_path=path,
                        executable=str(
                            Path(excel.Path)
                            / "EXCEL.EXE"
                        ),
                    )
                )

            except Exception:
                continue

    except Exception:
        pass

    return documents


def _get_powerpoint_documents() -> List[DocumentInfo]:
    """Return currently open Microsoft PowerPoint presentations."""

    documents: List[DocumentInfo] = []

    try:
        powerpoint = win32com.client.GetActiveObject(
            "PowerPoint.Application"
        )

        for presentation in powerpoint.Presentations:
            try:
                path = str(
                    presentation.FullName
                )

                if not path:
                    continue

                document_path = Path(path)

                if not document_path.is_file():
                    continue

                documents.append(
                    DocumentInfo(
                        application_name="POWERPNT.EXE",
                        document_path=path,
                        executable=str(
                            Path(powerpoint.Path)
                            / "POWERPNT.EXE"
                        ),
                    )
                )

            except Exception:
                continue

    except Exception:
        pass

    return documents


def get_open_office_documents() -> List[DocumentInfo]:
    """
    Return currently open Word, Excel and PowerPoint files.
    """

    documents: List[DocumentInfo] = []

    documents.extend(
        _get_word_documents()
    )

    documents.extend(
        _get_excel_documents()
    )

    documents.extend(
        _get_powerpoint_documents()
    )

    return documents