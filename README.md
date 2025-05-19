# gcPanel - Construction Management Dashboard

A comprehensive construction project management platform built with Streamlit, providing advanced visualization tools and workflow solutions for AEC professionals.

## Overview

gcPanel streamlines construction project management through an intuitive, data-driven interface. It integrates essential construction workflows—from preconstruction through closeout—with powerful data visualization and real-time analytics capabilities.

## Key Features

### Comprehensive Project Management
- **Dashboard Analytics**: Real-time KPIs and metrics on project performance
- **Project Timeline Visualization**: Interactive Gantt charts for schedule tracking
- **Cost Management**: Budget tracking, forecasting, and variance analysis
- **Document Control**: Centralized repository for drawings, RFIs, and specifications
- **BIM Integration**: 3D model visualization and data integration
- **Field Operations**: Daily reports, quality control, and issue tracking

### Technical Highlights
- **Modern Stack**: Built with Streamlit, Python, and SQLite (PostgreSQL-ready)
- **Secure Authentication**: Role-based access control with JWT verification
- **Responsive Design**: Mobile-friendly interface for field use
- **Advanced Visualizations**: Interactive charts and data visualization
- **Modular Architecture**: Easily extensible with additional modules
- **API Integration**: Supports external service integration via RESTful APIs

## Project Details

### Highland Tower Development
- $45.5M mixed-use development
- 120 residential units and 8 retail spaces
- 168,500 sq. ft across 15 stories above ground and 2 below
- Advanced construction management system implementation

## Developer Guide

### Project Structure

```
gcPanel/
├── app.py                 # Main application entry point
├── app_manager.py         # Application initialization and module routing
├── app_config.py          # Centralized configuration settings
├── assets/                # Static assets (CSS, images, etc.)
│   ├── container_styles.py    # UI container styling
│   └── styles.py              # Global CSS styles
├── components/            # Reusable UI components
│   ├── action_bar.py          # Action buttons for pages
│   ├── header_clean.py        # Application header
│   └── ...                    # Other components
├── core/                  # Core application services
├── data/                  # Data models and database utilities
├── modules/               # Application modules/pages
│   ├── dashboard/             # Dashboard module
│   ├── contracts/             # Contracts module
│   └── ...                    # Other modules
├── utils/                 # Utility functions and helpers
│   ├── ui_manager.py          # UI utility functions
│   └── ...                    # Other utilities
├── static/                # Static assets served by the application
└── tests/                 # Unit and integration tests
```

### Application Architecture

The gcPanel application follows a modular architecture with the following key components:

1. **Entry Point (app.py)**: Initializes the application and starts the main workflow.

2. **Application Manager (app_manager.py)**: Handles session state, navigation, and module routing.

3. **Configuration (app_config.py)**: Centralized settings organized by functional areas.

4. **Components**: Reusable UI elements that maintain consistent design throughout the app.

5. **Modules**: Individual functional areas of the application (Dashboard, Contracts, etc.).

### How to Extend the Application

#### Adding a New Module

1. **Create Module Directory**: Create a new directory in the `modules/` folder for your module:
   ```
   modules/new_module/
   ```

2. **Create Module Files**:
   ```python
   # modules/new_module/__init__.py
   import streamlit as st
   
   def render_new_module():
       st.title("New Module")
       # Your module content here
   ```

3. **Update Configuration**: Add your module to `app_config.py`:
   ```python
   # Add to MENU_OPTIONS
   MENU_OPTIONS = [
       # ... existing options
       "🆕 New Module",
   ]
   
   # Add to MENU_MAP
   MENU_MAP = {
       # ... existing mapping
       "🆕 New Module": "New Module",
   }
   
   # If your module needs action buttons
   PAGES_WITH_ACTIONS = {
       # ... existing pages
       "New Module": "New Item",
   }
   ```

4. **Register Module Renderer**: Add your module to the rendering function in `app_manager.py`:
   ```python
   # Import your module
   from modules.new_module import render_new_module
   
   # Add to module_mapping in render_selected_module
   module_mapping = {
       # ... existing modules
       "New Module": render_new_module,
   }
   ```

#### Creating New Components

1. **Create Component File**: Add a new file in the `components/` directory:
   ```python
   # components/new_component.py
   import streamlit as st
   
   def render_new_component(param1, param2=None):
       """
       Render a new component.
       
       Args:
           param1: First parameter description
           param2: Optional second parameter description
       
       Returns:
           Any data that needs to be returned
       """
       # Component implementation
       pass
   ```

2. **Import and Use**: Import and use your component in modules:
   ```python
   from components.new_component import render_new_component
   
   # In your module
   render_new_component("some value")
   ```

### Best Practices

1. **Modular Design**: Keep modules and components focused on specific functionality.

2. **Consistent Styling**: Use the provided styling utilities in `assets/` for UI consistency.

3. **Clean Imports**: Import only what you need to avoid circular dependencies.

4. **Documentation**: Add docstrings to all functions and modules explaining purpose and usage.

5. **Session State**: Use Streamlit's session state for storing persistent data between reruns.

6. **Configuration**: Add new configuration values to appropriate sections in `app_config.py`.

## Modules

| Module | Description |
|--------|-------------|
| **Dashboard** | Project overview with key metrics and analytics |
| **Project Information** | Central repository for project details and team information |
| **Schedule** | Gantt charts, milestone tracking, and progress visualization |
| **Safety** | Incident reports, safety metrics, and compliance tracking |
| **Contracts** | Contract management, change orders, and procurement |
| **Cost Management** | Budget tracking, forecasting, and financial reporting |
| **Engineering** | Technical documentation, specifications, and calculations |
| **Field Operations** | Daily reports, quality control, and issue tracking |
| **Documents** | Document management with version control and approval workflows |
| **BIM** | 3D model visualization and information extraction |
| **Closeout** | Project closeout documentation and warranty management |

## Implementation

### Installation Requirements
- Python 3.8+
- Streamlit 1.24+
- SQLAlchemy
- Plotly and Pandas for data visualization
- JWT for authentication

### Database Configuration
The platform supports both SQLite (local development) and PostgreSQL (production) databases through SQLAlchemy ORM.

### Authentication
Role-based access control with secure JWT implementation supports multiple user types:
- Administrator
- Project Manager
- Field Supervisor
- Subcontractor
- Client/Owner

## Future Roadmap

- **Mobile App**: Native companion app for field data collection
- **AI-Powered Analytics**: Predictive analytics for project risk assessment
- **Advanced BIM Integration**: Deeper integration with Revit and other BIM tools
- **Expanded Reporting**: Customizable reporting engine
- **Multi-Project Portfolio Management**: Roll-up reporting across multiple projects

## Screenshots

![gcPanel Dashboard](attached_assets/gcpanel-streamlit2.png)
*gcPanel Construction Management Dashboard - Highland Tower Project*

## License

© 2025 gcPanel. All rights reserved.