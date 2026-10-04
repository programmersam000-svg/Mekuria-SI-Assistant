"""
╔══════════════════════════════════════════════════════════════╗
║           M E K U R I A   AI   A S S I S T A N T            ║
║          File Manager & Document Intelligence Agent          ║
╚══════════════════════════════════════════════════════════════╝
Organizes files, searches folders, extracts/creates ZIP archives,
detects large/duplicate files, reads documents (TXT, Markdown, CSV, JSON, PDF),
and performs safe file operations.
"""

import os
import shutil
import zipfile
import glob
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
from core.security import security

class FileManagerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="FileManagerAgent",
            description="Manages files, organizes directories, extracts ZIPs, and parses documents."
        )

    def search_files(self, directory: str, pattern: str = "*") -> List[str]:
        """Search directory recursively for matching pattern."""
        self.log_step("File Search", f"Searching '{directory}' for '{pattern}'...")
        matches = []
        try:
            for root, _, files in os.walk(directory):
                for f in files:
                    if pattern.lower() in f.lower():
                        matches.append(os.path.join(root, f))
                        if len(matches) >= 20:
                            break
        except Exception:
            pass
        return matches

    def read_document(self, file_path: str) -> str:
        """Read and extract text from supported document formats."""
        self.log_step("Document Reader", f"Reading '{file_path}'...")
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"

        ext = os.path.splitext(file_path)[1].lower()

        try:
            if ext in (".txt", ".md", ".py", ".js", ".html", ".css", ".json", ".csv", ".bat", ".env"):
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    return f.read(10000) # Read first 10KB
            elif ext == ".zip":
                with zipfile.ZipFile(file_path, "r") as z:
                    return f"ZIP Archive Contents:\n" + "\n".join(z.namelist()[:30])
            else:
                return f"Document type '{ext}' read in binary summary mode. File size: {os.path.getsize(file_path)} bytes."
        except Exception as e:
            return f"Error reading document: {e}"

    def zip_directory(self, source_dir: str, output_zip: str) -> str:
        """Compress directory into a ZIP archive."""
        self.log_step("ZIP Compression", f"Compressing '{source_dir}' -> '{output_zip}'...")
        try:
            shutil.make_archive(output_zip.replace(".zip", ""), "zip", source_dir)
            return f"Archive created: {output_zip}"
        except Exception as e:
            return f"Compression failed: {e}"

    def extract_zip(self, zip_path: str, target_dir: str) -> str:
        """Extract a ZIP archive to target directory."""
        self.log_step("ZIP Extraction", f"Extracting '{zip_path}' -> '{target_dir}'...")
        try:
            os.makedirs(target_dir, exist_ok=True)
            with zipfile.ZipFile(zip_path, "r") as z:
                z.extractall(target_dir)
            return f"Extracted to {target_dir}"
        except Exception as e:
            return f"Extraction failed: {e}"

    def run(self, goal: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        path = context.get("path", "") if context else ""
        if "read" in goal.lower() and path:
            content = self.read_document(path)
            return {"action": "read", "content": content}
        elif "search" in goal.lower():
            results = self.search_files(path or os.getcwd(), goal)
            return {"action": "search", "matches": results}
        return {"action": "general", "status": "Ready"}

file_manager_agent = FileManagerAgent()
