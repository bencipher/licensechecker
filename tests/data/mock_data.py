valid_licenses = [
    """This software is licensed under the **Lesser General Public License
      (LGPL v3.0)**, meaning you are free to use, modify, and distribute this
        tool, provided that:""",
    """GNU LESSER GENERAL PUBLIC LICENSE Version 3, 29 June 2007
    Copyright (C) 2007 Free Software Foundation, Inc. <https://fsf.org/>
      Everyone is permitted to copy and distribute verbatim copies of this
        license document, but changing it is not allowed.""",
]

invalid_licenses = [
    """This software is licensed under the ****, meaning you are free
      to use, modify, and distribute this tool, provided that:""",
    """GNU LICENSE, 29 June 2007 Copyright (C) 2007 Free Software
    Foundation, Inc. <https://fsf.org/> Everyone is permitted to copy
      and distribute verbatim copies of this license document, but
      changing it is not allowed.""",
]


empty_license = ["", " ", "\n"]


invalid_file_content = [
    "This is not a valid license text.",
    "No license information here.",
]

# Mock directory structure
mock_directory_valid_structure = {
    "license.md": valid_licenses[0],
    "license": valid_licenses[1],
    "setup.cfg": "[metadata]\nname = example\nversion = 0.1.0\nlicense = MIT License\n",
    "pyproject.toml": '[tool.poetry]\nname = "example"\nversion = "0.1.0"\nlicense = "MIT License"\n',
}
# Mock directory structure
mock_directory_invalid_structure = {
    "license.md": invalid_licenses[0],
    "license.apache.rst": invalid_licenses[1],
    "license": empty_license[0],
    "invalid_file_content.txt": invalid_file_content[0],
}
