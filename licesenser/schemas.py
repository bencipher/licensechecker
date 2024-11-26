from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class ucstr(str):
    """Uppercase string."""

    __slots__ = ()

    def __new__(cls, v: str | None) -> "ucstr":
        """Create a new ucstr from a str.

        :param str v: string to cast
        :return ucstr: uppercase string.
        """
        if v is None:
            return ucstr("")
        return super().__new__(cls, v.upper())

    def __get_pydantic_core_schema__(self, handler):
        return handler.generate_schema(str)


UNKNOWN = ucstr("UNKNOWN")
JOINS = ucstr(";; ")


class PackageInfo(BaseModel):
    """PackageInfo type."""

    name: str
    local_version: Optional[str] = Field(default=UNKNOWN)
    latest_version: Optional[str] = Field(default=UNKNOWN)
    size: int = Field(default=-1)
    homepage: Optional[str] = Field(default=UNKNOWN)

    author: Optional[str] = Field(default=UNKNOWN)
    author_email: Optional[str] = Field(default=UNKNOWN)
    license: ucstr = Field(default=UNKNOWN)
    is_license_compatible: bool = Field(default=False)
    error_code: int = Field(default=0)

    @property
    def name_with_version(self) -> str:
        """Return the name and local version."""
        return f"{self.name}-{self.local_version}"

    @field_validator("name")
    def name_must_not_be_empty(cls, v):
        if not v:
            raise ValueError("name must not be empty")
        return v

    def __hash__(self):
        return hash((self.name, self.local_version, self.latest_version))

    def __eq__(self, other):
        if not isinstance(other, PackageInfo):
            return NotImplemented
        return (self.name, self.local_version, self.latest_version) == (
            other.name,
            other.local_version,
            other.latest_version,
        )

    def get_filtered_dict(self, hide_output_parameters: List[ucstr]) -> dict:
        """Return a filtered dictionary of the object.

        :param list[ucstr] hide_output_parameters: list of parameters to ignore
        :return dict: filtered dictionary
        """
        return {
            k: v
            for k, v in self.model_dump().items()  # Use Pydantic's dict method
            if k.upper() not in hide_output_parameters
        }
