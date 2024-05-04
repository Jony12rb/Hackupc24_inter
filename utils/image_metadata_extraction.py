from PIL import Image
from PIL.ExifTags import TAGS

def get_metadata_dict(imagepath):
    # read the image data using PIL
    exifdata = Image.open(imagepath).getexif()
    metadata_dict = {}
    # iterating over all EXIF data fields
    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # decode bytes
        if isinstance(data, bytes):
            data = data.decode()
        metadata_dict[f"{tag}"] = data
    return metadata_dict