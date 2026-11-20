# ADR 0001: Explicit Data-Directory Setup

**Status:** Accepted

## Context

The configuration module (`src/config.py`) previously created the project's data directories whenever it was imported.

This meant that simply importing configuration could modify the filesystem. Imports should define configuration without causing unnecessary filesystem changes.

## Decision

Directory creation is now handled by an explicit `ensure_data_directories()` function in `src/config.py`.

The data acquisition notebook calls this function during setup, before using the configured data paths.

The TMDb cache-writing function also retains its own directory creation step so it can create the cache directory when saving cached responses.

## Consequences

- Importing `src.config` no longer creates project data directories.
- Directory creation happens explicitly when required.
- The setup function can be called repeatedly without causing errors if the directories already exist.
- Any other script that needs these directories must call the setup function or create the specific directory it needs.