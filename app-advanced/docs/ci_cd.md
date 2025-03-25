# CI/CD Guide

This guide explains the Continuous Integration and Continuous Deployment (CI/CD) setup for the Invoice OCR API.

## Overview

CI/CD is a software development practice that automates the building, testing, and deployment of applications. This project uses GitHub Actions for CI/CD, which automatically runs tests and builds Docker images when code is pushed to the repository.

## How It Works

The CI/CD workflow is defined in `.github/workflows/ci_cd.yml`. It consists of the following jobs:

### 1. Test Job

This job runs whenever code is pushed to the `main` branch or a pull request is created:

1. Sets up a Python environment
2. Installs system dependencies (Tesseract OCR and Poppler)
3. Installs Python dependencies
4. Creates a temporary `.env` file for testing
5. Runs all tests with pytest and generates a coverage report

### 2. Build Job

This job runs only when code is pushed to the `main` branch:

1. Sets up Docker Buildx for multi-platform builds
2. Logs in to GitHub Container Registry (GHCR)
3. Builds the Docker image
4. Pushes the image to GHCR with two tags:
   - `latest`: Always points to the most recent version
   - `{commit-sha}`: A specific version tied to the commit

### 3. Deploy Job (Commented Out)

A deployment job template is included but commented out, as deployment methods vary greatly depending on your hosting environment.

## GitHub Container Registry

The Docker images are stored in GitHub Container Registry, which makes them easy to access and deploy. The image is available at:

```
ghcr.io/yourusername/invoice-ocr-api:latest
```

Replace `yourusername` with your GitHub username.

## Setting Up Your Repository

To use this CI/CD pipeline with your own repository:

1. **Fork or Clone the Repository**: Start with your own copy of the code
2. **Configure Repository Settings**:
   - Go to Settings > Actions > General
   - Ensure "Allow all actions and reusable workflows" is enabled
   - Go to Settings > Packages
   - Ensure "Inherit access from source repository" is enabled

3. **Add Repository Secrets** (if needed):
   - For deployment credentials or sensitive information
   - Go to Settings > Secrets and variables > Actions
   - Click "New repository secret" and add your secrets

## Customizing the Workflow

You can customize the CI/CD workflow by editing `.github/workflows/ci_cd.yml`:

### Adding More Tests

```yaml
- name: Run tests
  run: |
    pytest --cov=app tests/
    # Add more test commands here
```

### Changing Build Options

```yaml
- name: Build and push Docker image
  uses: docker/build-push-action@v2
  with:
    context: .
    push: true
    # Add build arguments or platform options here
    tags: |
      ghcr.io/${{ github.repository_owner }}/invoice-ocr-api:latest
      ghcr.io/${{ github.repository_owner }}/invoice-ocr-api:${{ github.sha }}
```

### Adding Deployment

Uncomment and customize the deployment job:

```yaml
deploy:
  needs: build
  runs-on: ubuntu-latest
  if: github.event_name == 'push' && github.ref == 'refs/heads/main'
  
  steps:
  - uses: actions/checkout@v2
  
  - name: Deploy to your environment
    run: |
      # Add deployment steps specific to your hosting
      # For example, deploying to a cloud provider or VPS
```

## Monitoring CI/CD Runs

You can monitor your CI/CD runs in the GitHub interface:

1. Go to your repository
2. Click on the "Actions" tab
3. View the list of workflow runs
4. Click on a specific run to see details
5. View logs for each job and step

## Best Practices

1. **Run Tests Locally First**: Always run tests locally before pushing to ensure the CI pipeline passes
2. **Use Descriptive Commit Messages**: Makes it easier to track which changes are being built and deployed
3. **Review Workflow Runs**: Check the Actions tab after pushing to ensure everything runs correctly
4. **Keep Secrets Secure**: Never commit sensitive information; use repository secrets instead