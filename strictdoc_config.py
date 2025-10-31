from strictdoc.core.project_config import ProjectConfig

def create_config() -> ProjectConfig:
    config = ProjectConfig(
        project_title="yeemidi test project",
        project_features = [
            "REQUIREMENT_TO_SOURCE_TRACEABILITY",
            "SOURCE_FILE_LANGUAGE_PARSERS"
        ],
        exclude_source_paths=["*"],
        include_source_paths=["src/*"],
        exclude_doc_paths=["*"],
        include_doc_paths=["requirements/*"]

    )
    return config
    