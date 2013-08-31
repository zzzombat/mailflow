from mailflow import settings
from fs.osfs import OSFS

fs = OSFS(settings.RAW_EMAIL_FOLDER)