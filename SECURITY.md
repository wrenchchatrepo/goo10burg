# Security Policy

## Supported Versions

This project uses the latest stable versions of all dependencies as specified in `requirements-updated.txt`. We recommend always using the most recent versions of dependencies to ensure you have the latest security fixes.

## Dependency Management

To update your environment to use the secure versions of dependencies:

1. Create a new virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies using the updated requirements file:
```bash
pip install -r requirements-updated.txt
```

## Security Updates

- All dependencies are specified with minimum versions (>=) to ensure you can easily update to newer, more secure versions as they become available
- Regular security audits are recommended using tools like `pip-audit` or `safety`
- Dependencies are kept up-to-date with the latest stable releases

## Reporting a Vulnerability

If you discover a security vulnerability, please report it by:

1. Opening a GitHub issue with the label "security"
2. Avoiding public disclosure until the vulnerability has been addressed
3. Providing detailed information about the vulnerability and steps to reproduce

We take security seriously and will respond to vulnerability reports promptly.
