EXTENSION_TO_LANGUAGE: dict[str, str] = {
    # ─────────── Common Programming Languages ───────────
    ".py": "python",
    ".java": "java",
    ".js": "javascript",
    ".jsx": "javascript",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".c": "c",
    ".h": "c",               
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".c++": "cpp",
    ".hpp": "cpp",
    ".hh": "cpp",
    ".hxx": "cpp",
    ".cs": "csharp",
    ".go": "go",
    ".rs": "rust",
    ".rb": "ruby",
    ".php": "php",
    ".swift": "swift",
    ".kt": "kotlin",
    ".kts": "kotlin",
    ".dart": "dart",
    ".m": "objc",
    ".mm": "objc",           
    ".scala": "scala",
    ".scala.html": "scala",  
    ".erl": "erlang",
    ".ex": "elixir",
    ".exs": "elixir",
    ".hs": "haskell",
    ".lhs": "haskell",
    ".elm": "elm",
    ".clj": "clojure",
    ".cljs": "clojure",
    ".cljc": "clojure",
    ".edn": "clojure",
    ".fs": "fennel",
    ".fennel": "fennel",
    ".d": "d",
    ".vala": "vala",
    ".jl": "julia",
    ".rs": "rust",
    ".sql": "sql",
    ".pgsql": "sql",         
    ".psql": "sql",
    ".r": "r",
    ".kt": "kotlin",
    ".kts": "kotlin",
    ".go": "go",
    ".lua": "lua",
    ".jl": "julia",
    ".sh": "bash",
    ".bash": "bash",
    ".zsh": "bash",          
    ".fish": "fish",
    ".ps1": "powershell",
    ".psm1": "powershell",
    ".vb": "clarity",        
    ".vbs": "clarity",
    ".cmd": "batch",
    ".bat": "batch",
    ".asm": "asm",
    ".s": "asm",
    ".S": "asm",
    ".f90": "fortran",
    ".f95": "fortran",
    ".f": "fortran",
    ".for": "fortran",
    ".rs": "rust",
    # ─────────── Web & Markup ───────────
    ".html": "html",
    ".htm": "html",
    ".xhtml": "xml",
    ".xml": "xml",
    ".xsd": "xml",
    ".xsl": "xml",
    ".json": "json",
    ".jsonc": "json",
    ".jsonnet": "jsonnet",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".csv": "csv",
    ".tsv": "tsv",
    ".md": "markdown",
    ".markdown": "markdown",
    ".mdx": "markdown_inline",
    ".rst": "rst",
    ".org": "org",
    ".tex": "latex",
    ".bib": "bibtex",
    ".csv": "csv",
    # ─────────── Configuration & Build ───────────
    "Makefile": "make",
    "makefile": "make",
    ".mk": "make",
    ".cmake": "cmake",
    "CMakeLists.txt": "cmake",
    "Dockerfile": "dockerfile",
    "dockerfile": "dockerfile",
    ".dockerfile": "dockerfile",
    ".tf": "terraform",
    ".tfvars": "terraform",
    ".hcl": "hcl",
    ".hcl.json": "hcl",
    "go.mod": "gomod",
    "go.sum": "gosum",
    ".gradle": "groovy",
    "BUILD": "gn",
    "BUILD.bazel": "gn",
    ".bazel": "gn",
    ".ninja": "ninja",
    ".meson": "meson",
    "meson.build": "meson",
    ".mk": "make",  
    ".bitbake": "bitbake",
    # ─────────── Scripting & DSLs ───────────
    ".ps1": "powershell",
    ".psm1": "powershell",
    ".rb": "ruby",
    ".py": "python",
    ".pl": "perl",
    ".pm": "perl",
    ".pm6": "perl",
    ".tcl": "tcl",
    ".lua": "lua",
    ".rb": "ruby",
    ".rake": "ruby",
    ".rs": "rust",
    ".go": "go",
    ".hs": "haskell",
    ".erl": "erlang",
    ".sh": "bash",
    ".fish": "fish",
    ".ps1": "powershell",
    ".groovy": "groovy",
    ".gradle": "groovy",
    ".eex": "embeddedtemplate",
    ".heex": "heex",
    ".ex": "elixir",
    ".exs": "elixir",
    ".elm": "elm",
    ".nim": "pony",
    ".pony": "pony",
    ".rio": "pony",
    ".clojure": "clojure",
    ".cljs": "clojure",
    ".cljc": "clojure",
    ".edn": "clojure",
    ".dart": "dart",
    ".qml": "qmljs",
    ".qmljs": "qmljs",
    ".qs": "query",
    ".sh": "bash",
    ".fish": "fish",
    ".ps1": "powershell",
    # ─────────── Language-Specific Source Files ───────────
    ".ada": "ada",
    ".adb": "ada",
    ".ads": "ada",
    ".agda": "agda",
    ".apex": "apex",
    ".ino": "arduino",
    ".astro": "astro",
    ".beancount": "beancount",
    ".bicep": "bicep",
    ".bb": "bitbake",
    ".cairo": "cairo",
    ".capnp": "capnp",
    ".chatito": "chatito",
    ".clarity": "clarity",
    ".commonlisp": "commonlisp",
    ".cl": "commonlisp",
    ".clj": "clojure",
    ".cpon": "cpon",
    ".d": "d",
    ".dart": "dart",
    ".doxygen": "doxygen",
    ".dtd": "dtd",
    ".el": "elisp",
    ".erl": "erlang",
    ".fennel": "fennel",
    ".fir": "firrtl",
    ".func": "func",
    ".gd": "gdscript",
    ".gitattributes": "gitattributes",
    ".gitignore": "gitignore",
    ".glsl": "glsl",
    ".vert": "glsl",
    ".frag": "glsl",
    ".gn": "gn",
    ".hazel": "hare",
    ".hare": "hare",
    ".haxe": "haxe",
    ".heex": "heex",
    ".hlsl": "hlsl",
    ".hypr": "hyprlang",
    ".ispc": "ispc",
    ".janet": "janet",
    ".julia": "julia",
    ".kconfig": "kconfig",
    ".kdl": "kdl",
    ".latex": "latex",
    ".ld": "linkerscript",
    ".ll": "llvm",
    ".lp": "lucid-pascal",
    ".lua": "lua",
    ".luadoc": "luadoc",
    ".luap": "luap",
    ".luau": "luau",
    ".magik": "magik",
    ".matlab": "matlab",
    ".mermaid": "mermaid",
    ".meson": "meson",
    ".nix": "nix",
    ".nqc": "nqc",
    ".objc": "objc",
    ".odin": "odin",
    ".org": "org",
    ".pas": "pascal",
    ".pp": "pascal",
    ".pem": "pem",
    ".pgn": "pgn",
    ".po": "po",
    ".pony": "pony",
    ".prisma": "prisma",
    ".properties": "properties",
    ".proto": "proto",
    ".psv": "psv",
    ".puppet": "puppet",
    ".purs": "purescript",
    ".pymanifest": "pymanifest",
    ".qmldir": "qmldir",
    ".rkt": "racket",
    ".re": "re2c",
    ".readline": "readline",
    "requirements.txt": "requirements",
    ".ron": "ron",
    ".rst": "rst",
    ".scm": "scheme",
    ".ss": "scheme",
    ".scss": "scss",
    ".smali": "smali",
    ".smithy": "smithy",
    ".sol": "solidity",
    ".sparql": "sparql",
    ".svelte": "svelte",
    ".td": "tablegen",
    ".thrift": "thrift",
    ".toml": "toml",
    ".tsx": "tsx",
    ".twig": "twig",
    ".typ": "typst",
    ".udev": "udev",
    ".rules": "udev",
    ".ungrammar": "ungrammar",
    ".uxntal": "uxntal",
    ".v": "v",
    ".sv": "verilog",
    ".svh": "verilog",
    ".vhdl": "vhdl",
    ".vhd": "vhdl",
    ".vim": "vim",
    ".vue": "vue",
    ".wgsl": "wgsl",
    ".xcompose": "xcompose",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".yuck": "yuck",
    ".zig": "zig"
}

