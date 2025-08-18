from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtGui import QPixmap, QFont, QCursor, QIcon
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices

try:
	from modules.otherTools import translation
except Exception:
	# Fallback simple translation (avoid crash if import path changes)
	def translation(key, lang):
		return key

class AboutDialog(QDialog):
	def __init__(self, parent):
		super().__init__(parent)
		self.parent = parent
		self.lang = getattr(parent, 'user_language', 'en')
		self.setWindowTitle(translation("about_dialog_title", self.lang))
		self.setModal(True)
		try:
			self.setWindowIcon(QIcon("images/ansiflow-icon.png"))
		except Exception:
			pass
		self.buildUI()

	def buildUI(self):
		layout = QVBoxLayout()
		layout.setContentsMargins(20,20,20,20)
		layout.setSpacing(12)

		# Logo
		logo_label = QLabel()
		pix = QPixmap("images/ansiflow.png")
		if not pix.isNull():
			logo_label.setPixmap(pix.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
			logo_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
			layout.addWidget(logo_label)

		# Description
		desc = QLabel(translation("about_dialog_description", self.lang))
		desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
		desc.setWordWrap(True)
		layout.addWidget(desc)

		# Version
		version_text = f"{translation('about_dialog_version', self.lang)}: {getattr(self.parent, 'app_version', '0.0.0')}"
		version_label = QLabel(version_text)
		version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		layout.addWidget(version_label)

		# Link
		link_layout = QHBoxLayout()
		link_layout.addStretch()
		link_prefix = QLabel(translation("about_dialog_website", self.lang))
		link_prefix.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
		project_url = "https://github.com/4strium/Ansiflow"
		link_label = QLabel(f"<a href='{project_url}' style='color:#2979ff;text-decoration:none;'>GitHub</a>")
		link_label.setOpenExternalLinks(True)
		link_layout.addWidget(link_prefix)
		link_layout.addWidget(link_label)
		link_layout.addStretch()
		layout.addLayout(link_layout)

		# Close button
		close_btn = QPushButton(translation("about_dialog_close", self.lang))
		close_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
		close_btn.clicked.connect(self.accept)
		close_btn.setDefault(True)
		layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)

		self.setLayout(layout)
		self.setFixedWidth(400)
		self.adjustSize()
