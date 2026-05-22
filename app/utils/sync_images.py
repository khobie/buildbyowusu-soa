"""Copy media from IMAGES/ master folder into app/static/img/ for web serving."""
import os
import shutil

# Project root (school_anaesthesia/)
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IMAGES_DIR = os.path.join(ROOT, 'IMAGES')
STATIC_IMG = os.path.join(ROOT, 'app', 'static', 'img')

# Master filename in IMAGES → web path under static/img/
SYNC_MAP = [
    ('hero/engin_akyurt-surgery-3034133.jpg', 'hero/surgery.jpg'),
    ('hero/sanjiang-classroom-2787754.jpg', 'about/classroom.jpg'),
    ('logos/SOA & CC Logo.png', 'logos/soa-logo.png'),
    ('faculty/director.jpeg', 'faculty/director.jpeg'),
    ('about/anaesthesia-training.jpg', 'about/anaesthesia-training.jpg'),
]


def _copy_file(src, dest_rel):
    dest = os.path.join(STATIC_IMG, dest_rel.replace('/', os.sep))
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy2(src, dest)
    return dest_rel


def sync_images_from_folder():
    """Copy known IMAGES files into app/static/img/."""
    copied = []
    for src_rel, dest_rel in SYNC_MAP:
        src = os.path.join(IMAGES_DIR, src_rel.replace('/', os.sep))
        if not os.path.isfile(src):
            continue
        copied.append(_copy_file(src, dest_rel))

    # Any images in IMAGES/gallery/ → static/img/gallery/
    gallery_src = os.path.join(IMAGES_DIR, 'gallery')
    if os.path.isdir(gallery_src):
        for name in os.listdir(gallery_src):
            if name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
                src = os.path.join(gallery_src, name)
                if os.path.isfile(src):
                    copied.append(_copy_file(src, f'gallery/{name}'))

    return copied
