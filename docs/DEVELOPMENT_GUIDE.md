# Development Tools & Extensions Guide

## 🚀 Installed VS Code Extensions

### Frontend Development

- **ES7+ React/Redux/React-Native snippets** - Smart code snippets for React
- **Prettier - Code formatter** - Automatic code formatting
- **ESLint** - Code quality and error detection
- **Auto Rename Tag** - Auto-rename paired HTML/JSX tags
- **Auto Close Tag** - Automatically close HTML/JSX tags
- **Tailwind CSS IntelliSense** - Tailwind CSS class completion
- **Error Lens** - Inline error/warning display
- **HTML CSS Support** - HTML & CSS IntelliSense

### Backend Development

- **Python** - Python language support
- **Pylance** - Advanced Python type checking
- **Ruff** - Fast Python linter
- **Django** - Django framework support

### Development Utilities

- **GitLens** - Git blame & history inline
- **Todo Tree** - Display TODO/FIXME comments
- **Bookmarks** - Mark and navigate code sections
- **GitHub Repositories** - Manage repositories
- **Code Spell Checker** - Spell checking
- **YAML** - YAML file support
- **Makefile Tools** - Makefile support

---

## 📝 Code Quality Tools

### Frontend

#### ESLint

- Automatic linting for React/JavaScript
- Detects errors and code smells
- Run: `npm run lint`
- Fix automatically: `npm run lint:fix`

#### Prettier

- Automatic code formatting
- Consistent code style
- Run: `npm run format`
- Check without fixing: `npm run format:check`

**Configuration:** `.eslintrc.json` and `.prettierrc.json`

### Backend

#### Black

- Python code formatter
- Automatic code style
- Run: `black .`

#### Flake8

- Python linter
- Error detection
- Run: `flake8 .`

#### Ruff

- Fast Python linter
- Modern replacement for flake8
- Run: `ruff check .`

#### isort

- Organize Python imports
- Run: `isort .`

---

## ⚙️ VS Code Settings

### Auto-formatting

- **Save**: Files auto-format on save
- **JavaScript/JSX**: Prettier formatter
- **Python**: Black formatter

### Code Quality

- **ESLint**: Auto-fix on save
- **Python**: Flake8 linting enabled

### File Exclusions

- Hides: `__pycache__`, `.pyc`, `node_modules`, etc.
- Search excludes same paths

---

## 🛠️ Useful npm Commands

```bash
# Development
npm run dev          # Start Vite dev server
npm start            # Alias for dev

# Building
npm run build        # Production build
npm run preview      # Preview production build

# Code Quality
npm run lint         # Check for ESLint errors
npm run lint:fix     # Fix ESLint errors automatically
npm run format       # Format code with Prettier
npm run format:check # Check formatting without changes
```

---

## 🐍 Useful Python Commands

```bash
# Format
black .              # Format all Python files
isort .              # Organize imports

# Lint
flake8 .             # Check for errors
ruff check .         # Fast linting

# Run Django
python manage.py runserver      # Start Django
python manage.py makemigrations # Create migrations
python manage.py migrate        # Apply migrations
```

---

## 📋 Daily Development Workflow

### Frontend

1. `npm run dev` - Start dev server
2. Edit components in src/
3. Auto-formatting on save
4. ESLint errors show inline
5. `npm run lint:fix` - Fix all errors
6. `npm run build` - Build for production

### Backend

1. `python manage.py runserver` - Start Django
2. Edit Django apps
3. Auto-formatting on save
4. Ruff/Flake8 errors show inline
5. `black .` - Format code
6. `ruff check .` - Check for errors

---

## 💡 Extension Tips

### GitLens

- Hover over code to see commit info
- Click blame to see full history
- Use Gitlens sidebar for detailed history

### Todo Tree

- Marks TODO/FIXME comments
- Click to navigate
- Filter by type in sidebar

### Error Lens

- Shows errors inline on code
- Click to see details
- Hover for full error message

### Bookmarks

- Right-click to bookmark lines
- Navigate via Bookmarks panel
- Organize with labels

---

## 🎯 Best Practices

### Frontend

1. Run `npm run format` before commits
2. Ensure `npm run lint` passes
3. Use snippets from ES7+ plugin
4. Let Prettier handle formatting

### Backend

1. Run `black .` before commits
2. Ensure `ruff check .` passes
3. Use `isort .` for imports
4. Follow PEP 8 style guide

---

## 🔧 Configuration Files

- `.eslintrc.json` - ESLint rules for JavaScript/React
- `.prettierrc.json` - Prettier formatting rules
- `.gitignore` - Git exclusions
- `.vscode/settings.json` - VS Code settings
- `.vscode/extensions.json` - Recommended extensions

---

## 📚 Resources

- [Prettier Docs](https://prettier.io/)
- [ESLint Docs](https://eslint.org/)
- [Black Docs](https://black.readthedocs.io/)
- [Ruff Docs](https://docs.astral.sh/ruff/)
- [Django Docs](https://docs.djangoproject.com/)
- [React Docs](https://react.dev/)
- [Vite Docs](https://vitejs.dev/)

---

## ✅ Quick Checklist

Before committing code:

- [ ] Run `npm run lint:fix` (frontend)
- [ ] Run `npm run format` (frontend)
- [ ] Run `black .` (backend)
- [ ] Run `ruff check .` (backend)
- [ ] No console errors
- [ ] All tests passing
- [ ] Code reviewed

---

**Happy Coding! 🎉**
