# Contributing to Remedium Hospital Management System

Thank you for your interest in contributing to Remedium HMS! We appreciate your time and effort to help improve our open-source hospital management system.

## 🤝 Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) to ensure a welcoming environment for everyone.

## 🚀 How Can I Contribute?

### Reporting Bugs
- Ensure the bug hasn't already been reported by searching through existing issues
- Use a clear and descriptive title for your issue
- Include as much relevant information as possible:
  - Steps to reproduce the issue
  - Expected behavior
  - Actual behavior
  - Environment details (OS, Python version, Django version)
  - Any relevant screenshots or logs

### Suggesting Features
- Check if the feature has already been suggested in existing issues
- Explain your idea clearly and provide use cases
- Describe the potential benefits for users

### Pull Requests
1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Update documentation if needed
6. Commit your changes (`git commit -m 'Add some amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a pull request

## 🛠 Development Setup

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Remedium-HMS.git
   cd Remedium-HMS
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create the default user groups:
   ```bash
   python manage.py create_groups
   ```

7. Create a superuser account:
   ```bash
   python manage.py createsuperuser
   ```

8. Run the development server:
   ```bash
   python manage.py runserver
   ```

## 📝 Code Style

- Follow PEP 8 guidelines for Python code
- Use descriptive variable and function names
- Write clear, concise comments when necessary
- Maintain consistency with existing code patterns
- Add docstrings to functions and classes

## 🧪 Testing

- Write tests for new features and bug fixes
- Run existing tests before submitting your PR:
  ```bash
  python manage.py test
  ```

## 🏷 Issue Labels

- `bug`: Issues with the system functionality
- `enhancement`: New features or improvements
- `documentation`: Issues related to documentation
- `good first issue`: Good for newcomers to the project
- `help wanted`: Issues that need extra attention
- `question`: Ask questions about the project

## ✅ PR Review Process

- All PRs are reviewed by the core team
- Feedback will be provided within 3-7 days
- PRs should have clear descriptions of changes made
- All tests must pass before merging

## Questions?

Feel free to open an issue if you have any questions about contributing.

---

Thank you for contributing to Remedium HMS!