#  App Docs

<hr>
## Technology Stack

### Frontend

**Languages:**

- HTML
- CSS
- Javascript

**Frameworks:**

- Bootstrap 5.2.1
- jQuery 3.6.1 (CDN)
- axios 1.2.2 (CDN)
- Popper 2.11.6 (CDN)

**Miscellaneous**

- FontAwesome Icons

<br>

### Backend

**Languages:**

- Python 3.8 (As of 1/6/23 - Railway uses Nixpacks which defaults to 3.8)

**Frameworks:**

- Flask v2.2.2
  - Flask-SQLAlchemy v2.5.1
  - Flask-Bcrypt v1.0.1
  - Flask-WTF v1.0.1

**Database:**

- PostgreSQL 13(As of 1/6/23 - Railway uses PSQL 13 image from Docker)

**API:**

- SendGrid (Email Service)

**Storage**

- AWS S3 (File Storage)

<br>

### Host

- Railway

<hr>

#### Project Tree

```
Production-Site/
├─app.py
├─config.py
├─db.py
├─models/
│ ├─error.py
│ ├─file.py
│ ├─forms.py
│ ├─materials.py
│ ├─nest.py
│ ├─part.py
│ ├─project.py
│ ├─requests.py
│ └─user.py
├─requirements.txt
├─routes/
│ ├─amada.py
│ ├─documentation.py
│ ├─errors.py
│ ├─forming.py
│ ├─general.py
│ ├─prototypes.py
│ ├─punch.py
│ ├─requests.py
│ ├─seed.py
│ ├─trumpf.py
│ └─user.py
├─static/
│ ├─app.js
│ ├─bootstrap/
│ │ ├─bootstrap.bundle.js
│ │ ├─bootstrap.bundle.js.map
│ │ ├─bootstrap.min.css
│ │ └─bootstrap.min.css.map
│ ├─data_explorers/
│ │ ├─eco.js
│ │ └─explorer.js
│ ├─guides/
│ │ ├─DataExplorer Users Guide.pdf
│ │ ├─MaterialExplorer Users Guide.pdf
│ │ ├─ParameterExplorer Users Guide.pdf
│ │ ├─ProductionDesigner Users Guide.pdf
│ │ ├─salvagnini-user-guide.pdf
│ │ ├─VPSS3i BEND Operation Guide.pdf
│ │ ├─VPSS3i BEND Parameter Guide.pdf
│ │ ├─VPSS3i BEND Users Guide.pdf
│ │ └─VPSS3i BLANK Users Guide.pdf
│ ├─hubs/
│ │ ├─dataexplorer.js
│ │ ├─home.js
│ │ ├─production.js
│ │ └─sop.js
│ ├─images/
│ │ ├─banner.jpg
│ │ ├─blankcam/
│ │ │ └─images
│ │ ├─icon.ico
│ │ ├─logo.jpg
│ │ └─trutops/
│ │   └─images
│ ├─nesting_calculator/
│ │ ├─nesting-main.js
│ │ ├─nesting-parts.js
│ │ ├─nestingCalculator.js
│ │ └─routingCalculator.js
│ ├─production/
│ │ ├─blanks.js
│ │ ├─error-log.js
│ │ ├─request.js
│ │ └─sort.js
│ ├─prototypes/
│ │ ├─my-projects.js
│ │ ├─part.js
│ │ └─projects.js
│ ├─styles.css
│ └─user/
│   ├─change_password.js
│   └─verification.js
├─templates/
│ ├─base.html
│ ├─error_log/
│ │ ├─add-error.html
│ │ ├─add-file.html
│ │ ├─edit-error.html
│ │ ├─error-log.html
│ │ └─error.html
│ ├─dashboard.html
│ ├─hubs/
│ │ ├─amada.html
│ │ ├─forming.html
│ │ ├─punch.html
│ │ └─trumpf.html
│ ├─misc/
│ │ ├─blanks.html
│ │ ├─eco.html
│ │ ├─explorer.html
│ │ ├─nesting-calculator.html
│ │ ├─requests.html
│ │ └─todo.html
│ ├─prototypes/
│ │ ├─add-file.html
│ │ ├─bug-request.html
│ │ ├─create_part.html
│ │ ├─create_project.html
│ │ ├─edit_part.html
│ │ ├─edit_project.html
│ │ ├─file-versions.html
│ │ ├─my-projects.html
│ │ ├─part.html
│ │ ├─project.html
│ │ └─projects.html
│ ├─sops/
│ │ ├─bend_operation.html
│ │ ├─bend_parameters.html
│ │ ├─bend_users.html
│ │ ├─blankcam.html
│ │ ├─data_explorer.html
│ │ ├─material_explorer.html
│ │ ├─offline_loading.html
│ │ ├─parameter_explorer.html
│ │ ├─punch_sop.html
│ │ ├─salvagnini_guide.html
│ │ └─trutops.html
│ └─user/
│   ├─change_password.html
│   ├─login.html
│   ├─profile.html
│   ├─sign_up.html
│   └─verification.html
└─utilities.py
```
