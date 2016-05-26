apt-get update
apt-get -y install imagemagick
mount 10.240.105.92:var/www/html/data /home/gauravlangan_gmail_com/data
# Use the metadata server to get the configuration specified during
# instance creation. Read more about metadata here:
# https://cloud.google.com/compute/docs/metadata#querying
IMAGE_URL=$(curl http://metadata/computeMetadata/v1/instance/attributes/url -H "X-Google-Metadata-Request: True"
)
TEXT=$(curl http://metadata/computeMetadata/v1/instance/attributes/text -H "X-Google-Metadata-Request: True")
CS_BUCKET=$(curl http://metadata/computeMetadata/v1/instance/attributes/bucket -H "X-Google-Metadata-Request: Tr
ue")
mkdir image-output
cd image-output
wget $IMAGE_URL
convert * -pointsize 30 -fill white -stroke black -gravity center -annotate +10+40 "$TEXT" output.png
# Store the image in Google Cloud Storage and allow all users
# to read it.
gsutil cp -a public-read output.png gs://$CS_BUCKET/output.png
