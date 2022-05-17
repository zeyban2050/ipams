from django.conf import settings
from storages.backends.gcloud import GoogleCloudStorage
from storages.utils import setting
from urllib.parse import urljoin

class GoogleCloudMediaFileStorage(GoogleCloudStorage):
    """ Google file storage class which gives a media file path from       
    MEDIA_URL not google generated one."""
    
    bucket_name = setting('GS_BUCKET_NAME')
    
    def url(self, name):
        """ Gives correct MEDIA_URL and not google generated url."""
        print('inside')
        
        return urljoin(settings.MEDIA_URL, name)












# from google.cloud import storage


# def upload_blob(bucket_name, source_file_name, destination_blob_name):
#     """Uploads a file to the bucket."""
#     # The ID of your GCS bucket
#     # bucket_name = "your-bucket-name"
#     # The path to your file to upload
#     # source_file_name = "local/path/to/file"
#     # The ID of your GCS object
#     # destination_blob_name = "storage-object-name"

#     storage_client = storage.Client()
#     bucket = storage_client.bucket(bucket_name)
#     blob = bucket.blob(destination_blob_name)

#     blob.upload_from_filename(source_file_name)

#     print(
#         "File {} uploaded to {}.".format(
#             source_file_name, destination_blob_name
#         )
#     )