import re
from pathlib import PurePosixPath

from fastapi.staticfiles import StaticFiles
from starlette.responses import Response
from starlette.types import Scope


_REPORT_FILENAME_PATTERN = re.compile(
    r"(?:inventario|alertas|movimientos)-[0-9a-f]{8}\.(?:pdf|xlsx)"
)


class DownloadableReportStaticFiles(StaticFiles):
    """Serve generated reports as attachments without changing their static URLs."""

    async def get_response(self, path: str, scope: Scope) -> Response:
        response = await super().get_response(path, scope)
        filename = PurePosixPath(path).name

        if (
            response.status_code == 200
            and path == filename
            and _REPORT_FILENAME_PATTERN.fullmatch(filename)
        ):
            response.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
            response.headers["Cache-Control"] = "private, no-store"

        return response
