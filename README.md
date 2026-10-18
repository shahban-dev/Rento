# Rento — Property Rental Platform (Pakistan)

A Django + Django REST Framework web app for listing and discovering rental
properties (rooms, houses, shops, hostels, apartments) across Pakistan.
Semester project — Muhammad Shahban (F23BDOCS1M01111), Web Engineering.

Features: property listings with search/filters, owner dashboard
(add/edit/delete), favorites, inquiries, reviews, user roles
(owner/tenant), and a DRF JSON API under `/api/`.

## Run locally (Windows)

```bat
python -m venv myworld
myworld\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ — admin at http://127.0.0.1:8000/admin/

## Run locally (macOS/Linux)

```bash
python3 -m venv myworld
source myworld/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Notes

- Uses SQLite — no database server needed. `db.sqlite3` is created on first
  `migrate` and is intentionally not committed to the repo.
- Sample property images in `media/properties/` are demo content.
- `SRS.md` is the project's SRS document.
