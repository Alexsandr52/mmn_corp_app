# MMN Corp Barcode Generator

A modern Flask-based web application for generating and managing barcodes with Progressive Web App (PWA) capabilities. Perfect for inventory management, product tracking, and supply chain operations.

![Flask](https://img.shields.io/badge/Flask-2.2.2-green)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

- **Multiple Barcode Formats**
  - EAN-13 (13-digit codes)
  - EAN-8 (8-digit codes)
  - Code39 (custom alphanumeric codes)

- **Web Interface**
  - Responsive Bootstrap 5 design
  - Interactive barcode viewer
  - Modal forms for easy barcode entry
  - Recently used barcodes display (last 5 items)

- **Database Storage**
  - SQLite database for barcode persistence
  - Tag/description support for each barcode
  - Quick access to stored barcodes

- **Progressive Web App**
  - Installable on mobile devices
  - Offline functionality via service worker
  - Fast loading with resource caching

## Technology Stack

### Backend
- **Python 3.10+** - Core language
- **Flask 2.2.2** - Web framework
- **SQLite** - Database
- **python-barcode 0.13.1** - Barcode generation
- **Pillow 9.0.0** - Image processing

### Frontend
- **Bootstrap 5.3.3** - UI framework
- **Vanilla JavaScript** - Interactivity
- **PWA** - Progressive Web App features

### Deployment
- **Docker** - Containerization support
- **Port 5000** - Default application port

## Installation

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/mmn_corp_app.git
   cd mmn_corp_app
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

### Docker Setup

1. **Build the Docker image**
   ```bash
   docker build -t mmn-barcode-app .
   ```

2. **Run the container**
   ```bash
   docker run -p 5000:5000 mmn-barcode-app
   ```

## Usage

### Generating Barcodes

1. Click the "Add Barcode" button (bottom right corner)
2. Enter the barcode code in the modal form
3. Add a descriptive tag
4. Click "Save Changes"

### Barcode Format Selection

The application automatically selects the appropriate barcode format based on code length:
- **13 digits** → EAN-13
- **8 digits** → EAN-8
- **Other lengths** → Code39

### Viewing Stored Barcodes

- Recently used barcodes appear in the "Recently Used" section
- Click on any barcode card to view the full-size image
- Switch between sample types using the radio buttons

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DATABASE_PATH=database.db
FLASK_DEBUG=False
PORT=5000
```

### Database Configuration

The application uses SQLite by default. The database is automatically initialized on first run. To use a custom database path, set the `DATABASE_PATH` environment variable.

## Project Structure

```
mmn_corp_app/
├── app.py                 # Main Flask application
├── barcode_gen.py         # Barcode generation logic
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── .gitignore            # Git ignore rules
├── README.md             # Project documentation
├── static/               # Static assets
│   ├── css/
│   │   └── style.css     # Custom styles
│   ├── images/
│   │   ├── upc.svg       # Sample UPC barcode
│   │   ├── data_matrix.jpeg  # Sample Data Matrix
│   │   └── temp_ucp/     # Generated barcodes
│   ├── manifest.json     # PWA manifest
│   └── service-worker.js # PWA service worker
└── templates/
    └── index.html        # Main HTML template
```

## API Endpoints

### `GET /`
Main application page

### `POST /save_barcode`
Generate and save a new barcode

**Parameters:**
- `barcode`: The barcode code
- `tag`: Description/tag for the barcode

### `GET /health`
Health check endpoint

## Development

### Adding New Features

1. Barcode generation logic is in `barcode_gen.py`
2. Web routes are defined in `app.py`
3. Frontend templates are in `templates/`
4. Static assets are in `static/`

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Log important operations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Troubleshooting

### Barcode Generation Fails

- Ensure the code is not empty
- Check that the code length is appropriate for the barcode type
- Verify write permissions in the `static/images/temp_ucp/` directory

### Database Errors

- Check that the application has write permissions for the database file
- Ensure SQLite is properly installed
- Try deleting `database.db` and restarting the application

### PWA Not Installing

- Ensure the site is served over HTTPS (or localhost)
- Check that `manifest.json` is accessible
- Verify the service worker is registered correctly

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [python-barcode](https://github.com/WhyNotHugo/python-barcode) - Barcode generation library
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Bootstrap](https://getbootstrap.com/) - UI framework

## Support

For support, please open an issue on GitHub or contact the maintainers.

---

Made with ❤️ by MMN Corp
