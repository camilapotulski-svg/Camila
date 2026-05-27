# Contributing to Sustainable Agriculture Initiative

Thank you for your interest in contributing to our mission of sustainable agriculture! This document provides guidelines and instructions for contributing.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. All contributors must adhere to our Code of Conduct:
- Be respectful and inclusive
- Welcome diverse perspectives
- Focus on constructive collaboration
- Report inappropriate behavior

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- Git
- PostgreSQL 12+

### Development Setup

```bash
# Fork the repository
git clone https://github.com/YOUR_USERNAME/Camila.git
cd Camila

# Create a virtual environment
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
npm install

# Create a development branch
git checkout -b feature/your-feature-name
```

## Contribution Types

### 1. Code Contributions

**Areas for Contribution:**
- Core agricultural logic improvements
- API endpoint development
- Frontend components
- Machine learning models
- Database optimizations

**Process:**
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/feature-name`
3. Make your changes with clear, descriptive commits
4. Write or update tests
5. Ensure code passes quality checks:
   ```bash
   black .
   flake8 .
   pytest
   ```
6. Push to your fork and create a Pull Request

### 2. Documentation

We welcome documentation improvements:
- API documentation
- User guides
- Setup instructions
- Best practices guides
- Code comments and docstrings

### 3. Bug Reports

Found a bug? Help us fix it:
1. Check existing issues to avoid duplicates
2. Create a clear issue with:
   - Description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - System information
   - Screenshots/logs if applicable

### 4. Feature Requests

Have an idea? We'd love to hear it:
1. Check existing issues and discussions
2. Create an issue with:
   - Clear description of the feature
   - Why it's needed
   - Possible implementation approach
   - Use cases and examples

### 5. Research & Data

Help improve our agricultural knowledge:
- Contribute soil health data
- Share crop research findings
- Provide regional agricultural insights
- Suggest sustainability metrics

## Coding Standards

### Python Style Guide
- Follow PEP 8
- Use type hints for function parameters and returns
- Write docstrings for all functions and classes
- Maximum line length: 100 characters

Example:
```python
def calculate_soil_health(soil_test: SoilTest, 
                         field: Field) -> float:
    """
    Calculate soil health score based on test results.
    
    Args:
        soil_test: The soil test results
        field: The field being assessed
    
    Returns:
        Health score from 0-100
    """
    score = (soil_test.organic_matter * 0.5 + 
             soil_test.ph_rating * 0.3 + 
             soil_test.microbial_activity * 0.2)
    return score
```

### Git Commit Messages
- Use clear, descriptive messages
- Start with a verb: "Add", "Fix", "Update", "Improve"
- Keep first line under 50 characters
- Reference issues when relevant: "Fixes #123"

Example:
```
Add water use efficiency calculator

- Calculate irrigation efficiency percentage
- Compare actual vs optimal water usage
- Provide conservation recommendations

Fixes #45
```

### Testing Requirements
- Write tests for new features
- Maintain >80% code coverage
- Test both success and failure cases
- Use descriptive test names

```python
def test_crop_rotation_prevents_same_family():
    """Verify crop rotation avoids same plant family."""
    field = Field(field_id="F1", area_hectares=10)
    planner = CropRotationPlanner(field)
    
    # Arrange
    wheat = Crop(name="Wheat", crop_type=CropType.GRAIN)
    planner.rotation_history = [wheat]
    
    # Act
    similar_grain = Crop(name="Barley", crop_type=CropType.GRAIN)
    planner.plan_rotation_sequence([similar_grain])
    
    # Assert
    assert planner.rotation_history[-1].crop_type != CropType.GRAIN
```

## Pull Request Process

1. **Before submitting:**
   - Update documentation
   - Add tests for new features
   - Run full test suite: `pytest`
   - Check code formatting: `black --check .`
   - Update CHANGELOG.md

2. **PR Description:**
   - Clear title and description
   - Reference related issues
   - Explain changes and rationale
   - Include screenshots/demos if relevant

3. **Review Process:**
   - At least one approval required
   - Address review feedback
   - Keep commits clean (squash if needed)
   - Ensure CI/CD checks pass

4. **After Merge:**
   - Delete feature branch
   - Monitor for any issues
   - Update relevant documentation

## Development Workflow

### Local Development
```bash
# Start backend server
python manage.py runserver

# In another terminal, start frontend
npm start

# Run tests with coverage
pytest --cov=backend tests/

# Format code
black .

# Run linter
flake8 .
```

### Branch Naming Conventions
- Feature: `feature/short-description`
- Bug fix: `bugfix/issue-description`
- Documentation: `docs/description`
- Refactor: `refactor/description`

## Areas Where We Need Help

### High Priority
- [ ] Performance optimization for large datasets
- [ ] Mobile app development
- [ ] Multi-language support
- [ ] Regional agriculture data validation

### Medium Priority
- [ ] Additional ML models for yield prediction
- [ ] Improved weather data integration
- [ ] Database query optimization
- [ ] UI/UX improvements

### Good for Beginners
- [ ] Add more crop profiles to database
- [ ] Improve code comments and docstrings
- [ ] Update documentation
- [ ] Create sample data scripts
- [ ] Add unit tests

## Resources

### Documentation
- [API Documentation](docs/api_documentation.md)
- [User Guide](docs/user_guide.md)
- [Best Practices](docs/best_practices.md)

### Learning Resources
- [Sustainable Agriculture Guide](https://www.sustainableagriculture.org)
- [Python Style Guide (PEP 8)](https://pep8.org)
- [Django Documentation](https://docs.djangoproject.com)

### Communication
- **Issues**: Use for bug reports and feature requests
- **Discussions**: Use for questions and ideas
- **Email**: info@sustainableagriculture.dev

## Recognition

We recognize all contributions! Contributors will be:
- Listed in CONTRIBUTORS.md
- Thanked in release notes
- Featured in project documentation
- Invited to project meetings

---

## Questions?

Don't hesitate to ask! 
- Open an issue with your question
- Email: contributors@sustainableagriculture.dev
- Join our community discussions

Thank you for making sustainable agriculture possible! 🌱