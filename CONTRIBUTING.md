# Contributing to Inventory Hub

Thank you for your interest in contributing to Inventory Hub! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Coding Standards](#coding-standards)

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Respect differing viewpoints

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/Inventory-Hub.git
   cd Inventory-Hub
   ```

3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/HubbTechDev/Inventory-Hub.git
   ```

## Development Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. Initialize the database:
   ```bash
   python init_db.py
   ```

5. Run the development server:
   ```bash
   python run.py
   ```

## Making Changes

1. Create a new branch for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes following our [coding standards](#coding-standards)

3. Test your changes thoroughly

4. Commit your changes:
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

## Testing

### Running Tests

Run all tests:
```bash
python -m unittest discover tests
```

Run specific test file:
```bash
python -m unittest tests.test_api
```

Run with coverage (if pytest is installed):
```bash
pytest --cov=backend tests/
```

### Writing Tests

- Write tests for all new features
- Ensure tests are isolated and repeatable
- Use descriptive test names
- Follow existing test patterns
- Aim for high code coverage

## Submitting Changes

1. Push your changes to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Create a Pull Request:
   - Go to the repository on GitHub
   - Click "New Pull Request"
   - Select your feature branch
   - Fill out the PR template with:
     - Description of changes
     - Related issue numbers
     - Screenshots (if UI changes)
     - Testing performed

3. Address review feedback:
   - Respond to comments
   - Make requested changes
   - Push updates to the same branch

## Coding Standards

### Python Code

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Write docstrings for modules, classes, and functions
- Keep functions small and focused
- Use type hints where appropriate

Example:
```python
def calculate_total_value(items: List[InventoryItem]) -> float:
    """
    Calculate the total value of inventory items.
    
    Args:
        items: List of inventory items
        
    Returns:
        Total value as float
    """
    return sum(item.price for item in items if item.price)
```

### JavaScript Code

- Use `const` and `let`, avoid `var`
- Use meaningful variable names
- Add comments for complex logic
- Keep functions small and focused
- Handle errors appropriately

### Database

- Write migrations for schema changes
- Use meaningful table and column names
- Add appropriate indexes
- Document complex queries

### Git Commits

- Write clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove, etc.)
- Keep the first line under 72 characters
- Add detail in the commit body if needed

Good commit messages:
```
Add user authentication with JWT tokens

- Implement registration endpoint
- Add login endpoint with password verification
- Create JWT token generation and validation
```

### Documentation

- Update README.md for user-facing changes
- Update API documentation for endpoint changes
- Add inline comments for complex code
- Update CHANGELOG.md (if exists)

## Areas for Contribution

### High Priority

- [ ] Additional merchant platform scrapers
- [ ] Export functionality (CSV, Excel)
- [ ] Advanced filtering and search
- [ ] Price history tracking
- [ ] Duplicate detection
- [ ] Email notifications for completed scrapes

### Medium Priority

- [ ] User settings and preferences
- [ ] Bulk operations on inventory
- [ ] Image preview/gallery
- [ ] Tags and categories for organization
- [ ] API rate limiting
- [ ] Improved error handling

### Documentation

- [ ] API documentation (Swagger/OpenAPI)
- [ ] User guide with screenshots
- [ ] Video tutorials
- [ ] Deployment guides for different platforms

### Testing

- [ ] E2E tests for critical user flows
- [ ] Performance testing
- [ ] Security testing
- [ ] Browser compatibility testing

## Need Help?

- Open an issue for questions
- Join discussions on GitHub
- Check existing issues and PRs
- Read the documentation

## License

By contributing to Inventory Hub, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to Inventory Hub! 🎉
