# ResearchDoc



ResearchDoc is a Django-based research management web application. It allows users to create research projects, store resources, write summaries with citations, build comparison tables, and search across their saved research content.



The project was developed as a final web application project for INFS3202/7202.

## Live Demo

ResearchDoc is deployed on PythonAnywhere:

https://arni2314.pythonanywhere.com/

Demo notes:
- The app supports user registration and login.
- Users can create projects, add resources, write summaries, add citations, create comparison tables, and search saved research content.
- Admin-only subscription management is available through staff accounts.



\## Features



\- User registration, login, and logout using Django authentication

\- Research project creation, editing, listing, and deletion

\- Resource management for uploaded papers, external links, notes, and searchable full text

\- Research summaries with manually added citations

\- Dynamic comparison tables with editable rows

\- Search across resource titles, notes, full text, and summary content

\- Admin-only subscription management with archive functionality

\- Basic accessibility improvements including semantic headings, labelled form fields, descriptive buttons, table headers, and text-based feedback messages



\## Technology Stack



\- Python

\- Django

\- SQLite for local/demo database

\- Bootstrap 5

\- HTML templates

\- GitHub for version control



\## Local Setup



Clone the repository:



```bash

git clone https://github.com/Arni-tech/researchdoc.git

cd researchdoc

````



Create and activate a virtual environment:



```bash

python -m venv venv

venv\\Scripts\\activate

```



Install dependencies:



```bash

pip install -r requirements.txt

```



Run migrations:



```bash

python manage.py migrate

```



Create an admin user:



```bash

python manage.py createsuperuser

```



Run the development server:



```bash

python manage.py runserver

```



Open the app locally:



```text

http://127.0.0.1:8000/

```



\## Project Structure



```text

researchdoc/

├── manage.py

├── requirements.txt

├── researchdoc/

│   ├── models.py

│   ├── forms.py

│   ├── views.py

│   ├── urls.py

│   ├── admin.py

│   └── templates/

│       └── researchdoc/

└── researchdoc\_project/

&#x20;   ├── settings.py

&#x20;   ├── urls.py

&#x20;   └── wsgi.py

```



\## Main App Workflow



Users can sign up or log in, create a research project, add resources to that project, write summaries, add citations, create comparison tables, and search across stored research material.



Admin users can access the subscription management section, where they can create, edit, and archive subscription records. Archiving a subscription changes its status and archive flag but does not delete the user account.



\## Comparison Tables



The comparison table feature was updated from a fixed structure into a more adaptable design. A comparison table now stores the overall table details, while each comparison row is stored separately. This allows users to add, edit, reorder, and delete rows.



\## Accessibility Notes



The templates include basic accessibility improvements:



\* Semantic page headings

\* Visible labels connected to form fields

\* Descriptive buttons and links

\* Table headers using `scope="col"`

\* Text-based success and error messages

\* Skip-to-main-content support in the base template



These changes improve basic WCAG alignment, although the project is not presented as a full formal WCAG audit.



\## Deployment Notes



The original course deployment was hosted on UQCloud. Since the course server is no longer active, the project can be run locally or deployed again using a Django-compatible hosting platform such as PythonAnywhere.



For a PythonAnywhere deployment, update `ALLOWED\_HOSTS`, configure static files, run migrations, and reload the web app through the PythonAnywhere dashboard.



\## Limitations



\* Uploaded files are stored, but PDF text is not automatically extracted.

\* Search uses user-provided resource text, notes, and summaries.

\* The subscription system is an admin management feature and does not control real billing or user access.

\* The project uses SQLite for simple local/demo setup.



\## Author



Arnav Negi



````



Before committing, create the file:



```bat id="b811mf"

notepad README.md

````



Paste the content, save, then:



```bat id="006vgd"

git add README.md

git commit -m "Add project README"

git push

```



