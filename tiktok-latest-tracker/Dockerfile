# Use a base image that has Node.js and Python pre-installed
# You can find suitable images on Docker Hub or use a more specific one
FROM mcr.microsoft.com/devcontainers/python:0-3.10-bullseye

# Install Node.js (e.g., version 18)
USER root
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive     && apt-get -y install --no-install-recommends nodejs npm     && apt-get clean     && rm -rf /var/lib/apt/lists/*
USER vscode

# Set the working directory
WORKDIR /workspaces/${localWorkspaceFolderBasename}

# Copy Playwright install command to be run by postCreateCommand or manually
# This avoids running it during Docker build time which might be slow or fail in some environments
# Playwright browsers will be installed by postCreateCommand

# Optional: Add any other global dependencies or setup steps here

# Switch back to non-root user
# USER vscode

CMD ["sleep", "infinity"]
