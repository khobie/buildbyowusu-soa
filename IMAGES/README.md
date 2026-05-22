# IMAGES — Media storage

Place all project media files here (photos, logos, PDFs, videos, etc.).

## Suggested subfolders

```
IMAGES/
├── logos/          School logo, favicon, partner logos
├── hero/           Homepage banner images
├── faculty/        Staff and faculty photos
├── gallery/        Event and campus gallery
├── news/           News article images
├── programmes/     Programme-related images
├── partners/       Hospital partner logos
└── documents/      Brochures, PDFs (non-upload)
```

## Using images on the website

After adding or updating files here, run:

```bash
flask --app run sync-images
```

This copies masters into `app/static/img/` for the live site.

### Current site mapping

| Your file in `IMAGES/` | Used on the website for |
|------------------------|-------------------------|
| `logos/SOA & CC Logo.png` | Navbar, footer, browser tab icon |
| `hero/engin_akyurt-surgery-3034133.jpg` | Homepage hero & clinical training |
| `hero/sanjiang-classroom-2787754.jpg` | About the School section |
| `faculty/director.jpeg` | Director's welcome (home & about) |
| `about/anaesthesia-training.jpg` | Backup / optional |

Add more folders (`gallery/`, `news/`, etc.) and run `sync-images` again after we extend the sync script.

## Uploads from users

Student documents, applications, and lecture notes still go to `app/static/uploads/` via the app upload system.