LANGUAGE_NODE_TYPES: dict[str, dict[str, list[str]]] = {
    "actionscript": {
        "functions": ["function_definition", "method_definition"],
        "classes": ["class_declaration"]
    },
    "ada": {
        "functions": ["procedure_declaration", "function_declaration"],
        "classes": ["package_body", "type_declaration"]
    },
    "agda": {
        "functions": ["function_clause", "function_definition"],
        "classes": []
    },
    "apex": {
        "functions": ["method_declaration", "function_declaration"],
        "classes": ["class_declaration", "interface_declaration"]
    },
    "arduino": {
        "functions": ["function_definition"],
        "classes": []
    },
    "asm": {
        "functions": [],
        "classes": []
    },
    "astro": {
        "functions": [],
        "classes": []
    },
    "bash": {
        "functions": ["function_definition"],
        "classes": []
    },
    "beancount": {
        "functions": [],
        "classes": []
    },
    "bibtex": {
        "functions": [],
        "classes": []
    },
    "bicep": {
        "functions": [],
        "classes": []
    },
    "bitbake": {
        "functions": [],
        "classes": []
    },
    "c": {
        "functions": ["function_definition"],
        "classes": []
    },
    "cairo": {
        "functions": ["function_definition"],
        "classes": []
    },
    "capnp": {
        "functions": [],
        "classes": ["struct_definition", "union_definition"]
    },
    "chatito": {
        "functions": [],
        "classes": []
    },
    "clarity": {
        "functions": ["define_public_function", "define_private_function"],
        "classes": []
    },
    "clojure": {
        "functions": ["defn", "fn", "defmulti", "defmethod"],
        "classes": ["defprotocol", "defrecord", "deftype"]
    },
    "cmake": {
        "functions": [],
        "classes": []
    },
    "comment": {
        "functions": [],
        "classes": []
    },
    "commonlisp": {
        "functions": ["defun", "defmacro", "defgeneric"],
        "classes": ["defclass"]
    },
    "cpon": {
        "functions": [],
        "classes": []
    },
    "cpp": {
        "functions": ["function_definition"],
        "classes": ["class_specifier", "struct_specifier", "union_specifier"]
    },
    "csharp": {
        "functions": ["method_declaration", "constructor_declaration", "destructor_declaration"],
        "classes": ["class_declaration", "struct_declaration", "interface_declaration", "record_declaration"]
    },
    "css": {
        "functions": [],
        "classes": []
    },
    "csv": {
        "functions": [],
        "classes": []
    },
    "cuda": {
        "functions": ["function_definition"],
        "classes": ["class_specifier", "struct_specifier"]
    },
    "d": {
        "functions": ["function_definition", "function_declaration"],
        "classes": ["class_declaration", "struct_declaration", "union_declaration", "interface_declaration"]
    },
    "dart": {
        "functions": ["function_signature", "method_signature"],
        "classes": ["class_declaration", "mixin_declaration", "extension_declaration"]
    },
    "dockerfile": {
        "functions": [],
        "classes": []
    },
    "doxygen": {
        "functions": [],
        "classes": []
    },
    "dtd": {
        "functions": [],
        "classes": []
    },
    "elisp": {
        "functions": ["function_definition"],
        "classes": []
    },
    "elixir": {
        "functions": ["function_definition"],
        "classes": ["module_definition"]
    },
    "elm": {
        "functions": ["value_declaration", "definition"],
        "classes": []
    },
    "embeddedtemplate": {
        "functions": [],
        "classes": []
    },
    "erlang": {
        "functions": ["function_clause", "function_definition"],
        "classes": ["module_declaration"]
    },
    "fennel": {
        "functions": ["function_definition"],
        "classes": []
    },
    "firrtl": {
        "functions": [],
        "classes": ["module_declaration"]
    },
    "fish": {
        "functions": ["function_definition"],
        "classes": []
    },
    "fortran": {
        "functions": ["function_subprogram", "subroutine_subprogram"],
        "classes": []
    },
    "func": {
        "functions": [],
        "classes": []
    },
    "gdscript": {
        "functions": ["function_definition"],
        "classes": ["class_definition"]
    },
    "gitattributes": {
        "functions": [],
        "classes": []
    },
    "gitcommit": {
        "functions": [],
        "classes": []
    },
    "gitignore": {
        "functions": [],
        "classes": []
    },
    "gleam": {
        "functions": [],
        "classes": []
    },
    "glsl": {
        "functions": ["function_definition"],
        "classes": []
    },
    "gn": {
        "functions": [],
        "classes": []
    },
    "go": {
        "functions": ["function_declaration", "method_declaration"],
        "classes": []
    },
    "gomod": {
        "functions": [],
        "classes": []
    },
    "gosum": {
        "functions": [],
        "classes": []
    },
    "groovy": {
        "functions": ["method_declaration"],
        "classes": ["class_declaration", "interface_declaration", "annotation_type_declaration"]
    },
    "gstlaunch": {
        "functions": [],
        "classes": []
    },
    "hack": {
        "functions": ["function_declaration"],
        "classes": ["class_definition", "interface_definition", "trait_definition"]
    },
    "hare": {
        "functions": ["function_declaration"],
        "classes": []
    },
    "haskell": {
        "functions": ["function_declaration", "pattern_synonym_declaration"],
        "classes": ["data_declaration", "type_declaration", "class_declaration"]
    },
    "haxe": {
        "functions": ["function_declaration"],
        "classes": ["class_declaration", "interface_declaration", "enum_declaration"]
    },
    "hcl": {
        "functions": [],
        "classes": []
    },
    "heex": {
        "functions": [],
        "classes": []
    },
    "hlsl": {
        "functions": ["function_prototype", "function_definition"],
        "classes": []
    },
    "html": {
        "functions": [],
        "classes": []
    },
    "hyprlang": {
        "functions": [],
        "classes": []
    },
    "ispc": {
        "functions": ["function_definition"],
        "classes": []
    },
    "janet": {
        "functions": ["function_declaration"],
        "classes": []
    },
    "java": {
        "functions": ["method_declaration", "constructor_declaration"],
        "classes": ["class_declaration", "interface_declaration", "enum_declaration"]
    },
    "javascript": {
        "functions": ["function_declaration", "function_expression", "arrow_function"],
        "classes": ["class_declaration"]
    },
    "jsdoc": {
        "functions": [],
        "classes": []
    },
    "json": {
        "functions": [],
        "classes": []
    },
    "jsonnet": {
        "functions": [],
        "classes": []
    },
    "julia": {
        "functions": ["function_definition"],
        "classes": []
    },
    "kconfig": {
        "functions": [],
        "classes": []
    },
    "kdl": {
        "functions": [],
        "classes": []
    },
    "kotlin": {
        "functions": ["function_declaration"],
        "classes": ["class_declaration", "object_declaration", "interface_declaration", "enum_declaration"]
    },
    "latex": {
        "functions": [],
        "classes": []
    },
    "linkerscript": {
        "functions": [],
        "classes": []
    },
    "llvm": {
        "functions": [],
        "classes": []
    },
    "lua": {
        "functions": ["function_declaration"],
        "classes": []
    },
    "luadoc": {
        "functions": [],
        "classes": []
    },
    "luap": {
        "functions": [],
        "classes": []
    },
    "luau": {
        "functions": ["function_declaration"],
        "classes": []
    },
    "make": {
        "functions": [],
        "classes": []
    },
    "markdown": {
        "functions": [],
        "classes": []
    },
    "markdown_inline": {
        "functions": [],
        "classes": []
    },
    "matlab": {
        "functions": ["function_definition"],
        "classes": []
    },
    "mermaid": {
        "functions": [],
        "classes": []
    },
    "meson": {
        "functions": [],
        "classes": []
    },
    "ninja": {
        "functions": [],
        "classes": []
    },
    "nix": {
        "functions": ["function_definition"],
        "classes": []
    },
    "nqc": {
        "functions": [],
        "classes": []
    },
    "objc": {
        "functions": ["function_definition", "method_declaration"],
        "classes": ["interface_declaration", "implementation_definition"]
    },
    "ocaml": {
        "functions": ["value_binding", "function_binding"],
        "classes": []
    },
    "ocaml_interface": {
        "functions": [],
        "classes": []
    },
    "odin": {
        "functions": ["proc_decl", "function_literal"],
        "classes": ["type_decl"]
    },
    "org": {
        "functions": [],
        "classes": []
    },
    "pascal": {
        "functions": ["procedure_declaration", "function_declaration"],
        "classes": ["class_declaration", "record_declaration", "interface_declaration"]
    },
    "pem": {
        "functions": [],
        "classes": []
    },
    "perl": {
        "functions": ["subroutine_definition"],
        "classes": []
    },
    "pgn": {
        "functions": [],
        "classes": []
    },
    "php": {
        "functions": ["function_definition", "method_declaration"],
        "classes": ["class_declaration", "interface_declaration", "trait_declaration"]
    },
    "po": {
        "functions": [],
        "classes": []
    },
    "pony": {
        "functions": ["fun_declaration"],
        "classes": ["class_declaration", "actor_declaration", "object_declaration"]
    },
    "powershell": {
        "functions": ["function_definition"],
        "classes": []
    },
    "printf": {
        "functions": [],
        "classes": []
    },
    "prisma": {
        "functions": [],
        "classes": []
    },
    "properties": {
        "functions": [],
        "classes": []
    },
    "proto": {
        "functions": [],
        "classes": ["message_definition", "service_definition", "enum_definition"]
    },
    "psv": {
        "functions": [],
        "classes": []
    },
    "puppet": {
        "functions": ["function_definition"],
        "classes": []
    },
    "purescript": {
        "functions": ["function_definition"],
        "classes": []
    },
    "pymanifest": {
        "functions": [],
        "classes": []
    },
    "python": {
        "functions": ["function_definition"],
        "classes": ["class_definition"]
    },
    "qmldir": {
        "functions": [],
        "classes": []
    },
    "qmljs": {
        "functions": [],
        "classes": []
    },
    "query": {
        "functions": [],
        "classes": []
    },
    "r": {
        "functions": ["function_definition"],
        "classes": []
    },
    "racket": {
        "functions": ["define", "lambda"],
        "classes": []
    },
    "re2c": {
        "functions": [],
        "classes": []
    },
    "readline": {
        "functions": [],
        "classes": []
    },
    "requirements": {
        "functions": [],
        "classes": []
    },
    "ron": {
        "functions": [],
        "classes": []
    },
    "rst": {
        "functions": [],
        "classes": []
    },
    "ruby": {
        "functions": ["method"],
        "classes": ["class", "module"]
    },
    "rust": {
        "functions": ["function_item", "method_declaration", "closure_expression"],
        "classes": ["struct_item", "enum_item", "trait_item", "union_item"]
    },
    "scala": {
        "functions": ["defn"],
        "classes": ["class_definition", "object_definition", "trait_definition", "case_class_definition"]
    },
    "scheme": {
        "functions": ["define", "lambda"],
        "classes": []
    },
    "scss": {
        "functions": [],
        "classes": []
    },
    "smali": {
        "functions": [],
        "classes": []
    },
    "smithy": {
        "functions": [],
        "classes": []
    },
    "solidity": {
        "functions": ["function_definition"],
        "classes": ["contract_definition", "interface_definition", "library_definition"]
    },
    "sparql": {
        "functions": [],
        "classes": []
    },
    "swift": {
        "functions": ["function_declaration"],
        "classes": ["class_declaration", "struct_declaration", "enum_declaration", "protocol_declaration"]
    },
    "sql": {
        "functions": [],
        "classes": []
    },
    "squirrel": {
        "functions": ["function_declaration"],
        "classes": []
    },
    "starlark": {
        "functions": ["function_definition"],
        "classes": []
    },
    "svelte": {
        "functions": [],
        "classes": []
    },
    "tablegen": {
        "functions": [],
        "classes": []
    },
    "tcl": {
        "functions": [],
        "classes": []
    },
    "terraform": {
        "functions": [],
        "classes": []
    },
    "test": {
        "functions": [],
        "classes": []
    },
    "thrift": {
        "functions": [],
        "classes": ["struct_definition", "service_definition", "enum_definition"]
    },
    "toml": {
        "functions": [],
        "classes": []
    },
    "tsv": {
        "functions": [],
        "classes": []
    },
    "tsx": {
        "functions": ["function_declaration", "function_expression", "jsx_element"],
        "classes": ["class_declaration"]
    },
    "twig": {
        "functions": [],
        "classes": []
    },
    "typescript": {
        "functions": ["function_declaration", "function_expression", "arrow_function"],
        "classes": ["class_declaration", "interface_declaration", "enum_declaration"]
    },
    "typst": {
        "functions": [],
        "classes": []
    },
    "udev": {
        "functions": [],
        "classes": []
    },
    "ungrammar": {
        "functions": [],
        "classes": []
    },
    "uxntal": {
        "functions": [],
        "classes": []
    },
    "v": {
        "functions": ["function_declaration", "function_definition"],
        "classes": []
    },
    "verilog": {
        "functions": [],
        "classes": ["module_declaration", "class_declaration"]
    },
    "vhdl": {
        "functions": [],
        "classes": ["entity_declaration", "architecture_body"]
    },
    "vim": {
        "functions": ["function_definition"],
        "classes": []
    },
    "vue": {
        "functions": [],
        "classes": []
    },
    "wgsl": {
        "functions": ["function_definition"],
        "classes": []
    },
    "xcompose": {
        "functions": [],
        "classes": []
    },
    "xml": {
        "functions": [],
        "classes": []
    },
    "yaml": {
        "functions": [],
        "classes": []
    },
    "yuck": {
        "functions": [],
        "classes": []
    },
    "zig": {
        "functions": ["function_declaration", "function_definition"],
        "classes": []
    },
    "magik": {
        "functions": [],
        "classes": []
    }
}